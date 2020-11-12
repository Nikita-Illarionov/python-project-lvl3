from page_loader.main import load_page
from page_loader.cli import get_parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    load_page(args.address, args.output)


if __name__ == '__main__':
    main()
