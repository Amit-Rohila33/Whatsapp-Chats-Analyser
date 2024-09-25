import re
import pandas as pd
import helper
from faker import Faker

# Initialize Faker instance for generating fake names
fake = Faker()

# Dictionary to store real-to-fake name mappings
user_mapping = {}

def preprocess(data, api_key):
    pattern = '\\d{1,2}/\\d{1,2}/\\d{2,4},\\s\\d{1,2}:\\d{2}\\s[APap][Mm]\\s-\\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    message_type = []

    for message in df['user_message']:
        entry = re.split('([\\w\\W]+?):\\s', message)
        if entry[1:]:
            user = entry[1]
            if user not in user_mapping:
                user_mapping[user] = fake.name()
            users.append(user_mapping[user])
            
            msg = entry[2]
            messages.append(msg)

            # Identify whether message is forwarded or original
            msg_type = helper.identify_message_type(api_key, msg)
            message_type.append(msg_type)
        else:
            users.append('group_notification')
            messages.append(entry[0])
            message_type.append('group_notification')

    df['user'] = users
    df['message'] = messages
    df['message_type'] = message_type  # New column for forwarded/original status

    # Add other preprocessing steps
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"11 PM - 12 AM")
        elif hour == 0:
            period.append(f"12 AM - 1 AM")
        elif hour == 11:
            period.append(f"11 AM - 12 PM")
        elif hour == 12:
            period.append(f"12 PM - 1 PM")
        elif hour < 12:
            period.append(f"{hour} AM - {hour + 1} AM")
        else:
            period.append(f"{hour - 12} PM - {hour - 11} PM")

    df['period'] = period

    return df

