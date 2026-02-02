import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="League final positions simulation",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent / "output" / "after3rdMatchday"
FILE_PATHS = {
    'teams': DATA_DIR / 'teams_data.json',
    'prob_table': DATA_DIR / 'prob_table.json',
    'next_matchday': DATA_DIR / 'next_matchday_probs.json',
    'remaining': DATA_DIR / 'remaining_matches.json',
    'points': DATA_DIR / 'estimated_points_needed.json'
}

# Load data functions
@st.cache_data
def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

# Main app
def main():
    st.markdown('<h1 class="main-header">⚽ League final positions simulation</h1>', unsafe_allow_html=True)
    
    # Load data
    try:
        teams_data = load_json(FILE_PATHS['teams'])
        prob_table = load_json(FILE_PATHS['prob_table'])
        next_matchday = load_json(FILE_PATHS['next_matchday'])
        remaining_matches = load_json(FILE_PATHS['remaining'])
        points_needed = load_json(FILE_PATHS['points'])
            
    except FileNotFoundError as e:
        st.error(f"⚠️ Error: Could not find data files. Please upload the required JSON files.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"⚠️ Error: Invalid JSON format in one of the files.")
        st.stop()
    
    # Display all sections
    show_overview(teams_data, prob_table, points_needed)
    st.markdown("---")
    
    show_current_standings(teams_data)
    st.markdown("---")
    
    show_position_probabilities(prob_table)
    st.markdown("---")
    
    show_next_matchday(next_matchday)
    st.markdown("---")

def show_overview(teams_data, prob_table, points_needed):
    """Display overview with key metrics and insights"""
    st.markdown('<h2 class="section-header">📈 Simulation overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
        
    with col1:
        total_matches = sum(team['M'] for team in teams_data.values())
        st.metric("Matches played", total_matches // 2)

    with col2:
        st.metric("Matches remaining", 44 - (total_matches // 2))
    
    with col3:
        st.metric("Estimated points for title", f"{points_needed['points_for_title']:.1f}")
    
    with col4:
        st.metric("Estimated points for safe positions", f"{points_needed['points_for_safety']:.1f}")
    
    st.markdown("")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Title race leaders")
        # Get top 3 teams by title probability
        title_probs = {team: probs['pos_1'] for team, probs in prob_table.items()}
        top_3 = sorted(title_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for i, (team, prob) in enumerate(top_3, 1):
            current_pts = teams_data[team]['Pts']
            st.markdown(f"""
                <div class="metric-card">
                    <strong>{i}. {team}</strong><br>
                    Title probability: <strong>{prob*100:.1f}%</strong><br>
                    Current points: {current_pts}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("")
    
    with col2:
        st.subheader("⚠️ Relegation battle")
        # Get bottom 3 teams by safety (high prob of bottom positions)
        num_teams = len(prob_table)
        bottom_pos = f'pos_{num_teams}'
        if bottom_pos in list(prob_table.values())[0]:
            relegation_probs = {team: probs[bottom_pos] for team, probs in prob_table.items()}
            bottom_3 = sorted(relegation_probs.items(), key=lambda x: x[1], reverse=True)[:3]
            
            for i, (team, prob) in enumerate(bottom_3, 1):
                current_pts = teams_data[team]['Pts']
                st.markdown(f"""
                    <div class="metric-card">
                        <strong>{i}. {team}</strong><br>
                        Last place probability: <strong>{prob*100:.1f}%</strong><br>
                        Current points: {current_pts}
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("")
    
    # Championship probability chart
    st.markdown('<h3 class="section-header">🏅 Championship probabilities</h3>', unsafe_allow_html=True)
    
    title_df = pd.DataFrame([
        {'Team': team, 'Probability': round(prob['pos_1'] * 100, 2)}
        for team, prob in prob_table.items()
    ]).sort_values('Probability', ascending=True)
    
    fig = px.bar(
        title_df,
        x='Probability',
        y='Team',
        orientation='h',
        labels={'Probability': 'Championship probability [%]'},
        color='Probability',
        color_continuous_scale='Blues',
        text='Probability'
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_current_standings(teams_data):
    """Display current league standings"""
    st.markdown('<h2 class="section-header">📊 Current league standings</h2>', unsafe_allow_html=True)
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(teams_data, orient='index')
    df['Team'] = df.index
    df = df.sort_values(['Pts', 'GD', 'GF'], ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = 'Pos'
    
    # Reorder columns
    df = df[['Team', 'M', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']]
    
    # Display table with styling
    st.dataframe(
        df.style.background_gradient(subset=['Pts'], cmap='Greens')
              .background_gradient(subset=['GD'], cmap='RdYlGn')
              .format({'GF': '{:.0f}', 'GA': '{:.0f}', 'GD': '{:+.0f}', 'Pts': '{:.0f}'}),
        use_container_width=True,
        height=400
    )
    
    # Stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚽ Top scorers")
        top_scorers = df.nlargest(5, 'GF')[['Team', 'GF']].sort_values('GF', ascending=True)
        fig = px.bar(top_scorers, x='GF', y='Team', orientation='h', 
                     labels={'GF': 'Goals scored'}, color='GF', color_continuous_scale='Reds',
                     text='GF')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Best defenses")
        best_defense = df.nsmallest(5, 'GA')[['Team', 'GA']].sort_values('GA', ascending=False)
        fig = px.bar(best_defense, x='GA', y='Team', orientation='h',
                     labels={'GA': 'Goals conceded'}, color='GA', color_continuous_scale='Blues_r',
                     text='GA')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def show_position_probabilities(prob_table):
    """Display position probability heatmap and charts"""
    st.markdown('<h2 class="section-header">🎯 Position probabilities</h2>', unsafe_allow_html=True)
    
    st.info("This heatmap shows the probability of each team finishing in each position based on Monte Carlo simulations.")
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(prob_table, orient='index')
    df = df * 100  # Convert to percentages
    
    # Sort by first position probability
    df = df.sort_values('pos_1', ascending=True)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=[f'Pos {i}' for i in range(1, len(df.columns) + 1)],
        y=df.index,
        colorscale='YlGnBu',
        text=df.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Probability [%]")
    ))
    
    fig.update_layout(
        title="Position probability heatmap [%]",
        xaxis_title="Final position",
        yaxis_title="Team",
        height=600,
        hovermode=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Most likely position for each team
    st.markdown('<h3 class="section-header">📍 Most likely final position</h3>', unsafe_allow_html=True)
    
    most_likely = []
    for team in df.index:
        max_prob = df.loc[team].max()
        max_pos = df.loc[team].idxmax()
        pos_num = int(max_pos.split('_')[1])
        most_likely.append({
            'Team': team,
            'Most likely position': pos_num,
            'Probability': round(max_prob, 2)
        })
    
    ml_df = pd.DataFrame(most_likely).sort_values('Most likely position', ascending=False)
    
    num_positions = len(df.columns)
    
    fig = px.scatter(
        ml_df,
        x='Most likely position',
        y='Team',
        size='Probability',
        color='Probability',
        color_continuous_scale='Viridis',
        labels={'Probability': 'Probability [%]'},
        title='Most likely final position by team'
    )
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'trace'}
    )
    fig.update_xaxes(
        autorange='reversed',
        tickmode='linear',
        tick0=1,
        dtick=1,
        range=[num_positions + 0.5, 0.5]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Team-specific position distribution
    st.markdown('<h3 class="section-header">📊 Team position distribution</h3>', unsafe_allow_html=True)
    
    # Team selector dropdown
    selected_team = st.selectbox(
        "Select a team to view their position distribution:",
        options=sorted(prob_table.keys())
    )
    
    # Get position probabilities for selected team
    team_probs = prob_table[selected_team]
    positions = list(range(1, len(team_probs) + 1))
    probabilities = [round(team_probs[f'pos_{i}'] * 100, 2) for i in positions]
    
    # Create DataFrame for plotting
    dist_df = pd.DataFrame({
        'Position': positions,
        'Probability': probabilities
    })
    
    # Create bar chart
    fig = px.bar(
        dist_df,
        x='Position',
        y='Probability',
        labels={'Probability': 'Probability [%]', 'Position': 'Final Position'},
        title=f'Distribution of Final Positions for {selected_team}',
        text='Probability'
    )
    
    fig.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside',
        marker_color='skyblue'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis_title='Probability [%]',
        yaxis_range=[0, max(probabilities) * 1.2]
    )
    
    fig.update_xaxes(
        tickmode='linear',
        tick0=1,
        dtick=1
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_next_matchday(next_matchday):
    """Display next matchday predictions"""
    st.markdown('<h2 class="section-header">🗓️ Next matchday predictions</h2>', unsafe_allow_html=True)
    
    st.info("Win probabilities for upcoming matches based on team strengths and current form.")
    
    for match in next_matchday:
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"### {match['Team A']}")
            st.markdown(f"**Win: {match['A_win_%']:.1f}%**")
        
        with col2:
            st.markdown("### vs")
            st.markdown(f"**Draw: {match['Draw_%']:.1f}%**")
        
        with col3:
            st.markdown(f"### {match['Team B']}")
            st.markdown(f"**Win: {match['B_win_%']:.1f}%**")
        
        # Probability bar
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=['Outcome'],
            x=[match['A_win_%']],
            name=match['Team A'],
            orientation='h',
            marker=dict(color='#1f77b4'),
            text=f"{match['A_win_%']:.1f}%",
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            y=['Outcome'],
            x=[match['Draw_%']],
            name='Draw',
            orientation='h',
            marker=dict(color='#7f7f7f'),
            text=f"{match['Draw_%']:.1f}%",
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            y=['Outcome'],
            x=[match['B_win_%']],
            name=match['Team B'],
            orientation='h',
            marker=dict(color='#ff7f0e'),
            text=f"{match['B_win_%']:.1f}%",
            textposition='inside'
        ))
        
        fig.update_layout(
            barmode='stack',
            height=100,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()