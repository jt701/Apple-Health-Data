import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#takes in xml, returns record df and workout df
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
#aggregates by summing, if avg = True it aggregrates by mean for metrics like blood oxygen, etc. 
def resample_sum(df, time_period, avg = False):
    df.set_index('startDate', inplace=True)
    if avg:
        daily_counts = df['value'].resample('D').mean()
    else:
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



#provides daily averages over sample_period for metric
#if avg is True, signals to resample sum that aggregration by mean must occur
def daily_stats(df, sample_period, avg = False):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'day', avg)
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#provides cumulative averages over sample_period for metric
#calls resample_sum_avg if avg is True
#metric is cumulative over chunk_size (i.e chunk_size = 'week' would take the cumulative sum in chunks of weeks)
#chunk_size is 'week', 'month', 'year'
def longer_stats(df, sample_period, chunk_size, avg = False):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, chunk_size, avg)
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]
    
#returns all stats for a given metric, takes in whether it is an averaged metric, or a workout
#currently, only validates that there are elements in the metric_df
#returns list of given metric
#mean, median, max, min for daily: week, month, year, all time and cumulative: week, month, year in that order
#unlabeled such that we can run array to dataframe and then csv
def get_all_stats(df, metric, avg = False, workout = False):
    if workout or metric == "WorkoutMinutes":
        metric_df = df
    else:
        metric_df = get_metric_df(df, metric)
    if len(metric_df) == 0:
        return [metric]
    results = [metric]
    results.extend(daily_stats(metric_df, 7, avg))
    results.extend(daily_stats(metric_df, 30, avg))
    results.extend(daily_stats(metric_df, 365, avg))
    results.extend(daily_stats(metric_df, 10000, avg))
    results.extend(longer_stats(metric_df, 364, 'week', avg))
    results.extend(longer_stats(metric_df, 360, 'month', avg))
    num_years = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    results.extend(longer_stats(metric_df, num_years * 365, 'year', avg))
    return results

def main(filepath):
    record, workout = xml_to_df(filepath)
    process_df(record)
    process_workout(workout)
    results = []
    results.append(get_all_stats(record, "StepCount"))
    results.append(get_all_stats(record, "FlightsClimbed"))
    results.append(get_all_stats(record, "DistanceWalkingRunning"))
    results.append(get_all_stats(record, "AppleExerciseTime"))
    results.append(get_all_stats(record, "AppleStandTime"))
    results.append(get_all_stats(record, "SleepAnalysis"))
    results.append(get_all_stats(record, "WorkoutMinutes", workout = True))
    results.append(get_all_stats(record, "RespiratoryRate"))
    results.append(get_all_stats(record, "OxygenSaturation"))
    results.append(get_all_stats(record, "HeartRateVariabilitySDNN"))
    results.append(get_all_stats(record, "HeartRate"))
    results.append(get_all_stats(record, "RunningSpeed"))
    results.append(get_all_stats(record, "WalkingSpeed"))
    return results