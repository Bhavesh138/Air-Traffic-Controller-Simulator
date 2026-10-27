# Air Traffic Controller Kinematics Simulation

A 3D object-oriented kinematics engine written in Python that simulates aircraft trajectories, collision detection, and structural integrity for an automated Air Traffic Control (ATC) system.

## Key Features
* **Continuous Time Physics:** Tracks position and velocity vectors over continuous, fractional time intervals using algebraic kinematics (quadratic equation modeling).
* **Collision & Accident Detection:** Calculates precise intersection times for mid-air collisions, impact times for ground crashes, and tracks structural failure thresholds. 
* **State Management:** Manages safe landings vs. terminal accidents, isolating inactive aircraft to prevent ghost collisions.
* **Floating-Point Precision:** Uses epsilon-based calculations to handle irrational time values without rounding errors.

## How to Run
Run the simulation by feeding the input test cases directly into the driver script via your terminal:

```bash
python3 main.py < input1.txt
python3 main.py < input2.txt