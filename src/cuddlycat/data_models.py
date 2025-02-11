import pydantic
import typing


class Business(pydantic.BaseModel):
    """
    Represents a business entity with its details and matching information.

    Attributes:
        business_name (str): The original name of the business.
        matched_name (str): The name matched in a directory or search.
        yelp_url (Optional[str]): The Yelp URL for the business, if available.
        message (str): A description of the matching process or status.
        uuid (str): A unique identifier for the business entry.
    """

    business_name: str = pydantic.Field(..., description="Original business name")
    matched_name: str = pydantic.Field(default="", description="Matched business name")
    yelp_url: typing.Optional[str] = pydantic.Field(
        default="", description="Yelp business page URL"
    )
    message: str = pydantic.Field(..., description="Matching or status message")
    uuid: str = pydantic.Field(..., description="Unique identifier")


class PageContent(pydantic.BaseModel):
    """
    Represents the content of a web page.

    Attributes:
        encoding (str): The character encoding of the page content.
        mimeType (str): The MIME type of the content.
        data (str): The actual content of the page.
    """

    encoding: str
    mimeType: str
    data: str


class PageMetadata(pydantic.BaseModel):
    """
    Represents metadata about a web page.

    Attributes:
        url (str): The URL of the page.
        title (str): The title of the page.
        timestamp (str): A timestamp associated with the page.
        savedAt (str): When the page was saved.
        uuid (str): A unique identifier for the page.
    """

    url: str
    title: str
    timestamp: str
    savedAt: str
    uuid: str


class PageData(pydantic.BaseModel):
    """
    Combines metadata and content for a complete page representation.

    Attributes:
        metadata (PageMetadata): Metadata about the page.
        content (PageContent): Content of the page.
    """

    metadata: PageMetadata
    content: PageContent
