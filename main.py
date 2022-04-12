from typing import List

from flask import Flask, request, Response
from datetime import datetime
import json
import database

app = Flask(__name__)


@app.route('/api/users/report', methods=['GET'])
def api_get_users():
    answer = json.dumps(database.get_users())
    if answer != '{}':
        return Response(response=answer, status=200)
    return Response(response='Empty DB', status=200)


@app.route('/api/users/report/<user_id>', methods=['GET'])
def api_get_user(user_id):
    answer = json.dumps(database.get_user_by_id(user_id))
    if answer != '{}':
        return Response(response=answer, status=200)
    return Response(response='There is no such user_id', status=200)


@app.route('/api/users/start', methods=['POST'])
def api_add_user():
    bad_response_message = "user can't start a new task until previous is done."
    good_response_message = "task is inserted to users task table."
    params_error_message = "bad body params, the required params"
    required_params = ['name', 'task']
    method = database.insert_user

    return handle_request(method, bad_response_message, good_response_message, params_error_message, required_params)


@app.route('/api/users/end', methods=['PUT'])
def api_update_user():
    bad_response_message = "user didn't start new task"
    good_response_message = "users table updated successfully."
    params_error_message = "bad body params, the required params"
    required_params = ['name']
    method = database.update_user

    return handle_request(method, bad_response_message, good_response_message, params_error_message, required_params)


def handle_request(method, bad_response_message: str, good_response_message: str, params_error_message: str,
                   required_params: List[str]):
    user = request.get_json()
    current_time = datetime.now().strftime("%H:%M")
    for key in required_params:
        if user.get(key) is None:
            params_error_message = ':'.join([params_error_message, str(required_params)])
            return Response(response=params_error_message, status=200)
    if method(user, current_time) is False:
        return Response(response=bad_response_message, status=200)
    return Response(response=good_response_message, status=200)


if __name__ == "__main__":
    database.create_db_table()
    app.run()  # run app
