from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


USERS = {
  'admin': 'xuning123',
  'roger': 'roger'
}

@auth.get_password
def get_pw(username):
    return USERS.get(username, None)

