# ⚽ Football League Simulation — Elo vs Poisson Models

## 📋 Project Overview

This project simulates the remainder of a football league season using **Monte Carlo simulations** powered by **Elo ratings**.  
It estimates the **probability of each team finishing in every table position**, given the current standings and remaining fixtures.

Two modeling approaches are implemented in separate Jupyter notebooks:

| Notebook | Description |
|-----------|--------------|
| `elo_simulation.ipynb` | Match outcomes are drawn directly from Elo-based win/draw/loss probabilities. |
| `poisson_simulation.ipynb` | Match goals are simulated from a Poisson distribution, with expected goals derived from Elo differences. |

Both versions dynamically update Elo ratings after each simulated match and aggregate thousands of season simulations to estimate outcome probabilities.

---

## 🚀 Key Features

- Dynamic **Elo rating updates** after every simulated match.  
- Flexible configuration (number of simulations, Elo K-factor, etc.).  
- Automatic handling of tiebreakers (goal difference, goals scored).  
- Statistical summaries of finishing position probabilities.  
- Rich **visualizations**: heatmaps, probability bars, and distributions.

---

## 📈 Model Details

### 1️⃣ Elo-based Model (`elo_simulation.ipynb`)

Each match result (win/draw/loss) is sampled probabilistically based on Elo ratings:

$$
P(A\ wins) = \frac{1}{1 + 10^{(ELO_B - ELO_A)/400}}
$$

After each match:

$$
ELO_{new} = ELO_{old} + K \cdot (S - E)
$$

where `S` is the actual result (1, 0.5, or 0), and `E` is the expected score.

---

### 2️⃣ Poisson-based Model (`poisson_simulation.ipynb`)

Here, Elo ratings are converted into **expected goals (λ)** for each team, and match outcomes are determined from **simulated goal counts**:

$$
\lambda_A = baseGoals \times 10^{(ELO_A - ELO_B)/800}
$$

$$
\lambda_B = baseGoals \times 10^{(ELO_B - ELO_A)/800}
$$

---

## 🧮 Simulation Workflow

1. Load the current league table and remaining fixtures.
2. Calculate initial Elo ratings from team performance.
3. For each simulation (e.g., 10,000 times):
    - Simulate remaining matches using chosen model (Elo or Poisson).
    - Update points, goals, and Elo ratings dynamically.
    - Sort and rank teams by points, goal difference, and goals scored.
    - Record each team’s final position.
4. Aggregate all simulations to compute probability distributions for league outcomes.


---
