import os
from flask import Flask
from flask import request
from uwaterlooapi import UWaterlooAPI
import json
import requests

uw = UWaterlooAPI( api_key="234279968e219cf1f180a48bf217c318" )
COURSE_BASE_URL = "https://api.uwaterloo.ca/v2/courses/"
KEY = "?key=234279968e219cf1f180a48bf217c318"
URL = "https://api.uwaterloo.ca/v2/courses/{}/{}.json?key=234279968e219cf1f180a48bf217c318"

def get_course_url( dcode, cnum ):
    return COURSE_BASE_URL + dcode + "/" + cnum + ".json" + KEY

def create_app( test_config=None ):
    app = Flask( __name__, instance_relative_config=True )
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile( 'config.py', silent=True )
    else:
        app.config.from_mapping( test_config )

    '''
    If there are or's, we only return the first combination of ands
    '''
    def prerequisite_list( prereqs ):
        ans = []
        for idx, item in enumerate( prereqs ):
            if type( item ) is str:
                ans.append( item )
            elif type( item ) is int:
                if type( prereqs[idx + 1] ) is str:
                    ans += prerequisite_list( [prereqs[idx + 1]] ) 
                else:
                    ans += prerequisite_list( prereqs[idx + 1 ] )
                break
            else:
                ans += prerequisite_list( prereqs[idx] ) 
        return ans

    '''
    Given a course string, returns a tuple of department and code
    '''
    def get_course_info( course ):
        i = 0
        for c in course:
            if c >= '0' and c <= '9':
                break
            i += 1
        return ( course[:i], course[i:] )

    def preprocess_courses( json_data ):
        json_courses_taken = json_data['courses_taken']
        json_courses_to_take = json_data['courses_to_take']

        courses = []
        prerequisites = {}
        terms_offered = {}

        # Map each course to its immediate prerequisites
        for json_course in json_courses_to_take:
            course = json_course['dcode'] + str( json_course['cnum'] )
            courses.append( course )
            course_prerequisites = uw.course_prerequistes( json_course['dcode'], json_course['cnum'] )
            prerequisites[course] = prerequisite_list( course_prerequisites['prerequisites_parsed'] )

        # For all courses ( courses to take and prerequisites ) find the term offered info
        # and put it in a dictionary
        for course in courses:
            course_info = get_course_info( course )
            tList = requests.get( get_course_url( course_info[0], course_info[1] ) ).json()['data']['terms_offered']
            terms_offered[course] = tList 
            for prereq in prerequisites[course]:
                prereq_info = get_course_info( prereq )
                pList = requests.get( get_course_url( prereq_info[0], prereq_info[1] ) ).json()['data']['terms_offered']
                terms_offered[prereq] = pList

        return ( courses, prerequisites, terms_offered )

    @app.route( '/course_planner', methods=['POST'] )
    def course_planner():
        json_data = request.get_json()
        preprocess_courses( json_data )
        return "course_planner"

    return app
