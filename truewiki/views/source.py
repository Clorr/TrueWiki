import os
import wikitextparser

from wikitexthtml.render import wikilink

from .. import singleton
from ..content import breadcrumb
from ..wiki_page import WikiPage
from ..wrapper import wrap_page


def view(user, page: str) -> str:
    filename = WikiPage(page).page_ondisk_name(page)
    filename = f"{singleton.STORAGE.folder}/{filename}"
    if os.path.exists(filename):
        with open(filename) as fp:
            body = fp.read()
    else:
        body = ""

    wikipage = WikiPage(page).render()

    templates_used = [f"<li>[[:Template:{template}]]</li>" for template in wikipage.templates]
    errors = [f"<li>{error}</li>" for error in wikipage.errors]

    wtp = wikitextparser.parse("\n".join(sorted(templates_used)))
    wikilink.replace(WikiPage(page), wtp)
    templates_used = wtp.string

    templates = {
        "page": body,
        "templates_used": templates_used,
        "errors": "\n".join(errors),
        "breadcrumbs": breadcrumb.create(page),
    }
    variables = {
        "has_templates_used": "1" if templates_used else "",
        "has_errors": "1" if errors else "",
        "display_name": user.display_name if user else "",
    }

    return wrap_page(page, "Source", variables, templates)
