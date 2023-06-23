#!/bin/bash
#TODO
api_endpoint="http://127.0.0.1:8000"
#commands
curl -X GET $api_endpoint/list-directory?directory=material
output='{"files":["test.pdf"]}'
curl -X GET $api_endpoint/list-directory?directory=transcripts
output='{"files":["lecture_1.txt"]}'
curl -X GET $api_endpoint/list-directory?directory=summaries
output='{"files":["help.txt"]}'
curl -X GET $api_endpoint/list-directory?directory=videos
output='{"files":[]}'