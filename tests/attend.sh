#!/bin/bash
#TODO
api_endpoint="http://127.0.0.1:8000"
user="ahmed"
userId="5225"
token="random_text"

curl -X POST -H "Content-Type: application/json" -d '{"user":"$user","userId":"$userId","token":"$token"}' $api_endpoint/attend/
output={"message":"attendance recorded"}