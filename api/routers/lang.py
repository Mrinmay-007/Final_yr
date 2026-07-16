

from functools import lru_cache

from fastapi import APIRouter, HTTPException, Query
from deep_translator import GoogleTranslator

router = APIRouter(
    prefix="/translate",
    tags=["Translation"]
)

# Supported Indian languages
SUPPORTED_LANGUAGES = {
    "bengali": "bn",
    "bhojpuri": "bho",
    "gujarati": "gu",
    "hindi": "hi",
    "kannada": "kn",
    "maithili": "mai",
    "malayalam": "ml",
    "marathi": "mr",
    "meitei": "mni-Mtei",
    "odia": "or",
    "punjabi": "pa",
    "sanskrit": "sa",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur",
    "santali": "sat",
    "awadhi": "awa",
    "bodo": "brx",
    "khasi": "kha",
    "kokborok": "trp",
    "marwadi": "mwr",
    "tulu": "tcy",
}


@lru_cache(maxsize=1000)
def translate_cached(text: str, target_lang: str) -> str:
    """
    Cache translations to improve performance for repeated requests.
    """
    return GoogleTranslator(
        source="en",
        target=target_lang
    ).translate(text)


@router.get("/")
async def translate_text(
    text: str = Query(..., description="Text to translate from English"),
    target_language: str = Query(
        ...,
        description="Target language (e.g. hindi, bengali, tamil)"
    ),
):
    target_language = target_language.strip().lower()

    if target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported language.",
                "supported_languages": sorted(SUPPORTED_LANGUAGES.keys()),
            },
        )

    try:
        lang_code = SUPPORTED_LANGUAGES[target_language]

        translated_text = translate_cached(text, lang_code)

        return {
            "success": True,
            "source_language": "English",
            "target_language": target_language.title(),
            "translated_text": translated_text,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )
