import dataclasses
import datetime


@dataclasses.dataclass
class Document:
    id: int 
    title: str
    author: str
    body: str
    datetime: datetime.datetime
    url: str

    @property
    def fulltext(self):
        return ''.join[self.title, self.body]
