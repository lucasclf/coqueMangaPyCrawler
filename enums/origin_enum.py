from enum import Enum, auto


class OriginEnum(Enum):
    LER_MANGA = ("https://img.lermanga.org", "/capitulo-")
    MANGA_LIVRE = ("", "")
    UNION_MANGA = ("https://umangas.club/leitor/mangas/", "")

    def __init__(self, url, chapter_prefix):
        self.url = url
        self.chapter_prefix = chapter_prefix

    @staticmethod
    def find_by_name(name):
        for origin_enum in OriginEnum:
            if origin_enum.name.upper() == name.upper():
                return origin_enum
        return None
