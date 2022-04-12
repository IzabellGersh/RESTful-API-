import database
from main import app


class TestMyApp:
    def test_create(self):
        database.create_db_table()

    def test_add_user(self):
        with app.test_client() as app_test:
            data_to_test = {"name": "ddd", "task": "ddd"}
            rv = app_test.post('/api/users/start', json=data_to_test)
            assert rv.get_data() == b'task is inserted to users task table.'

    def test_add_user_not_ended(self):
        with app.test_client() as app_test:
            data_to_test = {"name": "ddd", "task": "ddd"}
            rv = app_test.post('/api/users/start', json=data_to_test)
            assert rv.get_data() == b"user can't start a new task until previous is done."

    def test_add_user_bad_params(self):
        with app.test_client() as app_test:
            data_to_test = {"name": "ddd"}
            rv = app_test.post('/api/users/start', json=data_to_test)
            assert rv.get_data() == b"bad body params, the required params:['name', 'task']"

    def test_update_user(self):
        with app.test_client() as app_test:
            data_to_test = {"name": "ddd"}
            rv = app_test.put('/api/users/end', json=data_to_test)
            assert rv.get_data() == b"users table updated successfully."

    def test_update_user_allready_ended(self):
        with app.test_client() as app_test:
            data_to_test = {"name": "ddd"}
            rv = app_test.put('/api/users/end', json=data_to_test)
            assert rv.get_data() == b"user didn't start new task"

    def test_update_user_bad_params(self):
        with app.test_client() as app_test:
            data_to_test = {}
            rv = app_test.put('/api/users/end', json=data_to_test)
            assert rv.get_data() == b"bad body params, the required params:['name']"

    def test_report(self):
        with app.test_client() as app_test:
            rv = app_test.get('/api/users/report')
            assert rv.status == '200 OK'
