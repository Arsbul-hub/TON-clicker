import pyrebase

config = {
    "apiKey": "AIzaSyB2kPLlIUqj6g1zxdJpsiuPfLay30LhF68",
    "authDomain": "ton-clicker.firebaseapp.com",
    "databaseURL": "https://ton-clicker-default-rtdb.firebaseio.com",
    "storageBucket": "ton-clicker.appspot.com",
    "serviceAccount": "ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
d = db.get()
print(d.val())
