import functions as f
import matplotlib.pyplot as plt

lab_data = f.load_file_df('data/lab_data.csv')
app_data = f.load_folder_df('data/participants')
f.bar(0, 1, lab_data, app_data)
# print(x)

