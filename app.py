import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(layout = 'wide', page_title= 'Startup analysis')

# CUSTOM CSS
st.markdown("""
<style>

/* Main App Background */
.main {
    background-color: #0E1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E0F2FE, #BFDBFE);
    border-right: 1px solid #93C5FD;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #1F2937, #111827);
    border: 1px solid #374151;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

/* Metric Hover Effect */
div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    transition: 0.3s ease-in-out;
}

/* Metric Label */
div[data-testid="metric-container"] label {
    color: #9CA3AF !important;
    font-size: 15px !important;
}

/* Metric Value */
div[data-testid="metric-container"] div {
    color: white !important;
}

/* Headers */
h1, h2, h3 {
    color: white;
}

/* Divider */
hr {
    border-color: #374151;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 16px;
    font-weight: 600;
}

/* Sidebar labels */
.css-1d391kg label {
    font-size: 14px !important;
}
/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {
    color: #1E293B !important;
}

/* Sidebar selectbox text */
section[data-testid="stSidebar"] .stSelectbox label {
    color: white !important;
}

/* Sidebar multiselect text */
section[data-testid="stSidebar"] .stMultiSelect label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


df = pd.read_csv('startup-cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors = "coerce")
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year



#st.dataframe(df)

def load_overall_analysis():
    st.title('Interactive analytics dashboard for Indian startups')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        #Total invested amount
        total  = round(filtered_df['amount'].sum())
        st.metric('Total Funding',str(total) + ' Cr')

    with col2:
        #Max amount infused in a startup
        max_funding= filtered_df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Highest Funding',str(max_funding) + ' Cr')

    with col3:
        #Avg ticket size
        avg_funding = round(filtered_df.groupby('startup')['amount'].sum().mean())
        st.metric('Average Investment', str(avg_funding) + ' Cr')

    with col4:
        #total funded startup
        num_startups = filtered_df['startup'].nunique()
        st.metric('Total Startups', num_startups)
    st.markdown("---")


    st.subheader('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = filtered_df.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp_df = filtered_df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5= px.line(temp_df, x = 'x-axis', y= 'amount')
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")


    st.subheader("Top Funding Cities")
    city_df = (
        filtered_df.groupby('city')['amount']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    fig6= px.bar(
        x=city_df.values,
        y=city_df.index,
        orientation='h',
        labels={
            'x': 'Total Funding',
            'y': 'City'})
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("---")


    st.subheader("Top Sectors")
    sector_df = (
        filtered_df.groupby('vertical')['amount']
        .sum()
        .sort_values(ascending=False)
        .head(10))
    fig7 = px.pie(
        values=sector_df.values,
        names=sector_df.index)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("---")


    st.subheader("Funding Round Distribution")
    round_df = (
        filtered_df.groupby('round')['amount']
        .sum()
        .sort_values(ascending=False)
        .head(10))
    fig8 = px.bar(
        x=round_df.index,
        y=round_df.values,
        labels={
            'x': 'Funding Round',
            'y': 'Funding Amount'})
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("---")

    st.subheader("Top Active Investors")
    all_investors = []
    for investors in filtered_df['investors'].dropna():
        investor_names = investors.split(',')
        for name in investor_names:
            all_investors.append(name.strip())
    investor_df = pd.Series(all_investors).value_counts().head(10)

    fig9 = px.bar(
        x=investor_df.index,
        y=investor_df.values,
        labels={'x': 'Investor','y': 'Number of Investments'})
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown("---")

    st.subheader("Funding Heatmap")
    heatmap_df = filtered_df.pivot_table(values='amount',index='year',columns='month',aggfunc='sum')

    fig10 = px.imshow(heatmap_df,aspect='auto')
    st.plotly_chart(fig10, use_container_width=True)

    st.info("""
    Insights:

    • Bengaluru dominates startup funding ecosystem.
    
    • FinTech and E-commerce sectors receive highest investments.
    
    • Early-stage funding rounds are most common.
    
    • Startup funding rapidly increased after 2015.
    """)

def load_startup_details():
    st.title('Startup Analysis')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total = round(startup_df['amount'].sum())
        st.metric('Total Funding', str(total) + ' Cr')

    with col2:
        max_funding = round(startup_df['amount'].max())
        st.metric('Highest Funding', str(max_funding) + ' Cr')

    with col3:
        investors = startup_df['investors'].nunique()
        st.metric('Investors', investors)

    with col4:
        rounds = startup_df['round'].nunique()
        st.metric('Rounds', rounds)

    st.subheader("Funding Timeline")
    timeline_df = (
        startup_df.groupby('year')['amount']
        .sum()
        .reset_index())
    fig9 = px.line(
        timeline_df,
        x='year',
        y='amount',
        markers=True)
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("Funding Details")
    st.dataframe(startup_df[[
                'date','investors','round','amount','city','vertical']])

    st.subheader("Similar Startups")
    sector = startup_df['vertical'].values[0]
    similar_df = df[
        (df['vertical'] == sector)
        & (df['startup'] != selected_startup)]
    st.write(similar_df['startup'].unique())


def load_investor_details(investor):
    investor_df = filtered_df[
        filtered_df['investors'].str.contains(investor, na=False)]
    st.title(investor)

    #load the last 5 investments by investors
    st.subheader("Most Recent Investments")
    last_5df = investor_df.head()[['date','startup','vertical','city','round','amount']]
    st.dataframe(last_5df)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        #biggest investments
        big_series = (investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head())
        st.subheader('Biggest Investments')

        fig = px.bar(
            x=big_series.index,
            y=big_series.values,
            labels={
                'x': 'Startup',
                'y': 'Investment Amount'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        vertical_series = (investor_df.groupby('vertical')['amount'].sum().head())
        st.subheader('Sectors Invested in')
        fig1 = px.pie(values=vertical_series.values,names=vertical_series.index)
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")


    # stage
    stage = (
        investor_df.groupby('round')['amount'].sum().sort_values(ascending=False).head())
    st.subheader('Funding Stage Distribution')

    fig2 = px.pie(values=stage.values,names=stage.index)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")
    #city
    city = (investor_df.groupby('city')['amount'].sum().head())
    st.subheader('Investments Across Cities')
    fig3 = px.bar(
        x=city.index,
        y=city.values,
        labels={'x': 'City','y': 'Investment Amount'})
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("---")

    #YoY Investment
    filtered_df['year'] = filtered_df['date'].dt.year
    year_series = (investor_df.groupby('year')['amount'].sum().reset_index())
    st.subheader('Year Over Year Investment')
    fig4 = px.line(year_series,x='year',y='amount',markers=True)
    st.plotly_chart(fig4, use_container_width=True)

st.sidebar.markdown("""
# Startup Funding Analysis
""")

st.sidebar.caption("Dashboard Navigation")

option = st.sidebar.selectbox(
    'Select One',
    ['Overall Analysis','Startup','Investor','About Project'])

st.sidebar.markdown("---")

with st.sidebar.expander("Filters", expanded=True):

    selected_year = st.multiselect(
        "Select Year",
        sorted(df['year'].dropna().unique())
    )

    selected_city = st.multiselect(
        "Select City",
        sorted(df['city'].dropna().unique())
    )

    selected_sector = st.multiselect(
        "Select Sector",
        sorted(df['vertical'].dropna().unique())
    )

    selected_round = st.multiselect(
        "Funding Round",
        sorted(df['round'].dropna().unique())
    )
filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df['year'].isin(selected_year)]

if selected_city:
    filtered_df = filtered_df[filtered_df['city'].isin(selected_city)]

if selected_sector:
    filtered_df = filtered_df[filtered_df['vertical'].isin(selected_sector)]

if selected_round:
    filtered_df = filtered_df[filtered_df['round'].isin(selected_round)]



if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(filtered_df['startup'].dropna().unique()))
    startup_df = filtered_df[filtered_df['startup'] == selected_startup]
    load_startup_details()

elif option == 'Investor':

    investor_series = filtered_df['investors'].dropna()

    investor_list = []

    for investors in investor_series:

        investor_names = investors.split(',')

        for name in investor_names:
            investor_list.append(name.strip())

    investor_list = sorted(set(investor_list))

    selected_investor = st.sidebar.selectbox(
        'Select Investor',
        investor_list
    )

    load_investor_details(selected_investor)

elif option == 'About Project':
    st.title('Startup Funding Intelligence Dashboard')
    st.write("""
        This project analyzes the Indian startup ecosystem
        using interactive visualizations and business insights.

        The dashboard helps users explore:
        - startup funding trends
        - investor activities
        - sector performance
        - city-wise funding distribution
        - startup growth patterns
        """)

    st.subheader("📂 Dataset Source")
    st.write("""
        Dataset used in this project:

        Kaggle Startup Funding Dataset

        The dataset contains information about:
        - startups
        - investors
        - funding rounds
        - funding amounts
        - cities
        - industries
        - investment dates
        """)

    st.subheader("🛠️ Tools & Technologies Used")
    st.write("""
        - Python
        - Streamlit
        - Pandas
        - Plotly
        - PyCharm
        - Kaggle Dataset
        """)

    st.subheader("🎯 Project Objectives")
    st.write("""
        The main objectives of this project are:

        - Analyze Indian startup ecosystem
        - Identify funding trends
        - Understand investor behavior
        - Compare startup sectors
        - Visualize funding distribution
        - Build an interactive analytics dashboard
        """)

    st.subheader("💡 Skills Demonstrated")
    st.write("""
        Through this project, the following skills were demonstrated:

        - Data Cleaning
        - Exploratory Data Analysis
        - Data Visualization
        - Dashboard Development
        - Business Intelligence
        - Interactive UI Design
        - Python Programming
        - Streamlit Web App Development
        """)

    st.subheader("⭐ Dashboard Features")
    st.write("""
        Features included in the dashboard:

        ✅ Overall startup ecosystem analysis

        ✅ Startup-wise analysis

        ✅ Investor-wise analysis

        ✅ Funding trend visualization

        ✅ Interactive charts using Plotly

        ✅ Funding heatmaps

        ✅ Sector and city analysis

        ✅ KPI metrics and business insights
        """)

    st.markdown("---")
    st.success("End-to-end interactive Business Intelligence dashboard built using Python and Streamlit.")








