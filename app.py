import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp chat analyzer")
#code to upload file in sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    #to read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #to convert it into string
    data=bytes_data.decode("utf-8")
    #to preprocess data in the form of dataframe
    df=preprocessor.preprocess(data)


    #fetch unique user
    user_list= df['user'].unique().tolist()

    #arrange in ascending order and remove grp notifi
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user= st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        #Stats Area
        st.title("Top Statistics")

        num_messages, words, num_media_messages, link = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("<p style='margin-bottom:0; font-size:24px;'>Total Messages</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top:0; font-size:24px; font-weight:bold;'>{num_messages}</p>",
                        unsafe_allow_html=True)

        with col2:
            st.markdown("<p style='margin-bottom:0; font-size:24px;'>Total Words</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top:0; font-size:24px; font-weight:bold;'>{words}</p>",
                        unsafe_allow_html=True)

        with col3:
            st.markdown("<p style='margin-bottom:0; font-size:24px;'>Media Shared</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top:0; font-size:24px; font-weight:bold;'>{num_media_messages}</p>",
                        unsafe_allow_html=True)

        with col4:
            st.markdown("<p style='margin-bottom:0; font-size:24px;'>Links Shared</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top:0; font-size:24px; font-weight:bold;'>{link}</p>",
                        unsafe_allow_html=True)

        #timline
        #monthly
        st.title("Monthly Timeline")
        timeline= helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1,col2= st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity(selected_user, df)
            fig,ax= plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #most active user(group level)
        if selected_user== 'Overall':
            st.title('Most Active Users')
            x,new_df= helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Frequently Used Words")
        most_common_df=helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       #emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user,df)

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
            with col2:
                fig,ax=plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

                st.pyplot(fig)