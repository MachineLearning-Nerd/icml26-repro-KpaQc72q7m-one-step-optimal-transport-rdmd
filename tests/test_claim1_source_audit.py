from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_claim1_audit_maps_theorem_scope():
    text = (ROOT / 'evidence/claim1_attempt1/SOURCE_AUDIT.md').read_text()
    assert 'theoretical optimum' in text
    assert 'convergence in probability' in text
    assert 'inconclusive' in text

def test_primary_source_excerpt_is_retained():
    text = (ROOT / 'evidence/claim1_attempt1/source_excerpt.tex').read_text()
    assert 'Theorem' in text
    assert 'quadratic cost' in text
