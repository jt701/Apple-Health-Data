import final_functions as f
import pandas as pd

#return df of all statistics
def main(filepath):
    data  = f.main(filepath)
    column_labels = ['metric', 'W-avg', 'W-med', 'W-max', 'W-min']
    column_labels.extend(['M-avg', 'M-med', 'M-max', 'M-min'])
    column_labels.extend(['Y-avg', 'Y-med', 'Y-max', 'Y-min'])
    column_labels.extend(['All-avg', 'All-med', 'All-max', 'All-min'])
    column_labels.extend(['W(sum)-avg', 'W(sum)-med', 'W(sum)-max', 'W(sum)-min'])
    column_labels.extend(['M(sum)-avg', 'M(sum)-med', 'M(sum)-max', 'M(sum)-min'])
    column_labels.extend(['Y(sum)-avg', 'Y(sum)-med', 'Y(sum)-max', 'Y(sum)-min'])
    df = pd.DataFrame(data, columns = column_labels)
    return df

#returns number of valid metrics
def valid_rows(df):
    count = 0
    for i in range(len(df)):
        if len(df.iloc[i].dropna()) > 1:
            count += 1
    return count

#return number of boxes filled 
def entries_filled(df):
    return df.count().sum() - 13






