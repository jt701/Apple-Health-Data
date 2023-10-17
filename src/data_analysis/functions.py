import pandas as pd
import matplotlib.pyplot as plt
import os
def load_file_df(file_path):
    return pd.read_csv(file_path)

#gives list of dfs in alphabetical file name order
def load_folder_df(folder_path):
    files = os.listdir(folder_path)
    files = sorted(files)
    df_list = []
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        df_list.append(pd.read_csv(file_path))
    return df_list
        
#bar graph     
def bar(metric_num, stat_num, lab_data, app_data, title='Bar Chart Example', xlabel='Categories', ylabel='Values'):
    fig, ax = plt.subplots()
    subjects = [lab_data.loc[i, 'study_id'] for i in range(len(lab_data))]
    values = []
    for i in range(len(app_data)):
        curr_stats = app_data[i]
        val = curr_stats.iloc[metric_num, stat_num]
        values.append(val)
    ax.bar(subjects, values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()
    
def get_vals():
    print("none")
    

    
