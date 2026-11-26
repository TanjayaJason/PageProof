"""Generate a synthetic PDF in ignored data/; no private documents included."""
from pathlib import Path
import pymupdf
path = Path('data/scholarship.pdf')
path.parent.mkdir(exist_ok=True)
with pymupdf.open() as doc:
    page = doc.new_page()
    page.insert_text((72, 72), 'Example Scholarship Guide (synthetic)\n\n'
        'Applicants must have a minimum GPA of 3.25.\n'
        'Applications close on 15 June. Submit a transcript and a motivation letter.\n'
        'This fictional guide exists only to demonstrate PageProof.')
    doc.save(path)
print(path)
