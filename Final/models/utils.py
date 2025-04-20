import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf 

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
    df_AQI = df["AQI"].to_numpy()
    df_datetime = df["Date (LT)"].to_numpy()
    plot = plt.figure(figsize=(12,6))
    plt.plot(df_datetime, df_AQI)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    for label, (value, color) in aqi_levels.items():
        plt.axhline(y=value, color=color, linestyle='--', linewidth=1.5, alpha=0.8, label=label)
    return plot

def build_DiD_graph(treatment_df, post_df):
    treatment_df['treated'] = 1
    post_df['treated'] = 0
    aqi_df = pd.concat([treatment_df, post_df], ignore_index=True)
    
    aqi_df['post'] = aqi_df['Year'] >= 2018
    aqi_df['did'] = aqi_df['treated'] * aqi_df['post']
    
    model = smf.ols('AQI ~ treated + post +did', data=aqi_df).fit()
    
    return model
    