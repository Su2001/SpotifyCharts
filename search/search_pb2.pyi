from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Song(_message.Message):
    __slots__ = ("id", "title", "artists")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ARTISTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    artists: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., artists: _Optional[str] = ...) -> None: ...

class GetSearchRequest(_message.Message):
    __slots__ = ("songname",)
    SONGNAME_FIELD_NUMBER: _ClassVar[int]
    songname: str
    def __init__(self, songname: _Optional[str] = ...) -> None: ...

class GetSearchResponse(_message.Message):
    __slots__ = ("songs",)
    SONGS_FIELD_NUMBER: _ClassVar[int]
    songs: _containers.RepeatedCompositeFieldContainer[Song]
    def __init__(self, songs: _Optional[_Iterable[_Union[Song, _Mapping]]] = ...) -> None: ...
