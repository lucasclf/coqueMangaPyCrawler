from enums.output_format_enum import OutputFormatEnum


class ConfigMangaCrawler:
    json_path = None
    destiny_path = None
    logs_path = None
    output_format = OutputFormatEnum.CBZ
    script_is_ending = None

    def __init__(self):
        self.destiny_path = ""
        self.json_path = ""
        self.logs_path = ""
        self.script_is_ending = False
