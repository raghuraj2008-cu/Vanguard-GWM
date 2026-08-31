"""
engine.py - Core Orchestration Engine for Vanguard-GWM
Connects streaming telemetry, Graph World Model rollouts, and SDN enforcement.
"""
import torch
import logging
from typing import Dict, List, Any
from src.world_model import GATv2SpatialEncoder, TemporalDynamicsTransformer, MultiTaskDecoder
from src.sdn_enforcer import SDNEnforcer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("Vanguard-Engine")

class VanguardEngine:
    def __init__(self, in_node_features: int = 5, in_edge_features: int = 5, latent_dim: int = 64, horizon_k: int = 5, risk_threshold: float = 0.60):
        self.latent_dim = latent_dim
        self.horizon_k = horizon_k
        self.risk_threshold = risk_threshold
        
        # Exact Neural Network Modules from src/world_model.py
        self.spatial_encoder = GATv2SpatialEncoder(
            in_node_features=in_node_features,
            in_edge_features=in_edge_features,
            latent_dim=latent_dim
        )
        self.dynamics_transformer = TemporalDynamicsTransformer(
            latent_dim=latent_dim,
            nhead=4,
            num_layers=2
        )
        self.decoder = MultiTaskDecoder(
            latent_dim=latent_dim,
            num_mitre_stages=5
        )
        
        # Closed-Loop Enforcement
        self.sdn_enforcer = SDNEnforcer()
        self.history_buffer: List[torch.Tensor] = []

    def process_graph_snapshot(self, x: torch.Tensor, edge_index: torch.Tensor, edge_attr: torch.Tensor, target_ip: str) -> Dict[str, Any]:
        """
        Processes snapshot G_t, computes forward latent rollout, and evaluates mitigation thresholds.
        """
        self.spatial_encoder.eval()
        self.dynamics_transformer.eval()
        self.decoder.eval()

        with torch.no_grad():
            # 1. Spatial Perception (G_t -> z_t)
            z_nodes, z_graph = self.spatial_encoder(x, edge_index, edge_attr)
            
            # z_graph shape: [1, latent_dim]
            if z_graph.dim() == 1:
                z_graph = z_graph.unsqueeze(0)
                
            self.history_buffer.append(z_graph)
            if len(self.history_buffer) > 8:
                self.history_buffer.pop(0)

            # 2. Transition Dynamics Rollout [z_t+1 ... z_t+K]
            # Stack along sequence dimension: shape [1, seq_len, latent_dim]
            context_seq = torch.cat(self.history_buffer, dim=0).unsqueeze(0)
            rollout_latents = self.dynamics_transformer.predict_rollout(context_seq, k_steps=self.horizon_k)

            # 3. Multi-Task Projections across the trajectory
            risk_scores = []
            phase_predictions = []
            
            for k_idx in range(self.horizon_k):
                z_hat = rollout_latents[:, k_idx, :] # [1, latent_dim]
                preds = self.decoder(z_hat)
                risk_val = preds["risk_score"].item()
                stage_idx = int(torch.argmax(preds["mitre_stage_logits"], dim=-1).item())
                
                risk_scores.append(float(risk_val))
                phase_predictions.append(stage_idx)

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
                "peak_risk": round(peak_risk, 4),
                "risk_trajectory": [round(r, 4) for r in risk_scores],
                "sdn_quarantine_enforced": enforcement_triggered
            }
