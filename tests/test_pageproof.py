from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import pymupdf
import pytest
from typer.testing import CliRunner
from pageproof import core
from pageproof.cli import app

@pytest.fixture
def pdf():
    with pymupdf.open() as doc:
        doc.new_page().insert_text((72,72), 'Welcome to the synthetic guide.')
        doc.new_page().insert_text((72,72), 'Applicants need a minimum GPA of 3.25.')
        return doc.tobytes()

def test_page_evidence_and_abstention(pdf, monkeypatch):
    monkeypatch.setattr(core, 'model_result', lambda *a, **kw: pytest.fail('Unexpected LLM path'))
    chunks = core.extract([('guide.pdf',pdf)])
    report = core.answer(chunks, 'minimum GPA')
    assert report['mode'] == 'retrieval'
    assert report['claims'] == []
    assert report['evidence'][0]['page'] == 2
    assert report['evidence'][0]['file'] == 'guide.pdf'
    assert core.answer(chunks, 'volcanology')['mode'] == 'abstained'

@pytest.mark.parametrize('question', ['', ' ', 'x'*1501])
def test_question_limits(pdf, question):
    with pytest.raises(ValueError, match='question'):
        core.answer(core.extract([('guide.pdf',pdf)]),question)

def test_pdf_limits_and_blank():
    with pytest.raises(ValueError):
        core.extract([])
    with pytest.raises(ValueError):
        core.extract([('not.txt',b'not a pdf')])
    with pymupdf.open() as doc:
        doc.new_page()
        blank = doc.tobytes()
    with pytest.raises(ValueError, match='No readable text'):
        core.extract([('blank.pdf',blank)])

def test_citation_validator_uses_fake_output(pdf, monkeypatch):
    chunks = core.extract([('guide.pdf',pdf)])
    selected = core.retrieve(chunks,'minimum GPA')[0]
    claim = core.Claim(text='Minimum GPA is 3.25.', chunk_id=selected.id, quote=selected.text)
    monkeypatch.setattr(core,'model_result',lambda *a,**kw: core.Answer(abstained=False,claims=[claim]))
    assert core.answer(chunks,'minimum GPA',True)['claims'][0]['page'] == 2
    claim.quote = 'This fabricated quotation is not in the PDF.'
    with pytest.raises(ValueError,match='citation'):
        core.answer(chunks,'minimum GPA',True)

def test_cli_json_and_missing_input(tmp_path,pdf):
    path = tmp_path/'guide.pdf'
    path.write_bytes(pdf)
    import json
    result = CliRunner().invoke(app,[str(path),'minimum GPA'])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)['evidence'][0]['page'] == 2
    assert CliRunner().invoke(app,[str(tmp_path/'missing.pdf'),'GPA']).exit_code == 1

def test_web_form_offline(pdf):
    from streamlit.testing.v1 import AppTest
    root = Path(__file__).resolve().parents[1]
    upload = SimpleNamespace(name='guide.pdf',getvalue=lambda:pdf)
    with patch('streamlit.file_uploader',return_value=[upload]):
        ui = AppTest.from_file(str(root/'app.py')).run()
        assert not ui.exception
        ui.text_input[0].set_value('minimum GPA')
        next(button for button in ui.button if button.label == 'Find evidence').click()
        ui.run()
        assert not ui.exception
        assert len(ui.expander) == 1
        assert 'page 2' in ui.expander[0].label
