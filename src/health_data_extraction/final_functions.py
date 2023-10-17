import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt
import numpy as np


def xml_to_df(filepath):
    """Iteratively parses through each item in filepath and returns workout and record dataframes 

    Args:
        filepath (path): apple health data xml file

    Returns:
        pd.Dataframe: two dataframes corresponding to workout and regular health events
    """
    record_data = []
    workout_data = []

    for event, elem in et.iterparse(filepath):
        if elem.tag == "Record":
            record_data.append(elem.attrib)
        elif elem.tag == "Workout":
            workout_data.append(elem.attrib)
        elem.clear()  # Clear the element from memory after processing

    record_df = pd.DataFrame(record_data)
    workout_df = pd.DataFrame(workout_data)
    
    return record_df, workout_df


def process_df(df):
    """Processes and mutates dataframe to make it cleaner, only for records df

    Args:
        df (pd.Dataframe): record dataframe 

    Returns:
        None (mutates df directly to save storage becasue of their size)
    """
    if df.empty:
        return df
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
    """Processes and mutates dataframe to make it cleaner, only for workouts df

    Args:
        df (pd.Dataframe): workouts dataframe 

    Returns:
        None (mutates df directly to save storage becasue of their size)
    """
    if df.empty:
        return df
    for col in ['startDate']:
        df[col] = pd.to_datetime(df[col])
    df['duration'] = pd.to_numeric(df['duration'])
    df.dropna(subset=['duration'], inplace= True)
    df['workoutActivityType'] =df['workoutActivityType'].str.replace('HKWorkoutActivityType', '')
    df.rename(columns={"duration": "value"}, inplace = True)
  
def get_metric_df(df, metric):
    """Returns dataframe with only a certain health metric

    Args:
        df (pd.Dataframe): workout or record df
        metric (string): describes specific health metric

    Returns:
        pd.Dataframe: dataframe that only contains specified metric
    """
    if metric == "SleepAnalysis":
        df = df[df["type"] == metric]
        return df.dropna(subset=['source'])
    return df[df["type"] == metric]

def reduce(df, time_period):
    """Takes dataframe and only includes data for a certain time period

    Args:
        df (pd.Dataframe): metric dataframe
        time_period (int): number of days to include

    Returns:
        pd.Dataframe: dataframe that only includes data from a certain time period
    """
    max_date = df['startDate'].max().replace(hour=0, minute=0, second=0, microsecond=0)
    time_frame = max_date - dt.timedelta(days=time_period)
    df = df[df['startDate'] < max_date]
    return df[df['startDate'] > time_frame]


def resample_sum(df, time_period, avg = False):
    """Aggregrates data by a certain time period. 
    Summed for most metrics (stepCount etc.) but metrics like heart rate are averaged

    Args:
        df (pd.Dataframe): metric dataframe
        time_period (int): numbers of days to group sample buy
        avg (bool, optional): whether or not aggregration is done by averaging. Defaults to False.

    Returns:
        pd.Dataframe: dataframe that is aggregrated by a certain time period
    """
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


def daily_stats(df, sample_period, avg = False):
    """Obtains daily mean, median, max, min stats over a certain sample_period
    If average is True, daily stats are found by aggregration. In other words, 
    cumulative sum over a sample period is calculated. 

    Args:
        df (pd.Dataframe): metric dataframe_
        sample_period (int): number of days sampled
        avg (bool, optional): Whether or not the stat is cumulative. Defaults to False.

    Returns:
        int array: mean, median, max, min for daily over sample period
    """
    delta = df['startDate'].max() -  df['startDate'].min()
    if delta.days < sample_period and sample_period < 1000:
        return [np.nan for i in range(4)]
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'day', avg)
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]


def longer_stats(df, sample_period, chunk_size, avg = False):
    """Gets stats for chunks greater than a singular day. 

    Args:
        df (pd.Dataframe): metric dataframe
        sample_period (int): number of days sampled
        chunk_size (int): how many days in a chunk (i.e 7 if we want week to week comparisons)
        avg (bool, optional): Whether or not stats should be cumulative. Defaults to False.

    Returns:
        int array: mean, median, max, min for respective sample period and chunk size
    """
    delta = df['startDate'].max() -  df['startDate'].min()
    if delta.days < sample_period:
        return [np.nan for i in range(4)]
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, chunk_size, avg)
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]
    
def get_all_stats(df, metric, avg = False, workout = False):
    """Returns all stats for a given metric

    Args:
        df (pd.Dataframe): metric dataframe
        metric (string): type of health metric
        avg (bool, optional):Whether or not metric itself needs to be aggregrated
            by average instead of sum(i.e heart rate). Defaults to False.
        workout (bool, optional): Whether or not metric is workout metric. Defaults to False.

    Returns:
       pd.Dataframe: has all stats (chunked by week, month, year, all-time) and over various time periods in
       a singular array. Represents a row in final dataframe. 
    """
    if df.empty:
        results = [metric]
        results.extend([np.nan for i in range (28)])
        return results
    if workout or metric == "WorkoutMinutes":
        metric_df = df
    else:
        metric_df = get_metric_df(df, metric)
    if metric_df.empty or len(metric_df) == 0:
        results = [metric]
        results.extend([np.nan for i in range (28)])
        return results
    results = [metric + get_units(metric)]
    results.extend(daily_stats(metric_df, 7, avg))
    results.extend(daily_stats(metric_df, 30, avg))
    results.extend(daily_stats(metric_df, 365, avg))
    results.extend(daily_stats(metric_df, 10000, avg))
    results.extend(longer_stats(metric_df, 364, 'week', avg))
    results.extend(longer_stats(metric_df, 360, 'month', avg))
    num_years = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    results.extend(longer_stats(metric_df, num_years * 365, 'year', avg))
    return results

#gets units for a given metric, needs to be updated if new metric is added
def get_units(metric):
    """Gets unit name based on metric

    Args:
        metric (string): type of health metric

    Returns:
        string: unit for the respective health metric
    """
    if metric == "StepCount":
        return "(steps)"
    elif metric == "FlightsClimbed":
        return "(flights)"
    elif metric == "DistanceWalkingRunning":
        return "(miles)"
    elif metric == "AppleExerciseTime" or metric == "AppleStandTime" or metric == "SleepAnalysis" or metric == "WorkoutMinutes":
        return "(min)"
    elif metric == "RespiratoryRate":
        return "(breaths/min)"
    elif metric == "OxygenSaturation":
        return "(fraction)"
    elif metric == "HeartRateVariabilitySDNN":
        return "(ms)"
    elif metric == "HeartRate":
        return "(BPM)"
    elif metric == "RunningSpeed" or metric == "WalkingSpeed":
        return "(mph)"
    return ""
    
def main(filepath):
    """Calls get all stats for each metric. Appends each one to an array.

    Args:
        filepath (path): filepath for apple health xml file

    Returns:
        array: each element is all the stats for a specific metric. Array of depth 2
    """
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
    results.append(get_all_stats(workout, "WorkoutMinutes", workout = True))
    results.append(get_all_stats(record, "RespiratoryRate", avg = True))
    results.append(get_all_stats(record, "OxygenSaturation", avg = True))
    results.append(get_all_stats(record, "HeartRateVariabilitySDNN", avg = True))
    results.append(get_all_stats(record, "HeartRate", avg = True))
    results.append(get_all_stats(record, "RunningSpeed", avg = True))
    results.append(get_all_stats(record, "WalkingSpeed", avg = True))
    return results