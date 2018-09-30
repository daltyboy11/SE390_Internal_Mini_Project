import pprint                           # pretty printing
from flask import Flask                 # flask app
from flask import request               # flask app
from uwaterlooapi import UWaterlooAPI   # UWaterloo Open Data API
import json
import requests

pp = pprint.PrettyPrinter( indent=4 )
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
                if type( prereqs[len( prereqs ) - 1] ) is str:
                    ans += prerequisite_list( [prereqs[len( prereqs ) - 1]] ) 
                else:
                    ans += prerequisite_list( prereqs[len( prereqs ) - 1] )
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

    '''
    Regular track means non-advanced course. E.g. CS 145 would be transformed to CS 135.
    Non advanced courses are left untouched
    '''
    def get_regular_track_course( course ):
        dcode, cnum = get_course_info( course )
        if ( dcode != "CS" and dcode != "MATH" ):
            return course
        cnum = int( cnum )
        if cnum == 145 or \
        cnum == 146 and dcode == "MATH" or \
        cnum == 147 and dcode == "MATH" or \
        cnum == 148 and dcode == "MATH" or \
        cnum == 245 and dcode == "MATH" or \
        cnum == 247 and dcode == "MATH" or \
        cnum == 249 and dcode == "MATH":
            return dcode + str( cnum - 10 )
        return course

    def get_all_prereqs( prerequisites ):
        while True:
            needsRefresh = False
            prereq_prereqs = {}
            for course, course_prereqs in prerequisites.items():
                # Skip over courses with no prerequisites
                if len( course_prereqs ) == 0:
                    continue
                # We need to find the prerequisites for our prerequisites
                # For each prerequisite, if we do not have its prerequisites
                # Then add its prerequisites to the dictionary using the
                # uw open data api
                for prereq in course_prereqs:
                    if prereq in prerequisites:
                        continue
                    needsRefresh = True
                    prereq_info = get_course_info( prereq )
                    prereq_prerequisites = uw.course_prerequistes( prereq_info[0], prereq_info[1] )
                    prereq_prerequisites_parsed = [ get_regular_track_course( x ) for x in prerequisite_list( prereq_prerequisites.get('prerequisites_parsed', [] ) ) ]
                    prereq_prereqs[prereq] = prereq_prerequisites_parsed

            if not needsRefresh:
                break

            for prereq, prereq_list in prereq_prereqs.items():
                prerequisites[prereq] = prereq_list
        
    def preprocess_courses( json_data ):
        json_courses_taken = json_data['courses_taken']
        json_courses_to_take = json_data['courses_to_take']

        courses_taken = []
        courses = []
        prerequisites = {}
        terms_offered = {}

        for json_course in json_courses_taken:
            courses_taken.append( get_regular_track_course( json_course['dcode'] + str( json_course['cnum'] ) ) )
            
        for json_course in json_courses_to_take:
            course = json_course['dcode'] + str( json_course['cnum'] )
            courses.append( course )
            course_prerequisites = uw.course_prerequistes( json_course['dcode'], json_course['cnum'] )
            parsed_course_prerequisites = prerequisite_list( course_prerequisites['prerequisites_parsed'] )
            prerequisites[course] = [ get_regular_track_course( x ) for x in prerequisite_list( parsed_course_prerequisites ) ]
            get_all_prereqs( prerequisites )

        for key, value in prerequisites.items():
            dcode, cnum = get_course_info( key )
            terms_offered[key] = requests.get( get_course_url( dcode, cnum ) ).json()['data']['terms_offered']

        print()
        print( "Courses Taken" )
        pp.pprint( courses_taken )
        print( "Courses to Take" )
        pp.pprint( courses )
        print( "All Prerequisites" )
        pp.pprint( prerequisites )
        print( "Terms offered" )
        pp.pprint( terms_offered )
        return ( courses, prerequisites, terms_offered )

    @app.route( '/course_planner', methods=['POST'] )
    def course_planner():
        json_data = request.get_json()
        courses, prerequisites, terms_offered = preprocess_courses( json_data )
        return "course_planner"

    return app
