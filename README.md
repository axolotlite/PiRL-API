# PiRL API
a simple api server for PIRL, designed for use with it's companion mobile app.
this is a containerized version that uses postgres as a db backend.

## environmental variables
example:
```
PORT=8000
HOST=0.0.0.0
POSTGRES_DB=attendance_record
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```
create your own .env file and add them to it.

## running the server
first install the requirements
`pip install -r requirements.txt`
then start the server
`python pirl_api.py`

## api calls:

'/list-directory'
a get request that returns a json object listing directories and their content.
there are 4 possible directories: material, transcripts, summaries and videos.
you can autmatically create these directories using
`python create_material.py`
example return:
```
{
    "material": {"content": ["test.pdf"]},
    "transcripts": {"content": ["lecture_1.txt"]},
    "summaries": {"content": ["help.txt"]},
    "videos": {"content": []}
}
```

'/attend/'
a post request used to record your attendance into a database
it takes a json object containing user, userId and a token.
upon successful registery it should push the object into a database to record student attendance.

'/download'
a get request that allows you to download an object from inside the data directory.
takes two parameters, the directory and the file contained inside it.

'/uploadfile/'
a post request that allows you to upload a file and specify the location on which to save it.
takes two parameters, a directory inside data and the file uploaded.

'/OK'
a simple get request that serves a health check