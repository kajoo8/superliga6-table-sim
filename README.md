# ⚽ Football League Simulation

## 📋 Project Overview

This project simulates the remainder of a football league season using **Monte Carlo simulations** powered by **Elo ratings**.  
It estimates the **probability of each team finishing in every table position**, given the current standings and remaining fixtures.

Two modeling approaches are implemented in separate Jupyter notebooks:

| Notebook | Description |
|-----------|--------------|
| `elo_simulation.ipynb` | Match outcomes are drawn directly from Elo-based win/draw/loss probabilities. |

Both versions dynamically update Elo ratings after each simulated match and aggregate thousands of season simulations to estimate outcome probabilities.

---

## 🚀 Key Features

- Monte Carlo simulations (10,000+ full-season runs).  
- Dynamic updating of **Elo ratings**, **team attack and defense strengths**, and **base goal rate (λ)**.  
- Automatic handling of league tiebreakers (goal difference, goals scored).  
- Comprehensive result statistics (title chances, relegation risk, position distributions).  
- Clear and attractive **visualizations**: probability bars, histograms, and heatmaps.

---

## 📈 Model Details

### 1️⃣ Elo-based Model (`elo_simulation.ipynb`) -- no longer developed

Each match result (win/draw/loss) is sampled probabilistically based on Elo ratings:

$$
P(A\ wins) = \frac{1}{1 + 10^{(ELO_B - ELO_A)/400}}
$$

After each match:

$$
ELO_{new} = ELO_{old} + K \cdot (S - E)
$$

where `S` is the actual result (1, 0.5, or 0), and `E` is the expected score. This model assumes the result depends directly on relative team ratings.

---

## 🧩 Simulation Workflow

1. Load current league table and remaining fixtures.  
2. Compute initial Elo, attack, defense, and base_lambda.  
3. For each simulation (e.g., 10,000 iterations):
   - Simulate every remaining match.  
   - Update team stats and parameters dynamically.  
   - Apply tiebreakers (goal difference → goals for → goals against).  
   - Record team positions and key metrics (points, GF, GA).  
4. Aggregate results across all runs to compute:
   - Probability of finishing in each table position,  
   - Title and relegation probabilities,  
   - Average points needed for 1st and 8th place (survival threshold).

---

