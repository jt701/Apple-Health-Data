import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#returns new df with all values of a specific day summed
def get_daily_df_sum(df, time_size = 'day'):
    df2 = df.groupby('startDate').agg({'value': 'sum'})
    return df2


#takes in daily df, returns daily metrics
def get_daily_stats(df):
    avg_daily_count = df[('value', 'sum')].mean()

#attempts to use deprecated pandas method to group by week
def test(df):
    weekly_avg_step_count = df.groupby(df["startDate"].dt.week)["value"].mean()
    return weekly_avg_step_count