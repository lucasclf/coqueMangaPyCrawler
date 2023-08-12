from dataclasses import dataclass


@dataclass
class Manga:
    name: str
    chapter: str
    origin: str
    prefix: str
    page: str = "1"
    extension: str = ".jpg"
