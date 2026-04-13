import json
import os
from pathlib import Path
from typing import Dict

_DEFAULT_LANG = "en"
_SUPPORTED_LANGS = {"en", "vi", "zh"}
_TRANSLATIONS_CACHE: Dict[str, Dict[str, str]] = {}


def _normalize_lang(raw_lang: str | None) -> str:
    if not raw_lang:
        return _DEFAULT_LANG

    lang = raw_lang.lower().strip()
    if "." in lang:
        lang = lang.split(".", 1)[0]
    if "_" in lang:
        lang = lang.split("_", 1)[0]
    if "-" in lang:
        lang = lang.split("-", 1)[0]

    return lang if lang in _SUPPORTED_LANGS else _DEFAULT_LANG


def get_language() -> str:
    return _normalize_lang(
        os.getenv("VECTCUT_LANG")
        or os.getenv("LC_ALL")
        or os.getenv("LANG")
    )


def _load_translations(lang: str) -> Dict[str, str]:
    if lang in _TRANSLATIONS_CACHE:
        return _TRANSLATIONS_CACHE[lang]

    locales_dir = Path(__file__).resolve().parent / "locales"
    file_path = locales_dir / f"{lang}.json"

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            _TRANSLATIONS_CACHE[lang] = {str(k): str(v) for k, v in data.items()}
            return _TRANSLATIONS_CACHE[lang]
    except Exception:
        pass

    _TRANSLATIONS_CACHE[lang] = {}
    return _TRANSLATIONS_CACHE[lang]


def t(key: str, default: str | None = None, **kwargs) -> str:
    lang = get_language()
    current = _load_translations(lang)
    fallback = _load_translations(_DEFAULT_LANG)

    template = current.get(key) or fallback.get(key) or default or key
    try:
        return template.format(**kwargs)
    except Exception:
        return template
