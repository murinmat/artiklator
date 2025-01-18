import pytest
from artiklator import articlerize, ArticleNotFoundException


def test_articlerize_no_translation():
    response = articlerize('Bier')
    assert response.article == 'das'
    assert response.german_noun == 'Bier'


def test_articlerize_with_translation():
    response = articlerize('Bier', 'en')
    assert response.article == 'das'
    assert response.german_noun.capitalize() == 'Bier'
    assert response.translation.capitalize() == 'Beer'


def test_articlerize_not_found():
    with pytest.raises(ArticleNotFoundException):
        articlerize('some other word')
