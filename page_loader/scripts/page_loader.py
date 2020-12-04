from page_loader.cli import get_parser
from page_loader import download, HTTPError404, HTTPError500
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    parser = get_parser()
    args = parser.parse_args()
    try:
        file_path = download(args.url, args.output)
        print(file_path)
    except PermissionError:
        logging.error('Not enough access rights in {args.ouput}')
        sys.exit(1)
    except FileNotFoundError:
        logging.error(f'No such directory: {args.output}')
        sys.exit(1)
    except HTTPError404:
        logging.error('HTTP error 404 for {args.url}: not found')
        sys.exit(1)
    except HTTPError500:
        logging.error('HTTP error 500 for {args.url}: Internal Server Error')
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
