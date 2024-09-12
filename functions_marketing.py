import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def clean_df_marketing(df):
    """
    This function, `clean_df_marketing`, cleans and preprocesses a marketing dataset stored in a pandas 
    DataFrame (`df`). It performs the following operations:
    1. **Column cleaning**
    2. **Education level mapping**
    3. **Living status mapping**
    4. **Age calculation**
    5. **Parent status**
    6. **Age and income range binning**
    7. **Column removal**
    The function returns the cleaned and preprocessed DataFrame.
    """

    # strip whitespace from column names
    df.columns = df.columns.str.strip()
    # drop duplicate rows
    df = df.drop_duplicates()

    # map specific education levels to broader categories
    education_levels = {'PhD': 'High', 'Master':'High', 
                        '2n Cycle': 'Middle', 'Graduation': 'Middle', 
                        'Basic': 'Low'
    }
    df["Education_Level"] = df['Education'].replace(education_levels) 

    # map specific living statuses to broader categories
    living_status = {'Alone': 'Living Alone', 'Absurd': 'Living Alone', 'YOLO': 'Living Alone', 'Widow': 'Living Alone', 'Single': 'Living Alone', 'Divorced': 'Living Alone',
                        'Together': 'Living with Others', 'Married': 'Living with Others'
    } 
    df['Living_Status'] = df['Marital_Status'].replace(living_status)

    # calculate age of customers based on birth year and customer date
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
    df["Age"] = df['Dt_Customer'].dt.year - df["Year_Birth"]

    # create a new column indicating whether a customer has children at home
    df['Is_Parent'] = (df['Kidhome'] + df['Teenhome'] > 0).astype(int)
    
    # drop customers with age > 100
    df = df[df['Age']<100]

    # bin age values into categorical ranges
    bins = [16, 24, 34, 44, 54, 64, 74] 
    labels = ['16-24', '25-34', '35-44', '45-54', '55-64', '65-74']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # bin income values into categorical ranges
    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, right=False)

    # drop unnecessary columns
    to_drop = ['Z_CostContact', 'Year_Birth', 'ID', 'Marital_Status', 'Education','Kidhome', 'Teenhome', 'Recency', 'MntFruits','MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts','MntGoldProds', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 
            'Complain', 'Z_CostContact', 'Z_Revenue', 'Response']
    df = df.drop(to_drop, axis=1)

    return df

def site_purchases_by_age(df_wine):
    """
    This function takes a pandas DataFrame (`df_wine`) and creates a bar plot showing the average number of purchases 
    in each age range for each purchase type (Deals, Web, Catalog, Store).
    """
    # group the DataFrame by age range and calculate the mean of each type of purchase
    age_grouped = df_wine.groupby('Age_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    # set the bar width
    bar_width = 0.15

    # create the x-values for the bars
    age_range = np.arange(len(age_grouped))

    # calculate the x-position of each bar
    r1 = age_range
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    plt.bar(r1, age_grouped['NumDealsPurchases'], color='#a3c2c2', width=bar_width, edgecolor='grey', label='Deals Purchases')
    plt.bar(r2, age_grouped['NumWebPurchases'], color='#f2b5d4', width=bar_width, edgecolor='grey', label='Web Purchases')
    plt.bar(r3, age_grouped['NumCatalogPurchases'], color='#c5a3ff', width=bar_width, edgecolor='grey', label='Catalog Purchases')
    plt.bar(r4, age_grouped['NumStorePurchases'], color='#f6cfb7', width=bar_width, edgecolor='grey', label='Store Purchases')

    # set the x-axis label
    plt.xlabel('Age range')

    # set the x-tick labels
    plt.xticks([r + bar_width*2 for r in range(len(age_grouped))], age_grouped['Age_Range'], rotation=45)

    # set the y-axis label
    plt.ylabel('Average purchases')

    # add a legend
    plt.legend(loc='upper left',bbox_to_anchor=(-0.1, 1))

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def site_purchases_by_income(df_wine):
    """
    This function takes a pandas DataFrame (`df_wine`) and creates a bar plot showing the average number of purchases 
    in each income range for each purchase type (Deals, Web, Catalog, Store).
    """
    income_grouped = df_wine.groupby('Income_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    # set the bar width
    bar_width = 0.15

    # create the x-values for the bars
    income_range = np.arange(len(income_grouped))

    # calculate the x-position of each bar
    r1 = income_range
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    plt.bar(r1, income_grouped['NumDealsPurchases'], color='#a3c2c2', width=bar_width, edgecolor='grey', label='Deals Purchases')
    plt.bar(r2, income_grouped['NumWebPurchases'], color='#f2b5d4', width=bar_width, edgecolor='grey', label='Web Purchases')
    plt.bar(r3, income_grouped['NumCatalogPurchases'], color='#c5a3ff', width=bar_width, edgecolor='grey', label='Catalog Purchases')
    plt.bar(r4, income_grouped['NumStorePurchases'], color='#f6cfb7', width=bar_width, edgecolor='grey', label='Store Purchases')

    # set the x-axis label
    plt.xlabel('Range income')

    # set the x-tick labels
    plt.xticks([r + bar_width*2 for r in range(len(income_grouped))], income_grouped['Income_Range'], rotation=45)

    # set the y-axis label
    plt.ylabel('Average purchases')

    # add a legend
    plt.legend()

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()


def web_visits_by_age(df_wine):
    """
    This function takes a pandas DataFrame (`df_wine`) and creates a bar plot showing the average number of visits 
    in each age range in the website.
    """
    # group the DataFrame by age range and calculate the mean of average visits
    avg_visits = df_wine.groupby('Age_Range', observed=False)['NumWebVisitsMonth'].mean().reset_index()

    # sort the DataFrame by age range
    avg_visits = avg_visits.sort_values(by='Age_Range')

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    sns.barplot(x='Age_Range', y='NumWebVisitsMonth', data=avg_visits, palette='pastel', hue='Age_Range', legend=False)

    # set the x-axis label
    plt.xlabel('Age range')

    # set the y-axis label
    plt.ylabel('Average visits in the website')

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def income_by_ages(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the average income 
    in each age range.
    """
    mean_income_by_age_range = df.groupby('Age_Range', observed=False)['Income'].mean()

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    mean_income_by_age_range.plot(kind='bar', color='#6a9ac4')

    # set the x-axis label
    plt.xlabel('Age range')

    # set the y-axis label
    plt.ylabel('Average income')

    # rotate the x-axis tick labels
    plt.xticks(rotation=40)

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def purchases_by_income(df_income):
    """
    This function takes a pandas DataFrame (`df_income`) and creates a scatter plot showing the relationship between
    income and wine purchases.
    """
    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the scatter plot
    plt.scatter(df_income['Income'], df_income['MntWines'], color='#6a9ac4', alpha=0.7, edgecolor='k')

    # set the x-axis label
    plt.xlabel('Incomes')

    # set the y-axis label
    plt.ylabel('Wine purchases')

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def purchases_by_income_line(df_income):
    """
    This function takes a pandas DataFrame (`df_income`) and creates a scatter plot with a regression line showing the relationship between
    income and wine purchases.
    """
    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the scatter plot with a regression line
    sns.regplot(x='Income', y='MntWines', data=df_income, scatter_kws={'color': '#6a9ac4', 'alpha': 0.7, 'edgecolor': 'k'}, line_kws={'color': 'red', 'lw': 2})

    # set the x-axis label
    plt.xlabel('Incomes')

    # set the y-axis label
    plt.ylabel('Wine purchases')

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def purchases_by_education(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the average number of purchases 
    in each education level.
    """
    # group the DataFrame by education level and calculate the mean of purchases

    education_mean = df.groupby('Education_Level')['MntWines'].mean().reset_index()

    # sort the DataFrame by mean of purchases
    education_mean = education_mean.sort_values(by='MntWines')

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    sns.barplot(x='Education_Level', y='MntWines', data=education_mean, palette='pastel', hue='Education_Level')

    # set the x-axis label
    plt.xlabel('Education level')

    # set the y-axis label
    plt.ylabel('Average purchases wine')

    # set the x-axis tick labels
    plt.xticks(rotation=0)

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def son_at_home(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a pie plot showing the average number of purchases 
    in each parent status.
    """
    # group the DataFrame by parent status and calculate the mean of purchases

    parent_mean = df.groupby('Is_Parent')['MntWines'].mean().reset_index()

    # map 0 and 1 to human readable labels
    parent_mean['Is_Parent'] = parent_mean['Is_Parent'].map({0: 'Not son at home', 1: 'Son at home'})

    # create the figure and axis
    plt.figure(figsize=(7, 7))

    # plot the pie
    plt.pie(parent_mean['MntWines'], labels=parent_mean['Is_Parent'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=140)

    # set the title
    plt.title('Purchases wine', fontweight='bold')

    # show the plot
    plt.show()

def purchases_by_living_status(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the average number of purchases 
    in each living status.
    """
    # group the DataFrame by living status and calculate the mean of purchases

    spend_by_livingstatus = df.groupby('Living_Status')['MntWines'].mean().reset_index()

    # create the figure and axis
    plt.figure(figsize=(10, 6))

    # plot the bars
    ax = sns.barplot(x='Living_Status', y='MntWines', data=spend_by_livingstatus, palette='pastel', hue='Living_Status')

    # set the x-axis label
    plt.xlabel('Living status')

    # set the y-axis label
    plt.ylabel('Average purchases wine')

    # add the text on the bars
    for i, row in spend_by_livingstatus.iterrows():
        ax.text(i, row['MntWines'] + 0.5, f'{row["MntWines"]:.2f}', ha='center')

    # adjust the layout
    plt.tight_layout()

    # show the plot
    plt.show()

def purchases_by_month(df):
    """
    This function takes a pandas DataFrame (`df`) and creates a bar plot showing the total purchases wine
    in each month of the year.
    """

    # Add a new column 'Month' to the DataFrame
    # This column will contain the month of each customer's date
    df['Month'] = df['Dt_Customer'].dt.month

    # Group the DataFrame by 'Month' and calculate the sum of 'MntWines'
    monthly_sales = df.groupby('Month')['MntWines'].sum().reset_index()

    # Create the figure and axis
    plt.figure(figsize=(10, 6))

    # Plot the bars
    plt.bar(monthly_sales['Month'], monthly_sales['MntWines'], color='#4a90e2')

    # Set the x-axis label
    plt.xlabel('Month')

    # Set the y-axis label
    plt.ylabel('Total purchases wine')

    # Set the x-tick labels
    plt.xticks(ticks=range(1, 13), labels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])

    # Adjust the layout
    plt.tight_layout()

    # Show the plot
    plt.show()
