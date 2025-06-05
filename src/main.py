from os_utils import copy_dir
from generator import generate_pages_recursive

def main():
    copy_dir("static", "public")
    generate_pages_recursive("content",
                  "template.html",
                  "public")

main()
