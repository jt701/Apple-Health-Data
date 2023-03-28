import final_functions as f
import pandas as pd

#x = f.main("data/marmor_health_data/export_fixed.xml")
x = f.main("data/joseph_health_data/export.xml")


column_labels = []
for i in range(29):
    column_labels.append('test')
#for i in x:
    #print(len(i)) 
#print(x[0])
#print(len(x[0]))
df = pd.DataFrame(x, columns = column_labels)
print(df)

def main(filepath):
    array_of_data  = f.main(filepath)
    column_labels = []