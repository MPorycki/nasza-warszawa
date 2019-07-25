from sqlalchemy import Column, String, Text

from .db import base


class DocTemplates(base):
    __tablename__ = 'doc_templates'

    id = Column(String(length=32), primary_key=True)
    name = Column(String(length=256))
    text = Column(Text)
    raw_text = Column(Text)
    custom_fields = Column(Text)
