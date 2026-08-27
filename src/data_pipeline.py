import polars as pl
import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data

def generate_synthetic_telemetry(num_records=600):
    np.random.seed(42)
    timestamps = np.sort(np.random.uniform(0, 100, num_records))
    
    ips = [f"192.168.1.{i}" for i in range(10, 18)] + ["10.0.0.99"]
    src_ips = np.random.choice(ips, num_records)
    dst_ips = np.random.choice(ips, num_records)
    
    mask = src_ips == dst_ips
    dst_ips[mask] = "10.0.0.99"
    
    syn_flag = np.random.binomial(1, 0.25, num_records)
    ack_flag = np.random.binomial(1, 0.75, num_records)
    rst_flag = np.random.binomial(1, 0.05, num_records)
    bytes_count = np.random.exponential(1800, num_records)
    iat_mean = np.random.exponential(0.04, num_records)
    iat_var = np.random.exponential(0.01, num_records)
    ttl_var = np.random.uniform(0, 4, num_records)
    
    labels = []
    for t in timestamps:
        if t < 25:
            labels.append(0)  # Benign Baseline
        elif t < 45:
            labels.append(1)  # Reconnaissance
        elif t < 65:
            labels.append(2)  # Initial Access
        elif t < 85:
            labels.append(3)  # Lateral Movement
        else:
            labels.append(4)  # Exfiltration
            
    return pl.DataFrame({
        "timestamp": timestamps,
        "src_ip": src_ips,
        "dst_ip": dst_ips,
        "syn_flag": syn_flag,
        "ack_flag": ack_flag,
        "rst_flag": rst_flag,
        "bytes": bytes_count,
        "iat_mean": iat_mean,
        "iat_var": iat_var,
        "ttl_var": ttl_var,
        "attack_stage": labels
    })

class TemporalGraphProcessor:
    def __init__(self, time_window=5.0):
        self.time_window = time_window
        self.ip_map = {}
        
    def _get_node_id(self, ip):
        if ip not in self.ip_map:
            self.ip_map[ip] = len(self.ip_map)
        return self.ip_map[ip]

    def build_graph_sequence(self, df: pl.DataFrame):
        max_t = df["timestamp"].max()
        windows = np.arange(0, max_t + self.time_window, self.time_window)
        graph_sequence = []
        
        unique_ips = list(set(df["src_ip"].to_list() + df["dst_ip"].to_list()))
        for ip in unique_ips:
            self._get_node_id(ip)
            
        num_nodes = len(self.ip_map)
        
        for w_start in windows:
            w_end = w_start + self.time_window
            sub_df = df.filter((pl.col("timestamp") >= w_start) & (pl.col("timestamp") < w_end))
            
            if len(sub_df) == 0:
                continue
                
            src_indices = [self._get_node_id(ip) for ip in sub_df["src_ip"]]
            dst_indices = [self._get_node_id(ip) for ip in sub_df["dst_ip"]]
            
            edge_index = torch.tensor([src_indices, dst_indices], dtype=torch.long)
            edge_attr = torch.tensor(
                sub_df.select(["syn_flag", "ack_flag", "rst_flag", "bytes", "iat_mean", "ttl_var"]).to_numpy(),
                dtype=torch.float
            )
            
            x = torch.ones((num_nodes, 8), dtype=torch.float)
            stage_mode = int(sub_df["attack_stage"].mode()[0])
            y = torch.tensor([stage_mode], dtype=torch.long)
            
            data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)
            data.timestamp = w_start
            graph_sequence.append(data)
            
        return graph_sequence, self.ip_map
