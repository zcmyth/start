from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == 'admin':
        return 'xuning123'
    return None
