import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import seaborn as sns

karachi_prefix = "../data/karachi/Karachi_PM2.5_"
new_delhi_prefix = "../data/new_delhi/NewDelhi_PM2.5_"
karachi_suffix = "_YTD.csv"
new_delhi_suffix = "_YTD.csv"

aqi_levels = {
    "Good (0-50)": (50, 'green'),
    "Moderate (51-100)": (100, 'yellow'),
    "Unhealthy for Sensitive Groups (101-150)": (150, 'orange'),
    "Unhealthy (151-200)": (200, 'red'),
    "Very Unhealthy (201-300)": (300, 'purple'),
    "Hazardous (301+)": (301, 'maroon')
}

def create_new_delhi_filepath(year):
    new_delhi_filepath = f"{new_delhi_prefix}{year}{new_delhi_suffix}"
    return new_delhi_filepath

def build_delhi_df(years):
    
    delhi_df = pd.read_csv(create_new_delhi_filepath(years[0]))
    years.pop(0)
    
    for year in years:
        delhi_df = pd.concat([delhi_df, pd.read_csv(create_new_delhi_filepath(year))],ignore_index=True)
    
    delhi_df = delhi_df.drop(["Parameter"], axis=1)
    delhi_df = delhi_df.replace(to_replace="Invalid", value=np.nan)
    delhi_df = delhi_df.dropna()
    
    return delhi_df

def create_chennai_filepath(year):
    new_delhi_filepath = f"{new_delhi_prefix}{year}{new_delhi_suffix}"
    return new_delhi_filepath

def build_chennai_df(years):
    
    chennai_df = pd.read_csv(create_chennai_filepath(years[0]))
    years.pop(0)
    
    for year in years:
        chennai_df = pd.concat([chennai_df, pd.read_csv(create_chennai_filepath(year))], ignore_index=True)
    
    chennai_df = chennai_df.drop(["Parameter"], axis=1)
    chennai_df = chennai_df.replace(to_replace="Invalid", value=np.nan)
    chennai_df = chennai_df.dropna()
    
    return chennai_df 

def build_AQI_time_graph(df, title):
    key_points = ["2015-01-01 01:00 AM", "2016-01-01 01:00 AM", "2017-01-01 01:00 AM", "2018-01-01 01:00 AM", "2019-01-01 01:00 AM", "2020-01-01 01:00 AM", "2021-01-01 01:00 AM", "2022-01-01 01:00 AM", "2023-01-01 01:00 AM", "2024-01-01 01:00 AM", "2025-01-01 01:00 AM", ]
    labels = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    df_AQI = df["AQI"].to_numpy()
    df_datetime = df["Date (LT)"].to_numpy()
    plot = plt.figure(figsize=(18,6))
    plt.plot(df_datetime, df_AQI)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(key_points, labels)
    for label, (value, color) in aqi_levels.items():
        plt.axhline(y=value, color=color, linestyle='--', linewidth=1.5, alpha=0.8, label=label)
    plt.legend(title='AQI Levels')
    return plot

def build_DiD_graph(delhi_df, chennai_df, policy_date='2018-01-01', rolling_window=30):
    # Convert to datetime and sort
    delhi_df['datetime'] = pd.to_datetime(delhi_df['Date (LT)'])
    chennai_df['datetime'] = pd.to_datetime(chennai_df['Date (LT)'])

    delhi_df = delhi_df.sort_values('datetime').set_index('datetime')
    chennai_df = chennai_df.sort_values('datetime').set_index('datetime')

    # Step 2: Rolling mean smoothing
    delhi_df['AQI_smooth'] = delhi_df['AQI'].rolling(window=rolling_window, min_periods=1).mean()
    chennai_df['AQI_smooth'] = chennai_df['AQI'].rolling(window=rolling_window, min_periods=1).mean()

    # Step 3: Combine datasets
    combined = pd.DataFrame({
        'Delhi': delhi_df['AQI_smooth'],
        'Chennai': chennai_df['AQI_smooth']
    }).dropna()

    # Step 4: Split around policy date
    policy_date = pd.to_datetime(policy_date)
    pre_policy = combined[combined.index < policy_date]
    post_policy = combined[combined.index >= policy_date]


    # Step 5: Estimate Delhi counterfactual post-policy
    # Calculate average change in Chennai (control)
    chennai_change = post_policy['Chennai'].mean() - pre_policy['Chennai'].mean()

    # Estimate counterfactual: Delhi pre-policy + Chennai change
    delhi_counterfactual_mean = pre_policy['Delhi'].mean() + chennai_change
    counterfactual = pd.Series(delhi_counterfactual_mean, index=post_policy.index)

    # Step 6: Plot
    plt.figure(figsize=(14, 6))

    # Actual data
    plt.plot(combined.index, combined['Delhi'], label='New Delhi (Actual)', color='red')
    plt.plot(combined.index, combined['Chennai'], label='Chennai (Control)', color='blue')

    # Counterfactual
    plt.plot(counterfactual.index, counterfactual, label='New Delhi (Counterfactual)', linestyle='dotted', color='gray')

    # Highlight DiD gap
    plt.fill_between(post_policy.index,
                     post_policy['Delhi'],
                     counterfactual,
                     where=(post_policy['Delhi'] > counterfactual),
                     interpolate=True,
                     color='orange',
                     alpha=0.3,
                     label='DiD Effect')

    # Policy marker
    plt.axvline(policy_date, color='black', linestyle='--', label='Policy (2018)')
    plt.text(policy_date, combined['Delhi'].max(), 'Policy Introduced', rotation=90, va='top', ha='right')

    plt.title('Difference-in-Differences: Daily AQI (Smoothed)')
    plt.xlabel('Date')
    plt.ylabel(f'AQI ({rolling_window}-day Rolling Avg)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
   
    
    