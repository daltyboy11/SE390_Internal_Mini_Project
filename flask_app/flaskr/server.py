from course import Course
import json
import requests
from uwaterlooapi import UWaterlooAPI
from flask import Flask
from flask import request

app = Flask(__name__)

uw = UWaterlooAPI( api_key="234279968e219cf1f180a48bf217c318" )

@app.route( "/course_planner", methods=['POST'] )
def course_planner():
    json_data = request.get_json()
    plan_courses( json_data['courses_taken'], json_data['courses_to_take'] )
    return "course_planner"


def plan_courses( json_courses_taken, json_courses_to_take ):
    # convert courses_taken_json and json_courses_to_take to array objects of courses
    courses_taken = []
    courses_to_take = []

    for course in json_courses_taken:
        courses_taken.append( Course( course['dcode'], course['cnum'] ) )

    for course in json_courses_to_take:
        courses_taken.append( Course( course['dcode'], course['cnum'] ) )

    prepreocess_courses( courses_taken, courses_to_take )

'''
For each course in courses to take, we use the uw open data api
To get
1. The seasons during which the course is offered
2. The prerequisite courses for the course
'''
def preprocess_courses( courses_taken, courses_to_take ):
    for course in courses_to_take:
        prerequisites = uw.course_prerequisites( course.dept, course.cnum )
        print( prerequisites )
