import functions as f

record = f.xml_to_df("joseph_health_data/export.xml")
f.process_df(record)
stepCount = f.get_metric_df(record, "StepCount")
print(f.daily_stats(stepCount, 365))

"""
x = f.reduce(stepCount, 365)
y = f.resample(x, 'day')
print((float(y.max())))
print(y.min())
print(type(y.mean()))
#print(f.resample(parsed, 'year').loc['2015-12-31 00:00:00-08:00',0])
#print(parsed.columns)

#print(float(f.resample(parsed, 'year')))
"""


