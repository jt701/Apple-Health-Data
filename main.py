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
   

