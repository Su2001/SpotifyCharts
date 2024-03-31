from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Song(_message.Message):
    __slots__ = ("id", "title", "artists", "rank")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ARTISTS_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    artists: str
    rank: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., artists: _Optional[str] = ..., rank: _Optional[int] = ...) -> None: ...

class GetTopChartsRequest(_message.Message):
    __slots__ = ("date", "country")
    DATE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    date: str
    country: str
    def __init__(self, date: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class GetTopChartsResponse(_message.Message):
    __slots__ = ("songs",)
    SONGS_FIELD_NUMBER: _ClassVar[int]
    songs: _containers.RepeatedCompositeFieldContainer[Song]
    def __init__(self, songs: _Optional[_Iterable[_Union[Song, _Mapping]]] = ...) -> None: ...
