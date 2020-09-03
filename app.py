import flask_bootstrap as bt
import flask_compress as cmp
from flask import Flask, render_template, redirect, url_for, request
from database import (createDB, getSearchedArticles, getSearchedTweets,
                      getGeneratedTweet, getGeneratedArticle, tech_tweets, tech_articles)

app = Flask(__name__)
cmp.Compress(app)
app.secret_key = b"/[fds]se3dljS,:@ghQi)czl'`lh#'>uh<@jt6}7ifd5^&O9R]FDt?yK^|&i;dU78gk*o"
bt.Bootstrap(app)


@app.route("/")
def start():
    return redirect(url_for("index"))
    # if it isn't already on index it loads onto index page


@app.route("/index", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if request.get("new_article") == "Generate new Article":
            # if generate new article button is pressed
            return redirect(url_for("index"))
            # reloads page because it each time it happens a random article is chosen
        if request.get("new_tweet") == "Generate New Tweet":
            return redirect(url_for("index"))
            # reloads the page because each time a new page is loaded a new tweet is loaded anyway

    return render_template("index.html",
                           title=getGeneratedArticle()[0],
                           author=getGeneratedArticle()[1],
                           description=getGeneratedArticle()[2],
                           date=getGeneratedArticle()[3],
                           news_source=getGeneratedArticle()[4],
                           link=getGeneratedArticle()[5],
                           user=getGeneratedTweet()[0],
                           text=getGeneratedTweet()[2],
                           url=getGeneratedTweet()[1],
                           )
    # renders the html with variables used with auto escaping defined within the parameters
    # use list indexing because values're returned as a list instead of tuple


@app.route("/search", methods=["POST", "GET"])
def search():
    global search_query
    # search query can be used for getting search results in search results page
    # because it can only be gotten from the search page
    if request.method == "POST":
        search_query = request.form["search"]
        if search_query:
            search_query = "%" + search_query + "%"
            # cleans search query for sqlite
            if "--" not in search_query and "'" not in search_query and "OR" not in search_query:
                # if they try sql injection with -- to comment and ' to end access main query
                return redirect(url_for("search_results", query=search_query))
            else:
                redirect(url_for("search"))
                # if sql injection is attempted
        else:
            # if there isn't a search query
            redirect(url_for("search"))
    return render_template("search.html")


@app.route("/search_results?query=<query>")
def search_results(query):
    scraped_tweets = getSearchedTweets(query)
    scraped_articles = getSearchedArticles(query)
    return render_template("search_results.html", tech_tweets=tech_tweets, tech_articles=tech_articles,
                           scraped_tweets=scraped_tweets, scraped_articles=scraped_articles)


if __name__ == "__main__":
    app.run()