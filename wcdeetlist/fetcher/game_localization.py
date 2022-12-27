from pydantic import validate_arguments
from pyfilter import FromList
import requests

from ..config import DC_LOCALIZATION_ENDPOINT

class GameLocalization:
    @validate_arguments
    def __init__(
        self,
        language:str
    ) -> None:
        self.__language = language

    def get(self) -> list[dict] | None:
        print("> [localization-fetcher] Coletando dados de localização para tradução de textos e nomes...")

        response = requests.get(DC_LOCALIZATION_ENDPOINT.format(self.__language))

        print("> [localization-fetcher] Coleta concluída | Analizando resposta...")

        if response.status_code == 200:
            return response.json()

        else:
            raise Exception(f"> [localization-fetcher-error] Ocorreu um erro ao fazer a requisção no endpoint de localização.\nSTATUS_CODE: {response.status_code}")

    def get_dict(self) -> dict | None:
        localization = self.get()
        localization_dict = FromList(localization).join_keys_of_child_dicts_in_a_new_dict()

        return localization_dict
