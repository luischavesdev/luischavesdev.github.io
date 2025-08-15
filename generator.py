# Props to https://github.com/jontopielski/jontopielski.github.io for a simple generator srcript I could "borrow".

from bs4 import BeautifulSoup
from pathlib import Path
import re, os, sys, json

TEMPLATES_FOLDER = Path("templates/")
DATA_FOLDER = Path("data/")
PREPROJ_FOLDER = Path("pregen-projects/")
PROJECTS_FOLDER = Path("projects/")
BANNERS_FOLDER = Path("assets/img/projects/")


def inject_footers(source_html_file):
    footer_html = get_html_at_file_location(TEMPLATES_FOLDER / "footer.html")
    inject_html_into_file_at_target(footer_html, source_html_file, "index.html", "footer-generation", "footer", True)


def inject_skill_panels(source_html_file):
    skill_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "skill-panel.html")

    with open(DATA_FOLDER / "skills.json", encoding="utf-8") as json_file:
        skills_json = json.load(json_file)

    skills_html = []
    for skill_idx, skill_entry in enumerate(skills_json):
        next_template = skill_template_html.format(
            data_0=skills_json[skill_idx]["title"],
            data_1=skills_json[skill_idx]["iconID"],
        )
        skills_html.append(next_template)

    skills_html = "".join(skills_html)
    inject_html_into_file_at_target(skills_html, source_html_file, "index.html", "skill-generation")


def inject_education_panels(source_html_file):
    education_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "education-panel.html")

    with open(DATA_FOLDER / "education.json", encoding="utf-8") as json_file:
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
    inject_html_into_file_at_target(education_html, source_html_file, "index.html", "education-generation")


# --- || Projects Related Injection || ---


def inject_project_highlights(source_html_file):
    highlight_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "project-highlight.html")
    tag_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "project-tag.html")

    with open(DATA_FOLDER / "projects.json", encoding="utf-8") as json_file:
        projects_json = json.load(json_file)

    with open(DATA_FOLDER / "highlights.json", encoding="utf-8") as json_file:
        highlights_json = json.load(json_file)

    selected_data = []
    for category_idx, category_entry in enumerate(projects_json):
        for project_idx, project_entry in enumerate(projects_json[category_idx]):

            # Check if project is highlight project
            is_in_highlights = False
            for highlight_idx, highlight_entry in enumerate(highlights_json):
                if projects_json[category_idx][project_idx]["title"] == highlights_json[highlight_idx]:
                    is_in_highlights = True
            if not is_in_highlights:
                continue

            # Create a string with all the description list items
            description_html = []
            for description_idx, description_entry in enumerate(projects_json[category_idx][project_idx]["tldr"]):
                description_html.append(
                    "<li>" + projects_json[category_idx][project_idx]["tldr"][description_idx] + "</li>"
                )
            description_html = "".join(description_html)

            # Create a string with all the tag elements
            tags_html = []
            for tag_idx, tag_entry in enumerate(projects_json[category_idx][project_idx]["tags"]):
                next_tag_template = tag_template_html.format(
                    data_0=projects_json[category_idx][project_idx]["tags"][tag_idx]
                )
                tags_html.append(next_tag_template)
            tags_html = "".join(tags_html)

            # Store all the needed highlight project data
            selected_data.append(
                [
                    projects_json[category_idx][project_idx]["title"],
                    PROJECTS_FOLDER / projects_json[category_idx][project_idx]["link"],
                    BANNERS_FOLDER / projects_json[category_idx][project_idx]["bannerURL"],
                    projects_json[category_idx][project_idx]["bannerAlt"],
                    projects_json[category_idx][project_idx]["context"],
                    projects_json[category_idx][project_idx]["date"],
                    projects_json[category_idx][project_idx]["teamSize"],
                    projects_json[category_idx][project_idx]["duration"],
                    projects_json[category_idx][project_idx]["employment"],
                    description_html,
                    tags_html,
                ]
            )

    # Create final html string ordered by the highlights json file
    highlights_html = []
    for highlight_idx, highlight_entry in enumerate(highlights_json):
        data_to_use = ""
        for project_data in selected_data:
            if project_data[0] == highlights_json[highlight_idx]:
                data_to_use = project_data

        if data_to_use != "":
            next_template = highlight_template_html.format(
                data_0=data_to_use[0],
                data_1=data_to_use[1],
                data_2=data_to_use[2],
                data_3=data_to_use[3],
                data_4=data_to_use[4],
                data_5=data_to_use[5],
                data_6=data_to_use[6],
                data_7=data_to_use[7],
                data_8=data_to_use[8],
                data_9=data_to_use[9],
                data_10=data_to_use[10],
            )

            highlights_html.append(next_template)

    highlights_html = "".join(highlights_html)
    inject_html_into_file_at_target(highlights_html, source_html_file, "index.html", "highlights-generation")


def inject_project_cards(source_html_file):
    card_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "project-card.html")

    with open(DATA_FOLDER / "projects.json", encoding="utf-8") as json_file:
        projects_json = json.load(json_file)

    with open(DATA_FOLDER / "project-ordering.json", encoding="utf-8") as json_file:
        order_json = json.load(json_file)

    for category_idx, category_entry in enumerate(projects_json):

        cards_html = []
        for project_idx, project_entry in enumerate(projects_json[category_idx]):

            # Create a string with all project filters
            filters_html = []
            for filter_idx, filter_entry in enumerate(projects_json[category_idx][project_idx]["filters"]):
                filters_html.append(" filter-" + projects_json[category_idx][project_idx]["filters"][filter_idx])
            filters_html = "".join(filters_html)

            # Word-based clamp the title string to display. Also remove anything inside parenthesis
            title_string = re.sub(r"\((.*?)\)", "", projects_json[category_idx][project_idx]["title"])
            clamped_title = title_string
            max_title_len = 24
            for i in range(0, max_title_len):
                clamped_title = " ".join(title_string.split()[:i])
                if len(clamped_title) > max_title_len:
                    clamped_title = " ".join(title_string.split()[: (i - 1)])
                    break

            # Get project order from appropriate json to then store on the html element
            custom_order = order_json["custom"][category_idx].index(projects_json[category_idx][project_idx]["title"])
            chronological_order = order_json["chronological"][category_idx].index(
                projects_json[category_idx][project_idx]["title"]
            )

            next_template = card_template_html.format(
                data_0=clamped_title,
                data_1=(category_idx + 1),
                data_2=filters_html,
                data_3=custom_order,
                data_4=chronological_order,
                data_5=BANNERS_FOLDER / projects_json[category_idx][project_idx]["bannerURL"],
                data_6=projects_json[category_idx][project_idx]["bannerAlt"],
                data_7=projects_json[category_idx][project_idx]["tldr"][0][:-1],
                data_8=PROJECTS_FOLDER / projects_json[category_idx][project_idx]["link"],
            )
            cards_html.append(next_template)

        cards_html = "".join(cards_html)
        inject_html_into_file_at_target(
            cards_html, source_html_file, "index.html", ("projects-generation" + str(category_idx + 1))
        )


def generate_project_pages():
    page_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "project-page.html")
    tag_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "project-tag.html")
    link_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "cta-link.html")
    button_template_html = get_html_at_file_location(TEMPLATES_FOLDER / "cta-button.html")

    with open(DATA_FOLDER / "projects.json", encoding="utf-8") as json_file:
        projects_json = json.load(json_file)

    for category_idx, category_entry in enumerate(projects_json):
        for project_idx, project_entry in enumerate(projects_json[category_idx]):

            # Check if context field needs to be a link
            context_url = projects_json[category_idx][project_idx]["contextURL"]
            context_text = projects_json[category_idx][project_idx]["context"]
            context_html = ""
            if context_url:
                context_html = "<a href=\"" + context_url + "\"target=\"_blank\">" + "<em>" + context_text + "</em></a>"
            else:
                context_html = "<p><em>" + projects_json[category_idx][project_idx]["context"] + "</em></p>"

            # Create appropriate call to action button
            project_url = projects_json[category_idx][project_idx]["projectURL"]
            cta_html = ""

            if project_url:
                cta_text = "Ask for it!" if "@" in project_url else "Check it!"

                cta_html = link_template_html.format(
                    data_0=projects_json[category_idx][project_idx]["projectURL"],
                    data_1=cta_text,
                )
            else:
                cta_html = button_template_html

            # Create a string with all the description list items
            description_html = []
            for description_idx, description_entry in enumerate(projects_json[category_idx][project_idx]["tldr"]):
                description_html.append(
                    "<li>" + projects_json[category_idx][project_idx]["tldr"][description_idx] + "</li>"
                )
            description_html = "".join(description_html)

            # Create a string with all the tag elements
            tags_html = []
            for tag_idx, tag_entry in enumerate(projects_json[category_idx][project_idx]["tags"]):
                next_tag_template = tag_template_html.format(
                    data_0=projects_json[category_idx][project_idx]["tags"][tag_idx]
                )
                tags_html.append(next_tag_template)
            tags_html = "".join(tags_html)

            page_html = page_template_html.format(
                data_0=projects_json[category_idx][project_idx]["title"],
                data_1=projects_json[category_idx][project_idx]["title"],
                data_2=context_html,
                data_3=cta_html,
                data_4=projects_json[category_idx][project_idx]["date"],
                data_5=projects_json[category_idx][project_idx]["teamSize"],
                data_6=projects_json[category_idx][project_idx]["duration"],
                data_7=projects_json[category_idx][project_idx]["employment"],
                data_8=description_html,
                data_9=tags_html,
            )

            project_body_html = get_html_at_file_location(
                PREPROJ_FOLDER / projects_json[category_idx][project_idx]["link"]
            )
            inject_html_into_file_at_target(
                project_body_html,
                page_html,
                PROJECTS_FOLDER / projects_json[category_idx][project_idx]["link"],
                "body-generation",
                direct_source=True,
            )


# --- || Utilities || ---


def get_html_at_file_location(file_location):
    with open(file_location, encoding="utf-8") as file:
        return file.read()


# Pass multiple true if we want to inject at multiple points on target file
def inject_html_into_file_at_target(
    inject_html, source_html, output_name, target_id, element_type="div", multiple=False, direct_source=False
):
    html_to_use = source_html if direct_source else get_html_at_file_location(source_html)
    soup = BeautifulSoup(html_to_use, "html.parser")
    found_divs = soup.find_all(element_type, id=target_id) if multiple else soup.find(element_type, id=target_id)

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
    if os.path.exists("index.html"):
        os.remove("index.html")

    os.chdir(PROJECTS_FOLDER)
    for file in os.listdir():
        os.remove(file)


# --- || Main || ---


if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean_generated_stuff()
    else:
        if "--projgen" in sys.argv:
            generate_project_pages()

        source_to_use = "pregen-index.html"
        inject_footers(source_to_use)

        source_to_use = "index.html"
        inject_project_highlights(source_to_use)
        inject_skill_panels(source_to_use)
        inject_education_panels(source_to_use)
        inject_project_cards(source_to_use)
