# Export sensetice data and obfuscate it

> It is possible to export the sensitive data and obfuscate (encode) it.

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

5) Train an ML model on encoded dataset and predict something. Send predicted results (also encoded) back who holds the mapping JSON / Pickle.

6) Decode back predicted values to normal values using the maping JSON or pickle file.

Have fun! ML team and production data are isolated!

PS if you think this approach is not safe please try to decode encoded CSV in the data folder but do not use mapping JSON / pickle. If you do it please send it to me and I will remove this project as unsafe right away! 

### Warning!
PSS I was wrong that it is impossible to reveal some kind of information. It is possible since the structure of the data, relations between features and in a feature are preserved. For example, it is possible to decode the mean and std of a salary column thus it is possible to decode salaries. Of course, it is impossible to see names, emails, phones, SSN and any other personal information but again it is possible to decode continuous variables and dates in the dataset. So, ideally, the Federative learning is the best!

### Prerequisites

You need to use Python 3.7 and later version. 

## License

This project is licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

