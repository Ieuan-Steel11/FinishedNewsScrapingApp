from random import choice
from newsapi import NewsApiClient
import tweepy

newsapi = NewsApiClient(api_key='SECRET')


class TechArticles:

    def __init__(self, Random):
        self.response_from_news_api = newsapi.get_everything(language='en', sources="""
                                                                               bbc-news, the-verge, abc-news, 
                                                                               al-jazeera-english, associated-press, 
                                                                               independent, the-guardian, 
                                                                               bleacher-report, bloomberg, cnn, c
                                                                               bs-news,
                                                                               cbc-news, buzzfeed, espn, google-news, 
                                                                               google-news-uk, ign, msnbc, nbc-news, 
                                                                               news24, new_scientist, newsweek, polygon,
                                                                               reuters, rte, techcrunch, techradar,
                                                                               financial-times, ars-technica, bbc-sport,
                                                                               business-insider, business-insider-uk,
                                                                               fox-news 
                                                                                """
                                                        )
        # gets the articles
        self.article_collection = [Article for Article in self.response_from_news_api["articles"]]
        # creates a list of articles using a list comprehension
        self.article_collection = [self._getArticleData(Article) for Article in self.article_collection]
        # sets it up so that the stored articles only have the data we want
        self.random = Random
        # if the user wants a random article default parameter so the user can choose
        if self.random:
            self.generated_article = choice(self.article_collection)
            # gets a random article each time class object is created
        elif not self.random:
            self.generated_article = self.article_collection[0]
            # gets first article

    @staticmethod
    def _getArticleData(article):
        title = article.get("title")
        author = article.get("author", "N/A")
        description = article.get("description")
        date = article.get("publishedAt", "N/A")[0:10]
        news_source = article.get("source").get("id", "N/A")
        link = article.get("url")
        image_link = article.get("urlToImage")
        content = article.get("content")
        # gets all the information about the article

        return [title, author, description, date, news_source, link, image_link, content]

    @staticmethod
    def getArticleTitle(article):
        return article[0]

    @staticmethod
    def getArticleAuthor(article):
        return article[1]

    @staticmethod
    def getArticleDescription(article):
        return article[2].lower()

    @staticmethod
    def getArticleDate(article):
        return article[3]
        # date sliced so it only returns the date and not time

    @staticmethod
    def getArticleSource(article):
        return article[4]

    @staticmethod
    def getArticleUrl(article):
        return article[5]

    @staticmethod
    def getArticleImageLink(article):
        return article[6]

    @staticmethod
    def getArticleContent(article):
        return article[6]

    @staticmethod
    def getArticleKeyWords(article):
        return article[-1]

    def getArticle(self, article):
        title = self.getArticleTitle(article)
        author = self.getArticleAuthor(article)
        description = self.getArticleDescription(article)
        date = self.getArticleDate(article)
        news_source = self.getArticleSource(article)
        link = self.getArticleUrl(article)
        image_link = self.getArticleImageLink(article)
        content = self.getArticleContent(article)
        # gets all the information about the article

        return [title, author, description, date, news_source, link, image_link, content]


class TechTweets:
    twitter_search_query = "news -filter:retweets"
    # search query for twitter

    consumer_api_key = "SECRET"
    consumer_secret_api_key = "SECRET"
    # twitter developer api keys

    auth = tweepy.OAuthHandler(consumer_api_key, consumer_secret_api_key)
    # authorises program to use api with twitter

    API = tweepy.API(auth)

    # starts api using auth to authenticate the api keys

    def __init__(self, Random):
        self.err = tweepy.error.TweepError

        self.random = Random
        # boolean to decide whether a tweet is random
        self.tweets = tweepy.Cursor(self.API.search, q=self.twitter_search_query, tweet_mode='extended').items(325)
        # scrapes all tweets using a search query
        self.tweets = [tweet._json for tweet in self.tweets]
        # stores all the tweets in a list
        # have to access a protected member variable _json which is the raw json data
        # because the normal parsing doesn't work when instantiating the api
        # and the status object normally returned isn't subscriptable or iterable
        self.tweets = [self.getTweetJSONData(tweet) for tweet in self.tweets]
        # the storage of tweets only has the data we want
        if self.random:
            self.generated_tweet = choice(self.tweets)
            # gets a random tweet
        elif not self.random:
            self.generated_tweet = self.tweets[0]
            # gets first tweet that comes up
        else:
            pass

    def getAllTweets(self):
        return self.tweets

    @staticmethod
    def getTweetJSONData(tweet):
        # tweet gotten from original json response
        ID = tweet.get("id_str")
        screen_name = tweet.get("user").get("screen_name")
        content = tweet.get("full_text")
        date = tweet.get("created_at", "N/A")[0:9] + " " + tweet.get("created_at")[-4:]
        # have to slice it to get the date as day, date, month, year

        user_url = tweet.get("user").get("url")
        user_id = tweet.get("user").get("id_str")
        is_quote = tweet.get("is_quote_status")
        number_of_favourites = tweet.get("favourite_count")
        number_of_retweets = tweet.get("retweet_count")
        number_of_quotes = tweet.get("quote_count")

        return [ID, screen_name, user_url, user_id, content, date,
                is_quote, number_of_favourites, number_of_retweets, number_of_quotes]

        # gets article info

    def getDBTweet(self, tweet):
        # tweet gotten from list in memory
        screen_name = self.getTweeterScreenName(tweet)
        user_url = self.getTweeterUrl(tweet)
        content = self.getTweetContent(tweet)

        return screen_name, user_url, content,

    @staticmethod
    def getDisplayTweet(tweet):
        # tweet gotten from the database
        screen_name = tweet[0]
        user_url = tweet[1]
        content = tweet[2]

        return screen_name, user_url, content

    @staticmethod
    def getTweetID(tweet):
        return tweet[0]

    @staticmethod
    def getTweeterScreenName(tweet):
        return tweet[1]

    @staticmethod
    def getTweeterUrl(tweet):
        return tweet[2]

    @staticmethod
    def getTweeterID(tweet):
        return tweet[3]

    @staticmethod
    def getTweetContent(tweet):
        return tweet[4]

    @staticmethod
    def getTweetDate(tweet):
        return tweet[5]

    @staticmethod
    def getIsQuote(tweet):
        return tweet[6]

    @staticmethod
    def getNumberOfFavourites(tweet):
        return tweet[7]

    @staticmethod
    def getNumberOfRetweets(tweet):
        return tweet[8]

    @staticmethod
    def getNumberOfQuotes(tweet):
        return tweet[9]
