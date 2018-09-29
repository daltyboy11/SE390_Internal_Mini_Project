import sys
sys.path.append('../')
from flaskr import create_app
from flaskr import utility

def test_config():
    assert not create_app().testing
    assert create_app( { 'TESTING' : True } ).testing

def test_course_planner( client ):
    json_data = {
                "courses_taken" : [ { "dcode" : "CS", "cnum" : 135 },
                                    { "dcode" : "CS", "cnum" : 136 }],

                "courses_to_take" : [ { "dcode" : "CS", "cnum" : 241 },
                                      { "dcode" : "CS", "cnum" : 348 },
                                      { "dcode" : "CS", "cnum" : 341 }],

                "term_to_start_planning" : { "season" : "F", "year" : 2019 }
                } 
    
    r = client.post( '/course_planner', json=json_data )
    assert True

def test_top_sort1():
    courses = [
        [ "CS248", ["CS138"] ],
        [ "CS138", [] ],
        [ "CS400", ["CS340"] ],
        [ "CS241", ["CS138"] ],
        [ "CS340", ["CS248", "CS240"] ],
        [ "CS240", [] ]
    ]
    stack = utility.top_sort(courses)
    assert stack == ['CS138', 'CS248', 'CS240', 'CS340', 'CS400', 'CS241']

def test_top_sort2():
    courses = [
        [ "MATH239", ["MATH146", "MATH145"] ],
        [ "MATH146", ["MATH145"] ],
        [ "MATH145", [] ]
    ]
    stack = utility.top_sort(courses)
    assert stack == ['MATH145', 'MATH146', 'MATH239']
