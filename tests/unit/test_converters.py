import unittest
from dataclasses import Field, fields

from assertpy import assert_that
from mockito import mock

from datamap.converters import identity, resolve_attribute_type_names, resolve_converter, converter_names
from datamap.time import parse_timestamp
from tests.unit.fixtures.date_attributes import DateAttribute


class ConvertersTestCase(unittest.TestCase):
    def test_resolve_attribute_types_when_string_type_as_String(self):
        attribute = mock({"type": "str"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("str")

    def test_resolve_attribute_types_when_optional_string_type_as_string(self):
        attribute = mock({"type": "Optional[str]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("str")

    def test_resolve_attribute_types_when_optional_int_type_as_string(self):
        attribute = mock({"type": "Optional[int]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("int")

    def test_resolve_attributes_type_when_optional_datetime_type_as_string(self):
        attribute = mock({"type": "Optional[datetime]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("datetime")

    def test_resolve_attributes_type_when_optional_date_type_as_string(self):
        attribute = mock({"type": "Optional[date]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("date")

    def test_resolve_attribute_types_when_union_int_type_as_string(self):
        attribute = mock({"type": "Union[int,NoneType]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("int", "NoneType")

    def test_resolve_attribute_types_when_union_with_multiple_types_as_string(self):
        attribute = mock({"type": "Union[Any,NoneType,int]"}, spec=Field)

        actual = resolve_attribute_type_names(attribute)

        assert_that(actual).contains_only("Any", "NoneType", "int")

    def test_resolve_converter_when_field_of_type_string(self):
        field = fields(DateAttribute)[0]

        actual = resolve_converter(field, "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb")

        assert_that(actual).is_same_as(identity)

    def test_resolve_converter_when_field_of_type_datetime(self):
        field = fields(DateAttribute)[7]

        actual = resolve_converter(field, 1647648000000)

        assert_that(actual).is_same_as(parse_timestamp)

    def test_converter_names(self):
        actual = list(converter_names("", ["str", "datetime", "UUID", "Any", "NoneType"]))

        assert_that(actual).contains_only("str_str",
                                          "str_datetime",
                                          "str_uuid",
                                          "str_any",
                                          "str_nonetype",
                                          "str",
                                          "datetime",
                                          "uuid",
                                          "any",
                                          "nonetype")
