import functions as f
import matplotlib.pyplot as plt

# lab_data = f.load_file_df('data/lab_data.csv')
lab_data = f.load_file_df('data/lab_data_new.csv')
app_data = f.load_folder_df('data/participants')


#Test SCATTER SUBPLOTS
f.scatter_subplots(lab_data, app_data, [0, 0, 0, 1, 1, 6, 6, 9, 9], [1, 5, 9, 21, 26, 1, 5, 4, 14], ["grip_test2", "rel_vo2_max", "chair_rise_test", "jump_height", "hr_max", "tug_test", "grip_strength", "abs_vo2_max", "rer_max"], 3, 3)

#Test SUBPLOT APP/LAB BAR PLOTS
# f.bar_subplots_app(app_data, lab_data, [0, 0, 0, 1, 1, 6, 6, 9, 9], [1, 5, 9, 21, 26, 1, 5, 4, 14], 3, 3)
# f.bar_subplots_lab(lab_data, ["grip_test2", "rel_vo2_max", "chair_rise_test", "jump_height", "hr_max", "tug_test", "grip_strength", "abs_vo2_max", "rer_max"], 3, 3 )

# TEST FULL SCATTER PLOTS
# f.scatter_full(lab_data, app_data, 2, 5, "abs_vo2_max")

# TEST FULL BAR GRAPHS
# f.bar_app(app_data, lab_data, 7, 4)

# TEST SCATTER GRAPHS
# app_vals = f.get_app_vals(app_data, 0, 1)
# lab_vals = f.get_lab_vals(lab_data, 'chair_rise_test')
# f.scatter(app_vals, lab_vals)

# TEST BAR GRAPHS
# values = f.get_app_vals(lab_data, app_data, 0, 1)
# values = f.get_lab_vals(lab_data,"chair_rise_test")
# subjects = f.get_subjects(lab_data)
# f.bar(subjects, values)


