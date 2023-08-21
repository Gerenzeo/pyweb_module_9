from pathlib import Path
from datetime import datetime
import json

from models import Author, Quote
from seeds.connection import connection_to_mongo


def read_data(filename: str) -> list:
    try:
        with open(Path(__file__).parent.parent.joinpath(filename), 'r') as fh:
            return json.load(fh)
    except FileNotFoundError as e:
        print(e)
    return []



if __name__ == '__main__':
    connection_to_mongo()

    authors_file = "data/authors.json"
    quotes_file = "data/quotes.json"

    for author in read_data(authors_file):
        record = Author(
            fullname=author.get('fullname'),
            # born_date=,
            born_date=datetime.strptime(author.get('born_date'), "%B %d, %Y").date(),
            born_location=author.get('born_location'),
            description=author.get('description')
        ).save()

    for quote in read_data(quotes_file):
        author_name = quote.get('author')
        author = Author.objects(fullname=author_name).first()
        if author:
            record = Quote(
                tags=quote.get('tags'),
                author=author,
                quote=quote.get('quote')
            ).save()




