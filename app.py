import streamlit as st
import preprocessor
import assist
import matplotlib.pyplot as plt
plt.style.use('ggplot')

st.set_page_config(
    page_title="Whatsapp Chat Analyzer",
    page_icon=":whatsapp:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded=st.sidebar.file_uploader("choose a file")
if uploaded is not None:
    byte=uploaded.getvalue()
    data=byte.decode('utf-8')
    df=preprocessor.preprocess(data)
    
    
    ulist=df['user'].unique().tolist()
    if "group notification" in ulist:
        ulist.remove("group notification")
    ulist.sort(reverse=True)
    ulist.insert(0,"OverAll")
    option=st.sidebar.selectbox("Select User",ulist)

# Button
    if st.sidebar.button("Analyze"):
        if option=="OverAll":
            messages,media,words,links=assist.group_stats(option,df)
        else:
            messages,media,words,links=assist.stats(option,df)

        
        cl1,cl2,cl3,cl4=st.columns(4)
        with cl1:
            st.header("Total")
            st.write(messages)
        with cl2:
            st.header("Media")
            st.write(media)
        with cl3:
            st.header("Links")
            st.write(links)
        with cl4:
            st.header("Words")
            st.write(words)
        # DataFrame
        assist.display(option,df)
        #monthly timeline
        st.header("Monthly Timeline")
        timeline=assist.monthly(option,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
         #daily timeline
        st.header("Daily Timeline")
        d_timeline=assist.daily(option,df)
        fig,ax=plt.subplots()
        ax.plot(d_timeline['dateonly'],d_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #hourly timeline
        st.header("Hourly Timeline")
        d_timeline=assist.hourly(option,df)
        fig,ax=plt.subplots()
        ax.plot(d_timeline['hour'],d_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       #Most Active Users
        if option=="OverAll":
            st.header("Most Active Users")
            col1,col2=st.columns(2)
            with col1:
                x=assist.most_active_plot(df)
                name=x.index
                value=x.values
                fig,ax=plt.subplots()
                ax.bar(name,value)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                 most_active_df=assist.most_active_df(df)
                 st.dataframe(most_active_df)
        # WordCloud
        st.header("WordCloud")
        wc_df=assist.wordcloud(option,df)
        fig,ax=plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)
        #Most used words
        st.header("Most Used Words")
        col1,col2=st.columns(2)
        with col1:
            df_=assist.most_used_words(option,df)
            st.dataframe(df_)
        with col2:
            df_=df_.head(20)
            fig,ax=plt.subplots()
            ax.bar(df_['word'],df_['count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        wc_df=assist.most_used_wordcloud(option,df)
        fig,ax=plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        #Emojis
        st.header("Emojis")
        col1,col2=st.columns(2)
        with col1:
            d_f=assist.emojis(option,df)
            st.dataframe(d_f)
        with col2:
            dt=assist.emojis(option,df).head(20)
            fig,ax=plt.subplots()
            ax.bar(dt['emoji'],dt['count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)