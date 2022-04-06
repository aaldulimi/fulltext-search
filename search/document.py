import dataclasses
import datetime


@dataclasses.dataclass
class Document:
    id: int 
    title: str
    url: str
    body: str
    author: str
    datetime: datetime.datetime

    @property
    def fulltext(self):
        return ''.join[self.title, self.body]
