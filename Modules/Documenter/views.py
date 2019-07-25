from Models.documenter import DocTemplates
from Models.db import session_scope


def fetch_all_templates() -> dict:
    """
    Returns all templates as JSON
    :return: JSON in format:
    {templates: [{template_id:"", template_name:"", template_raw_text:""},..]}
    """
    result = {"templates": []}
    for template in all_templates_from_db():
        result["templates"].append(template_to_dict(template))
    return result


def all_templates_from_db():
    with session_scope() as session:
        for template in session.query(DocTemplates).all():
            yield template


def template_to_dict(template: DocTemplates) -> dict:
    return {
        "template_id": template.id,
        "template_name": template.name,
        "template_raw_text": template.raw_text,
    }
