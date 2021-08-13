import pandas as pd
import numpy as np
import os

RIGHT_HAND_ALONE = r'extraFiles\HandRight.csv'


def clean_right_alone(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = rename_columns(df.columns, append_name='right')
    df = df[df['right_Hand Type'] == 'right']
    return df


def rename_columns(columns, append_name=None):
    cols = []
    for col in columns:

        col = str(col).strip()
        if append_name and col != 'Frame ID':
            col = append_name + '_' + col
        cols.append(col)
    return cols


def prepare_data(csv_path, name):
    # removing the white space in columns
    df = pd.read_csv(csv_path)
    df.columns = rename_columns(list(df.columns))

    # split to left - right hand
    if 'alone':
        right_hand = clean_right_alone(RIGHT_HAND_ALONE).drop(['Time'], axis=1)
        right_hand['Frame ID'] = df['Frame ID']
    else:
        right_hand = df[df['Hand Type'] == 'right'].drop(['Time'], axis=1)
    left_hand = df[df['Hand Type'] == 'left'].drop(['Time'], axis=1)

    # renaming the columns to left right
    right_hand.columns = rename_columns(list(right_hand.columns), 'right')
    left_hand.columns = rename_columns(list(left_hand.columns), 'left')

    # marging
    hands = pd.merge(left_hand, right_hand, on='Frame ID').drop(
        ['left_Hand Type', 'right_Hand Type', 'left_# hands', 'right_# hands'], axis=1)

    # add name
    hands['name'] = [name] * hands.shape[0]

    # add label
    if 'sync' in str(csv_path).lower():
        hands['label'] = ['sync'] * hands.shape[0]
    elif 'alone' in str(csv_path).lower():
        hands['label'] = ['alone'] * hands.shape[0]
    elif 'spontan' in str(csv_path).lower():
        hands['label'] = ['spontan'] * hands.shape[0]

    return hands


# name_id = 1
# for root, dir, files in os.walk('extraFiles\Training'):
#     for file in files:
#         df = prepare_data(os.path.join(root, file), name_id)
#         name_id += 1
# print(df.head())
clean_right_alone(RIGHT_HAND_ALONE)
