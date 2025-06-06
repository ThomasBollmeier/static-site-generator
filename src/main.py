import sys
from os_utils import copy_dir
from generator import generate_pages_recursive


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_dir("static", "docs")
    generate_pages_recursive(base_path,
                             "content",
                             "template.html",
                             "docs")


main()
