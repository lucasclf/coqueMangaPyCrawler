import logging.config
from urllib.parse import urljoin

from config.config_manga_crawler import ConfigMangaCrawler
from enums.extension_enum import ExtensionEnum
from enums.origin_enum import OriginEnum
from enums.output_format_enum import OutputFormatEnum
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
        self.refill_chapter = False

    def download_manga(self, manga):
        logger.debug(
            f"Download de {manga.name} iniciado, começando pelo {manga.chapter} através da plataforma {manga.origin}.")
        self.manga = manga

        while self.chapter_verification():
            logger.debug(f"Chapter {manga.chapter} existe.")

            self.download_chapter()

            if ConfigMangaCrawler.script_is_ending:
                return manga

            new_chapter = int(manga.chapter) + 1
            manga.chapter = str(new_chapter)

        return manga

    def download_chapter(self):
        page = 1

        folder_name = f"download/{self.manga.name}/{self.manga.chapter}"
        self.folder_path = FileManager.create_folder_and_get_path(folder_name)

        self.url_base = self.mount_url()

        url_complete = self.page_verification(page)
        if url_complete is None:
            self.refill_chapter = not self.refill_chapter
            self.url_base = self.mount_url()
            url_complete = self.page_verification(page)

        while url_complete is not None:
            logger.info(self.folder_path)
            download_manga(self.folder_path, self.manga, url_complete)
            page += 1
            url_complete = self.page_verification(page)

        if page != 1 and ConfigMangaCrawler.output_format == OutputFormatEnum.CBZ:
            path_without_chapter = self.folder_path.rsplit('/', 1)[0]
            FileManager.zip_file(self.folder_path, f"{self.manga.name}_{self.manga.chapter}", path_without_chapter)

    def mount_url(self):
        if self.refill_chapter:
            url = (
                    OriginEnum.LER_MANGA.url
                    + self.manga.prefix
                    + self.manga.name
                    + OriginEnum.LER_MANGA.chapter_prefix
                    + self.manga.chapter.zfill(2)
                    + "/"
            )
            logger.debug(f"Mounted URL: {url}")
            return url
        else:
            url = (
                    OriginEnum.LER_MANGA.url
                    + self.manga.prefix
                    + self.manga.name
                    + OriginEnum.LER_MANGA.chapter_prefix
                    + self.manga.chapter
                    + "/"
            )
            logger.debug(f"Mounted URL: {url}")
            return url

    def chapter_verification(self):
        logger.info(f"Iniciando verificação de capitulo: {self.manga.name} : capitulo {self.manga.chapter}")
        page = 1
        self.url_base = self.mount_url()

        if self.page_verification(page) is not None:
            return True

        self.refill_chapter = not self.refill_chapter
        self.url_base = self.mount_url()

        if self.page_verification(page) is not None:
            return True
        else:
            return False

    def page_verification(self, page):
        url = urljoin(self.url_base, f"{page}{self.manga.extension}")

        if url_verification(url):
            self.manga.page = str(page)
            return url

        for extension_enum in ExtensionEnum:
            url = urljoin(self.url_base, f"{page}{extension_enum.value}")
            if url_verification(url):
                self.manga.page = str(page)
                self.manga.extension = extension_enum.value
                return url
        return None
