from contextlib import contextmanager
import os

import pytest
from pytest import fixture

from Modules.Documenter.PDFDocument import PDFDocument


@fixture()
def test_doc():
    obj = PDFDocument(
        "41c3b833-cb4e-4e31-a499-422a3ca6a2be",
        "07054204-2a9a-4146-9942-47b077b557a7",
        {"custom_field1": "abc", "custom_field2": "see"},
    )
    return obj


@contextmanager
def tempfile(filename: str, create: bool):
    if create:
        open(filename, "w")
    yield filename
    os.remove(filename)


def test_create_filename_creates_correct_name(test_doc, monkeypatch):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument."
        "get_username_and_template",
        lambda x: ("test", "Test_template"),
    )

    # WHEN
    test_filename = test_doc.create_filename()

    # THEN
    assert test_filename == "test_Test_template.pdf"


def test_fill_form_creates_correct_text_when_correct_kwargs_are_given(
        test_doc, monkeypatch
):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.get_form_text",
        lambda x: "Hello {custom_field1}, long time no {custom_field2}",
    )

    # WHEN
    test_form = test_doc.fill_form()

    # THEN
    assert test_form == "Hello abc, long time no see"


def test_fill_form_creates_correct_text_when_too_many_kwargs_are_given(
        test_doc, monkeypatch
):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.get_form_text",
        lambda x: "Hello {custom_field1}, long time no {custom_field2}",
    )
    test_doc.custom_fields["custom_field3"] = "fake"

    # WHEN
    test_form = test_doc.fill_form()

    # THEN
    assert test_form == "Hello abc, long time no see"


def test_fill_form_raises_KeyError_when_not_enough_kwargs_are_given(
        test_doc, monkeypatch
):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.get_form_text",
        lambda x: "Hello {custom_field1}, long time no {custom_field2}",
    )
    test_doc.custom_fields.pop("custom_field2")

    # THEN
    with pytest.raises(KeyError):
        assert test_doc.fill_form()


def test_create_file_creates_file(test_doc, monkeypatch):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.fill_form",
        lambda x: "Test",
    )
    monkeypatch.setattr(
        "Modules.Documenter.PDFDocument.PDFDocument.create_filename",
        lambda x: "Test_abc.pdf",
    )
    test_filename = "Test_abc.pdf"

    # WHEN
    with test_doc.create_file() as _:
        # THEN
        os.path.isfile(test_filename)
