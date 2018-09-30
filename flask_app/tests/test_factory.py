import sys
sys.path.append('../')
from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app( { 'TESTING' : True } ).testing

def test_course_planner( client ):
    json_data_1 = {
                "courses_taken" : [ { "dcode" : "CS", "cnum" : 135 },
                                    { "dcode" : "CS", "cnum" : 136 }],

                "courses_to_take" : [ { "dcode" : "CS", "cnum" : 241 },
                                      { "dcode" : "CS", "cnum" : 348 },
                                      { "dcode" : "CS", "cnum" : 341 },
                                      { "dcode" : "MATH", "cnum" : 135 }],

                "term_to_start_planning" : { "season" : "F", "year" : 2019 }
                } 
    json_data_2 = {
                    "courses_taken" : [ { "dcode" : "CS", "cnum" : 145 } ],

                    "courses_to_take" : [ { "dcode" : "CS", "cnum" : 341 },
                                          { "dcode" : "SE", "cnum" : 380 } ]
                  }
    
    r = client.post( '/course_planner', json=json_data_2 )
    assert True
