from flask import Flask, jsonify,request
from marshmallow import ValidationError
from datetime import datetime, timedelta
import sys

from helpers.config import DATABASE_URI
from helpers.schema_validation import UserSchema, QuerySchema
from helpers.entities import User
from helpers.db_helper import DBHelper
from Exceptions.custom_exception import CustomException
from Exceptions.validation_exception import CustomValidationException
from Exceptions.database_exception import DatabaseException
from Exceptions.resource_not_found_exception import ResourceNotFoundException

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = DBHelper()

db.init_app(app)
with app.app_context():
    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")

@app.route('/postEP', methods=['POST'])
def post():
    '''
    TODO: Please add code here with respect to the following:
    - Endpoint expects a body containing a single parameter "name" and creates a new `User`-Instance
    - the id of the new user is returned instantly in the response
    '''
    schema = UserSchema()
    data = request.get_json()
    try:
        schema.load(data)
    except ValidationError as err:
        print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
        print(err.valid_data)  # => {"name": "John"}
        raise CustomValidationException(err.messages)

    name = data['name']
    date = datetime.now()
    user = User(name=name, date=date)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'id': user.id
        })
    except:
        db.session.rollback()
        raise DatabaseException(sys.exc_info())
    finally:
        db.session.close()
    

@app.route('/getEP')
def get():
    '''
    TODO: Please add code here with respect to the following:
    - Endpoint expects an query-parameter "userID"
    - `User`-Object with the corresponding id is returned if the object was created > 10 seconds ago
    - otherwise an error message indicating that the user has not yet been created will be returned with status-code 404
    '''
    user_id = request.args
    schema = QuerySchema()
    try:
        schema.load(user_id)
    except ValidationError as err:
        print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
        print(err.valid_data)  # => {"name": "John"}
        raise CustomValidationException(err.messages)

    id = user_id.get('userID')
    try:
        user = User.query.filter(User.id == id).one()
    except:
        raise ResourceNotFoundException('User Not Found')
    
    compare_date = user.date + timedelta(seconds=10)
    now = datetime.now()
    if compare_date > now:
        raise ResourceNotFoundException('User Not Created Yet')

    return jsonify({
        'user': user.as_dict()
    })

@app.errorhandler(CustomException)
def basic_error(e):       
    return jsonify({'error': e.msg}), e.code 
       

# TODO: the app should run on port 6001
if __name__ == '__main__':
    app.run(debug=True,port=6001)
