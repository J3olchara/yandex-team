#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyceum.settings')
    project_wd = Path(__file__).resolve().parent.parent
    if not load_dotenv(project_wd / '.env'):
        load_dotenv(project_wd / 'example.env')
    sys.path.append('.')
    try:
        from django.core.management import (  # pylint: disable=C0415
            execute_from_command_line,
        )
    except ImportError as exc:
        raise ImportError(
            'Couldn"t import Django. Are you sure it"s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    # if 'initdata' in sys.argv:
    #     return init_data()
    execute_from_command_line(sys.argv)


# def init_data() -> None:
#     default_fixtures_path =
#     Path(__file__).resolve().parent.parent / 'fixtures'
#
#     def create_parser() -> argparse.ArgumentParser:
#         nonlocal default_fixtures_path
#         arg_parser = argparse.ArgumentParser()
#         arg_parser.add_argument(
#             '-fp', '--fixtures-path', default=str(default_fixtures_path)
#         )
#         arg_parser.add_argument(
#             '-cm', '--check-migrations', default=str(default_fixtures_path)
#         )
#         arg_parser.add_argument('-m', '--migrate', default=False)
#         arg_parser.add_argument('-ld', '--load_data', default=False)
#         return arg_parser
#
#     parser = create_parser()
#     print(parser.parse_args(sys.argv[2:]))


if __name__ == '__main__':
    main()
