from setuptools import setup

with open("README.md", "r") as readme_file:
    readme_content = readme_file.read()

setup(
    name="wcdeetlist",
    version="0.0.0.4.1",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="scrapper scraper crawler deetlist",
    description=u"Web Crawler for https://deetlist.com",
    packages=[
        "wcdeetlist",
        "wcdeetlist/crawler",
        "wcdeetlist/crawler/islands",
        "wcdeetlist/crawler/items",
        "wcdeetlist/crawler/items/dragon",
        "wcdeetlist/parser",
        "wcdeetlist/parser/islands/heroic_race",
        "wcdeetlist/parser/items",
        "wcdeetlist/parser/items/dragon",
        "wcdeetlist/tools"
    ],
    install_requires=["requests", "bs4", "pydantic"],
)