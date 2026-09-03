# Vanguard-GWM

### Generative Graph World Model for Proactive Multi-Stage Network Attack Forecasting

<p align="center">
  <b>From reactive alert detection to proactive attack-trajectory forecasting.</b>
</p>

<p align="center">
  <a href="https://github.com/raghuraj72/Vanguard-GWM">
    <img src="https://img.shields.io/badge/GitHub-Vanguard--GWM-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Graph%20Neural%20Networks-GATv2-8A2BE2?style=for-the-badge" alt="GATv2">
  <img src="https://img.shields.io/badge/Streamlit-SOC%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## 📌 Overview

**Vanguard-GWM** is a research-oriented cybersecurity AI system designed to forecast the **next stages of a multi-stage network attack** from temporal network telemetry.

Traditional intrusion detection systems primarily answer:

> **"Is an attack happening right now?"**

Vanguard-GWM focuses on a different question:

> **"Given what is happening now, what is likely to happen next?"**

The system represents network activity as a sequence of dynamic graphs and combines **graph representation learning, temporal dynamics modeling, autoregressive forecasting, explainability, and SOC visualization** to estimate future attack trajectories.

The goal is to provide security analysts with an **early-warning signal** rather than only a post-facto alert.

---

## 🎯 Problem Statement

Modern network attacks are rarely single-step events.

A sophisticated intrusion can evolve through multiple stages:

```text
Reconnaissance
      ↓
Initial Access
      ↓
Execution
      ↓
Persistence
      ↓
Privilege Escalation
      ↓
Lateral Movement
      ↓
Impact
```

Conventional alert-based systems often operate on individual events or flows. This can make it difficult to understand the **temporal relationship between events, hosts, and communication paths**.

Vanguard-GWM models network activity as a dynamic graph:

```text
Gₜ = (Vₜ, Eₜ, Xₜ)
```

where:

* `Vₜ` = network entities / hosts
* `Eₜ` = communication relationships
* `Xₜ` = observed traffic features
* `t` = temporal observation window

The model then learns how the graph state evolves:

```text
Gₜ → Gₜ₊₁ → Gₜ₊₂ → ... → Gₜ₊ₖ
```

and uses the learned dynamics to forecast potential future attack states.

---

# 🧠 Core Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                    NETWORK TELEMETRY                         │
│        Flow / Transport Metadata / Traffic Statistics        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                 TEMPORAL GRAPH CONSTRUCTION                  │
│                                                              │
│        Gₜ = (Vₜ, Eₜ, Xₜ)                                    │
│                                                              │
│  Hosts → Nodes                                               │
│  Communications → Edges                                      │
│  Traffic statistics → Node / Edge features                   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     GATv2 ENCODER                            │
│                                                              │
│  Learns spatial relationships between network entities      │
│  and identifies important graph interactions.                │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│              TEMPORAL / CAUSAL DYNAMICS MODEL                 │
│                                                              │
│  Learns how latent network states evolve over time.          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                AUTOREGRESSIVE FORECASTING                    │
│                                                              │
│  Sₜ → Sₜ₊₁ → Sₜ₊₂ → ... → Sₜ₊ₖ                             │
│                                                              │
│  Forecast potential future attack-stage progression.         │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     EXPLAINABLE FORECAST                     │
│                                                              │
│  Predicted stage + confidence + influential features         │
│  + important graph relationships                              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    SOC DASHBOARD                             │
│                                                              │
│  Forecast Timeline │ Graph View │ What-If Analysis            │
│  Threat Context    │ XAI        │ Security Actions            │
└──────────────────────────────────────────────────────────────┘
```

---

# 🚀 Key Contributions

### 1. Dynamic Graph Representation

Network telemetry is transformed into temporal graph representations so that the model can reason about **relationships between communicating entities**, rather than treating every flow as an isolated observation.

### 2. Graph Attention Learning

A **GATv2-based spatial encoder** learns which nodes and interactions are most relevant to the current network state.

### 3. Temporal Attack-Trajectory Modeling

The learned graph representation is passed into a temporal dynamics component to model how the environment changes across successive observations.

### 4. Multi-Step Forecasting

Instead of producing only a current-state classification, Vanguard-GWM performs an **autoregressive rollout** to estimate possible future states.

### 5. Explainable Predictions

The system is designed to expose the network features and relationships contributing to a forecast, helping analysts understand **why** a future stage is being predicted.

### 6. Counterfactual / What-If Analysis

The dashboard provides a sandbox for exploring how changes to the network graph can affect the predicted trajectory.

---

# 🔬 Model Formulation

Let the observed network state at time `t` be represented as:

```text
Sₜ = Encoder(Gₜ)
```

The temporal dynamics model estimates:

```text
P(Sₜ₊₁ | Sₜ)
```

Repeated application produces an autoregressive rollout:

```text
Sₜ₊₁ ~ P(Sₜ₊₁ | Sₜ)

Sₜ₊₂ ~ P(Sₜ₊₂ | Sₜ₊₁)

...

Sₜ₊ₖ ~ P(Sₜ₊ₖ | Sₜ₊ₖ₋₁)
```

The resulting latent trajectory is mapped to predicted attack-stage states.

This formulation allows Vanguard-GWM to move beyond static classification toward **temporal attack forecasting**.

---

# 🔐 Security Perspective

Vanguard-GWM is designed around a defensive security workflow:

```text
Observe
   ↓
Represent
   ↓
Understand
   ↓
Forecast
   ↓
Explain
   ↓
Respond
```

The intended use is **defensive network monitoring, security research, and SOC decision support**.

It does not attempt to automate offensive intrusion activity.

---

# 📊 Evaluation

Vanguard-GWM includes a benchmark entry point in:

```text
benchmark.py
```

The repository currently includes comparison infrastructure for:

* Logistic Regression
* Random Forest
* Static MLP
* Vanguard-GWM

The benchmark reports:

* Precision
* Recall
* F1-score
* False-positive rate
* Predictive lead-time category

### ⚠️ Reproducibility note

Benchmark results should only be interpreted as empirical evidence when they are produced from the project's actual evaluation pipeline and documented dataset.

**Do not treat synthetic or simulated benchmark outputs as real-world performance measurements.**

The final research evaluation should report:

| Metric                   | Vanguard-GWM |
| ------------------------ | -----------: |
| Precision                |          TBD |
| Recall                   |          TBD |
| F1-score                 |          TBD |
| False Positive Rate      |          TBD |
| AUROC                    |          TBD |
| Forecast Horizon         |          TBD |
| Median Inference Latency |          TBD |
| P95 Inference Latency    |          TBD |

These values should be populated after running the validated experimental pipeline.

---

# 🧪 Recommended Research Evaluation

A complete evaluation should answer four questions.

### 1. Does Vanguard detect/forecast accurately?

Measure:

* Precision
* Recall
* F1
* AUROC
* AUPRC
* Confusion matrix

### 2. Does it forecast earlier?

Measure:

```text
Lead Time =
Actual Stage Time − First Correct Prediction Time
```

Evaluate multiple horizons, for example:

```text
+30s
+60s
+120s
+180s
```

The actual supported horizons should be reported from experiments rather than assumed.

### 3. Does every component matter?

Perform an ablation study:

```text
Full Vanguard-GWM
        │
        ├── − Graph Attention
        ├── − Temporal Dynamics
        ├── − Contrastive Objective
        └── − Autoregressive Rollout
```

### 4. Does the model generalize?

Evaluate across:

* Different attack scenarios
* Different traffic distributions
* Different temporal windows
* Unseen attack sequences where appropriate

---

# 🖥️ SOC Dashboard

Vanguard-GWM includes an interactive **Streamlit-based SOC dashboard**.

The dashboard is intended to expose the model's outputs in an analyst-friendly interface.

![Vanguard-GWM SOC Dashboard](./dashboard.png)

### Dashboard goals

* View current network state
* Inspect forecasted attack stages
* Explore temporal progression
* Inspect model explanations
* Run What-If / counterfactual experiments
* Present forecast information in a SOC-oriented interface

---

# ▶️ Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/raghuraj72/Vanguard-GWM.git
cd Vanguard-GWM
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

> The repository currently contains an empty `requirements.txt`. Before claiming a fully reproducible local installation, populate and validate this dependency file against the actual project environment.

## 4. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard is configured to run on Streamlit's default port:

```text
http://localhost:8501
```

---

# 🐳 Docker

The repository includes:

```text
Dockerfile
docker-compose.yml
```

The Docker image is based on Python 3.11 and exposes port `8501`.

Build and start the application:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8501
```

To stop the container:

```bash
docker compose down
```

---

# 📁 Repository Structure

```text
Vanguard-GWM/
│
├── app.py
│   └── Streamlit SOC dashboard
│
├── benchmark.py
│   └── Baseline benchmarking / evaluation entry point
│
├── src/
│   └── Core Vanguard-GWM implementation
│
├── assets/
│   └── Project assets
│
├── dashboard.png
│   └── Dashboard preview
│
├── Dockerfile
│   └── Container definition
│
├── docker-compose.yml
│   └── Container orchestration
│
├── requirements.txt
│   └── Python dependencies
│
├── Vanguard_GWM_Research_Paper.pdf.pdf
│   └── Research manuscript
│
├── vanguard_gwm_paper.tex
│   └── LaTeX source for the research paper
│
├── CYVERGE_SIH_2026_Vanguard_GWM.pdf
│   └── Project presentation document
│
├── CYVERGE_SIH_2026_Vanguard_GWM.pptx
│   └── Presentation source
│
└── Vanguard_GWM_SIH_Presentation.pptx
    └── Additional presentation material
```

---

# 🧰 Technology Stack

| Category                   | Technology                        |
| -------------------------- | --------------------------------- |
| Language                   | Python                            |
| Deep Learning              | PyTorch                           |
| Graph Learning             | GATv2 / Graph Neural Networks     |
| Data Processing            | Polars / Pandas                   |
| Machine Learning Baselines | scikit-learn                      |
| Visualization              | Streamlit                         |
| Containerization           | Docker                            |
| Security Context           | Network telemetry / SOC analytics |
| Explainability             | Attention / feature attribution   |
| Research                   | Temporal graph-based forecasting  |

---

# 📚 Research Materials

The repository contains supporting research and presentation material:

* **Research manuscript:** `Vanguard_GWM_Research_Paper.pdf.pdf`
* **LaTeX source:** `vanguard_gwm_paper.tex`
* **SIH presentation:** `Vanguard_GWM_SIH_Presentation.pptx`
* **Project presentation:** `CYVERGE_SIH_2026_Vanguard_GWM.pptx`
* **Submission document:** `Vanguard_GWM_SIH_Submission.pdf`

These materials document the motivation, architecture, methodology, and intended system design.

---

# 🧭 Development Roadmap

## Phase 1 — Core System

* [x] Temporal graph representation
* [x] Graph-based encoder
* [x] Temporal forecasting architecture
* [x] Streamlit dashboard
* [x] Docker support
* [x] Baseline benchmark entry point

## Phase 2 — Experimental Validation

* [ ] Real dataset evaluation
* [ ] Reproducible training pipeline
* [ ] Baseline comparison
* [ ] Forecast-horizon evaluation
* [ ] Ablation studies
* [ ] Repeated-run statistical analysis

## Phase 3 — Explainability

* [ ] Node-level attribution
* [ ] Edge-level attribution
* [ ] Feature importance
* [ ] Forecast confidence calibration
* [ ] Analyst-friendly explanation reports

## Phase 4 — Research & Deployment

* [ ] Robustness testing
* [ ] Distribution-shift evaluation
* [ ] Larger temporal evaluation
* [ ] Model checkpoint management
* [ ] Experiment tracking
* [ ] Production-oriented telemetry ingestion

---

# ⚠️ Limitations

Vanguard-GWM is a research prototype and should not be interpreted as a guaranteed real-world attack predictor.

Performance can be affected by:

* Training-data distribution
* Attack-sequence coverage
* Telemetry quality
* Class imbalance
* Temporal resolution
* Previously unseen attack behavior
* False-positive costs
* Distribution shift between benchmark and deployment environments

Forecasts should therefore be treated as **decision-support signals**, not as ground truth.

---

# 🔭 Future Work

Potential research directions include:

* Online continual learning
* Larger heterogeneous network graphs
* Uncertainty-aware forecasting
* Calibration of forecast probabilities
* Cross-dataset evaluation
* More rigorous causal modeling
* Long-horizon forecasting
* Federated security telemetry learning
* Real-time streaming ingestion
* Integration with defensive network policy systems

---

# 👨‍💻 Project

**Vanguard-GWM**
Generative Graph World Model for Proactive Multi-Stage Network Attack Forecasting

Built as a research and engineering project exploring the intersection of:

**Artificial Intelligence × Graph Neural Networks × Temporal Modeling × Cybersecurity**

---

# 📄 License

Add an explicit open-source license to this repository before publishing the project as reusable open-source software.

Recommended choices depend on the project's intended usage and any third-party dependencies.

---

# ⭐ If You Find This Project Interesting

Consider starring the repository and following the development of Vanguard-GWM.

**Repository:**
https://github.com/raghuraj72/Vanguard-GWM
