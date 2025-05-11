# Props to https://github.com/jontopielski/jontopielski.github.io for a simple generator srcript I could "borrow".

from bs4 import BeautifulSoup
import re, os, sys, json, markdown, yaml, markdown_it


def inject_project_highlights(source_html_file):
    highlight_template_html = get_html_at_file_location(
        "templates/project-highlight.html"
    )

    tag_template_html = get_html_at_file_location("templates/project-tag.html")

    with open("data/project-highlights.json", "r") as json_file:
        highlights_json = json.load(json_file)

    highlights_html = []
    for highlight_idx, highlight_entry in enumerate(highlights_json):

        # Create a string with all the description list items
        description_html = []
        for description_idx, description_entry in enumerate(
            highlights_json[highlight_idx]["description"]
        ):
            description_html.append(
                "<li>"
                + highlights_json[highlight_idx]["description"][description_idx]
                + "</li>"
            )
        description_html = "".join(description_html)

        # Create a string with all the tag elements
        tags_html = []
        for tag_idx, tag_entry in enumerate(highlights_json[highlight_idx]["tags"]):
            next_tag_template = tag_template_html.format(
                data_0=highlights_json[highlight_idx]["tags"][tag_idx]
            )
            tags_html.append(next_tag_template)
        tags_html = "".join(tags_html)

        next_template = highlight_template_html.format(
            data_0=highlights_json[highlight_idx]["title"],
            data_1=highlights_json[highlight_idx]["link"],
            data_2=highlights_json[highlight_idx]["bannerURL"],
            data_3=highlights_json[highlight_idx]["bannerAlt"],
            data_4=highlights_json[highlight_idx]["type"],
            data_5=highlights_json[highlight_idx]["date"],
            data_6=highlights_json[highlight_idx]["teamSize"],
            data_7=highlights_json[highlight_idx]["duration"],
            data_8=highlights_json[highlight_idx]["employment"],
            data_9=description_html,
            data_10=tags_html,
        )
        highlights_html.append(next_template)

    highlights_html = "".join(highlights_html)
    inject_html_into_file_at_target(
        highlights_html, source_html_file, "index.html", "highlights-generation"
    )


def inject_skill_panels(source_html_file):
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

    skills_html = "".join(skills_html)
    inject_html_into_file_at_target(
        skills_html, source_html_file, "index.html", "skill-generation"
    )


def inject_education_panels(source_html_file):
    education_template_html = get_html_at_file_location(
        "templates/education-panel.html"
    )

    with open("data/education.json", "r") as json_file:
        education_json = json.load(json_file)

    education_html = []
    for skill_idx, skill_entry in enumerate(education_json):
        next_template = education_template_html.format(
            data_0=education_json[skill_idx]["title"],
            data_1=education_json[skill_idx]["link"],
            data_2=education_json[skill_idx]["date"],
            data_3=education_json[skill_idx]["establishment"],
            data_4=education_json[skill_idx]["description"],
        )
        education_html.append(next_template)

    education_html = "".join(education_html)
    inject_html_into_file_at_target(
        education_html, source_html_file, "index.html", "education-generation"
    )


def inject_footers(source_html_file):
    footer_html = get_html_at_file_location("templates/footer.html")
    inject_html_into_file_at_target(
        footer_html, source_html_file, "index.html", "footer-generation", "footer", True
    )


# --- || Utilities || ---


def get_html_at_file_location(file_location):
    with open(file_location, "r", encoding="utf-8") as file:
        return file.read()


def inject_html_into_file_at_target(
    inject_html, source_html, output_name, target_id, element_type="div", multiple=False
):
    soup = BeautifulSoup(get_html_at_file_location(source_html), "html.parser")
    found_divs = (
        soup.find_all(element_type, id=target_id)
        if multiple
        else soup.find(element_type, id=target_id)
    )
    if not found_divs:
        print("Target div not found in the existing HTML.")
        return

    if not multiple:
        found_divs = [found_divs]

    for target_div in found_divs:
        # Cleans up whatever the div may have in case this is running over previously generated elements
        for child in target_div.find_all():
            child.decompose()

        custom_soup = BeautifulSoup(inject_html, "html.parser")
        target_div.append(custom_soup)

    with open(output_name, "w", encoding="utf-8") as file:
        file.write(soup.prettify())


def clean_generated_stuff():
    os.remove("index.html")


# --- || Main || ---


if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean_generated_stuff()
    else:
        source_to_use = "pregen-index.html"
        inject_footers(source_to_use)

        source_to_use = "index.html"
        inject_project_highlights(source_to_use)
        inject_skill_panels(source_to_use)
        inject_education_panels(source_to_use)
