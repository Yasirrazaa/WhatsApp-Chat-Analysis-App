import pandas as pd
from urlextract import URLExtract
import streamlit as st
from matplotlib.pyplot import matplotlib as plt
from wordcloud import WordCloud
import emoji
from collections import Counter


def group_stats(option,df):
        total_messages=df.shape[0]
        media=df[df['message']=="<Media omitted>\n"].shape[0]
        words=[]
        extract=URLExtract()
        links=[]
        for message in df['message']:
            words.extend(message.split())
        for message in df['message']:
            links.extend(extract.find_urls(message))    
        return total_messages,media,len(words),len(links)



def stats(option,df):
        user_df=df[df['user']==option]
        total_messages=user_df.shape[0]
        media=user_df[user_df['message']=="<Media omitted>\n"].shape[0]
        words=[]
        extract=URLExtract()
        links=[]
        for message in user_df['message']:
            words.extend(message.split())
        for message in user_df['message']:
            links.extend(extract.find_urls(message))
        return total_messages,media,len(words),len(links)
        

def display(option,df):
    user_df=df[df['user']==option]
    if option=="OverAll":
        st.header("Over All")
        st.dataframe(df)

    else:
        st.header(option)
        st.dataframe(df[df['user']==option])
        
def monthly(option,df):
    if option != "OverAll":
        df=df[df['user']==option]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+" "+"-"+" "+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily(option,df):
    if option != "OverAll":
        df=df[df['user']==option]
    timeline=df.groupby(['dateonly']).count()['message'].reset_index()
    return timeline


def hourly(option,df):
    if option != "OverAll":
        df=df[df['user']==option]
    timeline=df.groupby(['hour']).count()['message'].reset_index()
    return timeline

def most_active_plot(df):
    x=df['user'].value_counts().head()
    
    return x
def most_active_df(df):
    d=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'user','user':'percent'})
    return d
    
def wordcloud(option,df):
    if option != "OverAll":
        df=df[df['user']==option]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    wc_df=wc.generate(df['message'].str.cat(sep=" "))
    return wc_df
def most_used_words(option,df):
    temp_df=df[df['user']!="group_notification"]
    temp_df=temp_df[temp_df['message']!="<Media omitted>\n"]
    if option != "OverAll":
        temp_df=temp_df[temp_df['user']==option]
    f=open('stopwords.txt','r')
    stopwords=f.read()
    words=[]
    for message in temp_df['message']:
        for word in message.split():
            if word not in stopwords:
                words.append(word)
    
    dat=Counter(words).most_common()
    return pd.DataFrame(dat,columns=['word','count'])

def most_used_wordcloud(option,df):
    temp_df=df[df['user']!="group_notification"]
    temp_df=temp_df[temp_df['message']!="<Media omitted>\n"]
    if option != "OverAll":
        temp_df=temp_df[temp_df['user']==option]
    f=open('stopwords.txt','r')
    stopwords=f.read()
    words=[]
    for message in temp_df['message']:
        for word in message.split():
            if word not in stopwords:
                words.append(word)
    
    dat=Counter(words).most_common()
    dat=dict(dat)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    wc_df=wc.generate_from_frequencies(dat)
    return wc_df

# Emojis
def emojis(option,df):
    if option != "OverAll":
        df=df[df['user']==option]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0:'emoji',1:'count'})
    return emoji_df