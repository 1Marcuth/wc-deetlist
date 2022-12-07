from pydantic import validate_arguments

from ...config import DC_LOCALIZATION_ENDPOINT

class GameLocalization:
    @validate_arguments()
    def __init__(self, language: str):
        self.__language = language

    def get_dict(self) -> dict:
        pass

    def get(self) -> list[dict]:
        pass
