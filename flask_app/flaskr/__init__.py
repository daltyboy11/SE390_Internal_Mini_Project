import os
from flask import Flask
from flask import request
from uwaterlooapi import UWaterlooAPI

uw = UWaterlooAPI( api_key="234279968e219cf1f180a48bf217c318" )

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


    def preprocess_courses( json_data ):
        return

    @app.route( '/course_planner', methods=['POST'] )
    def course_planner():
        json_data = request.get_json()
        return "course_planner"

    return app
