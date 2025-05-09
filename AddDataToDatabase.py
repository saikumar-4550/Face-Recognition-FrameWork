import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognitionrealtime-5cee5-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref=db.reference('Students')
data={
    "22341A4550":{
        "major":"Web",
        "standing":"G",
        "Name":"SAI KUMAR",
        "Branch":"CSE(AI&DS)",
        "Year":3,
        "total_count":90,
        "starting_year":2022,
        'last_check_in_time':"2022-12-11 00:54:34"
    },
    "22341A4512":{
        "major":"ML",
        "standing":"G",
        "Name":"Pradeep",
        "Branch":"CSE(AI&DS)",
        "Year":3,
        "total_count":90,
        "starting_year":2022,
        'last_check_in_time':"2022-12-11 00:54:34"
    },
    "963852":{
        "major":"space",
        "standing":"G",
        "Name":"ELON",
        "Branch":"EEE",
        "Year":4,
        "total_count":80,
        "starting_year":2020,
        'last_check_in_time':"2024-12-11 00:54:34"
    },
    "321654":{
        "major":"robotics",
        "standing":"G",
        "Name":"murtaza",
        "Branch":"robo",
        "Year":3,
        "total_count":85,
        "starting_year":2021,
        'last_check_in_time':"2024-12-11 00:54:34"
    },
    "852741":{
        "major":"act",
        "standing":"G",
        "Name":"emily",
        "Branch":"film",
        "Year":2,
        "total_count":95,
        "starting_year":2024,
        'last_check_in_time':"2025-12-11 00:54:34"
    }
}
for key,value in data.items():
    ref.child(key).set(value)