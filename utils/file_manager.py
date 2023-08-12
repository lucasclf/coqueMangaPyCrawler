import os
import logging.config

from config.config_manga_crawler import ConfigMangaCrawler

logging.config.fileConfig("./config/logging_config.ini")
logger = logging.getLogger('cqnLogger')


class FileManager:
    @staticmethod
    def create_folder_and_get_path(folder_name):
        logger.debug("Iniciando criação da pasta: %s", folder_name)
        complete_folder_path = ConfigMangaCrawler.destiny_path + "/" + folder_name

        try:
            folder_path = os.path.join(os.getcwd(), complete_folder_path)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.debug("Pasta criada em: %s", folder_path)
                return folder_path
            else:
                logger.debug("Pasta %s já existe.", folder_path)
                return folder_path

        except Exception as e:
            logger.error("Error creating folder:", e)
            return None  # Or raise an exception

    @staticmethod
    def save_file(response, file_name):
        try:
            with open(file_name, "wb") as file:
                file.write(response.content)

            logger.info(f"{file_name} salvo com sucesso.")

        except Exception as e:
            raise RuntimeError(e)
