import pytest
import json

with open("data/exercises.json") as json_file:
  exercises = json.load(json_file)
json_file.close()
with open("data/users.json") as json_file:
  users = json.load(json_file)
json_file.close()
with open('data/workouts.json') as json_file:
  workouts = json.load(json_file)
json_file.close()

from answer import *


def test_single_user_max_weight():
    assert single_user_max_weight(29891, 568, '2018-03-05', '2018-03-06') == 160.0

def test_single_user_weight_sum():
    assert single_user_weight_sum(29891, 568, '2018-03-05', '2018-03-06') == 2420.0

def test_all_users_weight_sum():
    assert all_users_weight_sum(568, '2018-03-05', '2018-03-06') == 2420.0

def test_user_sum_by_month():
    assert user_sum_by_month(22677,326,'2017-01-01', '2017-12-31') == 'March'

def test_get_exercise_id():
    assert get_exercise_id('Bench Press') == 568

def test_user_id():
    assert get_user_id("Abby Smith") == 5101


