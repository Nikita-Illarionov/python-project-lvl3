from page_loader.main import load_page
from page_loader.cli import get_parser
from page_loader.correct_file import load_pictures
from page_loader.resources import load_resources


def main():
    parser = get_parser()
    args = parser.parse_args()
    file_path, body = load_page(args.address, args.output)
    load_pictures(args.address, file_path)
    load_resources(args.address, file_path)


if __name__ == '__main__':
    main()
