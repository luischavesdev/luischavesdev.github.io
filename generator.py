# Props to https://github.com/jontopielski/jontopielski.github.io for a simple generator srcript I could "borrow".

from bs4 import BeautifulSoup
import re, os, sys, json, markdown, yaml, markdown_it


def inject_skill_panels():
    skill_template_html = get_html_at_file_location("templates/skill-panel.html")

    with open("data/skills.json", "r") as json_file:
        skills_json = json.load(json_file)

    skills_html = []
    for skill_idx, skill_entry in enumerate(skills_json):
        next_template = skill_template_html.format(
            data_0=skills_json[skill_idx]["title"],
            data_1=skills_json[skill_idx]["iconID"],
        )
        skills_html.append(next_template)

    final_skills_html = "".join(skills_html)

    inject_html_into_file_at_target(
        final_skills_html, "pregen-index.html", "index.html", "skill-generation"
    )


# -------------------------------
# -----------------//ART//-------------
# ------------------------


def inject_art_panels():
    art_html = []
    art_template = get_html_at_file_location("templates/art-panel.html")
    for filename in os.listdir("art"):
        file_path = os.path.join("art", filename)
        next_template = art_template.format(data_0=file_path)
        art_html.append(next_template)
    art_html = "".join(art_html)
    inject_html_into_file_at_target(art_html, "base.html", "art.html", "gameData")


# -------------------------------
# -----------------//BLOG//-------------
# ------------------------


def inject_blog_links():
    blog_links_html = []
    blog_link_template = get_html_at_file_location("templates/blog-link.html")
    sorted_blog_paths = get_all_blog_paths()
    for blog_path in sorted_blog_paths:
        with open(blog_path, "r", encoding="utf-8") as file:
            markdown_content = file.readlines()
        yaml_data = get_yaml_object_from_markdown_content(markdown_content)
        next_template = blog_link_template.format(
            data_0=yaml_data["link"],
            data_1=yaml_data["title"],
            data_2=yaml_data["date"],
        )
        blog_links_html.append(next_template)
    blog_links_html = "".join(blog_links_html)
    inject_html_into_file_at_target(
        blog_links_html, "base.html", "blog.html", "blogLinks", "ul"
    )


def get_all_blog_paths():
    blog_dirs = []
    for dir_name in os.listdir("posts"):
        for filename in os.listdir(os.path.join("posts", dir_name)):
            if filename.endswith(".md"):
                blog_dirs.append(os.path.join("posts", dir_name, filename))
    return blog_dirs[::-1]


def create_blog_pages():
    for blog_path in get_all_blog_paths():
        with open(blog_path, "r", encoding="utf-8") as file:
            markdown_content = file.readlines()
        yaml_data = get_yaml_object_from_markdown_content(markdown_content)
        create_blog_page(blog_path, yaml_data["link"])


def create_blog_page(markdown_file, destination):
    md = markdown_it.MarkdownIt()
    with open(markdown_file, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
    front_matter_end = md_content.find("---", 1)
    if front_matter_end != -1:
        md_content = md_content[front_matter_end + 3 :]  # Skip "---"
    blog_html = md.render(md_content)
    inject_html_into_file_at_target(blog_html, "base.html", destination, "blogPost")
    make_links_relative_to_directory_level(destination)


def inject_footers():
    footer_html = get_html_at_file_location("templates/footer.html")
    inject_html_into_file_at_target(footer_html, "index.html", "index.html", "footer")
    inject_html_into_file_at_target(footer_html, "about.html", "about.html", "footer")


def inject_headers():
    header_html = get_html_at_file_location("templates/header.html")
    inject_html_into_file_at_target(header_html, "index.html", "index.html", "header")
    inject_html_into_file_at_target(header_html, "about.html", "about.html", "header")


# -------------------------------
# -----------------//UTILITIES//-------------
# ------------------------
def get_html_at_file_location(file_location):
    with open(file_location, "r", encoding="utf-8") as file:
        return file.read()

def inject_html_into_file_at_target(
    inject_html, source_html, output_name, target_id, element_type="div"
):
    soup = BeautifulSoup(get_html_at_file_location(source_html), "html.parser")
    target_div = soup.find(element_type, id=target_id)
    if not target_div:
        print("Target div not found in the existing HTML.")
        return
    
    # Cleans up whatever the div may have.
    for child in target_div.find_all():
        child.decompose()
    
    injection_soup = BeautifulSoup(inject_html, "html.parser")
    target_div.append(injection_soup)
    
    with open(output_name, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def clean_generated_stuff():
    os.remove("index.html")

    #generated_pages = ["art.html", "blog.html", "tools.html", "index.html"]
    #for page in generated_pages:
    #    os.remove(page)

    #os.chdir("blog")
    #for file in os.listdir():
    #    os.remove(file)




def get_yaml_object_from_markdown_content(markdown_lines):
    if markdown_lines[0].strip() == "---":
        front_matter_end = markdown_lines.index("---\n", 1)
        front_matter_content = "".join(markdown_lines[1:front_matter_end])
        front_matter = yaml.safe_load(front_matter_content)
    return front_matter

def make_links_relative_to_directory_level(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    link_elements = soup.find_all("a", href=True) + soup.find_all("link", href=True)
    for link in link_elements:
        href = link["href"]
        if not href.startswith("http") and not href.startswith("#"):
            link["href"] = "../" + href
    img_elements = soup.find_all("img", href=False)
    for img in img_elements:
        src = img["src"]
        if not href.startswith("http") and not href.startswith("#"):
            img["src"] = "../" + src
    source_elements = soup.find_all("source", href=False)
    for elem in source_elements:
        src = elem["src"]
        if not href.startswith("http") and not href.startswith("#"):
            elem["src"] = "../" + src
    script_elements = soup.find_all("script", href=False)
    for script in script_elements:
        src = script["src"]
        if not href.startswith("http") and not href.startswith("#"):
            script["src"] = "../" + src

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())


# -------------------------------
# -----------------//MAIN//-------------
# ------------------------

if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean_generated_stuff()
    else:
        # inject_game_cards()
        # inject_art_panels()
        # inject_blog_links()
        # create_blog_pages()
        inject_skill_panels()
