import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[ap]m\s-\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    dates = [sub.replace('\u202f', ' ') for sub in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message data_type
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message, maxsplit=1)  # Use maxsplit=1 to split only at the first occurrence
        if len(entry) >= 3:  # Check if there are at least three parts (before username, username, and message)
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period



    return df
