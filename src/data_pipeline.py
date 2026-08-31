"""
data_pipeline.py - Polars Streaming Parser and Dynamic Graph Generator
"""
import torch
import numpy as np
from torch_geometric.data import Data

class StreamingTelemetryParser:
    def __init__(self, window_size_sec: float = 2.0):
        self.window_size_sec = window_size_sec

    def synthesize_mock_window(self, num_nodes: int = 10, num_edges: int = 24) -> Data:
        """
        Synthesizes a temporal graph snapshot G_t with realistic network telemetry features.
        """
        # Node features: [deg_in, deg_out, avg_bytes, port_entropy, role_id]
        x = torch.randn(num_nodes, 5, dtype=torch.float32)
        
        # Directed edge connections
        src = torch.randint(0, num_nodes, (num_edges,))
        dst = torch.randint(0, num_nodes, (num_edges,))
        edge_index = torch.stack([src, dst], dim=0)
        
        # Edge attributes: [flags_bitmask, log_bytes, iat_mean, iat_var, ttl_var]
        edge_attr = torch.randn(num_edges, 5, dtype=torch.float32)
        
        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
