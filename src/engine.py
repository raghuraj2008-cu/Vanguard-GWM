"""
engine.py - Core Orchestration Engine for Vanguard-GWM
Connects streaming telemetry, Graph World Model rollouts, and SDN enforcement.
"""
import torch
import numpy as np
import logging
from typing import Dict, List, Any
from src.world_model import SpatialEncoder, DynamicsEngine, MultiTaskProjectionHead
from src.sdn_enforcer import SDNEnforcer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("Vanguard-Engine")

class VanguardEngine:
    def __init__(self, in_channels: int = 5, latent_dim: int = 64, horizon_k: int = 5, risk_threshold: float = 0.60):
        self.latent_dim = latent_dim
        self.horizon_k = horizon_k
        self.risk_threshold = risk_threshold
        
        # Neural Network Modules
        self.spatial_encoder = SpatialEncoder(in_channels=in_channels, hidden_dim=latent_dim, out_dim=latent_dim)
        self.dynamics_engine = DynamicsEngine(latent_dim=latent_dim, nhead=4, num_layers=2)
        self.projection_head = MultiTaskProjectionHead(latent_dim=latent_dim, num_classes=5)
        
        # Closed-Loop Enforcement
        self.sdn_enforcer = SDNEnforcer()
        self.history_buffer: List[torch.Tensor] = []

    def process_graph_snapshot(self, x: torch.Tensor, edge_index: torch.Tensor, edge_attr: torch.Tensor, target_ip: str) -> Dict[str, Any]:
        """
        Processes snapshot G_t, computes forward latent rollout, and checks mitigation thresholds.
        """
        self.spatial_encoder.eval()
        self.dynamics_engine.eval()
        self.projection_head.eval()

        with torch.no_grad():
            # 1. Spatial Perception (G_t -> z_t)
            z_t = self.spatial_encoder(x, edge_index, edge_attr)
            z_t_pooled = torch.mean(z_t, dim=0, keepdim=True)
            self.history_buffer.append(z_t_pooled)
            
            if len(self.history_buffer) > 8:
                self.history_buffer.pop(0)

            # 2. Transition Dynamics Rollout [z_t+1 ... z_t+K]
            trajectory_context = torch.stack(self.history_buffer, dim=0)
            rollout_latents = self.dynamics_engine.rollout(trajectory_context, steps=self.horizon_k)

            # 3. Multi-Task Projections
            risk_scores = []
            phase_predictions = []
            
            for z_hat in rollout_latents:
                risk, phase_logits = self.projection_head(z_hat)
                risk_scores.append(risk.item())
                phase_predictions.append(int(torch.argmax(phase_logits, dim=-1).item()))

            peak_risk = max(risk_scores)
            stages = ["Benign Baseline", "Reconnaissance", "Initial Access", "Lateral Movement", "Exfiltration"]
            current_stage = stages[phase_predictions[-1]]

            # 4. Closed-Loop Automated Defense
            enforcement_triggered = False
            if peak_risk >= self.risk_threshold:
                logger.warning(f"⚠️ THREAT DETECTED on {target_ip} (Peak Risk: {peak_risk:.2%}). Dispatching SDN drop rule.")
                enforcement_triggered = self.sdn_enforcer.push_quarantine_rule(target_ip=target_ip)

            return {
                "target_ip": target_ip,
                "current_stage": current_stage,
                "peak_risk": peak_risk,
                "risk_trajectory": risk_scores,
                "sdn_quarantine_enforced": enforcement_triggered
            }
