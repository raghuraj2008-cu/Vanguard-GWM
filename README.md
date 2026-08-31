@'
# 🛡️ Vanguard-GWM: Generative Graph World Model

> **SIH Problem Statement:** AI-based Network Attack Forecasting from Network Traffic Telemetry  
> **Repository:** [raghuraj2008-cu/Vanguard-GWM](https://github.com/raghuraj2008-cu/Vanguard-GWM)

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

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/raghuraj2008-cu/Vanguard-GWM.git](https://github.com/raghuraj2008-cu/Vanguard-GWM.git)
cd Vanguard-GWM