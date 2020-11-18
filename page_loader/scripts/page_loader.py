from page_loader.cli import get_parser
from page_loader.loading_page import download
from page_loader.updating import load_resources


def main():
    parser = get_parser()
    args = parser.parse_args()
    file_path = download(args.url, args.output)
    print(file_path)
    load_resources(args.url, file_path)


if __name__ == '__main__':
    main()
