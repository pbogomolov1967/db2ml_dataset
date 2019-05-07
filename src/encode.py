#!/usr/bin/env python3
# coding: utf8
import json
import random

from util import normalize, categorize, load_csv_as_is, \
    covert_date_to_epoch_seconds, convert_dates, save_mapping, save_mapping_as_is, rename_fields

INPUT_CSV_FILE = '../data/test_db-as-is.csv'  # an input CSV file - DO NOT SHARE!!!
OUTPUT_CSV_FILE = '../data/test_db-encoded.csv'  # a CSV file will be produced - you can share this CSV
MAPPING_PKL_FILE = '../data/test_db-mapping.pkl'  # a mapping file - DO NOT SHARE!!!
MAPPING_JSON_FILE = '../data/test_db-mapping.json'  # a mapping file - DO NOT SHARE!!!

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

df1 = load_csv_as_is(INPUT_CSV_FILE)  # source CSV as is
df2 = df1[mapping['fields_as_is']].copy()  # destination CSV

# list(df1.columns)
# ['emp_id', 'birth_date', 'gender', 'salary', 'title', 'salary_end_date', 'title_end_date']

avg_std_offsets = []
for field_name in mapping['normalized_fields']:
    print(f'normalize "{field_name}" field...')
    offsets = normalize(df1, df2, data_column_from=field_name, data_column_to=field_name)
    avg_std_offsets.append(offsets)
mapping['normalized_fields_with_avg_std_offsets'] = list(zip(mapping['normalized_fields'], avg_std_offsets))


for field_name in mapping['fields_dates_add_offset']:
    print(f'expand date from "{field_name}" field...')
    df1[field_name] = convert_dates(df1[field_name])
    covert_date_to_epoch_seconds(df1, df2, data_column_from=field_name, data_column_to=field_name,
                                 add_offset_as_seconds=mapping['dates_offset_seconds'])

mapping['categorize_mapping'] = categorize(df1, df2, mapping['categorize_fields'])

mapping['fields_mapping'] = rename_fields(df2.columns, mapping['fields_dates_add_offset'])
df2.rename(columns=mapping['fields_mapping'], inplace=True)

print(f'saving "{OUTPUT_CSV_FILE}"...')
df2.to_csv(OUTPUT_CSV_FILE, index=False)
print(f'please share ONLY "{OUTPUT_CSV_FILE}" file!')

mapping_json = json.dumps(mapping, indent=2, sort_keys=True)
save_mapping(mapping, MAPPING_PKL_FILE)
save_mapping_as_is(mapping_json, MAPPING_JSON_FILE)

print('done')
