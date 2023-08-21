from entities.Scrapper import QuotersScrapper, AuthorsScrapper
from seeds.connection import connection_to_mongo
from seeds.models import Author, Quote

def get_all_quotes_by_name(value):
    author = Author.objects(fullname=value).first()
    if author:
        authors_quotes = Quote.objects(author=author)

        for index, quote in enumerate(authors_quotes):
            print(f"{index + 1} - {quote.quote}")
    else:
        print(f'Author with name "{value}" is not exist!')
    print('\n')

def get_all_quotes_by_tagname(value):
    all_quotes = Quote.objects.all()
    index = 0
    for quote in all_quotes:
        if value in quote.tags:
            index += 1
            print(f"{index} - {quote.quote}")
    print('\n')

def get_all_quotes_by_tagnames(value):
    all_quotes = Quote.objects.all()

    for tag in value.split(','):
        for quote in all_quotes:
            if tag in quote.tags:
                print(quote.quote)

def main():
    url = 'http://quotes.toscrape.com'

    get_quotes = QuotersScrapper(url)
    authors_urls = get_quotes.grab_data()
    get_quotes.save()

    get_author = AuthorsScrapper(url)
    get_author.grab_data(authors_urls)
    get_author.save()

    # print(get_quotes.quotes)
    # print(get_author.authors)

    connection_to_mongo()

    while True:
        user = input('Enter command [press "quit" for exit]: ')

        if user == 'exit':
            break

        try:
            command, value = user.split(':')


            if command == 'name':
                get_all_quotes_by_name(value)
            elif command == 'tag':
                get_all_quotes_by_tagname(value)
            elif command == 'tags':
                get_all_quotes_by_tagnames(value)

        except (ValueError, NameError) as e:
            print("Template: <command>:<value>")

if __name__ == '__main__':
    main()