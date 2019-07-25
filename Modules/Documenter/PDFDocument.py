from contextlib import contextmanager
import os

import pdfkit

from Models.db import session_scope
from Models.documenter import DocTemplates
from Models.user_management import UMAccounts


class PDFDocument:
    """
    Object representing a PDF Document.
    To create PDFs we are using PDFKit library:
    https://pypi.org/project/pdfkit/
    """

    def __init__(self, template_id: str, owner_id: str, custom_fields: dict):
        self.template_id = template_id
        self.owner_id = owner_id
        self.custom_fields = custom_fields # TODO handle changing this to dict from str

    def get_username_and_template(self) -> tuple:
        with session_scope() as session:
            user_mail = (
                session.query(UMAccounts)
                .filter(UMAccounts.id == self.owner_id)
                .first()
                .email
            )
            template_name = (
                session.query(DocTemplates)
                .filter(DocTemplates.id == self.template_id)
                .first()
                .template_name
            )
            username = user_mail.split("@")[0]
            return username, template_name

    def create_filename(self) -> str:
        """
        Creates name of the file from user mail and document name
        :return: Filename as string in format user-mail_document-name
        """
        return "_".join(self.get_username_and_template()) + ".pdf"

    def fill_form(self) -> str:
        """
        Fills in form based on a template from the DB with the data from
        the custom_fields
        :return: Filled document form in HTML style as str
        """
        try:
            return self.get_form_text().format(**self.custom_fields)
        except KeyError:
            raise KeyError

    def get_form_text(self) -> str:
        """
        Queries the DB to get the template text based on template_id
        :return: Text of the template as str
        """
        with session_scope() as session:
            text = (
                session.query(DocTemplates)
                .filter(DocTemplates.id == self.template_id)
                .first()
                .template_text
            )
            return text

    @contextmanager
    def create_file(self, options=None):
        """
        Creates the PDF file, returns the filename and then removes the file
        after it is not needed anymore
        :param options:
        :return: Filename as str
        """
        filled_form = self.fill_form()
        filename = self.create_filename()
        if options:
            pdfkit.from_string(filled_form, filename, options=options)
        else:
            pdfkit.from_string(filled_form, filename)
        yield filename
        os.remove(filename)
