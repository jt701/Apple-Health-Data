import functions as f

record = f.xml_to_df("apple_health_export2:23/export.xml")
f.process_df(record)
print(record)