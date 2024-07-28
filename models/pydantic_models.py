from pydantic import BaseModel, AnyUrl
from typing import List, Optional
from datetime import datetime


# Assuming these are the minimal definitions for related models
class TopicModel(BaseModel):
    id: str  # assuming an ObjectId or some unique identifier
    name: str


class CountryModel(BaseModel):
    id: str
    name: str


class RegionModel(BaseModel):
    id: str
    name: str
    country: CountryModel


class CityModel(BaseModel):
    id: str
    name: str
    country: CountryModel
    region: Optional[RegionModel]


class NewspaperModel(BaseModel):
    id: str
    name: str
    root_url: str


# Corresponding Pydantic model for Article
class ArticleModel(BaseModel):
    url: AnyUrl
    img_url: AnyUrl
    timestamp: datetime
    title: str
    topics: List[str]
    # country: Optional[CountryModel]
    # region: Optional[RegionModel]
    # city: Optional[CityModel]
    # # source: NewspaperModel
    # source: str
    # summary: Optional[str]


def convert_article_to_pydantic(article):
    return ArticleModel(
        url=article.url,
        img_url=article.img_url if article.img_url else "",
        timestamp=article.timestamp,
        title=article.title,
        topics=[topic.name for topic in article.topics],
        # country=CountryModel(id=str(article.country.id), name=article.country.name) if article.country else None,
        # region=RegionModel(
        #     id=str(article.region.id),
        #     name=article.region.name,
        #     country=CountryModel(id=str(article.region.country.id), name=article.region.country.name)
        # ) if article.region else None,
        # city=CityModel(
        #     id=str(article.city.id),
        #     name=article.city.name,
        #     country=CountryModel(id=str(article.city.country.id), name=article.city.country.name),
        #     region=RegionModel(
        #         id=str(article.city.region.id),
        #         name=article.city.region.name,
        #         country=CountryModel(id=str(article.city.region.country.id), name=article.city.region.country.name)
        #     ) if article.city.region else None
        # ) if article.city else None,
        # # source=NewspaperModel(id=str(article.source.id), name=article.source.name, root_url=article.source.root_url),
        # source=article.source,
        # summary=article.summary
    )
