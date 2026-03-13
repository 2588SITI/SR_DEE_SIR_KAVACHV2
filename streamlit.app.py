import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Kavach Main Dashboard", page_icon="🚆", layout="wide")

# --- MOCK DATA ---
# 1. Operation Percentage
op_data = pd.DataFrame({'Status': ['Operated', 'Not Operated'], 'Value': [88, 12]})

# 2. Failure Heads
failure_data = pd.DataFrame({'Head': ['Loco', 'Crew', 'Station S&T'], 'Value': [45, 25, 30]})

# 3. Section Trends
section_data = pd.DataFrame({
    'Section':['Sec A', 'Sec B', 'Sec C', 'Sec D', 'Sec E'],
    'Failures':[12, 19, 8, 24, 15]
})

# 4. Crew Training
crew_data = pd.DataFrame({
    'Lobby':['Lobby 1', 'Lobby 2', 'Lobby 3', 'Lobby 4'],
    'Trained':[120, 98, 160, 85],
    'Total':[150, 110, 200, 90]
})

# 5. Station Failure List
station_failures = pd.DataFrame({
    'Station':['NDLS (New Delhi)', 'CNB (Kanpur)', 'PRYJ (Prayagraj)', 'DDU (Pt. DD Upadhyaya)'],
    'Date':['2023-10-24', '2023-10-24', '2023-10-23', '2023-10-22'],
    'Failure Head': ['Station S&T', 'Loco', 'Crew', 'Station S&T'],
    'Severity': ['High', 'Medium', 'Low', 'High']
})

# --- DASHBOARD HEADER ---
st.title("🚆 Kavach Main Dashboard")
st.markdown("---")

# --- ROW 1: KPI Metrics & Loco Status ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Trains Worked on Kavach")
    st.caption("(Last 24 Hours)")
    # Using Streamlit's native metric component
    st.metric(label="Total Trains", value="1,432", delta="12% vs Yesterday")

with col2:
    st.subheader("Operation Percentage")
    # Donut Chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=op_data['Status'], 
        values=op_data['Value'], 
        hole=0.7,
        marker_colors=['#10B981', '#E5E7EB'],
        textinfo='none'
    )])
    fig_donut.update_layout(
        showlegend=False, 
        margin=dict(t=10, b=10, l=10, r=10),
        height=200,
        annotations=[dict(text='<b>88%</b>', x=0.5, y=0.5, font_size=30, showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col3:
    st.subheader("Loco Status Summary")
    # Custom HTML/CSS for Status Bubbles
    bubble_html = """
    <div style="display: flex; justify-content: space-around; align-items: center; padding-top: 20px;">
        <div style="text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background-color: #dcfce7; border: 4px solid #22c55e; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="font-size: 20px; font-weight: bold; color: #15803d;">450</span>
            </div>
            <p style="margin-top: 10px; font-weight: 600; color: #4b5563;">Fit</p>
        </div>
        <div style="text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background-color: #fee2e2; border: 4px solid #ef4444; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="font-size: 20px; font-weight: bold; color: #b91c1c;">32</span>
            </div>
            <p style="margin-top: 10px; font-weight: 600; color: #4b5563;">Unfit</p>
        </div>
        <div style="text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background-color: #f3f4f6; border: 4px solid #9ca3af; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="font-size: 20px; font-weight: bold; color: #374151;">120</span>
            </div>
            <p style="margin-top: 10px; font-weight: 600; color: #4b5563;">Pending</p>
        </div>
    </div>
    """
    st.markdown(bubble_html, unsafe_allow_html=True)

st.markdown("---")

# --- ROW 2: Failure Analysis & Section Trends ---
col4, col5 = st.columns(2)

with col4:
    st.subheader("Major Heads of Failure")
    fig_pie = px.pie(
        failure_data, 
        names='Head', 
        values='Value',
        color_discrete_sequence=['#3b82f6', '#f59e0b', '#10b981']
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col5:
    st.subheader("Section-wise Failure Trends")
    fig_line = px.line(
        section_data, 
        x='Section', 
        y='Failures', 
        markers=True,
        line_shape='spline'
    )
    fig_line.update_traces(line_color='#ef4444', marker=dict(size=10))
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# --- ROW 3: Detailed Analytics ---
col6, col7 = st.columns(2)

with col6:
    st.subheader("Crew Training Progress (Lobby-wise)")
    # Reshaping data for grouped bar chart
    crew_melted = crew_data.melt(id_vars='Lobby', value_vars=['Trained', 'Total'], var_name='Type', value_name='Count')
    
    fig_bar = px.bar(
        crew_melted, 
        x='Lobby', 
        y='Count', 
        color='Type', 
        barmode='group',
        color_discrete_map={'Trained': '#3b82f6', 'Total': '#e5e7eb'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col7:
    st.subheader("Recent Station-wise Failures")
    
    def color_severity(val):
        color = '#fee2e2' if val == 'High' else '#fef3c7' if val == 'Medium' else '#dcfce7'
        text_color = '#b91c1c' if val == 'High' else '#b45309' if val == 'Medium' else '#15803d'
        return f'background-color: {color}; color: {text_color}; font-weight: bold;'

    # Applying styling to dataframe
    styled_df = station_failures.style.map(color_severity, subset=['Severity'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
