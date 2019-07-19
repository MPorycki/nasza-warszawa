import pdfkit

from Models.db import session_scope
from Models.documenter import DocTemplates


class PDFDocument:
    """
    Object representing a PDF Document.
    To create PDFs we are using PDFKit library:
    https://pypi.org/project/pdfkit/
    """

    def __init__(self, template_id: str, owner_id: str, custom_fields: dict):
        self.template_id = template_id
        self.owner_id = owner_id
        self.custom_fields = custom_fields

    def fill_form(self) -> str:
        """
        Fills in form based on a template from the DB with the data from the custom_fields
        :return: Filled document form in HTML style as str
        """
        form_text = self.get_form_text()
        # TODO wykminic jak stworzyc uniwersalny wypelniacz tego forma

    def get_form_text(self) -> str:
        """
        Queries the DB to get the template text based on template_id
        :return: Text of the template as str
        """
        with session_scope() as session:
            text = (
                session.query(DocTemplates)
                .filter(DocTemplates.template_id == self.template_id)
                .first()
                .template_text
            )
            return text

    def create_file(self, options=None):
        """
        Creates the PDF file, returns the filename and then removes the file after it is
        not needed anymore
        :param options:
        :return:
        """
        filled_form = self.fill_form()
        if options:
            pdfkit.from_string(filled_form, "test.pdf", options=options)
        else:
            pdfkit.from_string(filled_form, "test.pdf")
