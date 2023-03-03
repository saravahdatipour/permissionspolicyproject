import argparse
from crawler import crawl_csvfile,crawl_single_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawl in batch or single mode')
    parser.add_argument('--csv', metavar='FILE', help='address of the list of urls in csv format')
    parser.add_argument('--url', metavar='URL', help='URL to fetch')
    args = parser.parse_args()
    if args.csv:
        crawl_csvfile(args.csv)
    elif args.url:
        crawl_single_url(args.url)
    else:
        print("usage: main.py [--csv FILE] [--url URL]")
