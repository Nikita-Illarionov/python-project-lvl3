from page_loader.cli import get_parser
from page_loader.loading_page import download
from page_loader.updating import load_resources
import logging


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    parser = get_parser()
    args = parser.parse_args()
    logging.debug('parser has done, dowloading starts')
    file_path = download(args.url, args.output)
    logging.debug('dowloading has done, resource loading starts')
    logging.info(f'page saved in {file_path}')
    load_resources(args.url, file_path)


if __name__ == '__main__':
    main()
