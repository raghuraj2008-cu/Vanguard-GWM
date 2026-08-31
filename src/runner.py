"""
runner.py - Real-Time Graph Telemetry Streamer & Predictive Engine Runner
Streams temporal graph windows into VanguardEngine and monitors kill-chain progression.
"""
import time
import torch
import logging
from src.engine import VanguardEngine
from src.data_pipeline import StreamingTelemetryParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("Vanguard-Runner")

def run_pipeline(iterations: int = 5, delta_t_sec: float = 2.0):
    logger.info("Initializing Vanguard-GWM Streaming Telemetry Pipeline...")
    parser = StreamingTelemetryParser()
    engine = VanguardEngine(in_node_features=5, in_edge_features=5, latent_dim=64, horizon_k=5, risk_threshold=0.60)
    
    logger.info(f"Starting continuous streaming loop ({iterations} windows, interval: {delta_t_sec}s)...")
    
    for t_idx in range(iterations):
        logger.info(f"\n--- Ingesting Snapshot Window t={t_idx} ---")
        
        # 1. Synthesize streaming telemetry graph G_t
        graph_data = parser.synthesize_mock_window(num_nodes=12, num_edges=28)
        
        # 2. Extract tensors
        x = graph_data.x
        edge_index = graph_data.edge_index
        edge_attr = graph_data.edge_attr
        target_ip = "192.168.1.105"
        
        # 3. Process through Graph World Model
        start_time = time.perf_counter()
        result = engine.process_graph_snapshot(x, edge_index, edge_attr, target_ip)
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        
        # 4. Display operational metrics
        logger.info(f"Target Host: {result['target_ip']}")
        logger.info(f"Projected MITRE ATT&CK Phase: {result['current_stage']}")
        logger.info(f"Peak Risk: {result['peak_risk'] * 100:.1f}% | Horizon Trajectory: {result['risk_trajectory']}")
        logger.info(f"SDN Enforcement Action: {'⚡ QUARANTINE TRIGGERED' if result['sdn_quarantine_enforced'] else '✅ CLEAR'}")
        logger.info(f"Processing Latency: {latency_ms:.2f} ms")
        
        time.sleep(delta_t_sec)

if __name__ == "__main__":
    run_pipeline(iterations=5, delta_t_sec=1.5)
