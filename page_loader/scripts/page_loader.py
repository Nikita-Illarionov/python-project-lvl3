from page_loader.cli import get_parser
from page_loader import download
import logging
import sys
import requests


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    parser = get_parser()
    args = parser.parse_args()
    try:
        file_path = download(args.url, args.output)
        print(file_path)
    except PermissionError:
        logging.error('Not enough access rights')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('No such directory')
        sys.exit(1)
    except requests.exceptions.HTTPError:
        sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
