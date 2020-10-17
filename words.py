import os.path
from typing import List, NamedTuple


class NamedWordlist(NamedTuple):
    name: str
    wordlist: List[str]


def _load_wordlist(path: str) -> List[str]:
    with open(path) as words_file:
        return list(line.strip() for line in words_file)


def load_wordlists(wordlists_dir: str) -> List[NamedWordlist]:
    return [
        NamedWordlist("🇷🇺 ориг.", _load_wordlist(os.path.join(wordlists_dir, "ru/original.txt"))),
        NamedWordlist("🇷🇺 Дуэт", _load_wordlist(os.path.join(wordlists_dir, "ru/duet.txt"))),
        NamedWordlist("🇷🇺 18+", _load_wordlist(os.path.join(wordlists_dir, "ru/deep_undercover.txt"))),

        NamedWordlist("🇬🇧 orig.", _load_wordlist(os.path.join(wordlists_dir, "en/original.txt"))),
        NamedWordlist("🇬🇧 Duet", _load_wordlist(os.path.join(wordlists_dir, "en/duet.txt"))),
        NamedWordlist("🇬🇧 18+", _load_wordlist(os.path.join(wordlists_dir, "en/deep_undercover.txt")))
    ]


def split_words(words_raw: str) -> List[str]:
    splitted = words_raw.replace(",", "\n").splitlines(keepends=False)

    result = []
    for line in splitted:
        parts = line.split()
        if parts:
            result.append(" ".join(parts))

    return result
