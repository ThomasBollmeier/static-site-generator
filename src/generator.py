import os

from utils import markdown_to_html_node

def extract_title(markdown):
    """
    Extract the title from a markdown string.
    """
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title not found in markdown string.")

def generate_pages_recursive(base_path, from_path, template_path, dest_path):
    """
    Recursively generate pages from markdown files in a directory.
    """
    if not os.path.exists(from_path):
        raise Exception(f"Source path {from_path} does not exist.")

    if os.path.isfile(from_path):
        if from_path.endswith(".md"):
            dest_file = os.path.splitext(dest_path)[0] + ".html"
            generate_page(base_path, from_path, template_path, dest_file)
        return

    for item in os.listdir(from_path):
        item_path = os.path.join(from_path, item)
        dest_item_path = os.path.join(dest_path, item)
        generate_pages_recursive(base_path, item_path, template_path, dest_item_path)


def generate_page(base_path, from_path, template_path, dest_path):
    """
    Generate a page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    output = open(template_path, "r").read()
    output = output.replace("{{ Title }}", title)
    output = output.replace("{{ Content }}", html)
    output = output.replace("href=\"/", f"href=\"{base_path}")
    output = output.replace("src=\"/", f"src=\"{base_path}")

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as f:
        f.write(output)

