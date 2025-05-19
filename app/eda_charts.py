import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(style="darkgrid")

def show():
    st.title("📊 Exploratory Data Analysis")

    # Load dataset
    df = pd.read_csv("data/netflix_cleaned.csv")

    # Clean 'duration' column
    df['duration'] = df['duration'].str.extract('(\d+)').astype(float)

    # Explode genres
    df_exploded = df.copy()
    df_exploded['genre'] = df_exploded['listed_in'].str.split(', ')
    df_exploded = df_exploded.explode('genre')

    # Map country abbreviations
    country_abbr = {
        'United States': 'US', 'United Kingdom': 'UK', 'India': 'IN',
        'South Korea': 'KR', 'Canada': 'CA', 'Australia': 'AU',
        'Germany': 'DE', 'France': 'FR', 'Japan': 'JP', 'Mexico': 'MX'
    }
    df['country_abbr'] = df['country'].map(country_abbr).fillna(df['country'])

    charts = [
        {
            "title": "Distribution of Content Type",
            "plot_func": lambda ax: sns.countplot(data=df, x="type", palette="Set2", ax=ax),
            "columns": ["type"],
            "purpose": "Shows TV Shows vs Movies count.",
            "insights": "Movies dominate the catalog."
        },
        {
            "title": "Top 10 Genres by Number of Titles",
            "plot_func": lambda ax: (
                df_exploded['genre']
                .value_counts()
                .head(10)
                .plot(kind='pie', autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4), ax=ax)
            ),
            "columns": ["listed_in"],
            "purpose": "Visualize the genre share in a proportionate manner.",
            "insights": "Drama and Comedy dominate the genre distribution."
        },
        {
            "title": "Top 10 Countries by Content Count",
            "plot_func": lambda ax: sns.lineplot(
                x=df['country_abbr'].value_counts().head(10).index,
                y=df['country_abbr'].value_counts().head(10).values,
                marker="o", color="#E50914", ax=ax
            ),
            "columns": ["country"],
            "purpose": "Country contributions over ranking.",
            "insights": "US, IN, UK lead."
        },
        {
            "title": "Number of Releases per Year",
            "plot_func": lambda ax: df['release_year'].value_counts().sort_index().plot(kind='line', color="#E50914", ax=ax),
            "columns": ["release_year"],
            "purpose": "Trends over years.",
            "insights": "Spike from 2015-2020."
        },
        {
            "title": "TV Shows: Season Count Distribution",
            "plot_func": lambda ax: df[df['type'] == 'TV Show']['season_count'].value_counts().sort_index().rename(lambda x: f"Season {int(x)}").plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["type", "season_count"],
            "purpose": "How many seasons?",
            "insights": "1–3 seasons common."
        },
        {
            "title": "Top 10 Directors with Most Titles",
            "plot_func": lambda ax: df['director'].value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["director"],
            "purpose": "Prolific directors.",
            "insights": "Some have 10+ titles."
        },
        {
            "title": "Movie Duration Distribution",
            "plot_func": lambda ax: df[df['type'] == 'Movie']['duration'].plot(kind='hist', bins=30, color="#E50914", ax=ax),
            "columns": ["type", "duration"],
            "purpose": "Movie length distribution.",
            "insights": "Most between 80-120 mins."
        },
        {
            "title": "Content Rating Distribution",
            "plot_func": lambda ax: df['rating'].value_counts().plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["rating"],
            "purpose": "Rating frequency.",
            "insights": "TV-MA and TV-14 dominate."
        },
        {
            "title": "Content Added Over Time",
            "plot_func": lambda ax: pd.to_datetime(df['date_added']).dt.year.value_counts().sort_index().plot(kind='line', color="#E50914", ax=ax),
            "columns": ["date_added"],
            "purpose": "Addition trend.",
            "insights": "Major additions 2017-2020."
        },
        {
            "title": "Average Movie Duration by Genre",
            "plot_func": lambda ax: df_exploded[df_exploded['type'] == 'Movie'].groupby('genre')['duration'].mean().sort_values(ascending=False).head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["type", "listed_in", "duration"],
            "purpose": "Avg movie length by genre.",
            "insights": "Documentaries longer."
        },
        {
        "title": "Movie Durations by Genre",
        "plot_func": lambda ax: sns.boxplot(
        data=df_exploded[df_exploded['type'] == 'Movie'].loc[lambda x: x['genre'].isin(
        x['genre'].value_counts().head(8).index)],
        x="duration", y="genre", palette="Reds", ax=ax),"columns": ["type", "listed_in", "duration"],"purpose": "Spread of movie durations across genres.","insights": "Documentaries have high variance; most other genres fall between 60–120 mins."
        },  
        {
            "title": "Content Count by Month Added",
            "plot_func": lambda ax: pd.to_datetime(df['date_added']).dt.month.map({
                1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'
            }).value_counts().reindex(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["date_added"],
            "purpose": "Monthly additions.",
            "insights": "Mid-year and year-end surges."
        },
        {
            "title": "Top Production Countries",
            "plot_func": lambda ax: df['country_abbr'].value_counts().head(10).sort_values().plot(kind='barh', color="#E50914", ax=ax),
            "columns": ["country"],
            "purpose": "Visualize top producing countries clearly.",
            "insights": "US and India dominate production."
        },
        {
            "title": "Movie vs TV Show by Country(Top 5)",
            "plot_func": lambda ax: (
                df[df['country_abbr'].isin(df['country_abbr'].value_counts().head(5).index)]
                .groupby(['country_abbr', 'type'])
                .size()
                .unstack()
                .plot(kind='bar', stacked=True, color=["#E50914", "#430b0b"], ax=ax)
            ),
            "columns": ["country", "type"],
            "purpose": "Content type by country.",
            "insights": "Shows vs movies differ by country."
        },
        {
            "title": "TV Show Duration (Seasons)",
            "plot_func": lambda ax: df[df['type']=='TV Show']['season_count'].value_counts().head(5).rename(lambda x: f"Season {int(x)}").plot(kind='pie', autopct='%1.1f%%', ax=ax),
            "columns": ["type", "season_count"],
            "purpose": "TV show length distribution.",
            "insights": "Most have just 1 season."
        },
        {
            "title": "Content Count by Day of Week Added",
            "plot_func": lambda ax: sns.lineplot(
                x=pd.to_datetime(df['date_added']).dt.day_name().map({
                    'Monday':'Mon', 'Tuesday':'Tue', 'Wednesday':'Wed', 'Thursday':'Thu',
                    'Friday':'Fri', 'Saturday':'Sat', 'Sunday':'Sun'
                }).value_counts().reindex(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']).index,
                y=pd.to_datetime(df['date_added']).dt.day_name().map({
                    'Monday':'Mon', 'Tuesday':'Tue', 'Wednesday':'Wed', 'Thursday':'Thu',
                    'Friday':'Fri', 'Saturday':'Sat', 'Sunday':'Sun'
                }).value_counts().reindex(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']).values,
                marker="o", color="#E50914", ax=ax
            ),
            "columns": ["date_added"],
            "purpose": "Weekday content additions.",
            "insights": "Fridays/weekends popular."
        },
        {
            "title": "Correlation Heatmap of Numeric Features",
            "plot_func": lambda ax: sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=True, cmap='coolwarm', ax=ax),
            "columns": ["duration", "release_year", "season_count"],
            "purpose": "Correlation between numeric fields.",
            "insights": "Season count and release year show slight correlation."
        },
        {
            "title": "Monthly Releases Trend by Content Type",
            "plot_func": lambda ax: (
                df.groupby([pd.to_datetime(df['date_added']).dt.to_period('M'), 'type'])
                .size()
                .unstack()
                .fillna(0)
                .plot(ax=ax, color=["#E50914", "#430b0b"])
            ),
            "columns": ["date_added", "type"],
            "purpose": "Monthly release trends by content type.",
            "insights": "Movies and TV Shows added variably over time."
        }
    ]

    for i in range(0, len(charts), 3):
        cols = st.columns(3)
        for j, chart in enumerate(charts[i:i+3]):
            with cols[j]:
                st.subheader(chart["title"])
                fig, ax = plt.subplots(figsize=(5, 4))
                try:
                    chart["plot_func"](ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error rendering chart: {e}")
                st.markdown(f"<span style='color:red'><b>Columns Used:</b></span> {', '.join(chart['columns'])}", unsafe_allow_html=True)
                st.markdown(f"<span style='color:red'><b>Purpose:</b></span> {chart['purpose']}", unsafe_allow_html=True)
                st.markdown(f"<span style='color:red'><b>Insights:</b></span> {chart['insights']}", unsafe_allow_html=True)