from enums.origin_enum import OriginEnum
from origin_acessor.impl.ler_manga_origin_acessor import LerMangaAccessor


def create_accessor(origin):
    if origin == OriginEnum.LER_MANGA.name:
        return LerMangaAccessor()

    return None
