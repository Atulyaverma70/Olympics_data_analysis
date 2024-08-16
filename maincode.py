#main file
import numpy as np
import pandas as pd

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Inspect data
print(df.tail())
print(df.shape)

# Filter for Summer Olympics
df = df[df['Season'] == 'Summer']
print(df.shape)

# Merge with region data
print(region_df.tail())
df = df.merge(region_df, on='NOC', how='left')
print(df.tail())

# Check for unique regions, null values, and duplicates
print(df['region'].unique().shape)
print(df.isnull().sum())
print(df.duplicated().sum())

# Drop duplicates
df.drop_duplicates(inplace=True)
print(df.duplicated().sum())

# Medal counts and one-hot encoding
print(df['Medal'].value_counts())
df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
print(df.tail())

# Group by NOC for medal tally
print(df.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index())

# Create medal tally dataframe
medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
print(medal_tally)

# List of years and countries
years = df['Year'].unique().tolist()  
years.sort()
years.insert(0, 'Overall')
print(years)

country = np.unique(df['region'].dropna().values).tolist()
country.sort()
country.insert(0, 'Overall')
print(country)

# Function to fetch medal tally
def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

# Test the function
print(fetch_medal_tally(df,year='2016', country='India'))

df['Year'].unique().shape[0]-1
df['City'].unique().shape[0]
df['Sport'].unique().shape[0]
df['Event'].unique().shape[0]
df['Name'].unique().shape[0]
df['region'].unique().shape[0]

# Create a DataFrame showing the number of nations participating over time
nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
nations_over_time.columns = ['Editions', 'No of Countries']  # Rename columns for clarity
nations_over_time = nations_over_time.sort_values('Editions')  # Sort based on Editions

import plotly.express as px

fig=px.line(nations_over_time,x="Editions",y="No of Countries")
fig.show()

nations_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()

import seaborn as sns
import matplotlib.pyplot as plt

x = df.drop_duplicates(subset=['Sport', 'Year', 'Event'])

plt.figure(figsize=(25, 25))
heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
sns.heatmap(heatmap_data, annot=True, cmap='viridis')
plt.title('Sports and Events Over Time')
plt.show()

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

temp_df = df.dropna(subset=['Medal'])  
temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
new_df = temp_df[temp_df['region'] == 'India']
final_df = new_df.groupby('Year').count()['Medal'].reset_index()
fig = px.line(final_df, x="Year", y="Medal", title='Medal Count Over Time')
fig.show()


new_df = temp_df[temp_df['region'] == 'India']
plt.figure(figsize=(25,25))
sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True )

def most_successful_countrywise(df, country):
    # Filter out rows where 'Medal' is NaN and for the specified country
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    # Get the top 10 players with the most medals
    top_players = temp_df['Name'].value_counts().head(10).reset_index()
    top_players.columns = ['Name', 'Medals']
    
    # Merge with the original DataFrame to get additional details
    result = top_players.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates()
    
    return result

# Test the function
print(most_successful_countrywise(df, 'India'))


import plotly.figure_factory as ff

athlete_df=df.drop_duplicates(subset=['Name','region']) 
x1=athlete_df['Age'].dropna()
x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
fig=ff.create_distplot([x1,x2,x3,x4],['Overall age','Gold medalist','Silver medalist','Bronze Medalist'],show_hist=False,show_rug=False)
fig.show()

# List of famous sports
famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                 'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                 'Tennis', 'Golf', 'Softball', 'Archery',
                 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                 'Rhythmic Gymnastics', 'Rugby Sevens',
                 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

# Initialize lists for storing data
x = []
name = []

# Loop through each sport and filter the DataFrame
for sport in famous_sports:
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    name.append(sport)

# Create the distribution plot
fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
fig.update_layout(autosize=False, width=1000, height=600)
fig.show()


athlete_df['Medal'].fillna('No medal',inplace=True)
plt.figure(figsize=(10,10))
temp_df=athlete_df[athlete_df['Sport']=='Weightlifting']
sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)

men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
final=men.merge(women,on='year')
final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
final.fillna(0,inplace=True)
fig=px.line(final,x="Year",y=["Male","Female"])
fig.show()
