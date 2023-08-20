import os
import time
import logging.config

from config.config_manga_crawler import ConfigMangaCrawler
from origin_acessor import origin_acessor_factory
from utils import json_manager
from view import user_interface
from threading import Thread

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "config", "logging_config.ini"))
logger = logging.getLogger('cqnLogger')


def start():
    logger.info(os.path.join(os.path.dirname(__file__), "config", "logging_config.ini"))
    start_time = int(time.time() * 1000)
    logger.info("Iniciando operação.")

    json_path = ConfigMangaCrawler.json_path
    file = json_path

    mangas = json_manager.to_manga(file)
    for manga in mangas:
        cycle_start_time = int(time.time() * 1000)
        logger.info(f"Iniciando ciclo para o manga {manga.name}.")

        accessor = origin_acessor_factory.create_accessor(manga.origin)
        accessor.download_manga(manga)
        json_manager.update_json(file, manga)

        cycle_end_time = int(time.time() * 1000)
        cycle_duration = cycle_end_time - cycle_start_time

        logger.info(f"Ciclo para o manga {manga.name} encerrado. Tempo decorrido: {cycle_duration} ms.")

        if ConfigMangaCrawler.script_is_ending:
            logger.info(f"Programa encerrado antecipadamente no capitulo {manga.chapter} do {manga.name}")
            ConfigMangaCrawler.script_is_ending = False
            break

    end_time = int(time.time() * 1000)
    total_time = end_time - start_time
    logger.info(f"Operação encerrada. Tempo total: {total_time} ms.")


if __name__ == "__main__":
    def run_operation():

        while config_ui.process_button["text"] == "Iniciar processo":
            time.sleep(1)
        start()


    config_ui = user_interface.ConfigurationUI()
    operation_thread = Thread(target=run_operation)
    operation_thread.start()
    config_ui.root.mainloop()
    operation_thread.join()
