# ✈️ Air Traffic Controller Kinematics Simulator

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Build](https://img.shields.io/badge/Status-Passing-success.svg)
![Architecture](https://img.shields.io/badge/Design-Object--Oriented-orange.svg)

A 3D object-oriented kinematics engine written in Python that simulates aircraft trajectories, mid-air collision detection, ground impact thresholds, and structural integrity for an automated Air Traffic Control (ATC) system.

---

## 📌 Key Features
* **Continuous-Time Physics Engine:** Tracks 3D position $\mathbf{p}(t)$ and velocity $\mathbf{v}(t)$ vectors over continuous, irrational time intervals using exact algebraic kinematics (quadratic root solving) rather than discrete step-by-step approximations.
* **Event Prioritization & Collision Detection:** Computes exact intersection instants for mid-air collisions, vertical ground crashes ($z = 0$ with $v_z < 0$ or $a_z < 0$), and structural failure thresholds ($\Vert{}\mathbf{v}(t)\Vert{} > v_{\max}$).
* **Deterministic State Management:** Enforces strict precedence rules—resolving structural damage, ground impacts, and safe landings before evaluating multi-aircraft collisions—and isolates terminated aircraft from active airspace to prevent ghost collisions.
* **Floating-Point Precision:** Uses epsilon-bounded ($\epsilon = 10^{-6}$) comparator functions to evaluate irrational event timestamps reliably without floating-point drift.

---

## 📂 Repository Structure

```text
Air-Traffic-Controller/
│
├── src/
│   ├── air_traffic_control.py   # Core Flight and AirTrafficControl classes & kinematics solver
│   └── simulator.py             # CLI driver and command stream parser
│
├── tests/
│   ├── visible_cases_1.txt      # Single-flight trajectory and ground impact test
│   └── visible_cases_2.txt      # Multi-flight ATC collision & structural limit test
│
└── README.md                    # Project documentation
```

---

## 🚀 How to Run

Ensure you have **Python 3** installed. From the root `Air-Traffic-Controller` directory, run the simulator against the test suites using any of the following methods:

**Using the `--test` flag:**
```bash
python3 src/simulator.py --test tests/visible_cases_1.txt
python3 src/simulator.py --test tests/visible_cases_2.txt
```

**Using standard input redirection:**
```bash
python3 src/simulator.py < tests/visible_cases_1.txt
python3 src/simulator.py < tests/visible_cases_2.txt
```

---

## 📋 Supported Command Syntax

| Mode | Command Format | Description |
| :--- | :--- | :--- |
| **Single Flight** | `FLIGHT <max_speed> <x> <y> <z> <vx> <vy> <vz>` | Initializes a standalone aircraft at $t = 0$. |
| **Single Flight** | `ACCEL <t> <ax> <ay> <az>` | Updates the aircraft's 3D acceleration vector at time $t$. |
| **Single Flight** | `FSTATUS <t>` | Queries the aircraft status (`flying`, `accident`, `landed safely`) at time $t$. |
| **ATC Controller** | `CREATE <t> <id> <max_speed> <x> <y> <z> <vx> <vy> <vz>` | Registers a new flight in controlled airspace at time $t$. |
| **ATC Controller** | `UPDATE <t> <id> <ax> <ay> <az>` | Sends a 3D acceleration instruction to flight `<id>` at time $t$. |
| **ATC Controller** | `STATUS <t> <id>` | Queries the status of flight `<id>` at time $t$. |