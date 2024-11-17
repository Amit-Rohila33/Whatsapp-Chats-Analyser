import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# Group name input
group_name = st.sidebar.text_input("Enter the group name")

# Group type dropdown with custom input for "Other"
group_type_options = ["Friends", "Family", "Work", "Study", "Other"]
group_type = st.sidebar.selectbox("Select the group type", group_type_options)

if group_type == "Other":
    group_type = st.sidebar.text_input("Please specify the group type")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Add your OpenAI API key here
    api_key = process.env.OPENAI

    # Preprocess data using the modified preprocessor
    df = preprocessor.preprocess(data, api_key)

    # Remove group notification messages
    df = df[df['user'] != 'group_notification']

    # Show the DataFrame with forwarded/original message type
    st.dataframe(df[['only_date', 'user', 'day_name', 'message', 'message_type', 'period']])

    # Sidebar for user selection
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title(f"Top Statistics for {group_name} - {group_type}")
        st.markdown(f"**Total Messages:** {num_messages}")
        st.markdown(f"**Total Words:** {words}")
        st.markdown(f"**Media Shared:** {num_media_messages}")
        st.markdown(f"**Links Shared:** {num_links}")
        st.markdown(f"**Forwarded Messages:** {len(df[df['message_type'] == 'forwarded'])}")
        st.markdown(f"**Original Messages:** {len(df[df['message_type'] == 'original'])}")

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)
