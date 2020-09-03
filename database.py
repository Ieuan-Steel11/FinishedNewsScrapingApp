from scraping import TechTweets, TechArticles
import sqlite3


tech_tweets = TechTweets(Random=False)
tech_articles = TechArticles(Random=False)
# creates instance of classes to have access to articles and tweets


def createTweetsTable():
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 2/Scraped_Data_DB.db")
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor
    create_table_query = (
        """ 
            CREATE TABLE IF NOT EXISTS Tweets (
            screen_name TEXT,
            user_url TEXT,
            content TEXT,
            tweet TEXT
            );
        """
    )

    cursor.execute(create_table_query)
    # creates a table with all the data as columns
    scraped_data_db.commit()
    # confirms the creation of the table
    scraped_data_db.close()


def insertTweetsInTable():
    if not tech_tweets.err:
        # if there isn't an api problem
        scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
        cursor = scraped_data_db.cursor()
        # connects to the database and creates a cursor

        for tweet in tech_tweets.tweets:
            _tweet_data = tech_tweets.getDBTweet(tweet)
            insert_values_query = (
                """ 
                    INSERT INTO Tweets (screen_name, user_url, content)
                    VALUES (?, ?, ?);
                """
            )

            cursor.execute(insert_values_query, _tweet_data)
            # gives all the columns rows which are the values of the tweet
            scraped_data_db.commit()
            # makes the changes permanent
        scraped_data_db.close()


def getSearchedTweets(search_query):
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor

    tweets = cursor.execute("SELECT * FROM Tweets WHERE content LIKE ? ", [search_query]).fetchmany(50)
    tweets = list(dict.fromkeys(tweets))
    # remove duplicates
    scraped_data_db.close()
    return tweets


def getGeneratedTweet():
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor

    generated_tweet = cursor.execute("SELECT * FROM Tweets").fetchone()
    scraped_data_db.close()
    return generated_tweet


def createArticlesTable():
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor
    create_table_query = ("""
                            CREATE TABLE IF NOT EXISTS Articles (
                            title TEXT,
                            author TEXT,
                            description TEXT,
                            date TEXT,
                            news_source TEXT,
                            link TEXT,
                            article TEXT
                            );
                          """)
    # query that creates a table for an article
    cursor.execute(create_table_query)
    # creates table
    scraped_data_db.commit()
    # confirms table creation
    scraped_data_db.close()


def insertArticlesInTable():
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor
    for article in tech_articles.article_collection:
        _article_data = (article[0], article[1], article[2], article[3], article[4], article[5])
        insert_values_query = ("""
                                INSERT INTO Articles (title, author, description, date, news_source, link)
                                VALUES (?, ?, ?, ?, ?, ?);
                                """)
        # the query adds all values to the table

        cursor.execute(insert_values_query, _article_data)
        # adds the values to the database

        scraped_data_db.commit()
    # confirms all changes
    scraped_data_db.close()


def getSearchedArticles(search_query):
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor
    articles = cursor.execute("SELECT * FROM Articles WHERE description LIKE ?", [search_query]).fetchmany(200)
    articles = list(dict.fromkeys(articles))
    # remove duplicates
    scraped_data_db.close()
    return articles


def getGeneratedArticle():
    scraped_data_db = sqlite3.connect(r"/media/manieu-11/Drive 1/Scraped_Data_DB.db", check_same_thread=False)
    cursor = scraped_data_db.cursor()
    # connects to the database and creates a cursor
    generated_article = cursor.execute("SELECT * FROM Articles").fetchone()
    scraped_data_db.close()
    return generated_article


def createDB():
    insertTweetsInTable()
    insertArticlesInTable()
