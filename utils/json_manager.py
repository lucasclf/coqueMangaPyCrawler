import logging.config
import json

from models.manga_model import Manga

logging.config.fileConfig("./config/logging_config.ini")
logger = logging.getLogger('cqnLogger')


def to_manga(json_file):
    manga_list = []

    try:
        with open(json_file, 'r') as reader:
            manga_data_list = json.load(reader)
            for manga_data in manga_data_list:
                manga = Manga(**manga_data)
                manga_list.append(manga)
                logger.debug(f"Loaded manga: {manga.name}")
            return manga_list
    except IOError as ex:
        logger.error(ex)


def update_json(json_file, manga):
    logger.debug(f"Iniciada alteração do jsonFile, alteração do {manga.name} para capitulo {manga.chapter}")
    try:
        with open(json_file, 'r') as reader:
            manga_list = json.load(reader)

        for item in manga_list:
            if item['name'] == manga.name:
                item['chapter'] = manga.chapter
                break

        with open(json_file, 'w') as writer:
            json.dump(manga_list, writer, indent=4)

        logger.debug("Arquivo JSON modificado com sucesso!")
    except IOError as e:
        logger.error(e)
