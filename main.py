import final_functions as f
import pandas as pd

x = f.main("data/marmor_health_data/export_fixed.xml")
columns = []
for i in range(29):
    columns.append('test')
df = pd.DataFrame(x, columns)