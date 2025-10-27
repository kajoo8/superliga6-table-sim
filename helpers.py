import numpy as np


def compute_auto_elo(teams_data, alpha=1.0, beta=0.8, gamma=0.2, sigma=100.0):
    """
    Compute initial Elo ratings based on current league standings.
    Uses points per game, goal difference per game, and goals for per game.
    
    Parameters:
    -----------
    teams_data : dict
        Dictionary with team statistics (M, Pts, GD, GF)
    alpha : float
        Weight for points per game
    beta : float
        Weight for goal difference per game
    gamma : float
        Weight for goals for per game
    sigma : float
        Scale factor for Elo distribution
    
    Returns:
    --------
    elo : dict
        Dictionary of team names to Elo ratings
    """
    S = {}
    for t, d in teams_data.items():
        m = d["M"]
        if m <= 0:
            m = 1.0
        ppg = d["Pts"] / m
        gd_pg = d["GD"] / m
        gf_pg = d["GF"] / m
        S[t] = alpha * ppg + beta * gd_pg + gamma * gf_pg
    
    arr = np.array(list(S.values()))
    mean_S = arr.mean()
    std_S = arr.std(ddof=0)
    if std_S == 0:
        std_S = 1.0
    
    elo = {}
    for t, s in S.items():
        elo[t] = 1500.0 + sigma * ((s - mean_S) / std_S)
    
    return {t: round(elo[t]) for t in elo}


def calculate_base_goals(teams_data):
    """
    Calculates BASE_GOALS for whole league based on the actual table.
    
    teams_data: dict:
        {"Team": {"M": int, "GF": int, "GA": int, ...}, ...}
    
    Returns average goals per team per match.
    """
    total_goals = sum(data["GF"] for data in teams_data.values())
    total_matches = sum(data["M"] for data in teams_data.values()) / 2  # every game is counted twice in the table stats
    base_goals = total_goals / total_matches
    return base_goals / 2 # average goals per team per match


def estimate_draw_prob(teams_data):
    """
    Estimates draw prob based on current league data.
    You can change it to static value if preferred, e.g., 0.25.
    """
    total_draws = sum(d["D"] for d in teams_data.values()) / 2.0
    total_matches = sum(d["M"] for d in teams_data.values()) / 2.0
    if total_matches <= 0:
        return 0.25
    return total_draws / total_matches


def expected_score(elo_a, elo_b):
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400.0))


def match_probs(elo_a, elo_b, draw_prob):
    # standard elo expected score
    E_a = 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400.0))
    p_draw = draw_prob
    p_a = (1 - p_draw) * E_a
    p_b = (1 - p_draw) * (1 - E_a)
    # numeric scalling to ensure sum to 1
    tot = p_a + p_draw + p_b
    p_a /= tot; p_draw /= tot; p_b /= tot
    return p_a, p_draw, p_b


def update_elo(elo_a, elo_b, S_a, S_b, K=20):
    """
    Update Elo ratings based on match result.
    
    Parameters:
    -----------
    elo_a, elo_b : float
        Current Elo ratings
    S_a, S_b : float
        Match result scores (1.0, 0.5, or 0.0)
    K : float
        Elo K-factor (sensitivity of rating changes)
    
    Returns:
    --------
    elo_a_new, elo_b_new : float
        Updated Elo ratings
    """
    E_a = expected_score(elo_a, elo_b)
    E_b = 1 - E_a
    
    elo_a_new = elo_a + K * (S_a - E_a)
    elo_b_new = elo_b + K * (S_b - E_b)
    
    return elo_a_new, elo_b_new


def simulate_goals(elo_a, elo_b, base_lambda=1.5):
    """
    Simulate goals for both teams using Poisson distributions.
    Expected goals are based on Elo difference.
    
    Parameters:
    -----------
    elo_a : float
        Elo rating of team A
    elo_b : float
        Elo rating of team B
    base_lambda : float
        Base expected goals (average goals per team)

    Returns:
    --------
    goals_a, goals_b : int, int
        Simulated goals for teams A and B
    """
    # Calculate expected goals based on Elo difference
    exp_a = base_lambda * 10 ** ((elo_a - elo_b) / 800)
    exp_b = base_lambda * 10 ** ((elo_b - elo_a) / 800)

    # Sample from Poisson distributions
    goals_a = np.random.poisson(exp_a)
    goals_b = np.random.poisson(exp_b)

    return goals_a, goals_b


def get_match_result(goals_a, goals_b):
    """
    Determine match result based on goals scored.
    
    Parameters:
    -----------
    goals_a, goals_b : int
        Goals scored by teams A and B

    Returns:
    --------
    S_A, S_B : float
        Match result score (1.0 for win, 0.5 for draw, 0.0 for loss)
    """
    if goals_a > goals_b:
        return 1.0, 0.0  # Team A wins
    elif goals_a == goals_b:
        return 0.5, 0.5  # Draw
    else:

        return 0.0, 1.0  # Team B wins
