# Vanguard-GWM 🛡️
### Graph World Model for Predictive Cyber Attack Forecasting
**Smart India Hackathon 2026 | Problem Statement ID: 153**

---

## 📌 Overview
**Vanguard-GWM** shifts cyber defense from reactive, post-incident classification to **generative environment simulation**. By ingesting multi-level network telemetry (PCAP and NetFlow/IPFIX) and constructing discrete, time-windowed dynamic graphs ($G_t$), Vanguard-GWM explicitly models environment state transitions:

$$P(S_{t+1} \mid S_t, \dots, S_{t-w})$$

The platform executes **$K$-step forward autoregressive rollouts** to forecast multi-stage attack trajectories (MITRE ATT&CK) with a **2- to 10-minute predictive lead time** before critical infrastructure compromise occurs.

---

## 🚀 Key Features
- **Dual-Level Telemetry Ingestion:** Captures macro-flow statistics (TCP flags, byte ratios) and micro-packet metrics (TTL variance, Inter-Arrival Times).
- **Graph State Perception (GATv2):** Compresses dynamic graph topology into structured latent network states ($z_t \in \mathbb{R}^d$) with contrastive regularization (InfoNCE).
- **Temporal Dynamics World Model:** Uses a Causal Temporal Transformer to learn state-transition physics without future packet visibility.
- **Autoregressive $K$-Step Rollout:** Simulates unobserved future network states ($[\hat{z}_{t+1}, \dots, \hat{z}_{t+K}]$).
- **Multi-Horizon MITRE ATT&CK Mapping:** Maps simulated states to attack tactics (*Reconnaissance $\to$ Initial Access $\to$ Lateral Movement $\to$ Exfiltration*).
- **Dual-Layer XAI:** Combines intrinsic GAT edge-attention heatmaps with DeepSHAP feature attribution.
- **"What-If" Decision Simulation:** Allows analysts to evaluate host isolation policies within the World Model before executing firewall rules.

---

## 🛠️ Project Structure
```text
vanguard_gwm/
├── data/                  # Telemetry PCAP/CSV captures
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py   # Flow/Packet extraction & dynamic graph constructor
│   └── world_model.py     # GAT encoder, Temporal Dynamics & Rollout engine
├── app.py                 # Offline Streamlit decision-support dashboard
├── requirements.txt       # Project dependencies
└── README.md# Vanguard-GWM
