from setuptools import setup

with open("README.md", "r") as readme_bf:
    readme_content = readme_bf.read()

setup(
    name="wcdeetlist",
    version="0.0.0.3.8",
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
        "wcdeetlist/parser",
        "wcdeetlist/parser/islands/heroic_race",
        "wcdeetlist/parser/items",
    ],
    install_requires=["requests", "bs4"],
)