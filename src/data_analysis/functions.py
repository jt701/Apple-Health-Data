import pandas as pd
import matplotlib.pyplot as plt
import os

def load_file_df(file_path):
    return pd.read_csv(file_path)

#gives list of dfs in alphabetical file name order
#need participant csv to be in same order as they are in lab_data csv
def load_folder_df(folder_path):
    files = os.listdir(folder_path)
    files = sorted(files)
    df_list = []
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        df_list.append(pd.read_csv(file_path))
    return df_list
        
#bar graph     
def bar(subjects, values, title='Bar Chart Example', xlabel='Participants', ylabel='Values'):
    fig, ax = plt.subplots()
    ax.bar(subjects, values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()

#singular bar subplot
def bar_subplot(subjects, values, ax, title, xlabel, ylabel):
    ax.bar(subjects, values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return ax

#all bar subplots for app, input is list of subjects
#make sure xdim* ydim >= len(metric_list)
def bar_subplots_app(app_data, lab_data, metric_list, stat_list, plot_xdim, plot_ydim):
    subjects = get_subjects(lab_data)
    values = []
    for i in range(len(metric_list)):
        values.append(get_app_vals(app_data, metric_list[i], stat_list[i]))
    fig, axes = plt.subplots(plot_xdim, plot_ydim)
    for i in range(plot_xdim):
        for j in range(plot_ydim):
            curr_graph = i * plot_ydim + j
            if curr_graph >= len(metric_list):
                continue
            x_label = "Participants"
            metric_num = metric_list[curr_graph]
            stat_num = stat_list[curr_graph]
            metric = app_data[0].iloc[metric_num, 0]
            stat = app_data[0].columns[stat_num]
            y_label = metric + " " + stat
            title = y_label
            bar_subplot(subjects, values[curr_graph], axes[i,j], title, x_label, y_label)
    fig.suptitle("Bar Plots")
    plt.tight_layout()
    plt.show()

#subplots for bar, uses lab data 
def bar_subplots_lab(lab_data, test_list, plot_xdim, plot_ydim):
    subjects = get_subjects(lab_data)
    values = []
    for i in range(len(test_list)):
        values.append(get_lab_vals(lab_data, test_list[i]))
    fig, axes = plt.subplots(plot_xdim, plot_ydim)
    for i in range(plot_xdim):
        for j in range(plot_ydim):
            curr_graph = i * plot_ydim + j
            if curr_graph >= len(test_list):
                continue
            x_label = "Participants"
            y_label = test_list[curr_graph]
            title = y_label
            bar_subplot(subjects, values[curr_graph], axes[i,j], title, x_label, y_label)
    fig.suptitle("Bar Plots")
    plt.tight_layout()
    plt.show()
            
    
def bar_app(app_data, lab_data, metric_num, stat_num):
    subjects = get_subjects(lab_data)
    values = get_app_vals(app_data, metric_num, stat_num)
    metric = app_data[0].iloc[metric_num, 0]
    stat = app_data[0].columns[stat_num]
    y_label = metric + " " + stat 
    title = y_label
    bar(subjects, values, title, "Participants", y_label)

def bar_lab(lab_data, test):
    subjects = get_subjects(lab_data)
    values = get_lab_vals(lab_data, test)
    bar(subjects, values, test, "Participants", test)
    
    
def scatter(xvals, yvals, title='Scatter Example', xlabel='Categories', ylabel='Values'):
    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()
    
def scatter_full(lab_data, app_data, metric_num, stat_num, test):
    app_values = get_app_vals(app_data, metric_num, stat_num)
    lab_values = get_lab_vals(lab_data, test)
    metric = app_data[0].iloc[metric_num, 0]
    stat = app_data[0].columns[stat_num]
    app_label = metric + " " + stat 
    title = app_label + " vs " + test
    scatter(app_values, lab_values, title, app_label, test)
    

#gives subject list and values list   
def get_app_vals(app_data, metric_num, stat_num):
    values = []
    for i in range(len(app_data)):
        curr_stats = app_data[i]
        val = curr_stats.iloc[metric_num, stat_num]
        values.append(val)
    return values

def get_lab_vals(lab_data, test):
    values = [lab_data.loc[i, test] for i in range(len(lab_data))]
    return values

def get_subjects(lab_data):
    subjects = [lab_data.loc[i, 'study_id'] for i in range(len(lab_data))]
    return subjects
    
    

    
