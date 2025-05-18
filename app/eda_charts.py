import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set consistent Seaborn style
sns.set(style="darkgrid")

def show():
    st.title("📊 Exploratory Data Analysis")

    # Load cleaned Netflix dataset (make sure the path is correct)
    df = pd.read_csv("data/netflix_cleaned.csv")

    # Clean 'duration' column: extract numeric minutes only
    df['duration'] = df['duration'].str.extract('(\d+)').astype(float)

    # Explode genres for detailed genre analysis
    df_exploded = df.copy()
    df_exploded['genre'] = df_exploded['listed_in'].str.split(', ')
    df_exploded = df_exploded.explode('genre')

    # Dictionary for country abbreviations
    country_abbr = {
        'United States': 'US',
        'United Kingdom': 'UK',
        'India': 'IN',
        'South Korea': 'KR',
        'Canada': 'CA',
        'Australia': 'AU',
        'Germany': 'DE',
        'France': 'FR',
        'Japan': 'JP',
        'Mexico': 'MX',
        # Add more if needed
    }

    # Map country abbreviations, fallback to original if no abbreviation
    df['country_abbr'] = df['country'].map(country_abbr).fillna(df['country'])

    charts = [
        {
            "title": "Distribution of Content Type",
            "plot_func": lambda ax: sns.countplot(data=df, x="type", palette="Set2", ax=ax),
            "columns": ["type"],
            "purpose": "Shows how much content is TV Shows vs Movies.",
            "insights": "Movies dominate the Netflix catalog."
        },
        {
            "title": "Top 10 Genres by Number of Titles",
            "plot_func": lambda ax: df_exploded['genre'].value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["listed_in"],
            "purpose": "Reveals most popular genres.",
            "insights": "Dramas and Comedies are the most frequent."
        },
        {
            "title": "Top 10 Countries by Content Count",
            "plot_func": lambda ax: df['country_abbr'].value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["country"],
            "purpose": "Finds which countries contribute the most content.",
            "insights": "US, India, and UK dominate."
        },
        {
            "title": "Number of Releases per Year",
            "plot_func": lambda ax: df['release_year'].value_counts().sort_index().plot(kind='line', color="#E50914", ax=ax),
            "columns": ["release_year"],
            "purpose": "Tracks release trends over time.",
            "insights": "Sharp increase from 2015–2020, then a dip (likely pandemic)."
        },
        {
            "title": "TV Shows: Season Count Distribution",
            "plot_func": lambda ax: df[df['type'] == 'TV Show']['season_count'].value_counts().sort_index().rename(lambda x: f"Season {int(x)}").plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["type", "season_count"],
            "purpose": "Shows how many seasons most TV shows have.",
            "insights": "1–3 seasons are most common."
        },
        {
            "title": "Top 10 Directors with Most Titles",
            "plot_func": lambda ax: df['director'].value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["director"],
            "purpose": "Highlights prolific directors on Netflix.",
            "insights": "Some directors have 10+ titles."
        },
        {
            "title": "Movie Duration Distribution",
            "plot_func": lambda ax: df[df['type'] == 'Movie']['duration'].plot(kind='hist', bins=30, color="#E50914", ax=ax),
            "columns": ["type", "duration"],
            "purpose": "Analyzes movie length.",
            "insights": "Most movies are between 80–120 minutes."
        },
        {
            "title": "Content Rating Distribution",
            "plot_func": lambda ax: df['rating'].value_counts().plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["rating"],
            "purpose": "Shows how content is rated (TV-MA, PG-13, etc.).",
            "insights": "TV-MA and TV-14 dominate."
        },
        {
            "title": "Content Added Over Time",
            "plot_func": lambda ax: pd.to_datetime(df['date_added']).dt.year.value_counts().sort_index().plot(kind='line', color="#E50914", ax=ax),
            "columns": ["date_added"],
            "purpose": "Tracks when content was added to Netflix.",
            "insights": "Major additions from 2017 to 2020."
        },
        {
            "title": "Top 10 Most Common Actors",
            "plot_func": lambda ax: pd.Series(', '.join(df['cast'].dropna()).split(', ')).value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["cast"],
            "purpose": "Reveals frequently cast actors.",
            "insights": "Many recurring faces across shows/movies."
        },
        {
            "title": "Average Duration by Genre (Movies)",
            "plot_func": lambda ax: df_exploded[df_exploded['type'] == 'Movie'].groupby('genre')['duration'].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='#E50914', ax=ax),
            "columns": ["type", "listed_in", "duration"],
            "purpose": "Shows average movie length per genre.",
            "insights": "Documentaries tend to be longer."
        },
        {
            "title": "Genre Count for TV Shows",
            "plot_func": lambda ax: df_exploded[df_exploded['type'] == 'TV Show']['genre'].value_counts().head(10).plot(kind='bar', color='#E50914', ax=ax),
            "columns": ["type", "listed_in"],
            "purpose": "What genres are most common for TV shows.",
            "insights": "International TV, Drama, and Kids’ shows are common."
        },
        {
            "title": "Content Count by Month Added",
            "plot_func": lambda ax: pd.to_datetime(df['date_added']).dt.month.map({
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
            }).value_counts().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["date_added"],
            "purpose": "Which months Netflix adds more content.",
            "insights": "Mid-year and year-end see content surges."
        },
        {
            "title": "Top Production Countries (Grouped)",
            "plot_func": lambda ax: (
                df['country_abbr']
                .value_counts()
                .groupby(lambda x: x if df['country_abbr'].value_counts()[x] > 50 else 'Others')
                .sum()
                .sort_values(ascending=False)
                .plot(kind='bar', color="#E50914", ax=ax)
            ),
            "columns": ["country"],
            "purpose": "Group small countries to avoid clutter.",
            "insights": "Helps visualize major content producers clearly."
        },
        {
            "title": "Movie vs TV Show by Country (Top 5)",
            "plot_func": lambda ax: (
                df[df['country_abbr'].isin(df['country_abbr'].value_counts().head(5).index)]
                .groupby(['country_abbr', 'type'])
                .size()
                .unstack()
                .plot(kind='bar', ax=ax, color=["#E50914", "#430b0b"])
            ),
            "columns": ["country", "type"],
            "purpose": "Compare content type in top countries.",
            "insights": "TV shows are more common in India and UK than in US."
        },
        {
            "title": "TV Show Duration (Seasons) Pie Chart",
            "plot_func": lambda ax: df[df['type'] == 'TV Show']['season_count'].value_counts().head(5).rename(lambda x: f"Season {int(x)}").plot(kind='pie', autopct='%1.1f%%', ax=ax),
            "columns": ["type", "season_count"],
            "purpose": "Quick view of TV show lengths.",
            "insights": "Most shows have just 1 season."
        },
        {
            "title": "Content Count by Day of Week Added",
            "plot_func": lambda ax: pd.to_datetime(df['date_added']).dt.day_name().map({
                'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 'Thursday': 'Thu',
                'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
            }).value_counts().reindex(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["date_added"],
            "purpose": "Check when content gets added weekly.",
            "insights": "Fridays and weekends see more additions."
        },
        {
            "title": "Top 10 Countries by Content Count (Abbreviated)",
            "plot_func": lambda ax: df['country_abbr'].value_counts().head(10).plot(kind='bar', color="#E50914", ax=ax),
            "columns": ["country"],
            "purpose": "Shows top countries contributing content with short country codes.",
            "insights": "Abbreviated country codes provide cleaner, concise visualization."
        }
    ]

    # Layout: 3 charts per row
    for i in range(0, len(charts), 3):
        row = st.columns(3)
        for j in range(3):
            if i + j < len(charts):
                chart = charts[i + j]
                with row[j]:
                    st.markdown(f"<h4 style='color:#E50914'>{chart['title']}</h4>", unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(5, 4))
                    try:
                        chart["plot_func"](ax)
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Error rendering chart: {e}")
                    st.markdown(f"<b style='color:#E50914'>Columns Used:</b> {', '.join(chart['columns'])}", unsafe_allow_html=True)
                    st.markdown(f"<b style='color:#E50914'>Purpose:</b> {chart['purpose']}", unsafe_allow_html=True)
                    st.markdown(f"<b style='color:#E50914'>Insights:</b> {chart['insights']}", unsafe_allow_html=True)
