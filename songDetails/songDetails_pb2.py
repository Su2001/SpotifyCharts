# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: songDetails.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11songDetails.proto\"\x97\x01\n\nSongDetail\x12\x0f\n\x07song_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x61rtists\x18\x03 \x01(\t\x12\x0b\n\x03url\x18\x04 \x01(\t\x12\x18\n\x10numtimesincharts\x18\x05 \x01(\x05\x12\x15\n\rnumcountrydif\x18\x06 \x01(\x05\x12\x1a\n\x08\x63omments\x18\x07 \x03(\x0b\x32\x08.Comment\"P\n\x07\x43omment\x12\x12\n\ncomment_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x0f\n\x07song_id\x18\x03 \x01(\x05\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t\"#\n\x15GetSongDetailsRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"3\n\x16GetSongDetailsResponse\x12\x19\n\x04song\x18\x01 \x01(\x0b\x32\x0b.SongDetail2P\n\x0bSongDetails\x12\x41\n\x0eGetSongDetails\x12\x16.GetSongDetailsRequest\x1a\x17.GetSongDetailsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'songDetails_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SONGDETAIL']._serialized_start=22
  _globals['_SONGDETAIL']._serialized_end=173
  _globals['_COMMENT']._serialized_start=175
  _globals['_COMMENT']._serialized_end=255
  _globals['_GETSONGDETAILSREQUEST']._serialized_start=257
  _globals['_GETSONGDETAILSREQUEST']._serialized_end=292
  _globals['_GETSONGDETAILSRESPONSE']._serialized_start=294
  _globals['_GETSONGDETAILSRESPONSE']._serialized_end=345
  _globals['_SONGDETAILS']._serialized_start=347
  _globals['_SONGDETAILS']._serialized_end=427
# @@protoc_insertion_point(module_scope)