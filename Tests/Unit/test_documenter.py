from contextlib import contextmanager
import os

from pytest import fixture

from Modules.Documenter.PDFDocument import PDFDocument


@fixture()
def test_doc():
    obj = PDFDocument(
        "41c3b833-cb4e-4e31-a499-422a3ca6a2be",
        "07054204-2a9a-4146-9942-47b077b557a7",
        {"custom_field1": "abc"},
    )
    return obj


@contextmanager
def tempfile(filename: str, create: bool):
    if create:
        open(filename, "w")
    yield filename
    os.remove(filename)


def test_create_filename_creates_correct_name(monkeypatch):
    pass


def test_fill_form_creates_correct_text():
    pass


def test_create_file_creates_file(test_doc, monkeypatch):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.fill_form", lambda x: "Test"
    )
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.create_filename",
        lambda x: "Test_abc.pdf")
    test_filename = "Test_abc.pdf"

    # WHEN
    with test_doc.create_file() as _:
        # THEN
        os.path.isfile(test_filename)
