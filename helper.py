#this file will contain all the required functions

from urlextract import URLExtract  #for extracting links
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract= URLExtract() #obj

def fetch_stats(selected_user, df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    #1:fetching number of messages
    num_messages = df.shape[0]

    #2: fetching number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #3: fetching number of media mesages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4: fetching number of links shared
    link=[]
    for message in df['message']:
        link.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(link)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})

    return x,df

def create_wordcloud(selected_user,df):
    f = open('.idea/stop_hinglish.txt', 'r')  # for removing hinglish stop words
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification'] #remove grp_notif msg
    temp = temp[temp['message'] != '<Media omitted>\n'] #remove media omitted msg

    def remove_stop_words(message):    #remove hinglish stop words
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    f = open('.idea/stop_hinglish.txt', 'r') #for removing hinglish stop words
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df= pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    daily_timeline= df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap