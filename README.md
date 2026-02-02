# Monte Carlo League Simulation Dashboard

A comprehensive Streamlit dashboard for visualizing Monte Carlo simulation results of league standings and match outcomes.

## Features

### 📈 Overview
- Key metrics (teams, matches played, points needed for title/safety)
- Title race leaders with probabilities
- Relegation battle analysis
- Championship probability visualization

### 📊 Current Standings
- Live league table with sorting
- Color-coded performance metrics
- Top scorers visualization
- Best defenses comparison

### 🎯 Position Probabilities
- Interactive heatmap showing probability of each final position
- Most likely final position for each team
- Detailed probability distributions

### 🗓️ Next Matchday Predictions
- Win/Draw probabilities for upcoming matches
- Visual probability bars
- Head-to-head predictions

### 📅 Remaining Fixtures
- Complete list of remaining matches
- Fixture count by team
- Visual distribution of remaining games

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: With JSON files in the same directory

Place your JSON files in the same directory as `monte_carlo_app.py`:
- `teams_data.json`
- `prob_table.json`
- `next_matchday_probs.json`
- `remaining_matches.json`
- `estimated_points_needed.json`

Then run:
```bash
streamlit run monte_carlo_app.py
```

### Option 2: Upload files through the app

Run the app:
```bash
streamlit run monte_carlo_app.py
```

Then upload your JSON files using the sidebar file uploaders.

## JSON File Formats

### teams_data.json
```json
{
    "Team Name": {
        "M": matches_played,
        "W": wins,
        "D": draws,
        "L": losses,
        "GF": goals_for,
        "GA": goals_against,
        "GD": goal_difference,
        "Pts": points
    }
}
```

### prob_table.json
```json
{
    "Team Name": {
        "pos_1": probability,
        "pos_2": probability,
        ...
    }
}
```

### next_matchday_probs.json
```json
[
    {
        "Team A": "team_name",
        "A_win_%": win_probability,
        "Draw_%": draw_probability,
        "B_win_%": win_probability,
        "Team B": "team_name"
    }
]
```

### remaining_matches.json
```json
[
    ["Home Team", "Away Team"],
    ["Home Team", "Away Team"]
]
```

### estimated_points_needed.json
```json
{
    "points_for_title": number,
    "points_for_safety": number
}
```

## Navigation

Use the sidebar to switch between different views:
- **Overview**: High-level summary and key insights
- **Current Standings**: League table and team statistics
- **Position Probabilities**: Detailed probability analysis
- **Next Matchday**: Upcoming match predictions
- **Remaining Fixtures**: Schedule of remaining games

## Requirements

- Python 3.8+
- streamlit
- pandas
- plotly

## Tips

- The app will cache data for better performance
- Use the Overview page for quick insights
- Position Probabilities heatmap shows the full distribution
- Next Matchday predictions are based on simulation results
- All visualizations are interactive (hover for details)

## Troubleshooting

**File not found error**: Make sure your JSON files are in the same directory as the app, or upload them using the sidebar.

**JSON decode error**: Verify your JSON files are properly formatted.

**Import error**: Run `pip install -r requirements.txt` to install dependencies.
