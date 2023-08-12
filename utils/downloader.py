import logging.config
import requests
from utils.file_manager import FileManager

logging.config.fileConfig("./config/logging_config.ini")
logger = logging.getLogger('cqnLogger')


def url_verification(url):
    try:
        logger.debug("Iniciada verificação da URL: %s", url)
        response = requests.get(url)
        status_code = response.status_code

        logger.debug("Status code da URL %s é %s", url, status_code)
        return status_code == 200
    except Exception as e:
        logger.error("Erro ao acessar a URL: %s", e)
        return False


def download_manga(folder_path, manga, url_complete):
    logger.debug("Iniciando download do capitulo %s, pagina %s de %s", manga.chapter, manga.page, manga.name)

    file_name = f"{folder_path}/{str(manga.page).zfill(3)}{manga.extension}"

    try:
        response = requests.get(url_complete, stream=True)
        FileManager.save_file(response, file_name)

    except Exception as e:
        logger.error("Erro ao baixar o capitulo: %s", e)
