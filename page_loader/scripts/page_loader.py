from page_loader.cli import get_parser
from page_loader.page_loader import download
from page_loader.updating import load_resources
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    parser = get_parser()
    args = parser.parse_args()
    logging.debug('parser has done, dowloading starts')
    try:
        file_path = download(args.url, args.output)
        load_resources(args.url, file_path)
    except PermissionError:
        logging.error('Not enough access rights')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('no such directory')
        sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
