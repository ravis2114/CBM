# CBM

# requirements
`
pandas
`
# how to use it
`your_file_name.py`
```
from cbm.cbm_data_combine import DataDriver

driver = DataDriver('EVT_data', 'Ams')
data = driver.get_data()
uniq = driver.get_duplicated_col(data)
updated_col = driver.get_unique_col(data)
missing_col = driver.get_missing_col(updated_col)
```