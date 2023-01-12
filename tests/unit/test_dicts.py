import unittest
from datetime import datetime

from assertpy import assert_that

import tests
from datamapper.dicts import flatten_dict, from_dicts, rename_keys, remove_keys, from_collection, from_iterable, from_dict
from tests.unit.fixtures.date_attributes import DateAttribute
from tests.unit.fixtures.mentions import Mentions

ASSET_NAME = "2022-03-17 #1"
TYPE_NAME = "Effective End Date"


class DictTestCase(unittest.TestCase):
    def test_flatten_dict_when_value_contains_nested_dicts_then_flatten_those(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = flatten_dict(value)

        assert_that(actual).is_equal_to(
            {
                "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
                "createdBy": "00000000-0000-0000-0000-000000900002",
                "createdOn": 1647520829437,
                "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
                "lastModifiedOn": 1647520829438,
                "system": False,
                "resourceType": "DateAttribute",
                "typeId": "00000000-0000-0000-0000-000000000254",
                "typeResourceType": "DateAttributeType",
                "typeName": TYPE_NAME,
                "assetId": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "assetResourceType": "Asset",
                "assetName": ASSET_NAME,
                "value": 1647648000000,
            }
        )

    def test_from_dicts_when_module_where_dataclass_can_be_loaded_is_specified(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = from_dicts(value, module=tests.unit.fixtures.date_attributes, flatten=True)

        assert_that(actual).is_type_of(DateAttribute)
        assert_that(actual.id).is_equal_to("b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb")
        assert_that(actual.asset_id).is_equal_to("794d2c0b-efd2-446d-9c18-0be336fd61d9")
        assert_that(actual.system).is_false()
        assert_that(actual.asset_name).is_equal_to(ASSET_NAME)
        assert_that(actual.type_name).is_equal_to(TYPE_NAME)
        assert_that(actual.value).is_equal_to(datetime(2022, 3, 19, 1, 0, 0))
        assert_that(actual.created_by).is_equal_to(
            "00000000-0000-0000-0000-000000900002"
        )
        assert_that(actual.created_on.date()).is_equal_to(datetime.now().date())

    def test_from_dicts_when_dataclass_is_specified(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
            },
            "value": 1647648000000,
        }

        actual = from_dicts(value, data_class=DateAttribute, flatten=True)

        assert_that(actual).is_type_of(DateAttribute)
        assert_that(actual.id).is_equal_to("b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb")
        assert_that(actual.asset_id).is_equal_to("794d2c0b-efd2-446d-9c18-0be336fd61d9")
        assert_that(actual.system).is_false()
        assert_that(actual.asset_name).is_none()
        assert_that(actual.type_name).is_equal_to(TYPE_NAME)
        assert_that(actual.value).is_equal_to(datetime(2022, 3, 19, 1, 0, 0))
        assert_that(actual.created_by).is_equal_to(
            "00000000-0000-0000-0000-000000900002"
        )
        assert_that(actual.created_on).is_equal_to(
            datetime(2022, 3, 17, 13, 40, 29, 437000)
        )

    def test_from_dicts_when_dataclass_is_specified_with_overriden_converter(
        self,
    ):
        value = {
            "id": "43769358878509009",
            "unique_id": "46283_43769358878509009",
            "message": {"language": "fr", "sentiment": "negative"},
            "source": {
                "category": "social",
                "type": "SearchProviderTwitter",
                "service": "twitter",
                "id": "1592974618012573697",
                "domain": "twitter.com",
                "in_reply_to_message_id": "1592772575729700865",
            },
            "topic": {"id": 46283, "name": "CEO's"},
            "project": {"id": 3013, "name": "Politicians"},
            "status": "new",
            "permalink": "https://app.engagor.com/messages/1417/permalink/46283/43769358878509009/",
            "handled_by": None,
            "actions": [],
            "action_links": [
                {
                    "key": "reply",
                    "type": "web",
                    "name": "Reply",
                    "title": "Reply to this tweet",
                    "link": "https://app.engagor.com/inbox/1417/publish/twitter/reply/46283/43769358878509009",
                },
                {
                    "key": "reply",
                    "type": "api",
                    "link": "https://api.engagor.com/1417/publisher/add/?type=reply&topic_id=46283&mention_id=43769358878509009",
                    "http_method": "POST",
                },
            ],
            "date": {"added": 1668629719},
            "tags": ["FR"],
            "timestamps": {"handle_time": 0},
            "author": {"id": 3313939576, "managed": False},
            "original_author": {"id": 3214031521},
            "assignment": {"user_ids": [], "team_ids": [], "comments": ""},
            "assignees": [],
        }

        actual = from_dicts(value, data_class=Mentions, flatten=True)

        assert_that(actual).is_type_of(Mentions)
        assert_that(actual.unique_id).is_equal_to("46283_43769358878509009")
        assert_that(actual.id).is_equal_to("43769358878509009")
        assert_that(actual.author_id).is_equal_to(3313939576)
        assert_that(actual.original_author_id).is_equal_to(3214031521)
        assert_that(actual.message_title).is_none()
        assert_that(actual.message_content).is_none()
        assert_that(actual.message_language).is_equal_to("fr")
        assert_that(actual.message_sentiment).is_equal_to("negative")
        assert_that(actual.message_type).is_none()
        assert_that(actual.source_category).is_equal_to("social")
        assert_that(actual.source_service).is_equal_to("twitter")
        assert_that(actual.source_type).is_equal_to("SearchProviderTwitter")
        assert_that(actual.source_id).is_equal_to("1592974618012573697")
        assert_that(actual.source_in_reply_to_message_id).is_equal_to("1592772575729700865")
        assert_that(actual.source_domain).is_equal_to("twitter.com")
        assert_that(actual.source_url).is_none()
        assert_that(actual.source_application).is_none()
        assert_that(actual.source_profile).is_none()
        assert_that(actual.source_profile_name).is_none()
        assert_that(actual.location_continent_code).is_none()
        assert_that(actual.location_country_code).is_none()
        assert_that(actual.location_city).is_none()
        assert_that(actual.location_region).is_none()
        assert_that(actual.location_longitude).is_none()
        assert_that(actual.location_latitude).is_none()
        assert_that(actual.topic_id).is_equal_to(46283)
        assert_that(actual.project_id).is_equal_to(3013)
        assert_that(actual.status).is_equal_to("new")
        assert_that(actual.permalink).is_equal_to("https://app.engagor.com/messages/1417/permalink/46283/43769358878509009/")
        assert_that(actual.assignment_comment).is_none()
        assert_that(actual.response_time_seconds).is_none()
        assert_that(actual.response_time_seconds_during_bh).is_none()
        assert_that(actual.resolve_time_seconds).is_none()
        assert_that(actual.resolve_time_seconds_during_bh).is_none()
        assert_that(actual.handle_time_seconds).is_none()
        assert_that(actual.date_added).is_equal_to(datetime(2022, 11, 16, 21, 15, 19))
        assert_that(actual.date_published).is_none()

    def test_from_dicts_when_nothing_is_specified(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = from_dicts(value, flatten=True)

        assert_that(actual).is_equal_to(
            {
                "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
                "created_by": "00000000-0000-0000-0000-000000900002",
                "created_on": 1647520829437,
                "last_modified_by": "00000000-0000-0000-0000-000000900002",
                "last_modified_on": 1647520829438,
                "system": False,
                "resource_type": "DateAttribute",
                "type_id": "00000000-0000-0000-0000-000000000254",
                "type_resource_type": "DateAttributeType",
                "type_name": TYPE_NAME,
                "asset_id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "asset_resource_type": "Asset",
                "asset_name": ASSET_NAME,
                "value": 1647648000000,
            }
        )

    def test_from_dicts_with_iterable_when_nothing_is_specified(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = next(iter(from_dicts(iter([value]), flatten=True)))

        assert_that(actual).is_equal_to(
            {
                "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
                "created_by": "00000000-0000-0000-0000-000000900002",
                "created_on": 1647520829437,
                "last_modified_by": "00000000-0000-0000-0000-000000900002",
                "last_modified_on": 1647520829438,
                "system": False,
                "resource_type": "DateAttribute",
                "type_id": "00000000-0000-0000-0000-000000000254",
                "type_resource_type": "DateAttributeType",
                "type_name": TYPE_NAME,
                "asset_id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "asset_resource_type": "Asset",
                "asset_name": ASSET_NAME,
                "value": 1647648000000,
            }
        )

    def test_from_dicts_with_list_when_nothing_is_specified(
        self,
    ):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = next(iter(from_dicts([value], flatten=True)))

        assert_that(actual).is_equal_to(
            {
                "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
                "created_by": "00000000-0000-0000-0000-000000900002",
                "created_on": 1647520829437,
                "last_modified_by": "00000000-0000-0000-0000-000000900002",
                "last_modified_on": 1647520829438,
                "system": False,
                "resource_type": "DateAttribute",
                "type_id": "00000000-0000-0000-0000-000000000254",
                "type_resource_type": "DateAttributeType",
                "type_name": TYPE_NAME,
                "asset_id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "asset_resource_type": "Asset",
                "asset_name": ASSET_NAME,
                "value": 1647648000000,
            }
        )

    def test_rename_keys_without_suppressing_none_values(self):
        value = {
            'name': 'Charles Brown',
            'id': 'cobblehillblog.com',
            'img': 'https://app.engagor.com/global/img/icon/sources/source-blogs-60.png',
            'managed': False
        }

        actual = rename_keys(value, ("id", "service_id"), ("img", "image_url"), ("fullname", "full_name"))

        assert_that(actual).is_equal_to(
            {
                'name': 'Charles Brown',
                'full_name': None,
                'service_id': 'cobblehillblog.com',
                'image_url': 'https://app.engagor.com/global/img/icon/sources/source-blogs-60.png',
                'managed': False
            }
        )

    def test_rename_keys_with_suppressing_none_values(self):
        value = {
            'name': 'Charles Brown',
            'id': 'cobblehillblog.com',
            'img': 'https://app.engagor.com/global/img/icon/sources/source-blogs-60.png',
            'managed': False
        }

        actual = rename_keys(value, ("id", "service_id"), ("img", "image_url"), ("fullname", "full_name"), suppress_none=True)

        assert_that(actual).is_equal_to(
            {
                'name': 'Charles Brown',
                'service_id': 'cobblehillblog.com',
                'image_url': 'https://app.engagor.com/global/img/icon/sources/source-blogs-60.png',
                'managed': False
            }
        )

    def test_rename_keys_when_illegal_argument(self):
        with self.assertRaises(AttributeError) as context:
            rename_keys(["value"], ("id", "service_id"), ("img", "image_url"), ("fullname", "full_name"))

        assert_that(str(context.exception)).is_equal_to("Invalid argument type list passed as data, expected a dict!")

    def test_remove_keys(self):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = remove_keys(value, "system", "resourceType")

        assert_that(actual).is_equal_to(
            {
                "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
            }
        )

    def test_remove_keys_when_no_matching_keys(self):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = remove_keys(value, "resource_type", "asset_id")

        assert_that(actual).is_equal_to(value)

    def test_remove_keys_when_no_data(self):
        actual = remove_keys(None, "resource_type", "asset_id")

        assert_that(actual).is_none()

    def test_remove_keys_when_no_keys_to_remove_passed_then_do_nothing(self):
        value = {
            "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
            "createdBy": "00000000-0000-0000-0000-000000900002",
            "createdOn": 1647520829437,
            "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
            "lastModifiedOn": 1647520829438,
            "system": False,
            "resourceType": "DateAttribute",
            "type": {
                "id": "00000000-0000-0000-0000-000000000254",
                "resourceType": "DateAttributeType",
                "name": TYPE_NAME,
            },
            "asset": {
                "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
                "resourceType": "Asset",
                "name": ASSET_NAME,
            },
            "value": 1647648000000,
        }

        actual = remove_keys(value)

        assert_that(actual).is_same_as(value)

    def test_remove_keys_when_illegal_argument(self):
        with self.assertRaises(AttributeError) as context:
            remove_keys(["value"], "resource_type", "asset_id")

        assert_that(str(context.exception)).is_equal_to("Invalid argument type list passed as data, expected a dict!")

    def test_from_dict_when_illegal_argument_passed_then_raise_attribute_error(self):
        with self.assertRaises(AttributeError) as context:
            from_dict(["value"])

        assert_that(str(context.exception)).is_equal_to("Invalid argument type list passed as data, expected a dict!")

    def test_from_collection_when_illegal_argument_passed_then_raise_attribute_error(self):
        with self.assertRaises(AttributeError) as context:
            from_collection({})

        assert_that(str(context.exception)).is_equal_to("Invalid argument type dict passed as data, expected a collection!")

    def test_from_iterable_when_illegal_argument_passed_then_raise_attribute_error(self):
        with self.assertRaises(AttributeError) as context:
            from_iterable({})

        assert_that(str(context.exception)).is_equal_to("Invalid argument type dict passed as data, expected an iterable which isn't a collection!")
