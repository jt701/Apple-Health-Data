import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#To do/progess
""" 1. validate enough data points are present (remember 1 year time frame)
    -as long as dataframe is not null for now
    2. exports metrics to CSV, fill with NaN if not valid
    3. Types of Metrics
        a. workout
            i. no metric df needed
        b. regular cumulative
            i. ‘StepCount’
            ii. 'FlightsClimbed'
            iii. 'DistanceWalkingRunning'
            iv. 'AppleExerciseTime'
            v. ‘AppleStandTime’
            vi. 'SleepAnalysis'
        c. averaged
            i. 'RespiratoryRate'
            ii. 'OxygenSaturation'
        d. additional (averaged)
            i. 'HeartRateVariabilitySDNN'
            ii. 'HeartRate'
            iii. 'RunningSpeed'
            iv. 'WalkingSpeed'
            

""" 

#converts xml file to df using filepath
#need filepath export_cda.xml, (if a "fixed" xml file is present, use that one)
#phone must be updated to latest IOS
def xml_to_df(filepath):
    tree = et.parse(filepath) 
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    workout_list = [x.attrib for x in root.iter('Workout')]
    return pd.DataFrame(record_list), pd.DataFrame(workout_list)

#proccess record df to make it cleaner (dates, NaN values, etc.), mutates df
def process_df(df):
    for col in ['startDate', 'endDate', 'creationDate']:
       df[col] = pd.to_datetime(df[col])
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')
    df.loc[df["value"] == "HKCategoryValueSleepAnalysisAsleepUnspecified", "source"] = 0
    df.loc[df["type"] == "SleepAnalysis", "value"] = df.loc[df["type"] == "SleepAnalysis", "endDate"]-  df.loc[df["type"] == "SleepAnalysis", "startDate"] 
    df.loc[df["type"] == "SleepAnalysis", "value"] = df.loc[df["type"] == "SleepAnalysis", "value"].apply(lambda x: round(x.total_seconds() / 60, 2))
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['value'], inplace= True)
    
#process workout df to make it cleaner
def process_workout(df):
    for col in ['startDate']:
        df[col] = pd.to_datetime(df[col])
    df['duration'] = pd.to_numeric(df['duration'])
    df.dropna(subset=['duration'], inplace= True)
    df['workoutActivityType'] =df['workoutActivityType'].str.replace('HKWorkoutActivityType', '')
    df.rename(columns={"duration": "value"}, inplace = True)
   

#returns new df with only the given metric  
def get_metric_df(df, metric):
    if metric == "SleepAnalysis":
        df = df[df["type"] == metric]
        return df.dropna(subset=['source'])
    return df[df["type"] == metric]


#takes in time period and reduces to only this time period in days, does not include the lower bound
#starts at max data point and goes backwards (not at start of day)
def reduce(df, time_period):
    max_date = df['startDate'].max().replace(hour=0, minute=0, second=0, microsecond=0)
    time_frame = max_date - dt.timedelta(days=time_period)
    df = df[df['startDate'] < max_date]
    return df[df['startDate'] > time_frame]


#returns df in chunks of time_period (day, week, month)
#does so by resampling every x days (goes backwards from max date, not at start of day)
#aggregates by summing
def resample_sum(df, time_period):
    df.set_index('startDate', inplace=True)
    daily_counts = df['value'].resample('D').sum()
    
    if time_period == 'day':
        pass
    elif time_period == 'week':
        daily_counts = daily_counts.resample('7D').sum()
    elif time_period == 'month':
        daily_counts = daily_counts.resample('30D').sum()
    elif time_period == 'year':
        daily_counts = daily_counts.resample('365D').sum()
    return daily_counts.to_frame()

#resampling for metrics that must be averaged (blood oxygen, etc. )
def resample_sum_avg(df, time_period):
    df.set_index('startDate', inplace=True)
    daily_counts = df['value'].resample('D').mean()
    
    if time_period == 'day':
        pass
    elif time_period == 'week':
        daily_counts = daily_counts.resample('7D').sum()
    elif time_period == 'month':
        daily_counts = daily_counts.resample('30D').sum()
    elif time_period == 'year':
        daily_counts = daily_counts.resample('365D').sum()
    return daily_counts.to_frame()

#takes in metric df, how long the sample period is in days,the chunk size
#returns array of arrays
#first array is last week statistics, 2nd is month, 3rd is year
#in each smaller area, mean, median, max, min
def daily_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'day')
    print(chunked_df)
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def daily_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'day')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#return array of arrays reflecting daily data
#minimum one year data needed
def combined_daily_stats(df, metric):
    metric_df = get_metric_df(df, metric)
    #if len(metric_df) == 0:
        #return "NA"
    results = ["daily" + metric]
    results.extend(["week", daily_stats(metric_df, 7) ])
    results.extend(["month", daily_stats(metric_df, 30) ])
    results.extend(["year", daily_stats(metric_df, 365) ])
    results.extend(["all time", daily_stats(metric_df, 10000) ])
    return results

#for averaged stats
def combined_daily_stats_avg(df, metric):
    metric_df = get_metric_df(df, metric)
    #if len(metric_df) == 0:
        #return "NA"
    results = ["daily" + metric]
    results.extend(["week", daily_stats_avg(metric_df, 7) ])
    results.extend(["month", daily_stats_avg(metric_df, 30) ])
    results.extend(["year", daily_stats_avg(metric_df, 365) ])
    results.extend(["all time", daily_stats_avg(metric_df, 10000) ])
    return results

def combined_daily_stats_workout(df, metric):
    metric_df = df
    results = ["daily" + metric]
    results.extend(["week", daily_stats(metric_df, 7) ])
    results.extend(["month", daily_stats(metric_df, 30) ])
    results.extend(["year", daily_stats(metric_df, 365) ])
    results.extend(["all time", daily_stats(metric_df, 10000) ])
    return results


#defined as 7 days, chunks and provides stats based on week
def weekly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'week')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def weekly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'week')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#defined as 30 days, chunks and provides stats based on month
def monthly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'month')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def monthly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'month')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#defined as 365 days
def yearly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'year')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def yearly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'year')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]


#monthly and weekly stats combined, over 52 weeks and 12 30 day periods
def combined_longer_stats(df, metric):
    metric_df = get_metric_df(df, metric)
    results = ["daily" + metric]
    results.extend(["cumulative week", weekly_stats(metric_df, 364) ])
    results.extend(["cumulative month", monthly_stats(metric_df, 360) ])
    numYears = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    results.extend(["cumulative year", yearly_stats(metric_df, numYears * 365)])
    return results

#combined states for average metrics
def combined_longer_stats_avg(df, metric):
    metric_df = get_metric_df(df, metric)
    results = ["daily" + metric]
    results.extend(["cumulative week", weekly_stats_avg(metric_df, 364) ])
    results.extend(["cumulative month", monthly_stats_avg(metric_df, 360) ])
    numYears = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    results.extend(["cumulative year", yearly_stats_avg(metric_df, numYears * 365)])
    return results

#stats for workout specifically
def combined_longer_stats_workout(df, metric):
    metric_df = df
    results = ["daily" + metric]
    results.extend(["cumulative week", weekly_stats(metric_df, 364) ])
    results.extend(["cumulative month", monthly_stats(metric_df, 360) ])
    numYears = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    results.extend(["cumulative year", yearly_stats(metric_df, numYears * 365)])
    return results
    
  
    
    
    
    

    



