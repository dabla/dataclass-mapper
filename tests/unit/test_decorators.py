import unittest
from datetime import datetime
from uuid import UUID

from assertpy import assert_that

from tests.unit.fixtures.date_attributes import get_date_attribute, DateAttribute
from tests.unit.fixtures.tags import get_tags, validate_tag, get_tag, Tag
from tests.unit.fixtures.user import get_user, User


class DataMapTestCase(unittest.TestCase):
    def test_datamap_with_date_attribute(
            self,
    ):
        actual = get_date_attribute()

        assert_that(actual).is_type_of(DateAttribute)
        assert_that(actual.id).is_equal_to("b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb")
        assert_that(actual.asset_id).is_equal_to("794d2c0b-efd2-446d-9c18-0be336fd61d9")
        assert_that(actual.system).is_false()
        assert_that(actual.type_name).is_equal_to("Effective End Date")
        assert_that(actual.value).is_equal_to(datetime(2022, 3, 19, 1, 0, 0))
        assert_that(actual.created_by).is_equal_to(
            "00000000-0000-0000-0000-000000900002"
        )
        assert_that(actual.created_on).is_equal_to(
            datetime(2022, 3, 17, 13, 40, 29, 437000)
        )

    def test_datamap_with_tag(
            self,
    ):
        tags = get_tags()

        actual = next(tags)

        assert_that(actual).is_length(2)

        assert_that(actual[0]).is_type_of(Tag)
        assert_that(actual[0].id).is_equal_to(35792)
        assert_that(actual[0].tag).is_equal_to("(LANGUAGE)")
        assert_that(actual[0].is_smart_tag).is_false()
        assert_that(actual[0].color_code).is_equal_to("rgb(83,146,255)")
        assert_that(actual[0].filter).is_equal_to("usertag:\"(LANGUAGE)\"")
        assert_that(actual[0].is_visible).is_true()
        assert_that(actual[0].is_category_model_tag).is_none()

        assert_that(actual[1]).is_type_of(Tag)
        assert_that(actual[1].id).is_equal_to(7956854)
        assert_that(actual[1].tag).is_equal_to("2019 We Are Infrabel - Wave 1")
        assert_that(actual[1].is_smart_tag).is_false()
        assert_that(actual[1].color_code).is_equal_to("rgb(250,163,56)")
        assert_that(actual[1].filter).is_equal_to("usertag:\"2019 We Are Infrabel - Wave 1\"")
        assert_that(actual[1].is_visible).is_false()
        assert_that(actual[1].is_category_model_tag).is_none()

        actual = next(tags)

        assert_that(actual).is_length(2)
        assert_that(actual[0]).is_type_of(Tag)
        assert_that(actual[0].id).is_equal_to(4557288)
        assert_that(actual[0].tag).is_equal_to("3ième voie Bruges-Dudzele")
        assert_that(actual[0].is_smart_tag).is_false()
        assert_that(actual[0].color_code).is_equal_to("rgb(201,78,157)")
        assert_that(actual[0].filter).is_equal_to("usertag:\"3ième voie Bruges-Dudzele\"")
        assert_that(actual[0].is_visible).is_false()
        assert_that(actual[0].is_category_model_tag).is_false()

        assert_that(actual[1]).is_type_of(Tag)
        assert_that(actual[1].id).is_equal_to(300976)
        assert_that(actual[1].tag).is_equal_to("_Info Search")
        assert_that(actual[1].is_smart_tag).is_false()
        assert_that(actual[1].color_code).is_equal_to("rgb(122,140,64)")
        assert_that(actual[1].filter).is_equal_to("usertag:\"_Info Search\"")
        assert_that(actual[1].is_visible).is_false()
        assert_that(actual[1].is_category_model_tag).is_false()

    def test_datamap_with_user(
            self,
    ):
        actual = get_user()

        assert_that(actual).is_type_of(User)
        assert_that(actual.id).is_equal_to(UUID("b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb"))
        assert_that(actual.age).is_zero()
        assert_that(actual.username).is_equal_to("BKD7702")
        assert_that(actual.name).is_equal_to("David")
        assert_that(actual.surname).is_equal_to("Blain")
        assert_that(actual.active).is_true()

    def test_rename_and_remove_dict_keys_on_method_which_has_a_dict_as_an_argument(
            self,
    ):
        data = {"tag": "(LANGUAGE)",
                "id": 35792,
                "is_smarttag": False,
                "color_code": "rgb(83,146,255)",
                "filter": "usertag:\"(LANGUAGE)\"",
                "visible": True,
                "category_model_tag": False
                }

        actual = validate_tag(data, False)

        assert_that(actual).is_equal_to({"tag": "(LANGUAGE)",
                                         "id": 35792,
                                         "is_smart_tag": False,
                                         "color_code": "rgb(83,146,255)",
                                         "filter": "usertag:\"(LANGUAGE)\"",
                                         "is_visible": True,
                                         })

    def test_rename_and_remove_dict_keys_on_method_which_returns_a_dict(
            self,
    ):
        actual = get_tag()

        assert_that(actual).is_equal_to({"tag": "(LANGUAGE)",
                                         "id": 35792,
                                         "is_smart_tag": False,
                                         "color_code": "rgb(83,146,255)",
                                         "filter": "usertag:\"(LANGUAGE)\"",
                                         "is_visible": True,
                                         })
