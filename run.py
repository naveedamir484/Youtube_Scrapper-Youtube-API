from src.main import Scrapper
import argparse


parser = argparse.ArgumentParser(description='Youtube Scrapping Bot')
subparser = parser.add_subparsers(dest="mode")

search = subparser.add_parser("search", help="searching using keyword")
search.add_argument('-t', '--type', type=str, required=True, help="Type of data to Scrape e.g, videos, playlists or channels ")
search.add_argument('-k', '--keyword', type=str, required=True, help='Keyword to be searched')

scrape = subparser.add_parser("scrape", help="scraping using channel_id")
scrape.add_argument('-i', '--channel_id', type=str, required=True, help='Youtube channel_id')
args = parser.parse_args()


if __name__ == '__main__':

    if args.mode == "search":
        search_data = Scrapper().search(args.keyword, args.type)
        print(search_data)
    elif args.mode == "scrape":
        scrape = Scrapper().get_channel_detail(args.channel_id)
        print(scrape)
    else:
        print("Invalid syntex..")


# python run.py search -t 1 -k "artificial intelligence"
# python run.py scrape -i "UCGaYiIpVOEzUWWS9A1zrodQ"
