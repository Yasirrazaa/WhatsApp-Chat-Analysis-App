import regex as re
import pandas as pd

def preprocess(data):
    try:
        pattern='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'
        messages=re.split(pattern,data)[1:]
        dates=re.findall(pattern,data)
        df=pd.DataFrame({'user_message':messages,'date':dates})
        df['date']=pd.to_datetime(df['date'],format='%m/%d/%y, %H:%M - ')
    except:
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        messages=re.split(pattern,data)[1:]
        dates=re.findall(pattern,data)
        df=pd.DataFrame({'user_message':messages,'date':dates})
        df['date']=pd.to_datetime(df['date'],format='%d/%m/%Y, %H:%M - ')


    users=[]
    messages=[]
    for message in df['user_message']:
        text=re.split('([\w\W]+?):\s',message)
        if text[1:]:
            users.append(text[1])
            messages.append(text[2])
        else:
            users.append("group notification")
            messages.append(text[0])
    df['user']=users
    df['message']=messages
    del df['user_message']
    df['day_name']=df['date'].dt.day_name()
    df['dateonly']=df['date'].dt.date
    df['year']=df['date'].dt.year
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    return df

        