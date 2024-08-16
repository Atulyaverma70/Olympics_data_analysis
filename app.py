import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Load datasets
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess the data
df = preprocessor.preprocess(df, region_df)

# Set up the sidebar
st.sidebar.title("Olympics Analysis")
st.sidebar.image(r'images/gettyimages-466313493-2-removebg-preview (1).png', use_column_width=True)
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise analysis', 'Athlete wise analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    # Display appropriate title based on selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {str(selected_year)} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")
    else:
        st.title(f"{selected_country} Performance in {str(selected_year)} Olympics")
    
    st.table(medal_tally)

# Overall Analysis
if user_menu == 'Overall Analysis':
    # Calculate key statistics
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()
    
    # Display statistics
    st.title("Top Statistics till 2016")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Nations")
        st.title(nations)
    with col2:
        st.header("Events")
        st.title(events)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Participating Nations Over Time
    nations_over_time = helper.data_over_time(df, 'region')
    st.title("Participating Nations Over Time")
    fig = px.line(nations_over_time, x="Editions", y="No of Region")
    st.plotly_chart(fig)

    # Events Over Time
    events_over_time = helper.data_over_time(df, 'Event')
    st.title("Events Over Time")
    fig = px.line(events_over_time, x="Editions", y="No of Event")
    st.plotly_chart(fig)

    # Athletes Over Time
    athlete_over_time = helper.data_over_time(df, 'Name')
    st.title("Athletes Over Time")
    fig = px.line(athlete_over_time, x="Editions", y="No of Name")
    st.plotly_chart(fig)

    st.title("No of events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    sns.heatmap(heatmap_data, annot=True, cmap='viridis', ax=ax)
    st.pyplot(fig)

    st.title("Most Successful Players")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
     
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# Country-wise analysis
if user_menu == 'Country-wise analysis':
    st.sidebar.title('Country-wise analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country) 
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(f"{selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)

    st.title(f"Top 10 athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete wise analysis
if user_menu == 'Athlete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold medalist', 'Silver medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=100, ax=ax)
    st.pyplot(fig)

    st.title("Men vs Women Participants Over the Years")
    final = helper.men_v_women(df)
    fig = px.line(final, x="Year", y="Count", color="Sex", title="Participants Over the Years")
    st.plotly_chart(fig)




