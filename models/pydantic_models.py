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
    img_url: Optional[AnyUrl]
    timestamp: datetime
    title: Optional[str]
    topics: List[TopicModel]
    country: Optional[CountryModel]
    region: Optional[RegionModel]
    city: Optional[CityModel]
    source: NewspaperModel
    summary: Optional[str]

    class Config:
        from_attributes = True  # Allows compatibility with MongoEngine Document
