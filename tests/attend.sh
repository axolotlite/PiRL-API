#!/bin/bash
#TODO
api_endpoint="http://127.0.0.1:8000"
user="ahmed"
token="random_text"

curl -X GET "$api_endpoint/attend/?user=$user&token=$token"
output={"message":"attendance recorded"}