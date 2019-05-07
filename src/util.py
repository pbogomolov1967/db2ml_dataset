#!/usr/bin/env python3
# coding: utf8
import pickle
import random
import datetime
import pandas as pd
import numpy as np
from dateutil import tz


def load_csv_as_is(path_to_csv_file):
    """
    :param path_to_csv_file: full or relative
    :return: a loaded pandas data frame
    """
    print(f'loading "{path_to_csv_file}"...')
    df = pd.read_csv(path_to_csv_file, encoding='utf-8', sep=',')
    return df


def normalize(src_df, dst_df, data_column_from, data_column_to):
    """
    Normalize a data vector (or an array) as data = (data - average) / std
    :param src_df: as a pandas DataFrame with raw data
    :param dst_df: as a pandas DataFrame with encoded data
    :param data_column_from: a source data column in the DataFrame
    :param data_column_to: a destination column in the DataFrame
    :return: average and standard deviation were used in normalization,
             to restore you need to multiply by std and add average back
    """
    data = src_df[data_column_from]
    data = np.array(data)
    avg = data.mean()
    std = data.std()
    dst_df[data_column_to] = (data - avg) / std
    return avg, std


def covert_date_to_epoch_seconds(src_df, dst_df, data_column_from, data_column_to, add_offset_as_seconds):
    """
    Convert dates to epoch seconds and add same shift to all values
    :param src_df: as a pandas DataFrame with raw data
    :param dst_df: as a pandas DataFrame with encoded data
    :param data_column_from: a source data column in the DataFrame
    :param data_column_to: a destination column in the DataFrame
    :param add_offset_as_seconds: all dates will be shifted
    """
    data = src_df[data_column_from]
    epoch_seconds = data.apply(datetime.datetime.timestamp).astype('int64')
    dst_df[data_column_to] = epoch_seconds + add_offset_as_seconds


def categorize(src_df, dst_df, field_names):
    """
    Categorize all strings and integers
    :param src_df: as a pandas DataFrame with raw data
    :param dst_df: as a pandas DataFrame with encoded data
    :param field_names: those will be categorized
    :return: mapping for values
    """
    categorize_mapping = []
    for field_name in field_names:
        print(f'categorizing "{field_name}"...')
        data = src_df[field_name]
        unique_values = list(set(data))
        random.shuffle(unique_values)  # make it unpredictable
        field_mapping = dict(list(zip(list(map(lambda x: str(x), unique_values)),
                                      list(map(lambda x: f'C{x+1}', range(len(unique_values)))))))
        data = data.astype('str')
        data = data.apply(lambda x: field_mapping[x])
        dst_df[field_name] = data
        categorize_mapping.append((field_name, field_mapping))

    return categorize_mapping


def save_mapping(obj, filename):
    print(f'saving "{filename}"... DO NOT SHARE mapping and original CSV!')
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def save_mapping_as_is(obj, filename):
    print(f'saving "{filename}"... DO NOT SHARE mapping and original CSV!')
    with open(filename, 'wt') as output:  # Overwrites any existing file.
        output.write(obj)


def convert_dates(date_series):
    """
    Covert date column from the text representation to the datetime representation in UTC tz
    :param date_series: with dates as text, e.g. 2011-05-23
    :return: a series as datetime.datetime values in UTC tz
    """
    data = date_series.astype(str) + ' 00:00:00'
    utc_tz = tz.gettz('UTC')
    return data.apply(
        lambda dt: datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc_tz))


def rename_fields(col_names, datatime_fields):
    """
    Rename field names
    :param datatime_fields: fields with date/time
    :param col_names: from the data frame
    :return: renamed column names
    """
    # random.shuffle(cols)
    field_names_mapping = dict(zip(col_names, map(lambda x: f'F{x+1}', range(len(col_names)))))
    for field_name in datatime_fields:
        field_names_mapping[field_name] += 'DT'
    return field_names_mapping

