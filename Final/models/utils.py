import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import seaborn as sns

karachi_prefix = "../data/karachi/Karachi_PM2.5_"
new_delhi_prefix = "../data/new_delhi/NewDelhi_PM2.5_"
chennai_prefix = "../data/chennai/Chennai_PM2.5_"
karachi_suffix = "_YTD.csv"
new_delhi_suffix = "_YTD.csv"
chennai_suffix = "_YTD.csv"


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
    chennai_filepath = f"{chennai_prefix}{year}{chennai_suffix}"
    return chennai_filepath

def build_chennai_df(years):
    
    control_df = pd.read_csv(create_chennai_filepath(years[0]))
    years.pop(0)
    
    for year in years:
        control_df = pd.concat([control_df, pd.read_csv(create_chennai_filepath(year))], ignore_index=True)
    
    control_df = control_df.drop(["Parameter"], axis=1)
    control_df = control_df.replace(to_replace="Invalid", value=np.nan)
    control_df = control_df.dropna()
    
    return control_df

def build_monthly_df(df):
    df["timestamp"] = pd.to_datetime(df['Date (LT)'])
    df.set_index('timestamp', inplace=True)
    
    monthly_df = df['AQI'].resample('M').mean()
    monthly_df = monthly_df.reset_index()
    
    return monthly_df

def build_AQI_time_graph(df, x_label, y_label, title, filename):
    key_points = ["2015-01-01 01:00 AM", "2016-01-01 01:00 AM", "2017-01-01 01:00 AM", "2018-01-01 01:00 AM", "2019-01-01 01:00 AM", "2020-01-01 01:00 AM", "2021-01-01 01:00 AM", "2022-01-01 01:00 AM", "2023-01-01 01:00 AM", "2024-01-01 01:00 AM", "2025-01-02 01:00 AM", ]
    labels = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    df_AQI = df["AQI"].to_numpy()
    df_datetime = df[x_label].to_numpy()
    plot = plt.figure(figsize=(22,6))
    plt.plot(df_datetime, df_AQI)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    #plt.xticks(key_points, labels)
    for label, (value, color) in aqi_levels.items():
        plt.axhline(y=value, color=color, linestyle='--', linewidth=1.5, alpha=0.8, label=label)
    plt.legend(title='AQI Levels', loc="best")
    
    plt.savefig(filename)
    return plot

def build_DiD_graph(treatment_df, control_df, target_x, filename, policy_date='2018-01-01', rolling_window=30):
    treatment_df['datetime'] = pd.to_datetime(treatment_df[target_x])
    control_df['datetime'] = pd.to_datetime(control_df[target_x])

    treatment_df = treatment_df.groupby('datetime').mean(numeric_only=True).sort_index()
    control_df = control_df.groupby('datetime').mean(numeric_only=True).sort_index()

    treatment_df['AQI_smooth'] = treatment_df['AQI'].rolling(window=rolling_window, min_periods=1).mean()
    control_df['AQI_smooth'] = control_df['AQI'].rolling(window=rolling_window, min_periods=1).mean()

    combined = pd.DataFrame({
        'Delhi': treatment_df['AQI'],
        'Chennai': control_df['AQI']
    }).dropna()

    policy_date = pd.to_datetime(policy_date)
    pre_policy = combined[combined.index < policy_date]
    post_policy = combined[combined.index >= policy_date]

    chennai_change = post_policy['Chennai'].mean() - pre_policy['Chennai'].mean()

    delhi_counterfactual_mean = pre_policy['Delhi'].mean() + chennai_change
    counterfactual = pd.Series(delhi_counterfactual_mean, index=post_policy.index)

    plt.figure(figsize=(14, 6))

    plt.plot(combined.index, combined['Delhi'], label='New Delhi (Actual)', color='red')
    plt.plot(combined.index, combined['Chennai'], label='Chennai (Control)', color='blue')

    plt.plot(counterfactual.index, counterfactual, label='New Delhi (Counterfactual)', linestyle='dotted', color='gray')

    plt.fill_between(post_policy.index,
                     post_policy['Delhi'],
                     counterfactual,
                     where=(post_policy['Delhi'] > counterfactual),
                     interpolate=True,
                     color='orange',
                     alpha=0.3,
                     label='DiD Effect')

    plt.axvline(policy_date, color='black', linestyle='--', label='Policy (2018)')
    plt.text(policy_date, combined['Delhi'].max(), 'Policy Introduced', rotation=90, va='top', ha='right')

    plt.title('Difference-in-Differences: Daily AQI (Smoothed)')
    plt.xlabel('Date')
    plt.ylabel(f'AQI ({rolling_window}-day Rolling Avg)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
    
def build_DiD_model(treatment_df, control_df, target_x, policy_date = '2018-01-01'):
    # Convert datetime
    treatment_df['datetime'] = pd.to_datetime(treatment_df[target_x])
    treatment_df['datetime'] = pd.to_datetime(treatment_df[target_x])

    # Label the datasets
    treatment_df = treatment_df.copy()
    control_df = control_df.copy()
    treatment_df['city'] = 'delhi'
    control_df['city'] = 'chennai'

    # Combine
    df = pd.concat([treatment_df, control_df])
    
    # Remove missing
    df = df.dropna(subset=['AQI'])

    # Group by date to avoid duplicates
    df = df.groupby(['datetime', 'city']).mean(numeric_only=True).reset_index()

    # Create variables
    df['post'] = (df['datetime'] >= pd.to_datetime(policy_date)).astype(int)
    df['treatment'] = (df['city'] == 'delhi').astype(int)
    df['did'] = df['post'] * df['treatment']

    # Run regression
    model = smf.ols('AQI ~ treatment + post + did', data=df).fit()

    print(model.summary())

    return model
    
    