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


if __name__ == "__main__":
    # Create an instance of ArticleModel
    article = ArticleModel(
        url="https://example.com/article",
        img_url="https://example.com/image.jpg",
        timestamp=datetime.now(),
        title="Example Article",
        topics=["topic1", "topic2"],
        country="Example Country",
        region="Example Region",
        city="Example City",
        source="Example Source",
        summary="This is an example summary."
    )

    # Transform the object to a dictionary
    article_dict = article.dict()

    # Print the dictionary
    print(article_dict)