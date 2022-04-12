from flask import Flask, request, Response
from datetime import datetime
import json
import database


app = Flask(__name__)

@app.route('/api/users/report', methods=['GET'])
def api_get_users():
    return Response(response=json.dumps(database.get_users()), status=200)

@app.route('/api/users/report/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return Response(response=json.dumps(database.get_user_by_id(user_id)), status=200)

@app.route('/api/users/start',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    currentTime = datetime.now().strftime("%H:%M")
    if database.insert_user(user, currentTime) is False:
        return Response(response="user can't start a new task until previous is done.", status=200)
    return Response(response="task is inserted to users task table.", status=200)


@app.route('/api/users/end', methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    currentTime = datetime.now().strftime("%H:%M")
    if database.update_user(user, currentTime) is False:
        return Response(response="user didn't start new task", status=200)
    return Response(response="users table updated succssefully.", status=200)


if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    database.create_db_table()
    app.run() #run app