import os
import logging.config
import shutil
import zipfile

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

    @staticmethod
    def zip_file(folder_path, output_zip_name, output_zip_path):

        try:
            with zipfile.ZipFile(os.path.join(output_zip_path, f"{output_zip_name}.cbz"), 'w',
                                 zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder_path))
            logger.info("Compactação concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante a compactação: {e}")

        try:
            shutil.rmtree(folder_path)
            logger.info(f"Deleção da pasta {folder_path} executada com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao excluir a pasta: {e}")


