import re
import pandas as pd
import datetime


def preprocess_data(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s[ap]m\s-\s(.+?):\s(.+)'
    matches = re.findall(pattern, data)

    combined_messages = []
    combined_dates = []

    for match in matches:
        date = match[0]
        time = match[1]
        sender = match[2]
        message = match[3]

        combined_message = f"{sender}: {message}"
        date_obj = datetime.datetime.strptime(date, "%d/%m/%y")
        time_obj = datetime.datetime.strptime(time, "%I:%M")
        converted_time_str = time_obj.strftime("%H:%M")
        combined_date = f"{date}, {converted_time_str} - "

        combined_messages.append(combined_message)
        combined_dates.append(combined_date)

    df = pd.DataFrame({'user_message': combined_messages, 'message_date': combined_dates})
    df.message_date = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    df = pd.DataFrame({'user_message': combined_messages, 'message_date': combined_dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df.user_message:
        user, message = message.split(': ', 1)
        users.append(user)
        messages.append(message)

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

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
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

