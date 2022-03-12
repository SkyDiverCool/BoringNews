# thingy to read boring news faster

from logging import Handler
import feedparser
from newspaper import Article
from jinja2 import Environment, FileSystemLoader
from github import Github
from summarizer import Summarizer

feed = feedparser.parse("https://finance.yahoo.com/rss/") #If this works, you didn't even try

model = Summarizer(model="distilbert-base-uncased")

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')
templateminimal = env.get_template('templateminimal.html')

g = Github("github_token")

articlesarray = []

for entry in feed.entries:
    try:
        print("==Parsing new article==")
        articlelink = entry.link
        article = Article(articlelink, browser_user_agent="Mozilla/5.0")
        article.download()
        article.parse()
        result = model(article.text, num_sentences=3)
        print(result)
        articlesarray.append(result)
        print("Parsed article")
    except Exception as e:
        print(e)

print("Got articles")

output_from_parsed_template = template.render(articles = articlesarray)
output_from_parsed_minimaltemplate = templateminimal.render(articles = articlesarray)

file = open("articles.html", "w")
file.write(output_from_parsed_template)
file.close()

file = open("articlesminimal.html", "w")
file.write(output_from_parsed_minimaltemplate)
file.close()

repo = g.get_repo("github_username/github_repo")
contents = repo.get_contents("index.html")
repo.update_file(contents.path, "Automated Commit", output_from_parsed_template, contents.sha)

repo = g.get_repo("github_username/github_repo")
contents = repo.get_contents("minimal.html")
repo.update_file(contents.path, "Automated Commit", output_from_parsed_minimaltemplate, contents.sha)