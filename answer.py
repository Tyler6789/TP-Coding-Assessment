import pandas
import json
import pytest
import calendar

    
with open("data/exercises.json") as json_file:
  exercises = json.load(json_file)
json_file.close()
with open("data/users.json") as json_file:
  users = json.load(json_file)
json_file.close()
with open('data/workouts.json') as json_file:
  workouts = json.load(json_file)
json_file.close()

#create dataframes for use
users_table = pandas.json_normalize(users)
exercises_table = pandas.json_normalize(exercises)
workouts_table = pandas.json_normalize(workouts, record_path=['blocks', 'sets'], meta=['user_id', 'datetime_completed',['blocks', 'exercise_id']])
workouts_table['Total Weight'] = (workouts_table['weight'] * workouts_table['reps'])


questions = {
  # In total, how many pounds have these athletes Bench Pressed?
    "q1": {
        "total_weight": True, 
        "user_name": "all", 
        "exercise_title": "Bench Press",
        "date_start": "2015-01-01",
        "date_end": "2018-12-31",
  },
  # How many pounds did Barry Moore Back Squat in 2016?
    "q2": {
        "total_weight": True, 
        "user_name": "Barry Moore", 
        "exercise_title": "Back Squat",
        "date_start": "2016-01-01",
        "date_end": "2016-12-31",
  },
  # In what month of 2017 did Barry Moore Back Squat the most total weight?
    "q3": {
        "month": True,
        "user_name": "Barry Moore",
        "exercise_title": "Back Squat",
        "date_start": "2017-01-01",
        "date_end": "2017-12-31",

  },

  # What is Abby Smith's Bench Press PR weight?
  # PR defined as the most the person has ever lifted for that exercise, regardless of reps performed.
    "q4": {
        "max_weight_lifted": True,
        "user_name": "Abby Smith",
        "exercise_title": "Bench Press",
        "date_start": "2015-01-01",
        "date_end": "2018-12-31",

    },
  #test question for parameter validation testing
    "q5": {

    }

}


#create pandas dataframe, filtering and sorting data in workouts.json
def get_table_filter(user_id, exercise_id, date_start, date_end):
  table_filter_result = workouts_table.loc[(workouts_table['user_id'] == user_id) & (workouts_table['blocks.exercise_id'] == exercise_id) & (workouts_table['datetime_completed'] >= date_start) & (workouts_table['datetime_completed'] <= date_end) & (workouts_table['reps'] > 0)]
  return table_filter_result
    

#Find highest weight lifted for a single user
def single_user_max_weight(user_id, exercise_id, date_start, date_end):
  table_filter_result = get_table_filter(user_id, exercise_id, date_start, date_end)
  max_weight_lifted = table_filter_result['weight'].max()
  return max_weight_lifted
    
#Total pounds lifted by a single user for any exercise in any date range       
def single_user_weight_sum(user_id, exercise_id, date_start, date_end):
  table_filter_result = get_table_filter(user_id, exercise_id, date_start, date_end)
  return table_filter_result['Total Weight'].sum()
    

#find sum of weight lifted for all users for an exercise in any date range
def all_users_weight_sum(exercise_id, date_start, date_end):
  table_filter_result = workouts_table.loc[(workouts_table['blocks.exercise_id'] == exercise_id) & (workouts_table['datetime_completed'] >= date_start) & (workouts_table['datetime_completed'] <= date_end) & (workouts_table['reps'] > 0)]
  sum_of_weight = table_filter_result['Total Weight'].sum()
  return sum_of_weight


#Find sum of weight lifted by month in date range for a specific exercise and sort it to show the highest monthly total
def user_sum_by_month(user_id, exercise_id, date_start, date_end):
  table_filter_result = get_table_filter(user_id, exercise_id, date_start, date_end)
  month_filter = table_filter_result.sort_values(by='datetime_completed',  ascending=True)
  month_filter['month'] = pandas.DatetimeIndex(month_filter['datetime_completed']).month
  month_filter.index = pandas.to_datetime(month_filter.index)
  final_form = month_filter.groupby(pandas.Grouper(key='month')).sum(numeric_only=True)
  sort_by_weight = final_form.sort_values('weight', ascending=False)
  sort_by_weight['month'] = sort_by_weight.index.values
  sort_by_weight['month name'] = sort_by_weight['month']
  sort_by_weight['month name'] = sort_by_weight['month name'].apply(lambda x: calendar.month_name[x])
  first_row = sort_by_weight.iloc[[0]]
  # print(type(str(first_row['month'].values[0])))
  # print(first_row)
  return first_row['month name'].values[0]

#take input for paramaters
def get_function_by_input(input):
  if input.get("total_weight"):
    if input.get("user_name") == "all":
      return all_users_weight_sum, ["exercise_id", "date_start", "date_end"]
    else:
      return single_user_weight_sum, ["user_id", "exercise_id", "date_start", "date_end"]
  if input.get("max_weight_lifted"):
    if isinstance(input.get("user_name"), str):
      return single_user_max_weight, ["user_id", "exercise_id", "date_start", "date_end"]
  if input.get("month") == True:
    return user_sum_by_month, ["user_id", "exercise_id", "date_start", "date_end"]

#check for inclusion of exercise ID
def is_valid_params(input):
  if not isinstance(input.get("exercise_title"), str):
    return False
  if not isinstance(input.get("user_name"), str):
    return False
  return True

def get_exercise_id(exercise_title):
  exercise_id = exercises_table.loc[(exercises_table['title'] == exercise_title, 'id')]
  exercise_id_index = exercise_id.index[0]
  return exercise_id[exercise_id_index]


def get_user_id(user_name):
  first_name, last_name = user_name.split(" ")
  user_id = users_table.loc[(users_table['name_first'] == first_name, 'id' )]
  user_id_index = user_id.index[0]
  return user_id[user_id_index]


#find and store exercise_id, exercise_id, date_start, and date_end
def format_params(input, func_params):
  formatted_params = {}
  for param in func_params:
    if param == "exercise_id":
      formatted_params["exercise_id"] = get_exercise_id(input.get("exercise_title"))
    if param == "user_id":
      formatted_params["user_id"] = get_user_id(input.get("user_name"))
    if param == "date_start":
      formatted_params["date_start"] = input.get("date_start")
    if param == "date_end":
      formatted_params["date_end"] = input.get("date_end")
  return formatted_params

def answer_questions():
  answers = dict()
  for question, input in questions.items():
    if not is_valid_params(input):
      answers[question] = "Could not answer question. Invalid param entered."
      continue
    func_to_call, func_params = get_function_by_input(input) 
    params = format_params(input, func_params)
    answer = func_to_call(**params)
    answers[question] = answer
  return answers


if "__main__" == __name__:
  answers = answer_questions()
  print(json.dumps(answers, indent=4))





