import jwt
import requests
import json
from time import time
from flask import Flask, jsonify

app = Flask(__name__)

# Enter your API key and your API secret
API_KEY = 'Uxvt-0nJTuyZX8AmCt2Qbg'
API_SEC = 'uzcymC49QHWFDfPqeb0lXiVzoUIJ232p2sYf'

# create a function to generate a token
# using the pyjwt library


def generateToken():
    try: 
        token = jwt.encode(

		# Create a payload of the token containing (first value: encoded token, second value: secret key, third value: algorithm)
		# API Key & expiration time
		{'iss': API_KEY, 'exp': time() + 5000},

		# Secret used to generate token signature
		API_SEC,

		# Specify the hashing alg
		algorithm='HS256'
	    )
        return token

    except Exception as e:
        print(e)
        return jsonify({"message":"Invalid token"})
	
# create json data for post requests
meetingdetails = {"topic": "Nawaraj luitel",
				"type": 2,
				"start_time": "2022-03-22T10: 21: 57",
				"duration": "45",
				"timezone": "Asia/kathmandu",
				"agenda": "test",

				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

# send a request with headers including
# a token and meeting details


def createMeeting():
    
	headers = {'authorization': 'Bearer ' + generateToken(),
			'content-type': 'application/json'}
	r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings',
		headers=headers, data=json.dumps(meetingdetails))
	print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
	y = json.loads(r.text)
	join_URL = y["join_url"]
	meetingPassword = y["password"]

	print(
		f'\n here is your zoom meeting link {join_URL} and your \
		password: "{meetingPassword}"\n')


# run the create meeting function
createMeeting()
