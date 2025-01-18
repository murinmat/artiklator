import asyncio
from typing import List
from german_nouns.lookup import Nouns
from dataclasses import dataclass
from googletrans import Translator

NOUN_DICT = None


@dataclass(kw_only=True)
class ArtiklatorResponse:
    article: str
    german_noun: str


@dataclass(kw_only=True)
class TranslatedArtiklatorResponse(ArtiklatorResponse):
    translation: str


class ArticleNotFoundException(Exception):
    pass


async def __translate_coroutine(inp: str, target_language_code: str) -> str:
    async with Translator() as translator:
        result = await translator.translate(
            inp, src='de', dest=target_language_code
        )
        return result.text


def __translate(inp: str, target_language_code: str) -> str:
    coroutine = __translate_coroutine(inp, target_language_code)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        return loop.run_until_complete(coroutine)
    else:
        return asyncio.run(coroutine)


def articlerize(
    german_noun: str | List[str],
    include_google_translation: str | None = None
) -> ArtiklatorResponse | TranslatedArtiklatorResponse:
    global NOUN_DICT
    if NOUN_DICT is None:
        NOUN_DICT = Nouns()

    capitalized = german_noun.capitalize()
    translation = None

    try:
        resolved = {'m': 'der', 'f': 'die', 'n': 'das'}
        output = NOUN_DICT[capitalized]
        if len(output) == 0:
            raise ArticleNotFoundException(
                f'Did not find article for "{german_noun}".'
            )
        article = resolved[output[0]['genus']]
    except KeyError:
        raise ArticleNotFoundException(
            f'Did not find article for "{german_noun}".'
        )

    if include_google_translation is not None:
        translation = __translate(german_noun, include_google_translation)
        return TranslatedArtiklatorResponse(
            article=article, german_noun=german_noun, translation=translation
        )
    else:
        return ArtiklatorResponse(article=article, german_noun=german_noun)
