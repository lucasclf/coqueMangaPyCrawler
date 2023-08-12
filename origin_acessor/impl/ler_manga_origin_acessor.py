import logging.config
from urllib.parse import urljoin

from config.config_manga_crawler import ConfigMangaCrawler
from enums.extension_enum import ExtensionEnum
from enums.origin_enum import OriginEnum
from utils.downloader import download_manga, url_verification
from utils.file_manager import FileManager

logging.config.fileConfig("./config/logging_config.ini")
logger = logging.getLogger('cqnLogger')


class LerMangaAccessor:
    def __init__(self):
        self.url_base = None
        self.folder_path = None
        self.LerMangaOriginAccessor = None
        self.manga = None

    def download_manga(self, manga):
        logger.debug(f"Download de {manga.name} iniciado, começando pelo {manga.chapter} através da plataforma {manga.origin}.")
        self.manga = manga
        self.url_base = self.mount_url()

        while self.chapter_verification():
            logger.debug(f"Chapter {manga.chapter} existe.")
            self.url_base = self.mount_url()

            self.download_chapter()

            if ConfigMangaCrawler.script_is_ending:
                return manga

            new_chapter = int(manga.chapter)+1
            manga.chapter = str(new_chapter)

        return manga

    def download_chapter(self):
        page = 1

        folder_path = f"download/{self.manga.name}/{self.manga.chapter}"
        self.folder_path = FileManager.create_folder_and_get_path(folder_path)

        url_complete = self.page_verification(page)
        while url_complete is not None:
            logger.info(self.folder_path)
            download_manga(self.folder_path, self.manga, url_complete)
            page += 1
            url_complete = self.page_verification(page)

    def mount_url(self):
        url = (
                OriginEnum.LER_MANGA.url
                + self.manga.prefix
                + self.manga.name
                + OriginEnum.LER_MANGA.chapter_prefix
                # + str(int(self.manga.chapter)).zfill(2)
                + self.manga.chapter.zfill(2)
                + "/"
        )
        logger.debug(f"Mounted URL: {url}")
        return url

    def chapter_verification(self):
        logger.info(f"Iniciando verificação de capitulo: {self.manga.name} : capitulo {self.manga.chapter}")

        for extension_enum in ExtensionEnum:

            url = urljoin(self.url_base, f"1{extension_enum.value}")
            logger.debug(f"URL {url}")

            if url_verification(url):
                return True

        return False

    def page_verification(self, page):

        for extension_enum in ExtensionEnum:
            url = urljoin(self.url_base, f"{page}{extension_enum.value}")
            if url_verification(url):
                self.manga.page = str(page)
                self.manga.extension = extension_enum.value
                return url
        return None
