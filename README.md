
# WhatsApp Chat Analysis Application

## Introduction
This WhatsApp Chat Analysis Application processes and analyzes WhatsApp chat data, offering insights through an interactive web-based interface. The primary goal is to help users understand their communication patterns and trends, whether for personal curiosity, academic research, or enhancing group dynamics. Users can upload their exported WhatsApp chat history and immediately start analyzing the data without needing technical expertise.

## Objectives
- **User-Friendly Analysis**: Intuitive interface for non-technical users.
- **Interactive Visualization**: Engaging web experience with graphs, charts, and word clouds.
- **Comprehensive Insights**: Detailed analysis of communication patterns and trends.
- **Data-Driven Decisions**: Empowering users with data-backed insights.
- **Advanced Text Analytics**: Includes sentiment analysis and topic modeling.
- **Customization and Filtering****: Focus on specific time periods, participants, or keywords.
- **Real-Time Processing**: Immediate feedback and results.
- **Privacy and Security**: Data processed locally, ensuring privacy.
- **Educational and Research Applications**: Useful for academic analysis.

## Features
### Data Analysis
- **Group or Individual Stats**: Number of messages, links, media, and words.
- **Activity Tracking**: Monthly, daily, and hourly activity visualization.
- **User and Content Insights**: Most active users, most used words (word cloud), and most used emojis.

### Web Interface
- **Interactive GUI**: Developed with Streamlit for ease of use.
- **File Upload**: Simple upload process for WhatsApp chat export files.
- **Data Visualization**: Various interactive visualizations like bar charts, line graphs, and word clouds.

### Database and Database Operations
- **Database Choice**: Supports SQLite or MySQL.
- **Database Connectivity**: Managed with SQLAlchemy.
- **Data Ingestion**: Reads and processes WhatsApp chat export files.
- **Data Storage**: Stores parsed data in the database.
- **Data Analysis and Retrieval**: Efficient querying and analysis of stored data.

## Code Overview
- **`app.py`**: Main script to initialize and run the Streamlit application.
    ```python
    import streamlit as st
    from assist import process_chat
    from database_ops import setup_db

    def main():
        st.title('WhatsApp Chat Analysis')
        uploaded_file = st.file_uploader('Upload your chat file', type=['txt'])
        if uploaded_file:
            chat_data = process_chat(uploaded_file)
            setup_db(chat_data)
            st.write('Analysis complete!')

    if __name__ == "__main__":
        main()
    ```
- **`assist.py`**: Helper functions for data processing and analysis.
    ```python
    import pandas as pd

    def process_chat(file):
        # Logic to process chat file
        chat_data = pd.read_csv(file)
        return chat_data
    ```
- **`database_ops.py`**: Handles database operations using SQLAlchemy.
    ```python
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    Base = declarative_base()

    class Message(Base):
        __tablename__ = 'messages'
        id = Column(Integer, primary_key=True)
        user = Column(String)
        message = Column(String)

    def setup_db(chat_data):
        engine = create_engine('sqlite:///chats.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for _, row in chat_data.iterrows():
            message = Message(user=row['user'], message=row['message'])
            session.add(message)
        session.commit()
    ```

## Technologies
- **Programming Language**: Python
- **Libraries and Frameworks**:
  - Streamlit: For creating the interactive web application.
  - Pandas: For data manipulation and analysis.
  - SQLAlchemy: ORM for database operations.
  - MySQL Connector: For connecting to MySQL databases.
  - Wordcloud: For generating word cloud visualizations.
  - Emoji: For handling and analyzing emoji usage.
  - Matplotlib/Seaborn: For creating visualizations.

## Instructions to Run the Application Locally

### Prerequisites
1. **Python 3.7+**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **Virtual Environment** (optional but recommended): Create a virtual environment to manage dependencies.

### Installation Steps
1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd whatsapp-chat-analysis
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    streamlit run app.py
    ```

### Configuration
- **Database Configuration**: Modify `database_ops.py` to switch between SQLite and MySQL as needed.
    ```python
    # For SQLite (default)
    engine = create_engine('sqlite:///chats.db')

    # For MySQL
    # engine = create_engine('mysql+mysqlconnector://user:password@host/dbname')
    ```

## Future Enhancements
- **Advanced Analysis**: Adding sentiment analysis and topic modeling.
- **Support for Additional Platforms**: Extending support to Telegram, Facebook Messenger, and Slack.
- **Enhanced Visualizations**: Incorporating more advanced visualization techniques.
- **User Customization**: Allowing users to customize analysis parameters and visualizations.

## Conclusion
The WhatsApp Chat Analysis Application provides a robust tool for analyzing chat data, offering user-friendly, interactive, and comprehensive insights. With an emphasis on privacy and advanced features, it is ideal for both personal and academic use.
