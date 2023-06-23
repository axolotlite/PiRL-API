import os

def create_directories(array):
    for element in array:
        directory_name = str(element)
        try:
            os.makedirs("data/" + directory_name)
            print(f"Directory '{directory_name}' created.")
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")

# need to put this in a global file
available_directories = [
        "material", # lecture material
        "transcripts", # Ai based lecture transcript
        "summaries", # Ai summerization of transcripts
        "videos" # the recorded video
    ]
create_directories(available_directories)
