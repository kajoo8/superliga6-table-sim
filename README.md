# ⚽ Monte Carlo League Simulation Dashboard

Interactive Streamlit dashboard for visualizing Monte Carlo simulation results of league final positions.

## Features

### 📈 Simulation Overview
- Key metrics: number of teams, matches played, points needed for title and safety
- Title race leaders with championship probabilities
- Relegation battle statistics
- Championship probability bar chart for all teams

### 📊 Current League Standings
- Complete league table with all statistics (M, W, D, L, GF, GA, GD, Pts)
- Color-coded visualization (points in green gradient, goal difference in red-yellow-green)
- Top 5 scorers chart
- Top 5 best defenses chart

### 🎯 Position Probabilities
- Interactive heatmap showing probability of each team finishing in each position
- Most likely final position scatter plot
- Team-specific position distribution with dropdown selector
- All probabilities rounded to 2 decimal places

### 🗓️ Next Matchday Predictions
- Win/draw probabilities for upcoming matches
- Visual probability bars for each fixture
- Team-by-team matchup analysis

### 📅 Remaining Fixtures
- Complete list of remaining matches
- Distribution of remaining matches by team
- Visual bar chart showing fixture count per team

## Installation

```bash
pip install streamlit pandas plotly
```

## Required Data Files

The application expects the following JSON files in the `output/after3rdMatchday/` directory:

- `teams_data.json` - Current team statistics
- `prob_table.json` - Position probability table
- `next_matchday_probs.json` - Next matchday predictions
- `remaining_matches.json` - List of remaining fixtures
- `estimated_points_needed.json` - Points estimates for title and safety

## Usage

```bash
streamlit run streamlitApp.py
```

## Data Format

### teams_data.json
```json
{
  "Team Name": {
    "M": 3,
    "W": 2,
    "D": 1,
    "L": 0,
    "GF": 5,
    "GA": 2,
    "GD": 3,
    "Pts": 7
  }
}
```

### prob_table.json
```json
{
  "Team Name": {
    "pos_1": 0.45,
    "pos_2": 0.30,
    "pos_3": 0.15,
    ...
  }
}
```

### next_matchday_probs.json
```json
[
  {
    "Team A": "Team 1",
    "Team B": "Team 2",
    "A_win_%": 45.5,
    "Draw_%": 25.0,
    "B_win_%": 29.5
  }
]
```

### remaining_matches.json
```json
[
  ["Home Team", "Away Team"],
  ["Team A", "Team B"]
]
```

### estimated_points_needed.json
```json
{
  "points_for_title": 85.5,
  "points_for_safety": 38.2
}
```

## Features

- **Single Page Layout**: All statistics visible on one page without navigation
- **Dark Mode Support**: Optimized styling for both light and dark themes
- **Interactive Visualizations**: Hover-free charts with values displayed directly on bars
- **Responsive Design**: Adapts to different screen sizes
- **Team Selector**: Dropdown menu to analyze individual team position distributions

## Customization

The dashboard uses custom CSS for styling. Key style elements can be modified in the `st.markdown()` section at the top of the file:

- `.main-header` - Main dashboard title
- `.section-header` - Section headers
- `.metric-card` - Metric display cards (title race, relegation battle)

## Dependencies

- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations
- `json` - JSON file handling
- `pathlib` - File path operations

## License

This project is open source and available under the MIT License.
