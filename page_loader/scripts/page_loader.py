from page_loader.cli import get_parser
from page_loader import download, PageLoadingError
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    parser = get_parser()
    args = parser.parse_args()
    try:
        file_path = download(args.url, args.output)
        print(f'Page saved in {file_path}')
    except PageLoadingError as e:
        logging.error('status code is 500 or 400')
        sys.exit(1)
    except PermissionError:
        logging.error('Not enough access rights')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('No such file or directory')
        sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
