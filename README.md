@'
# Vanguard-GWM: Generative Graph World Model for Cyber Defense
<p align="center">
  <img src="assets/demo.png" alt="Vanguard-GWM Live Dashboard Demo" width="100%">
</p>


[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Geometric-ee4c2c.svg)](https://pytorch.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Proactive, multi-stage network attack trajectory forecasting using deep graph world models.** 
> Vanguard-GWM shifts enterprise security from reactive alert triage to preventative interception.

---

## 🚀 Visual Architecture Pipeline

```text
+-------------------------------------------------------------------+
|                        1. NETWORK TRAFFIC                         |
|                 (Encrypted TLS 1.3 / QUIC Streams)                |
+---------------------------------+---------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                     2. GRAPH CONSTRUCTION ($G_t$)                 |
|             (Polars Streaming & Transport Header Geometry)        |
+---------------------------------+---------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                     3. SPATIAL GATv2 ENCODER                      |
|            (InfoNCE Loss Binds Latent Geometry & Topology)        |
+---------------------------------+---------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                   4. CAUSAL DYNAMICS TRANSFORMER                  |
|          (Autoregressive Rollout $P(S_{t+1} | S_t)$ over K-Steps)   |
+---------------------------------+---------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                       5. ATTACK FORECAST                          |
|             (+180s to +600s Proactive Early Warning)              |
+---------------------------------+---------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                        6. SOC DASHBOARD                           |
|         (Streamlit UI, XAI Attribution & What-If Sandbox)         |
+-------------------------------------------------------------------+



---

## 📌 Executive Summary
Vanguard-GWM transitions network intrusion response from **reactive, post-facto classification** to **proactive trajectory forecasting**. Utilizing a contrastively pre-trained Graph Attention Network (GATv2) and a Causal Temporal Dynamics Transformer, Vanguard-GWM models the environment transition dynamics $P(S_{t+1} \mid S_t)$ to simulate multi-stage attack trajectories $K$-steps ahead before host compromise occurs.

---

## 🚀 Key Features
- **Payload-Agnostic Telemetry Ingestion:** Processes dynamic temporal graphs ($G_t$) from unencrypted packet headers (IAT variance, TCP flags, TTL jitter).
- **$K$-Step Autoregressive Rollout:** Projects multi-stage kill-chain progression across MITRE ATT&CK phases with **+25s to +180s lead time**.
- **Attention Explainability:** Non-black-box feature attribution scoring over packet-level and flow-level metrics.
- **"What-If" Policy Sandbox:** Counterfactual graph-pruning simulation paired with automated **OpenFlow 1.3 SDN flow-rule staging**.
- **Real-Time SOC Budget:** Sub-50ms inference latency ($36.4\text{ ms}$).

---

---

## 💻 Usage & Running the SOC Dashboard

Once you have the environment running (either via Docker or a local virtual environment), you can launch the interactive Streamlit SOC dashboard to explore real-time attack trajectory forecasts and run counterfactual "What-If" simulations:

```bash
streamlit run app.py

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/raghuraj2008-cu/Vanguard-GWM.git](https://github.com/raghuraj2008-cu/Vanguard-GWM.git)
cd Vanguard-GWM