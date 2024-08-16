import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        x = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x[['Gold', 'Silver', 'Bronze', 'Total']] = x[['Gold', 'Silver', 'Bronze', 'Total']].astype(int)
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['NOC'] = medal_tally['NOC'].apply(lambda x: f'{x:<10}')
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']] = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']].astype(int)
    return medal_tally 

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Editions', f'No of {col.capitalize()}']  # Rename columns for clarity
    nations_over_time = nations_over_time.sort_values('Editions')
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the number of medals per athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with the original DataFrame to get additional details
    x = medal_counts.head(15).merge(df[['Name', 'Sport', 'region']].drop_duplicates(), on='Name', how='left')

    return x[['Name', 'Medals', 'Sport', 'region']].drop_duplicates()


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])  
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])  
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    top_players = temp_df['Name'].value_counts().head(10).reset_index()
    top_players.columns = ['Name', 'Medals']
    
    result = top_players.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates()
    
    return result

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No medal', inplace=True)
    if sport == 'Overall':
        return athlete_df
    else:
        return athlete_df[athlete_df['Sport'] == sport]
    
def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    
    # Merge on 'Year' and rename columns
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    
    # Melt the DataFrame for Plotly
    final_melted = final.melt(id_vars='Year', value_vars=['Male', 'Female'], var_name='Sex', value_name='Count')
    
    return final_melted








