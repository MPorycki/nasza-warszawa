from contextlib import contextmanager
from copy import deepcopy
import os
import uuid

import pytest
from pytest import fixture

from Models.documenter import DocTemplates
from Modules.Documenter.PDFDocument import PDFDocument
from Modules.Documenter.views import template_to_dict, fetch_all_templates


@fixture()
def test_doc():
    obj = PDFDocument(
        "41c3b833-cb4e-4e31-a499-422a3ca6a2be",
        "07054204-2a9a-4146-9942-47b077b557a7",
        {"custom_field1": "abc", "custom_field2": "see"},
    )
    return obj


@fixture()
def test_db_doc():
    obj = DocTemplates
    obj.id = uuid.uuid4().hex
    obj.name = "Test_obj"
    obj.text = "Textytext {input_name}"
    obj.raw_text = "Textytext"
    obj.custom_fields = '{"input_name" : "Jan"}'
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


def test_template_to_dict_returns_correct_json(test_db_doc):
    # WHEN
    test_result = template_to_dict(test_db_doc)

    # THEN
    assert test_result == {
        "template_id": test_db_doc.id,
        "template_name": test_db_doc.name,
        "template_raw_text": test_db_doc.raw_text,
    }


def test_fetch_all_templates_returns_correct_data(test_db_doc, monkeypatch):
    # GIVEN
    monkeypatch.setattr(
        "Modules.Documenter.views.all_templates_from_db",
        lambda: [test_db_doc, deepcopy(test_db_doc)],
    )

    # WHEN
    test_result = fetch_all_templates()

    # THEN
    assert test_result["templates"] == [
        {
            "template_id": test_db_doc.id,
            "template_name": test_db_doc.name,
            "template_raw_text": test_db_doc.raw_text,
        },
        {
            "template_id": test_db_doc.id,
            "template_name": test_db_doc.name,
            "template_raw_text": test_db_doc.raw_text,
        },
    ]
