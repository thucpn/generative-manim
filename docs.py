import os
import re
import time
import requests
import html2text
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Base URL of the documentation
BASE_URL = "https://docs.manim.community/en/stable/"

# Base directory to save the markdown files
OUTPUT_DIR = "docs_md"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# A session to reuse HTTP connections
session = requests.Session()

def is_valid_url(url):
    """
    Only allow URLs that belong to the docs.manim.community/en/stable/ site.
    """
    parsed = urlparse(url)
    base_parsed = urlparse(BASE_URL)
    return (parsed.scheme in ("http", "https") and 
            parsed.netloc == base_parsed.netloc and 
            parsed.path.startswith(base_parsed.path))

def url_to_local_path(url):
    """
    Convert a URL into a local file path that preserves the URL’s folder structure.
    
    For example, a URL ending with:
        /_modules/manim/mobject/geometry/line.html
    will be saved as:
        docs_md/_modules/manim/mobject/geometry/line.html.md
    """
    parsed = urlparse(url)
    base_path = urlparse(BASE_URL).path
    # Get the relative path after the base
    rel_path = parsed.path[len(base_path):].lstrip("/")
    if not rel_path:
        rel_path = "index.html"
    local_path = os.path.join(OUTPUT_DIR, rel_path)
    # Ensure the file ends with .md (appending .md even if it ends with .html)
    local_path += ".md"
    return local_path

def convert_html_to_markdown(html_content):
    """
    Convert HTML content to Markdown using html2text.
    """
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0  # do not wrap lines
    return h.handle(html_content)

def crawl(url, visited):
    """
    Recursively crawl the documentation pages starting from the given URL.
    """
    if url in visited:
        return
    print(f"Processing: {url}")
    visited.add(url)
    
    try:
        response = session.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to get {url}: {e}")
        return

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract only the first element with class "content"
    content_div = soup.find(class_="content")
    if content_div:
        content_html = str(content_div)
    else:
        print(f"No content div found in {url}; using full page.")
        content_html = html_content

    markdown = convert_html_to_markdown(content_html)
    
    # Determine the local file path and ensure its directory exists
    local_path = url_to_local_path(url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Saved markdown to {local_path}")

    # Find and process links on the page
    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(url, href)
        full_url = full_url.split("#")[0]  # remove any fragment identifier
        if is_valid_url(full_url) and full_url not in visited:
            time.sleep(0.1)  # be polite with a short delay
            crawl(full_url, visited)

def combine_markdown_files(root_dir, output_file):
    """
    Recursively traverse root_dir and combine all .md files into one huge Markdown file.
    A heading structure (with '#' characters) is added based on the folder hierarchy.
    """
    with open(output_file, "w", encoding="utf-8") as out:
        def process_dir(current_dir, level):
            # Write a heading for the current directory (skip if we're at the root)
            if os.path.abspath(current_dir) != os.path.abspath(root_dir):
                dir_name = os.path.basename(current_dir)
                out.write("\n" + "#" * level + " " + dir_name + "\n\n")
            
            # Get sorted list of items
            items = sorted(os.listdir(current_dir))
            # Separate directories and markdown files
            dirs = [i for i in items if os.path.isdir(os.path.join(current_dir, i))]
            md_files = [i for i in items if os.path.isfile(os.path.join(current_dir, i)) and i.endswith(".md")]
            
            # Process markdown files in the current directory
            for md_file in md_files:
                file_path = os.path.join(current_dir, md_file)
                # Use a heading level one deeper than the directory
                out.write("\n" + "#" * (level + 1) + " " + md_file + "\n\n")
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read() + "\n\n")
            
            # Recursively process subdirectories
            for d in dirs:
                process_dir(os.path.join(current_dir, d), level + 1)
                
        process_dir(root_dir, 1)
    print(f"Combined markdown saved to {output_file}")

if __name__ == "__main__":
    visited = set()
    crawl(BASE_URL, visited)
    print("Download complete.")

    # After crawling, combine all markdown files into one huge markdown file.
    combined_output = "combined_docs.md"
    combine_markdown_files(OUTPUT_DIR, combined_output)
