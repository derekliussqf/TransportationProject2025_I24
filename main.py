import json
import pickle
import math
from collections import defaultdict

# ex create_pickle('nov22.pkl','Nov22small.json')
def create_pickle(pickle_file, json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    with open(pickle_file, "wb") as f:
        pickle.dump(data, f)
    print("DONE")

def open_pickle(pickle_file):
    with open(pickle_file, 'rb') as f:
        return pickle.load(pickle_file)

def open_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data



def speed(car_info):
    distance = math.sqrt(pow(car_info['y_position'][-1] - car_info['y_position'][0],2) + pow(car_info['x_position'][-1] - car_info['x_position'][0],2))
    time = car_info['last_timestamp'] - car_info['first_timestamp']
    return distance / time * 135 / 198

data = open_json('Nov22small.json')
camera_dict = defaultdict(list)
for i in range(200):
    camera_dict[data[i]['compute_node_id']].append(speed(data[i]))

print(camera_dict)