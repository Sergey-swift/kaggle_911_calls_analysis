# Author: Sergey Swift
# Project: Kaggle 911 Calls Analysis
# Date: November 2024

#%% Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

#%% Function Definitions

def load_data(filepath):
    """Loads data from a CSV file and returns a DataFrame."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """
    Performs initial preprocessing on the DataFrame.
    Includes feature engineering for 'Reason', 'Hour', 'Month', 'Day of Week', and 'Date'.
    """
    # Convert 'timeStamp' column to datetime
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    
    # Extract useful time-based features
    df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
    df['Month'] = df['timeStamp'].apply(lambda time: time.month)
    df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)
    
    # Map day of the week integers to string names
    dmap = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    df['Day of Week'] = df['Day of Week'].map(dmap)
    
    # Extract the 'Reason' for the call from the 'title' column
    df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
    
    # Extract the 'Date' from the timestamp
    df['Date'] = df['timeStamp'].apply(lambda t: t.date())
    return df

def basic_statistics(df):
    """Displays basic statistics and information about the DataFrame."""
    print("DataFrame Information:")
    df.info()
    print("\nTop 5 Zip Codes for 911 Calls:")
    print(df['zip'].value_counts().head(5))
    print("\nTop 5 Townships for 911 Calls:")
    print(df['twp'].value_counts().head(5))
    print(f"\nNumber of Unique Title Codes: {df['title'].nunique()}")

def visualize_reasons(df):
    """Creates a countplot for the reasons for 911 calls."""
    sns.countplot(x='Reason', data=df, palette="plasma")
    plt.title('911 Calls by Reason')
    plt.show()

def visualize_day_hour(df):
    """Creates a heatmap and clustermap for calls by day and hour."""
    day_hour = df.groupby(by=['Day of Week', 'Hour']).count()['Reason'].unstack()
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(day_hour, cmap='magma')
    plt.title('Heatmap of Calls by Day and Hour')
    plt.show()
    
    sns.clustermap(day_hour, cmap='inferno')
    plt.title('Clustermap of Calls by Day and Hour')
    plt.show()

def visualize_day_month(df):
    """Creates a heatmap and clustermap for calls by day and month."""
    day_month = df.groupby(by=['Day of Week', 'Month']).count()['Reason'].unstack()
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(day_month, cmap='viridis')
    plt.title('Heatmap of Calls by Day and Month')
    plt.show()
    
    sns.clustermap(day_month, cmap='cividis')
    plt.title('Clustermap of Calls by Day and Month')
    plt.show()

def visualize_calls_over_time(df):
    """Visualizes 911 calls over time, including by specific reasons."""
    # Aggregate calls by date
    df.groupby('Date').count()['twp'].plot()
    plt.title('911 Calls Over Time')
    plt.tight_layout()
    plt.show()
    
    # Plot calls over time for specific reasons
    for reason in df['Reason'].unique():
        df[df['Reason'] == reason].groupby('Date').count()['twp'].plot(label=reason)
    plt.title('911 Calls Over Time by Reason')
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualize_month_trends(df):
    """Visualizes monthly trends in the number of 911 calls."""
    by_month = df.groupby('Month').count()
    
    # Simple line plot
    by_month['twp'].plot()
    plt.title('Monthly Trend of 911 Calls')
    plt.tight_layout()
    plt.show()
    
    # Linear regression model
    sns.lmplot(x='Month', y='twp', data=by_month.reset_index())
    plt.title('Linear Fit for Monthly 911 Calls')
    plt.show()

#%% Main Execution Block

def main():
    # Define the file path
    filepath = input("Enter the path to the 911 CSV file: ").strip()
    
    # Load data
    df = load_data(filepath)
    if df is None:
        return
    
    # Preprocess data
    df = preprocess_data(df)
    
    # Display basic statistics
    basic_statistics(df)
    
    # Visualization
    visualize_reasons(df)
    visualize_day_hour(df)
    visualize_day_month(df)
    visualize_calls_over_time(df)
    visualize_month_trends(df)

# Run the main function
if __name__ == "__main__":
    main()
