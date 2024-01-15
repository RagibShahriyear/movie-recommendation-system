# data_url = https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?resource=download

# imports
import pandas as pd
import ast

# loading data
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# merging DataFrames
movies = movies.merge(credits, on="title")

# Feature selection
movies = movies[
    [
        "title",
        "genres",
        "keywords",
        "overview",
        "movie_id",
        "cast",
        "crew",
    ]
]

# Checking for missing data
movies.isnull().sum()

# checking which movie's features are missing
null_data = movies[movies.isnull().any(axis=1)]

# dropping the movies with missing features
movies.dropna(inplace=True)

# check if there are any duplicates
movies.duplicated().sum()


# data preprocessing

movies.iloc[0].genres


def my_convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L


movies["genres"] = movies["genres"].apply(my_convert)
movies["keywords"] = movies["keywords"].apply(my_convert)


def my_casts(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L


movies["cast"] = movies["cast"].apply(my_casts)

# movies.iloc[0].crew


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L


movies["crew"] = movies["crew"].apply(fetch_director)

# Turning the 'overview' into a list

movies["overview"] = movies["overview"].apply(lambda x: x.split())


# removing spaces from genres, keywords, crew, and cast columns
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" ", "") for i in x])

# creating one single column with everything
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

movies.head(5)

# new dataframe with tags
new_df = movies[["title", "movie_id", "tags"]]


new_df["tags"][0]

# converting the tags(list) into string
# new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))

new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())


# stemming
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)


new_df["tags"] = new_df["tags"].apply(stem)

# vectorization
# technique used = 'bag of words'

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(new_df["tags"]).toarray()

cv.get_feature_names_out()
