import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def plot_forex(specific_country):
    sp1 = specific_country.dropna()
# Convert daily data to monthly
    df_monthly = sp1.resample('M').last()

# Create a line plot for all currencies
    plt.figure(figsize=(12, 8))
    plt.plot(df_monthly)
    plt.title('Monthly Exchange Rates')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate')
    plt.grid(True)
    plt.show()

def analyze_currency_volatility_zar(df, window=30):
    """
    Analyze currency volatility and create visualizations
    
    Parameters:
    df: DataFrame with currency data
    window: Rolling window size for volatility calculation (default: 30 days)
    """
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate daily returns
    df['daily_return'] = df['South African rand (ZAR)                     '].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    # Calculate monthly average exchange rate
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_rates = df.groupby('YearMonth')['South African rand (ZAR)                     '].mean().reset_index()
    monthly_rates['YearMonth'] = monthly_rates['YearMonth'].astype(str)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('South African Rand (SAR)', fontsize=16)
    
    # Plot 1: Exchange Rate and Volatility
    ax1.plot(df['Date'], df['South African rand (ZAR)                     '], label='Exchange Rate', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Exchange Rate', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['Date'], df['volatility'], label='Volatility', color='red', alpha=0.7)
    ax1_twin.set_ylabel('30-Day Volatility', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Plot 2: Monthly Exchange Rate Changes
    monthly_changes = monthly_rates['South African rand (ZAR)                     '].pct_change() * 100
    ax2.bar(range(len(monthly_changes)), monthly_changes, color='green', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Monthly Change (%)')
    ax2.set_title('Monthly Exchange Rate Changes')
    
    # Set x-axis labels (every 3 months)
    x_ticks = range(0, len(monthly_changes), 3)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(monthly_rates['YearMonth'].iloc[x_ticks], rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return df[['Date', 'South African rand (ZAR)                     ', 'volatility']], monthly_rates

def analyze_currency_volatility_rub(df, window=30):
    """
    Analyze currency volatility and create visualizations
    
    Parameters:
    df: DataFrame with currency data
    window: Rolling window size for volatility calculation (default: 30 days)
    """
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle NaN values in RUB column
    # Forward fill, then backward fill to handle any remaining NaNs at the start
    df['Russian ruble (RUB)                     '] = df['Russian ruble (RUB)                     '].fillna(method='ffill').fillna(method='bfill')
    
    # Calculate daily returns
    df['daily_return'] = df['Russian ruble (RUB)                     '].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    # Calculate monthly average exchange rate
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_rates = df.groupby('YearMonth')['Russian ruble (RUB)                     '].mean().reset_index()
    monthly_rates['YearMonth'] = monthly_rates['YearMonth'].astype(str)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Russian Ruble (RUB) Analysis', fontsize=16)
    
    # Plot 1: Exchange Rate and Volatility
    ax1.plot(df['Date'], df['Russian ruble (RUB)                     '], label='Exchange Rate', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Exchange Rate (RUB/USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['Date'], df['volatility'], label='Volatility', color='red', alpha=0.7)
    ax1_twin.set_ylabel('30-Day Volatility', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Plot 2: Monthly Exchange Rate Changes
    monthly_changes = monthly_rates['Russian ruble (RUB)                     '].pct_change() * 100
    bars = ax2.bar(range(len(monthly_changes)), monthly_changes, color='green', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Monthly Change (%)')
    ax2.set_title('Monthly Exchange Rate Changes')
    
    # Add horizontal line at y=0 for reference
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.2)
    
    # Color bars based on positive/negative values
    for i, bar in enumerate(bars):
        if monthly_changes.iloc[i] < 0:
            bar.set_color('red')
        else:
            bar.set_color('green')
    
    # Set x-axis labels (every 3 months)
    x_ticks = range(0, len(monthly_changes), 3)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(monthly_rates['YearMonth'].iloc[x_ticks], rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Return processed data for further analysis if needed
    return df[['Date', 'Russian ruble (RUB)                     ', 'volatility']], monthly_rates

def print_summary_stats_rub(daily_data, monthly_data):
    print("\nRussian Ruble (RUB) Summary Statistics:")
    print(f"Average Exchange Rate: {daily_data['Russian ruble (RUB)                     '].mean():.4f}")
    print(f"Maximum Exchange Rate: {daily_data['Russian ruble (RUB)                     '].max():.4f}")
    print(f"Minimum Exchange Rate: {daily_data['Russian ruble (RUB)                     '].min():.4f}")
    print(f"Average Volatility: {daily_data['volatility'].mean():.4%}")
    print(f"Maximum Monthly Change: {monthly_data['Russian ruble (RUB)                     '].pct_change().max():.2%}")
    print(f"Minimum Monthly Change: {monthly_data['Russian ruble (RUB)                     '].pct_change().min():.2%}")

def print_summary_stats_zar(daily_data, monthly_data):
    print("\nRussian Ruble (RUB) Summary Statistics:")
    print(f"Average Exchange Rate: {daily_data['South African rand (ZAR)                     '].mean():.4f}")
    print(f"Maximum Exchange Rate: {daily_data['South African rand (ZAR)                     '].max():.4f}")
    print(f"Minimum Exchange Rate: {daily_data['South African rand (ZAR)                     '].min():.4f}")
    print(f"Average Volatility: {daily_data['volatility'].mean():.4%}")
    print(f"Maximum Monthly Change: {monthly_data['South African rand (ZAR)                     '].pct_change().max():.2%}")
    print(f"Minimum Monthly Change: {monthly_data['South African rand (ZAR)                     '].pct_change().min():.2%}")

def analyze_currency_volatility_ind(df, window=30):
    """
    Analyze currency volatility and create visualizations
    
    Parameters:
    df: DataFrame with currency data
    window: Rolling window size for volatility calculation (default: 30 days)
    """
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle NaN values in INR column
    # Forward fill, then backward fill to handle any remaining NaNs at the start
    df['Indian rupee (INR)                     '] = df['Indian rupee (INR)                     '].fillna(method='ffill').fillna(method='bfill')
    
    # Calculate daily returns
    df['daily_return'] = df['Indian rupee (INR)                     '].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    # Calculate monthly average exchange rate
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_rates = df.groupby('YearMonth')['Indian rupee (INR)                     '].mean().reset_index()
    monthly_rates['YearMonth'] = monthly_rates['YearMonth'].astype(str)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Indian Rupee (INR) Analysis', fontsize=16)
    
    # Plot 1: Exchange Rate and Volatility
    ax1.plot(df['Date'], df['Indian rupee (INR)                     '], label='Exchange Rate', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Exchange Rate (INR/USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['Date'], df['volatility'], label='Volatility', color='red', alpha=0.7)
    ax1_twin.set_ylabel('30-Day Volatility', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Plot 2: Monthly Exchange Rate Changes
    monthly_changes = monthly_rates['Indian rupee (INR)                     '].pct_change() * 100
    bars = ax2.bar(range(len(monthly_changes)), monthly_changes, color='green', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Monthly Change (%)')
    ax2.set_title('Monthly Exchange Rate Changes')
    
    # Add horizontal line at y=0 for reference
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.2)
    
    # Color bars based on positive/negative values
    for i, bar in enumerate(bars):
        if monthly_changes.iloc[i] < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')
    
    # Set x-axis labels (every 3 months)
    x_ticks = range(0, len(monthly_changes), 3)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(monthly_rates['YearMonth'].iloc[x_ticks], rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Return processed data for further analysis if needed
    return df[['Date', 'Indian rupee (INR)                     ', 'volatility']], monthly_rates

def print_summary_stats_ind(daily_data, monthly_data):
    """
    Print summary statistics for Indian Rupee (INR)
    
    Parameters:
    daily_data: DataFrame with daily exchange rates and volatility
    monthly_data: DataFrame with monthly exchange rates
    """
    print("\nIndian Rupee (INR) Summary Statistics:")
    print(f"Average Exchange Rate: {daily_data['Indian rupee (INR)                     '].mean():.4f}")
    print(f"Maximum Exchange Rate: {daily_data['Indian rupee (INR)                     '].max():.4f}")
    print(f"Minimum Exchange Rate: {daily_data['Indian rupee (INR)                     '].min():.4f}")
    print(f"Average Volatility: {daily_data['volatility'].mean():.4%}")
    print(f"Maximum Monthly Change: {monthly_data['Indian rupee (INR)                     '].pct_change().max():.2%}")
    print(f"Minimum Monthly Change: {monthly_data['Indian rupee (INR)                     '].pct_change().min():.2%}")

def analyze_currency_volatility_brl(df, window=30):
    """
    Analyze currency volatility and create visualizations
    
    Parameters:
    df: DataFrame with currency data
    window: Rolling window size for volatility calculation (default: 30 days)
    """
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle NaN values in BRL column
    # Forward fill, then backward fill to handle any remaining NaNs at the start
    df['Brazilian real (BRL)    '] = df['Brazilian real (BRL)    '].fillna(method='ffill').fillna(method='bfill')
    
    # Calculate daily returns
    df['daily_return'] = df['Brazilian real (BRL)    '].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    # Calculate monthly average exchange rate
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_rates = df.groupby('YearMonth')['Brazilian real (BRL)    '].mean().reset_index()
    monthly_rates['YearMonth'] = monthly_rates['YearMonth'].astype(str)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Brazilian Real (BRL) Analysis', fontsize=16)
    
    # Plot 1: Exchange Rate and Volatility
    ax1.plot(df['Date'], df['Brazilian real (BRL)    '], label='Exchange Rate', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Exchange Rate (BRL/USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['Date'], df['volatility'], label='Volatility', color='red', alpha=0.7)
    ax1_twin.set_ylabel('30-Day Volatility', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Plot 2: Monthly Exchange Rate Changes
    monthly_changes = monthly_rates['Brazilian real (BRL)    '].pct_change() * 100
    bars = ax2.bar(range(len(monthly_changes)), monthly_changes, color='green', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Monthly Change (%)')
    ax2.set_title('Monthly Exchange Rate Changes')
    
    # Add horizontal line at y=0 for reference
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.2)
    
    # Color bars based on positive/negative values
    for i, bar in enumerate(bars):
        if monthly_changes.iloc[i] < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')
    
    # Set x-axis labels (every 3 months)
    x_ticks = range(0, len(monthly_changes), 3)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(monthly_rates['YearMonth'].iloc[x_ticks], rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Return processed data for further analysis if needed
    return df[['Date', 'Brazilian real (BRL)    ', 'volatility']], monthly_rates

def print_summary_stats_brl(daily_data, monthly_data):
    """
    Print summary statistics for Brazilian Real (BRL)
    
    Parameters:
    daily_data: DataFrame with daily exchange rates and volatility
    monthly_data: DataFrame with monthly exchange rates
    """
    print("\nBrazilian Real (BRL) Summary Statistics:")
    print(f"Average Exchange Rate: {daily_data['Brazilian real (BRL)    '].mean():.4f}")
    print(f"Maximum Exchange Rate: {daily_data['Brazilian real (BRL)    '].max():.4f}")
    print(f"Minimum Exchange Rate: {daily_data['Brazilian real (BRL)    '].min():.4f}")
    print(f"Average Volatility: {daily_data['volatility'].mean():.4%}")
    print(f"Maximum Monthly Change: {monthly_data['Brazilian real (BRL)    '].pct_change().max():.2%}")
    print(f"Minimum Monthly Change: {monthly_data['Brazilian real (BRL)    '].pct_change().min():.2%}")

def analyze_currency_volatility_cny(df, window=30):
    """
    Analyze currency volatility and create visualizations
    
    Parameters:
    df: DataFrame with currency data
    window: Rolling window size for volatility calculation (default: 30 days)
    """
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle NaN values in CNY column
    # Forward fill, then backward fill to handle any remaining NaNs at the start
    df['Chinese yuan (CNY)                     '] = df['Chinese yuan (CNY)                     '].fillna(method='ffill').fillna(method='bfill')
    
    # Calculate daily returns
    df['daily_return'] = df['Chinese yuan (CNY)                     '].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    # Calculate monthly average exchange rate
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_rates = df.groupby('YearMonth')['Chinese yuan (CNY)                     '].mean().reset_index()
    monthly_rates['YearMonth'] = monthly_rates['YearMonth'].astype(str)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Chinese Yuan (CNY) Analysis', fontsize=16)
    
    # Plot 1: Exchange Rate and Volatility
    ax1.plot(df['Date'], df['Chinese yuan (CNY)                     '], label='Exchange Rate', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Exchange Rate (CNY/USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['Date'], df['volatility'], label='Volatility', color='red', alpha=0.7)
    ax1_twin.set_ylabel('30-Day Volatility', color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Plot 2: Monthly Exchange Rate Changes
    monthly_changes = monthly_rates['Chinese yuan (CNY)                     '].pct_change() * 100
    bars = ax2.bar(range(len(monthly_changes)), monthly_changes, color='green', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Monthly Change (%)')
    ax2.set_title('Monthly Exchange Rate Changes')
    
    # Add horizontal line at y=0 for reference
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.2)
    
    # Color bars based on positive/negative values
    for i, bar in enumerate(bars):
        if monthly_changes.iloc[i] < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')
    
    # Set x-axis labels (every 3 months)
    x_ticks = range(0, len(monthly_changes), 3)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(monthly_rates['YearMonth'].iloc[x_ticks], rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Return processed data for further analysis if needed
    return df[['Date', 'Chinese yuan (CNY)                     ', 'volatility']], monthly_rates

def print_summary_stats_cny(daily_data, monthly_data):
    """
    Print summary statistics for Chinese Yuan (CNY)
    
    Parameters:
    daily_data: DataFrame with daily exchange rates and volatility
    monthly_data: DataFrame with monthly exchange rates
    """
    print("\nChinese Yuan (CNY) Summary Statistics:")
    print(f"Average Exchange Rate: {daily_data['Chinese yuan (CNY)                     '].mean():.4f}")
    print(f"Maximum Exchange Rate: {daily_data['Chinese yuan (CNY)                     '].max():.4f}")
    print(f"Minimum Exchange Rate: {daily_data['Chinese yuan (CNY)                     '].min():.4f}")
    print(f"Average Volatility: {daily_data['volatility'].mean():.4%}")
    print(f"Maximum Monthly Change: {monthly_data['Chinese yuan (CNY)                     '].pct_change().max():.2%}")
    print(f"Minimum Monthly Change: {monthly_data['Chinese yuan (CNY)                     '].pct_change().min():.2%}")
