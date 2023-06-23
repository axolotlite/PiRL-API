#!/bin/bash
api_endpoint=http://127.0.0.1:8000
curl -X GET "$api_endpoint/download?directory=transcripts&file_name=lecture_1.txt"

output="So, why do we learn linux?
simple, because linux is good
linux is just"
