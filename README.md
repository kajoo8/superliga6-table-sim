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

- Monte Carlo simulations (10,000+ full-season runs).  
- Dynamic updating of **Elo ratings**, **team attack and defense strengths**, and **base goal rate (λ)**.  
- Optional hybrid approach: Poisson model with light Elo influence on goal expectations.  
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

### ⚽ 2️⃣ Poisson-based Model (`poisson_simulation.ipynb`)

In this version, **match scores are simulated from a Poisson distribution**:

$$
Goals_A \sim Pois(\lambda_A), \quad Goals_B \sim Pois(\lambda_B)
$$

Expected goals (λ) for each side depend on:
- `base_lambda` — average goals per team per match in the league,
- `attack` — team offensive strength relative to league average,
- `defense` — team defensive strength (higher = weaker defense),
- (optionally) `Elo` — small dynamic form correction.

$$
\lambda_A = λ \cdot attack_A \cdot defense_B
$$
$$
\lambda_B = λ \cdot attack_B \cdot defense_A
$$

After each simulated match:
- team goal stats (`GF`, `GA`, `M`) are updated,
- new `attack` and `defense` coefficients are **recomputed dynamically**,
- `base_lambda` is recalculated from league-wide averages to maintain realistic scoring levels.

This ensures that form and momentum directly influence future expected goals in subsequent simulations.

---

## 🔄 Dynamic Model Updating

### ⚙️ Attack and Defense Estimation

At any point in the simulation:

$$
attack_i = \frac{GF_i / M_i}{\bar{GF}/\bar{M}}, \quad defense_i = \frac{GA_i / M_i}{\bar{GF}/\bar{M}}
$$

where:
- $( GF_i, GA_i, M_i )$ — team i’s total goals for/against and matches played,  
- averages are computed across all teams.

Both values are normalized so their league mean equals 1.

### 🧮 Updating During Simulation

After every simulated match:
1. Update each team’s goals and matches played.  
2. Recompute `base_lambda`, `attack`, and `defense`. 

---

## 🧩 Simulation Workflow

1. Load current league table and remaining fixtures.  
2. Compute initial Elo, attack, defense, and base_lambda.  
3. For each simulation (e.g., 10,000 iterations):
   - Simulate every remaining match (Poisson or Elo model).  
   - Update team stats and parameters dynamically.  
   - Apply tiebreakers (goal difference → goals for → goals against).  
   - Record team positions and key metrics (points, GF, GA).  
4. Aggregate results across all runs to compute:
   - Probability of finishing in each table position,  
   - Title and relegation probabilities,  
   - Average points needed for 1st and 8th place (survival threshold).

---

