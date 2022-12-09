from bs4 import BeautifulSoup
from typing import List, Union
from datetime import datetime

from ....config import (
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    DRAGON_ELEMENTS,
    DRAGON_RARITYS
)

def attack_training_time_to_seconds(attack_training_time: str) -> int:
        if "hours" in attack_training_time:
            if attack_training_time == "24 hours":
                return 24 * SECONDS_PER_HOUR

            hours = datetime.strptime(attack_training_time, "%H hours").hour

            return hours * SECONDS_PER_HOUR
        
        elif "days" in attack_training_time:
            days = datetime.strptime(attack_training_time, "%d days").day

            return days * SECONDS_PER_DAY

def summon_or_breed_time_to_secounds(summon_or_breed_time: str):
    time = summon_or_breed_time.split(":")[1].split("(")[1].removesuffix(")")

    if "Hours" in summon_or_breed_time:
        hours = int(time.removesuffix(" Hours"))
        return hours * SECONDS_PER_HOUR

    elif "hr" in summon_or_breed_time and "min" in summon_or_breed_time:
        times = datetime.strptime(time, "%Hhr %Mmin")
        hours = times.hour
        minutes = times.minute

        return (minutes * SECONDS_PER_MINUTE) + (hours * SECONDS_PER_HOUR)

    else:
        raise Exception("Valor inesperado em summon or breed time")


class DragonPageParser:
    def __init__(self, page_html: str | bytes) -> None:
        self.__page_soup = BeautifulSoup(page_html, "html.parser")

    def get_name(self) -> str:
        name = self.__page_soup.select_one("h1").text
        return name

    def get_rarity(self) -> str:
        rarity_img = self.__page_soup.select_one("div.img_rar")
        rarity = rarity_img.attrs["class"][0].split("_")[2].upper()
        return rarity

    def get_elements(self) -> List[str]:
        elements_soup = self.__page_soup.select("#typ_hull .typ_i")

        elements = []

        for element_soup in elements_soup:
            abbreviated_element_name = element_soup.attrs["class"][1].split("_")[1]
            elements.append(DRAGON_ELEMENTS[abbreviated_element_name])

        return elements

    def get_image_url(self) -> str:
        image_url = self.__page_soup.select_one("img.drg_img").attrs["src"].replace("../", "https://deetlist.com/dragoncity/")
        return image_url

    def get_description(self) -> str:
        bio_soup = self.__page_soup.select_one("div#self_bio")

        description = bio_soup.text.split("\n")[2].replace("Description:", "").strip()

        return description

    def get_basic_attacks(self) -> List[dict]:
        basic_attacks_soup = self.__page_soup.select("p.brtext+ div.b_split div.att_hold")

        basic_attacks = []

        for basic_attack_soup in basic_attacks_soup:
            name = basic_attack_soup.text.split("\n")[2].strip()
            element = basic_attack_soup.text.split("\n")[3].split("|")[1].strip()
            damege = basic_attack_soup.text.split("\n")[3].split("|")[0].removeprefix("Damage:").strip()

            if damege.isnumeric():
                damege = int(damege)

            else:
                damege = None

            basic_attacks.append({
                "name": name,
                "element": element,
                "damege": damege,
            })

        return basic_attacks

    def get_trainable_attacks(self) -> List[dict]:
        trainable_attacks_soup = self.__page_soup.select("div.b_split+ div.b_split div.att_hold")

        trainable_attacks = []

        for trainable_attack_soup in trainable_attacks_soup:
            name = trainable_attack_soup.text.split("\n")[2].strip()
            element = trainable_attack_soup.text.split("\n")[3].split("|")[1].strip()
            damege = trainable_attack_soup.text.split("\n")[3].split("|")[0].replace("Damage:", "").strip()
            training_time = attack_training_time_to_seconds(trainable_attack_soup.text.split("\n")[3].split("|")[2].strip())

            if damege.isnumeric():
                damege = int(damege)

            else:
                damege = None

            trainable_attacks.append({
                "name": name,
                "element": element,
                "damege": damege,
                "training_time": training_time
            })

        return trainable_attacks

    def get_strengths(self) -> List[str]:
        strengths_soup = self.__page_soup.select(".spc2+ .b_split .typ_i")

        strengths = [ strength.attrs["class"][1].removeprefix("tb_") for strength in strengths_soup ]

        for i, strength in enumerate(strengths):
            if strength in DRAGON_ELEMENTS:
                strengths[i] = DRAGON_ELEMENTS[strength]

        return strengths

    def get_weaknesses(self) -> List[str]:
        weaknesses_soup = self.__page_soup.select(".b_split+ .b_split .typ_i")

        weaknesses = [ weakness.attrs["class"][1].removeprefix("tb_") for weakness in weaknesses_soup ]

        for i, weakness in enumerate(weaknesses):
            if weakness in DRAGON_ELEMENTS:
                weaknesses[i] = DRAGON_ELEMENTS[weakness]

        return weaknesses

    def get_book_id(self) -> int | None:
        id = self.__page_soup.select_one("#did .dt").text
        
        if id != "":
            return int(id)

    def get_category(self) -> int:
        return int(self.__page_soup.select_one("#dc .dt").text)

    def get_is_breedable(self) -> bool:
        return self.__page_soup.select_one("#br .dt").text == "Yes"

    def get_summmon_breed_time(self) -> int:
        return summon_or_breed_time_to_secounds(self.__page_soup.select_one("#bt").text)

    def get_buy_price(self) -> dict:####
        return {

        }

    def get_hatch_time(self) -> int:####
        return

    def get_xp_on_hatch(self) -> int:####
        return

    def get_release_date(self) -> int:####
        return

    def get_sell_price(self) -> int:####
        return {
            
        }

    def get_starting_income_of_gold(self) -> int:####
        return

    def get_all(self) -> dict:###
        return {
            "name": self.get_name(),
            "rarity": self.get_rarity(),
            "elements": self.get_elements(),
            "image_url": self.get_image_url(),
            "description": self.get_description(),
            "attacks": {
                "basic": self.get_basic_attacks(),
                "trainable": self.get_trainable_attacks(),
            },
            "strengths": self.get_strengths(),
            "weaknesses": self.get_weaknesses(),
            "book_id": self.get_book_id(),
            "category": self.get_category(),
            "is_breedable": self.get_is_breedable(),
        }
