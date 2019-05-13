# DB to ML DataSet

This project guides you how to:
- export data from DB to a big raw CSV,
- how to encode (obfuscate) CSV,
- how to keep mapping to get encoded data back and at ML prediction time.   

## Getting Started

1) Review a sample SQL at 'data/test_db-export.sql' and make your own to export as much as possible fields. 
Do not worry - all sensitive data will be encoded (obfuscated) in a final CSV. Finally run your own SQL and 
produce a raw CSV that will be encoded. 

2) Open 'encode.py' and fix fields as in your raw CSV.  

```
mapping = {
    'comments': """
        - Keep your mapping private and do NOT share to any ML person / team. 
        - Review and fix fields for your own CSV.
        - Share only encrypted CSV.
        - For prediction use same way to encrypt values before to pass it to the ML model.
        - Fix and use your own dates_offset_seconds, now 1234 days as offset it is just a sample!!! 
          Put your own positive number of days. So all dates will be shifted using that value.   
    """.strip(),
    'fields_as_is': ['emp_id'],  # will not be encoded
    'fields_dates_add_offset': ['birth_date', 'salary_end_date', 'title_end_date'],
    'dates_offset_seconds': 1234 * 24 * 60 * 60,  # all dates will be shifted
    'normalized_fields': ['salary'],  # as (value - avg) / std
    'categorize_fields': ['gender', 'title']
}
```    

3) Run 'encode.py' and produce encoded CSV plus mapping files. 

4) Share encoded CSV but DO NOT SHARE raw CSV and mapping files. Encoded CSV keeps the structure of the data 
but does not reveal its values.      

### Prerequisites

You need to use Python 3.7 and later version. 

## License

This project is licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

