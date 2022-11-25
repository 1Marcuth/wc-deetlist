from typing import Union
import requests

class WebCrawler:
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url = url

    def __request_html(self) -> Union[str, None]:
        response = requests.get(url=self.url)

        status_code = response.status_code

        if status_code == 200:
            return response.text

        else: 
            raise Exception(f"Ocorreu um erro ao fazer a requisição\n> STATUS_CODE: {status_code}")

    def get_html(self) -> str:
        return self.__request_html()

