from sqlalchemy import Column, String, Text

from .db import base


class DocTemplates(base):
    __tablename__ = 'doc_templates'

    template_id = Column(String(length=32), primary_key=True)
    template_text = Column(Text)
    template_raw_text = Column(Text)
