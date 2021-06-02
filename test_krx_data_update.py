import pytest

import krx_data_update


data = {"3S": {"종가": {"2020-01-01": 2000.0}, "시가": {"20201-01-01": 2010.0}}}
new_data = {"3S": {"종가": {"2020-01-02": 2020.0}, "시가": {"20201-01-02": 2010.0}}}
merged_data = {
    "3S": {
        "종가": {"2020-01-01": 2000.0, "2020-01-02": 2020.0},
        "시가": {"20201-01-01": 2010.0, "20201-01-02": 2010.0},
    }
}
item_name = "3S"


def test_load_data():
    data = krx_data_update.get_data("3S")
    assert list(data.keys())[0] == "3S"


def test_is_new_item_False():
    assert krx_data_update.is_new_item("3S") == False


def test_is_new_item_True():
    assert krx_data_update.is_new_item("Google") == True


def test_get_latest_data():
    assert krx_data_update.get_latest_date(data, item_name) == "20200101"


def test_merge_data():
    assert krx_data_update.merge_data(new_data, data, item_name) == merged_data
