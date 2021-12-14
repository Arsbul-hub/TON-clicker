
import firebase_admin
from firebase_admin import db
firebase_admin.delete_app(firebase_admin.get_app())
cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
app_d = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
})