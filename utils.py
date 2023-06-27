import os
import netifaces
def create_directories(array):
    if(not os.path.exists("data")):
        os.makedirs("data/")
    for filename in array:
        if os.path.exists("data/" + filename):
            print(f"{filename} exists")
            continue
        else:
            print(f"{filename} does not exist, creating...")
            os.makedirs("data/" + filename)
    return False
def get_ip(prefix=None):
    addresses = []
    for ifaceName in netifaces.interfaces():
        addresses.append([i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr':'No IP addr'}])])
    if(prefix):
        for address in addresses:
            if prefix in address[0]:
                return address[0]
    return addresses
if __name__ == "__main__":
    # need to put this in a global file
    # available_directories = [
    #         "material", # lecture material
    #         "transcripts", # Ai based lecture transcript
    #         "summaries", # Ai summerization of transcripts
    #         "videos" # the recorded video
    #     ]
    # create_directories(available_directories)
    # print(get_ip("192.168.1."))
    print(get_ip("127.0.0"))