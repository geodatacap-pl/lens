import os
import glob
import re
import requests

token_debug = "debugtoken"
endpoint_debug = "1"
resolution_debug = "1920x1080"
device_debug = "device_01"
url = "http://127.0.0.1:8000/node/store/post/"


def send_handler(file):
    package = {
        "token": token_debug,
        "endpoint_id": endpoint_debug,
        "device_id": device_debug,
        "resolution": resolution_debug,
        "content": concate_data(file),
    }
    print(concate_data(file))
    try:
        r = requests.post(url, json=package)
        # print(r.request.body)
        # print(r.request.headers)
        # print(r.json())
    except Exception as e:
        print("Error: " + str(e))
    finally:
        return


def concate_data(file):
    classes = {}

    with open(os.path.realpath(file.name), "r") as f:
        for line in f:
            line = line.rstrip()
            line = re.sub(r"[()\'\s]", "", line)
            line = line.split(",")
            if line[0] not in classes:
                classes[line[0]] = {
                    "accuracy": [],
                    "pos_x": [],
                    "pos_y": [],
                    "width": [],
                    "height": [],
                    "count": 1,
                }
            classes[line[0]]["accuracy"].append(float(line[1]))
            classes[line[0]]["pos_x"].append(int(line[2]))
            classes[line[0]]["pos_y"].append(int(line[3]))
            classes[line[0]]["width"].append(int(line[4]))
            classes[line[0]]["height"].append(int(line[5]))
            classes[line[0]]["count"] += 1

    for key in classes:
        for item in classes[key]:
            if item is not "count":
                values = classes[key][item]
                classes[key][item] = sum(values) / len(values)

    return classes
