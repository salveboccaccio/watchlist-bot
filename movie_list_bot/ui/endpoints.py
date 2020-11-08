"""
Endpoints and related functions this bot supports.
"""

from uuid import uuid4

# third-party
from imdb import IMDb

from telegram import InlineQueryResultArticle, InputTextMessageContent

# local
from . import emoji


IA = IMDb()


def _search_imdb(title: str, limit: int = 5):
    counter = 0
    for result in IA.search_movie(title):
        print("Found movie: {}".format(result["title"]))
        try:
            title = result["title"]
            thumb_url = result["cover url"]
            desc = result["year"]
        except KeyError:
            continue

        yield InlineQueryResultArticle(
            id=uuid4(),
            title=title,
            thumb_url=thumb_url,
            description=desc,
            input_message_content=InputTextMessageContent(result.getID()),
        )

        counter += 1
        if counter > limit:
            break


def create_message(movie_id: str):
    """ Displays a movie, given an IMDB movie ID """
    movie = IA.get_movie(movie_id, info=["main"])

    return "\n".join([
        f"{emoji.MOVIE} {movie['title']}",
        "",
        f"Year: {movie['year']}",
        "Genres:" + ", ".join(movie['genres']),
        "",
        "Plot",
        movie["plot outline"],
        "",
        f"Rating: {movie['rating']} / 10.0",
        "",
        # TODO - can this be formatted as markdown?
        # f"[thumbnail]\\({movie['cover url']}\\)",
        movie["cover url"],
    ])


def inline_search(update, context):
    """ Search trakt for a movie """
    # chat_id = update.message.chat_id

    query = update.inline_query.query

    print("dbg:")
    print(query)

    update.inline_query.answer(
        list(_search_imdb(query))
    )