from dotenv.main import rewrite
import jinja2
from dotenv import load_dotenv
from deta import Deta
import os
import urllib.parse
import random


load_dotenv()
# deta = Deta(os.getenv("DETA_TOKEN"))
# toolsdb = deta.Base("whatdevsneed-posts")


all_categories = [
    "AIs",
    "Analytics",
    "APIs",
    "Automation",
    "Backups",
    "Blockchain",
    "Blogging",
    "Collaboration",
    "Community",
    "Communication",
    "Continuous Integrations",
    "Databases",
    "Design",
    "Domains",
    "Emails",
    "Extensions",
    "Game Engines",
    "Hosting",
    "IDEs",
    "Issue Tracking",
    "Documentation",
    "Learning",
    "Legal",
    "Libraries",
    "Licensing",
    "Localization",
    "Logging",
    "Messaging",
    "Monitoring",
    "Payments",
    "Performance",
    "Productivity",
    "Publishing",
    "Security",
    "Software",
    "Storage",
    "Terminals",
    "Testing",
    "Other",
]


def categorylist() -> list:
    return all_categories


def search(query):
    search = toolsdb.fetch({"show": True}).items
    entries = list()
    for entry in search:
        if (
            (query.lower() in str(entry["name"]).lower())
            or (query.lower() in str(entry["description"]).lower())
            or (query.lower() in str(entry["category"]).lower())
        ):
            entries.append(entry)
    return tools_html(entries)


def tools(tag):
    if tag == "all":
        entries = toolsdb.fetch({"show": True}).items
    else:
        entries = toolsdb.fetch(
            {"show": True, "category": urllib.parse.unquote(tag)}
        ).items
    return tools_html(entries)


def tools_html(entries):
    if len(entries) == 0:
        tools_html = """ """
    else:
        random.shuffle(entries)
        tools_html = """"""

        with open("/templates/elements/tools.html", "r") as fp:
            tools_html_template = jinja2.Template(fp.read())
        for entry in entries:
            if entry["staffpick"] is True:
                staffpick_html = ""
            else:
                staffpick_html = """"""
            data = {
                "imgurl": entry["img"],
                "name": entry["name"],
                "category": entry["category"],
                "category_link": f"/category/{urllib.parse.quote(entry['category'])}",
                "staffpick": staffpick_html,
                "description": entry["description"],
                "link": f"{entry['link']}?ref=whatdevsneed",
                "sharelink": "",
                "pricing": entry["pricing"] 
            }
            tools_html += tools_html_template.render(data)
    return tools_html


def alert(id_: str) -> str:
    if id_ == "add-success":
        alert = """
            <div style="margin-bottom: 16px;padding: 10px;border-radius: 5px;background: rgba(25,135,84,0.1);color: var(--bs-green);border-width: 1px;border-style: solid;">
                <p style="margin-bottom: 0px;"><strong>Done! </strong>Your tool was submitted. It may take a bit to get reviewed.</p>
            </div>
        """
    elif id_ == "add-error":
        alert = """ 
            <div style="margin-bottom: 16px;padding: 10px;border-radius: 5px;background: rgba(220,53,69,0.1);color: var(--bs-red);border-width: 1px;border-style: solid;">
                <p style="margin-bottom: 0px;"><strong>Error! </strong>The tool couldn&#39;t be added.</p>
            </div>
        """
    return alert


def category_options():
    options_html = """"""
    for category in all_categories:
        options_html += """<option value="{0}">{0}</option>""".format(category)
    return options_html
