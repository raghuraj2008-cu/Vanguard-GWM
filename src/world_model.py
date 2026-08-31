"""
world_model.py - Generative Graph World Model Core Neural Architectures
Includes GATv2SpatialEncoder, TemporalDynamicsTransformer, and MultiTaskDecoder.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict

class GATv2SpatialEncoder(nn.Module):
    def __init__(self, in_node_features: int = 5, in_edge_features: int = 5, latent_dim: int = 64):
        super().__init__()
        self.latent_dim = latent_dim
        self.node_proj = nn.Linear(in_node_features, latent_dim)
        self.edge_proj = nn.Linear(in_edge_features, latent_dim)
        self.attn_fc = nn.Linear(latent_dim * 3, 1)
        self.leaky_relu = nn.LeakyReLU(0.2)
        self.out_fc = nn.Linear(latent_dim, latent_dim)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, edge_attr: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        num_nodes = x.size(0)
        h = self.node_proj(x)
        e = self.edge_proj(edge_attr)
        
        src, dst = edge_index[0], edge_index[1]
        h_src, h_dst = h[src], h[dst]
        
        score_input = torch.cat([h_src, h_dst, e], dim=-1)
        scores = self.leaky_relu(self.attn_fc(score_input)).squeeze(-1)
        alpha = torch.softmax(scores, dim=0).unsqueeze(-1)
        
        # Message passing aggregation
        msg = alpha * (h_dst + e)
        out_nodes = torch.zeros(num_nodes, self.latent_dim, device=x.device)
        out_nodes.index_add_(0, src, msg)
        out_nodes = F.elu(self.out_fc(out_nodes) + h)
        
        # Graph-level pooled latent representation z_t
        z_graph = torch.mean(out_nodes, dim=0, keepdim=True)
        return out_nodes, z_graph


class TemporalDynamicsTransformer(nn.Module):
    def __init__(self, latent_dim: int = 64, nhead: int = 4, num_layers: int = 2):
        super().__init__()
        self.latent_dim = latent_dim
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=latent_dim,
            nhead=nhead,
            dim_feedforward=latent_dim * 2,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.transition_head = nn.Linear(latent_dim, latent_dim)

    def predict_rollout(self, context_seq: torch.Tensor, k_steps: int = 5) -> torch.Tensor:
        """
        Autoregressively rolls out k_steps forward: [1, k_steps, latent_dim]
        """
        curr_seq = context_seq.clone()
        rollouts = []
        
        for _ in range(k_steps):
            out = self.transformer(curr_seq)
            next_z = self.transition_head(out[:, -1:, :]) # [1, 1, latent_dim]
            rollouts.append(next_z)
            curr_seq = torch.cat([curr_seq, next_z], dim=1)
            
        return torch.cat(rollouts, dim=1)


class MultiTaskDecoder(nn.Module):
    def __init__(self, latent_dim: int = 64, num_mitre_stages: int = 5):
        super().__init__()
        self.risk_head = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        self.mitre_head = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, num_mitre_stages)
        )

    def forward(self, z: torch.Tensor) -> Dict[str, torch.Tensor]:
        return {
            "risk_score": self.risk_head(z),
            "mitre_stage_logits": self.mitre_head(z)
        }
