import pandas as pd
import json

# {
#     "intents": [
#         "next day that X at least Y",
#         "next day that X at most Y",
#         "next day that X between Y and Z",
#         "next day that X is Y",
#         "today X at least Y",
#         "today X at most Y",
#         "today X between Y and Z",
#         "today X is Y",
#         "tomorrow X at least Y",
#         "tomorrow X at most Y",
#         "tomorrow X between Y and Z",
#         "tomorrow X is Y",
#         "what is X at time Y",
#         "what is X today?",
#         "what is X tomorrow?",
#         "other"
#     ]
# }

def retrieveInfo(df, query):
    intent = query['intent']
    if intent == 'next day that X at least Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the column where the value is at least Y
        for day in df.columns[1:]:
            if float(row[day].values[0]) >= Y: return day
    if intent == 'next day that X at most Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the column where the value is at most Y
        for day in df.columns[1:]:
            if float(row[day].values[0]) <= Y: return day
    if intent == 'next day that X between Y and Z':
        X = query['X']
        Y = float(query['Y'])
        Z = float(query['Z'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the column where the value is between Y and Z
        for day in df.columns[1:]:
            if float(row[day].values[0]) >= Y and float(row[day].values[0]) <= Z: return day
    if intent == 'next day that X is Y':
        X = query['X']
        try: Y = float(query['Y'])
        except: Y = query['Y']
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the column where the value is Y
        for day in df.columns[1:]:
            if float(row[day].values[0]) == Y: return day
    if intent == 'today X at least Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for today
        if 'AM' in df.columns[1]: values = row[df.columns[1:4]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[1:3]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[1:2]].values[0]
        # check if the value is at least Y
        if any([float(value) >= Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'today X at most Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for today
        if 'AM' in df.columns[1]: values = row[df.columns[1:4]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[1:3]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[1:2]].values[0]
        # check if the value is at most Y
        if any([float(value) <= Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'today X between Y and Z':
        X = query['X']
        Y = float(query['Y'])
        Z = float(query['Z'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for today
        if 'AM' in df.columns[1]: values = row[df.columns[1:4]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[1:3]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[1:2]].values[0]
        # check if the value is between Y and Z
        if any([float(value) >= Y and float(value) <= Z for value in values]): return 'yes'
        else: return 'no'
    if intent == 'today X is Y':
        X = query['X']
        try: Y = float(query['Y'])
        except: Y = query['Y']
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for today
        if 'AM' in df.columns[1]: values = row[df.columns[1:4]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[1:3]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[1:2]].values[0]
        # check if the value is Y
        if any([float(value) == Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'tomorrow X at least Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for tomorrow
        if 'AM' in df.columns[1]: values = row[df.columns[4:7]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[3:6]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[2:5]].values[0]
        # check if the value is at least Y
        if any([float(value) >= Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'tomorrow X at most Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for tomorrow
        if 'AM' in df.columns[1]: values = row[df.columns[4:7]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[3:6]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[2:5]].values[0]
        # check if the value is at most Y
        if any([float(value) <= Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'tomorrow X between Y and Z':
        X = query['X']
        Y = float(query['Y'])
        Z = float(query['Z'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for tomorrow
        if 'AM' in df.columns[1]: values = row[df.columns[4:7]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[3:6]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[2:5]].values[0]
        # check if the value is between Y and Z
        if any([float(value) >= Y and float(value) <= Z for value in values]): return 'yes'
        else: return 'no'
    if intent == 'tomorrow X is Y':
        X = query['X']
        Y = float(query['Y'])
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for tomorrow
        if 'AM' in df.columns[1]: values = row[df.columns[4:7]].values[0]
        if 'PM' in df.columns[1]: values = row[df.columns[3:6]].values[0]
        if 'Night' in df.columns[1]: values = row[df.columns[2:5]].values[0]
        # check if the value is Y
        if any([float(value) == Y for value in values]): return 'yes'
        else: return 'no'
    if intent == 'what is X at time Y':
        X = query['X']
        Y = query['Y']
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the value at time Y
        return row[Y].values[0]
    if intent == 'what is X today?':
        X = query['X']
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for today
        if 'AM' in df.columns[1]: 
            return 'Morning: ' + row[df.columns[1]].values[0] + ', Afternoon: ' + row[df.columns[2]].values[0] + ', Night: ' + row[df.columns[3]].values[0]
        if 'PM' in df.columns[1]: 
            return 'Afternoon: ' + row[df.columns[1]].values[0] + ', Night: ' + row[df.columns[2]].values[0]
        if 'Night' in df.columns[1]:
            return 'Night: ' + row[df.columns[1]].values[0]
    if intent == 'what is X tomorrow?':
        X = query['X']
        # find the row in df['Metric'] that matches X
        row = df.loc[df['Metric'] == X]
        # find the values for tomorrow
        if 'AM' in df.columns[1]: 
            return 'Morning: ' + row[df.columns[4]].values[0] + ', Afternoon: ' + row[df.columns[5]].values[0] + ', Night: ' + row[df.columns[6]].values[0]
        if 'PM' in df.columns[1]: 
            return 'Morning: ' + row[df.columns[3]].values[0] + ', Afternoon: ' + row[df.columns[4]].values[0] + ', Night: ' + row[df.columns[5]].values[0]
        if 'Night' in df.columns[1]:
            return 'Morning: ' + row[df.columns[2]].values[0] + ', Afternoon: ' + row[df.columns[3]].values[0] + ', Night: ' + row[df.columns[4]].values[0]

 