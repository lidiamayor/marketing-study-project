import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def clean_click(df):
    """
    This function takes a pandas DataFrame (`df`) and cleans/preprocesses it.
    It removes the columns: 'Unnamed: 0', 'Location', 'Device', 'Time_Spent_on_Site', 'Number_of_Pages_Viewed',
    and creates two new columns: 'Income_Range' and 'Age_Range', that are categorical bins of the 'Income' and 'Age' columns, respectively.
    """

    # drop columns that are not useful for the analysis
    df = df.drop(columns=['Unnamed: 0', 'Location', 'Device', 'Time_Spent_on_Site', 'Number_of_Pages_Viewed'])
    
    # create categorical bins for the Income column
    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, include_lowest=True)
    
    # create categorical bins for the Age column
    bins = [16, 24, 34, 44, 54, 90]
    labels = ['16-24', '25-34', '35-44', '45-54', '55+']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)
    
    return df

def click_by_category(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the percentage of clicks
    in each interest category.
    """

    # pivot the DataFrame to get the total counts for each category and click status
    df_pivot = df.pivot_table(index='Interest_Category', columns='Click', aggfunc='size', fill_value=0)
    
    # calculate the percentage of clicks for each category
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100
    
    # plot the bar chart
    ax = df_pivot_percentage.plot(kind='bar', figsize=(8, 6), color=['#d9e6f2', '#4a90e2'])
    
    # set the y-axis limits
    ax.set_ylim(46, 53)
    
    # set the x-axis label
    plt.xlabel('Category')
    
    # set the y-axis label
    plt.ylabel('Percentage (%)')
    
    # set the x-tick rotation
    plt.xticks(rotation=0)
    
    # add a legend
    plt.legend(title='Click', labels=['No Click', 'Click'])
    
    # adjust the layout
    plt.tight_layout()
    
    # show the plot
    plt.show()

def click_by_category_income(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the percentage of clicks
    in each interest category for each income range.
    """

    # group the DataFrame by income range, interest category, and click status
    df_grouped = df.groupby(['Income_Range', 'Interest_Category', 'Click'], observed=False).size().unstack(fill_value=0)
    
    # calculate the total counts for each income range and interest category
    df_grouped['Total'] = df_grouped[0] + df_grouped[1]
    
    # calculate the percentage of clicks for each income range and interest category
    df_grouped['Percentage_Click'] = df_grouped[1] / df_grouped['Total'] * 100
    
    # pivot the DataFrame to create a new DataFrame with the percentage of clicks
    df_pivot = df_grouped.reset_index().pivot(index='Income_Range', columns='Interest_Category', values='Percentage_Click')

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bar chart
    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    
    # set the y-axis limits
    ax.set_ylim(39, 61)
    
    # set the x-axis label
    plt.xlabel('Income range')
    
    # set the y-axis label
    plt.ylabel('Click (%)')
    
    # add a legend
    plt.legend(title='Category')
    
    # rotate the x-axis tick labels
    plt.xticks(rotation=40)
    
    # adjust the layout
    plt.tight_layout()
    
    # show the plot
    plt.show()

def click_by_category_age(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the percentage of clicks
    in each interest category for each age range.
    """

    # group the DataFrame by age range and interest category, and calculate the total clicks and total counts
    df_grouped = df.groupby(['Age_Range', 'Interest_Category'], observed=False).agg({'Click': ['sum', 'count']})

    # rename the columns
    df_grouped.columns = ['Total_Clicks', 'Total_Count']
    
    # calculate the percentage of clicks for each age range and interest category
    df_grouped['Percentage_Click'] = df_grouped['Total_Clicks'] / df_grouped['Total_Count'] * 100

    # pivot the DataFrame to create a new DataFrame with the percentage of clicks
    df_pivot = df_grouped.reset_index()
    df_pivot =df_pivot.pivot(index='Age_Range', columns='Interest_Category', values='Percentage_Click')

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bar chart
    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    
    # set the y-axis limits
    ax.set_ylim([40, 60])
    
    # set the x-axis label
    plt.xlabel('Age range')
    
    # set the y-axis label
    plt.ylabel('Click (%)')
    
    # add a legend
    plt.legend(title='Category', loc=('upper left'), bbox_to_anchor=(-0.02, 1))
    
    # rotate the x-axis tick labels
    plt.xticks(rotation=45)
    
    # adjust the layout
    plt.tight_layout()
    
    # show the plot
    plt.show()
