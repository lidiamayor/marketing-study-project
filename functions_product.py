import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def clean_df_product(df):
    """
    Clean the dataframe to get the data of both, men and women
    between 16 and 75 years old.
    """

    # Select the columns of interest
    df = df.iloc[:,:7].copy()

    # Rename the columns
    name_columns =  ['years','total','4+', '1-3', '-1','<<1','0']
    df.columns = name_columns
    
    # Replace the values of the years column
    df['years'] = df['years'].replace({
        '        Total':'Total',
        '        De 16 a 24 años': '16-24',
        '        De 25 a 34 años': '25-34',
        '        De 35 a 44 años': '35-44',
        '        De 45 a 54 años': '45-54',
        '        De 55 a 64 años': '55-64',
        '        De 65 a 74 años': '65-74',
        '        De 75 y más años': '75+'
    })

    # Get the data of both, men and women
    df_both = df.loc[37:44].copy()
    df_both.index = range(1, len(df_both)+1)
    df_both['total_cons'] = df_both['4+']+df_both['1-3']+df_both['-1']+df_both['<<1']
    df_both = df_both.drop(columns=['total','4+', '1-3', '-1','<<1'])

    # Get the data of men
    df_men = df.loc[46:53].copy()
    df_men.index = range(1, len(df_men)+1)
    df_men['total_cons'] = df_men['4+']+df_men['1-3']+df_men['-1']+df_men['<<1']
    df_men = df_men.drop(columns=['total', '4+', '1-3', '-1','<<1'])

    # Get the data of women
    df_women = df.loc[55:62].copy()
    df_women.index = range(1, len(df_women)+1)
    df_women['total_cons'] = df_women['4+']+df_women['1-3']+df_women['-1']+df_women['<<1']
    df_women = df_women.drop(columns=['total', '4+', '1-3', '-1','<<1'])

    return df_both, df_men, df_women

def consume_wine(df_both):
    """
    This function takes a pandas DataFrame (`df_both`) containing data about the consumption of wine 
    and creates a pie plot showing the percentage of consumers and not consumers between 16 and 75 years old.
    """

    # Get the values to plot

    labels = ['Consumers', 'Not consumers']
    values = [df_both['total_cons'].iloc[0], df_both['0'].iloc[0]]

    # Set the colors for the pie chart
    colors = ['#A3E4D7', '#FAD7A0']

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the pie chart
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Set the axis equal to ensure that the pie chart is drawn as a circle
    ax.axis('equal')

    # Set the title of the plot
    plt.title('Percentage >16 years consumers/not consumers')

    # Show the plot
    plt.show()

def consume_m_w_by_age(df_men, df_women):
    """
    This function takes two pandas DataFrames (`df_men` and `df_women`) containing data about the consumption of wine
    by men and women, respectively, and creates a line plot showing the percentage of consumers in each age range.
    """

    # Filter out the total values
    df_men_filtered = df_men[df_men['years'] != 'Total']
    df_women_filtered = df_women[df_women['years'] != 'Total']

    # Create the figure and axis
    plt.figure(figsize=(10, 6))

    # Plot the lines
    plt.plot(df_men_filtered['years'], df_men_filtered['total_cons'], marker='o', label='Men', color='#a3c2c2') 
    plt.plot(df_women_filtered['years'], df_women_filtered['total_cons'], marker='o', label='Women', color='#f2b5d4') 

    # Set the axis labels
    plt.xlabel('Age range')
    plt.ylabel('Consumers (%)')

    # Add a legend
    plt.legend()

    # Add a grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Add the text labels
    for i in range(len(df_men_filtered)):
        plt.text(i, df_men_filtered['total_cons'].iloc[i] + 1, f'{df_men_filtered["total_cons"].iloc[i]:.2f}%', ha='center', va='bottom', color='#a3c2c2')
        plt.text(i, df_women_filtered['total_cons'].iloc[i] + 1, f'{df_women_filtered["total_cons"].iloc[i]:.2f}%', ha='center', va='bottom', color='#f2b5d4')

    # Adjust the layout
    plt.tight_layout()

    # Show the plot
    plt.show()

def consume_men_women(df_men, df_women):
    """
    This function takes two pandas DataFrames (`df_men` and `df_women`) containing data about the consumption of wine
    by men and women, respectively, and creates a bar plot showing the total percentage of consumers.
    """

    # Filter out the total values
    total_men = df_men[df_men['years'] == 'Total']
    total_women = df_women[df_women['years'] == 'Total']

    # Create the figure and axis
    plt.figure(figsize=(8, 6))

    # Plot the bars
    plt.bar('Men', total_men['total_cons'].values[0], color='#a3c2c2') 
    plt.bar('Women', total_women['total_cons'].values[0], color='#f2b5d4') 

    # Set the axis labels
    plt.ylabel('Consumers (%)')

    # Adjust the layout
    plt.tight_layout()

    # Add the text labels
    for index, value in enumerate([total_men['total_cons'].values[0], total_women['total_cons'].values[0]]):
        plt.text(index, value + 1, f'{value:.2f}%', ha='center', va='bottom', fontsize=12, color='black')

    # Show the plot
    plt.show()

def consume_by_age(df_both):
    """
    This function takes a pandas DataFrame (`df_both`) containing data about the consumption of wine 
    by population >16 years old and creates a bar plot showing the percentage of consumers in each age range.
    """
    
    # Create the figure and axis
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='years', y='total_cons', data=df_both.loc[2:8], palette='viridis',hue='total_cons', legend=False)
    
    # Set the title, labels and x-tick rotation

    plt.title('Percentage of population >16 that consumes wine')
    plt.xlabel('Age range')
    plt.ylabel('Total consumption (%)')
    plt.xticks(rotation=30) 
    
    # Add the text labels on the bars
    for p in ax.patches:
        # Get the height of the bar
        height = p.get_height()
        # Round the height to 2 decimal places
        rounded_height = round(height, 2)
        # Annotate the bar with the rounded value
        ax.annotate(f'{rounded_height}', 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='center', 
                    xytext=(0, 5),
                    textcoords='offset points')

    # Adjust the layout
    plt.tight_layout()
    # Show the plot
    plt.show()
