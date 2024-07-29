from pydantic import BaseModel, AnyUrl
from typing import List, Optional
from datetime import datetime


# Corresponding Pydantic model for Article
class ArticleModel(BaseModel):
    url: AnyUrl
    img_url: AnyUrl
    timestamp: datetime
    title: str
    topics: List[str]
    country: Optional[str]
    region: Optional[str]
    city: Optional[str]
    # # source: NewspaperModel
    source: str
    summary: str


def convert_article_to_pydantic(article):
    return ArticleModel(
        url=article.url,
        img_url=article.img_url if article.img_url else "",
        timestamp=article.timestamp,
        title=article.title,
        topics=[topic.name for topic in article.topics],
        country=article.country.name if article.country else None,
        region=article.region.name if article.region else None,
        city=article.city.name if article.city else None,
        # TODO: # source=NewspaperModel(id=str(article.source.id), name=article.source.name, root_url=article.source.root_url),
        source=article.source,
        summary=article.summary,
    )
