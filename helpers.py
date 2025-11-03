import numpy as np
import pandas as pd


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


def simulate_goals(team_a, team_b, base_lambda, attack, defense, 
                   elo_a=None, elo_b=None, elo_factor=None, draw_bias=0.1):
    """
    Simulate goals for both teams using Poisson distributions.
    Combines attack/defense strengths and optionally Elo influence.
    Adds small bias to increase draw probability.

    Parameters
    ----------
    team_a, team_b : str
        Team names
    base_lambda : float
        Base expected goals per team
    attack, defense : dict
        Attack and defense multipliers per team (mean ≈ 1)
    elo_a, elo_b : float or None
        Optional Elo ratings (for hybrid correction)
    elo_factor : float or None
        If provided, controls Elo effect scale (e.g. 800)
    draw_bias : float
        Probability of forcing a draw (0–1)

    Returns
    -------
    goals_a, goals_b : int, int
        Simulated goals for teams A and B
    """
    exp_a = base_lambda * attack[team_a] * defense[team_b]
    exp_b = base_lambda * attack[team_b] * defense[team_a]

    # optional Elo adjustment
    if elo_a is not None and elo_b is not None and elo_factor is not None:
        elo_mult = 10 ** ((elo_a - elo_b) / elo_factor)
        exp_a *= elo_mult
        exp_b /= elo_mult

    goals_a = int(np.random.poisson(exp_a))
    goals_b = int(np.random.poisson(exp_b))

    if goals_a != goals_b and np.random.random() < draw_bias:
        avg_goals = int(round((goals_a + goals_b) / 2))
        goals_a = goals_b = max(0, avg_goals)

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


def init_attack_defense(teams_data):
    """
    Initialize attack and defense strengths and base_lambda from league table.
    """
    df = pd.DataFrame.from_dict(teams_data, orient='index')
    df['GFpg'] = df['GF'] / df['M']
    df['GApg'] = df['GA'] / df['M']

    base_lambda = df['GFpg'].mean()
    attack = (df['GFpg'] / base_lambda).to_dict()
    defense = (df['GApg'] / base_lambda).to_dict()

    # normalize (mean = 1)
    a_mean = np.mean(list(attack.values()))
    d_mean = np.mean(list(defense.values()))
    attack = {t: v / a_mean for t, v in attack.items()}
    defense = {t: v / d_mean for t, v in defense.items()}

    return base_lambda, attack, defense


def recompute_attack_defense(gf, ga, games, normalize=True):
    """
    Recompute base_lambda, attack, defense after matches.
    """
    df = pd.DataFrame({
        'GF': pd.Series(gf),
        'GA': pd.Series(ga),
        'M': pd.Series(games)
    })
    df['GFpg'] = df['GF'] / df['M'].replace(0, np.nan)
    df['GApg'] = df['GA'] / df['M'].replace(0, np.nan)
    df.fillna(df.mean(numeric_only=True), inplace=True)

    base_lambda = df['GFpg'].mean()
    attack = (df['GFpg'] / base_lambda).to_dict()
    defense = (df['GApg'] / base_lambda).to_dict()

    if normalize:
        a_mean = np.mean(list(attack.values()))
        d_mean = np.mean(list(defense.values()))
        attack = {t: v / a_mean for t, v in attack.items()}
        defense = {t: v / d_mean for t, v in defense.items()}

    return base_lambda, attack, defense


def fast_recompute_attack_defense(gf, ga, games):
    gfpg = {t: gf[t]/games[t] if games[t]>0 else 0 for t in gf}
    gapg = {t: ga[t]/games[t] if games[t]>0 else 0 for t in ga}
    base = np.mean(list(gfpg.values()))
    attack = {t: gfpg[t]/base for t in gf}
    defense = {t: gapg[t]/base for t in ga}
    mean_a = np.mean(list(attack.values()))
    mean_d = np.mean(list(defense.values()))
    attack = {t: v/mean_a for t,v in attack.items()}
    defense = {t: v/mean_d for t,v in defense.items()}
    return base, attack, defense