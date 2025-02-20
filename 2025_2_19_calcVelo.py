import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json
import pickle
import math
from collections import defaultdict


# original 
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



def avgspeed(car_info):
    distance = math.sqrt(pow(car_info['y_position'][-1] - car_info['y_position'][0],2) + pow(car_info['x_position'][-1] - car_info['x_position'][0],2))
    time = car_info['last_timestamp'] - car_info['first_timestamp']
    return distance / time * 135 / 198

def v_per_section(car_info):
    sections = len(car_info['y_position'])
    sec_num = sections-1
    velocity = []
    while sec_num >0:
      distance = math.sqrt(pow(car_info['y_position'][sec_num] - car_info['y_position'][sec_num-1],2) + pow(car_info['x_position'][sec_num] - car_info['x_position'][sec_num-1],2))
      time = car_info['timestamp'][sec_num]  - car_info['timestamp'][sec_num-1] 
      velo = distance / time * 135 / 198
      velocity.append(velo)
      sec_num -= 1
    return velocity

data = open_json('Nov22small.json')
camera_dict = defaultdict(list)
vehicle_dict = defaultdict(list)
vehicle_avg_dict = defaultdict(list)
vehicle_seg_dict = defaultdict(list)
for i in range(len(data)):
      camera_dict[f"{data[i]['compute_node_id']} mean_velocity"].append(avgspeed(data[i]))
      vehicle_avg_dict[f"{data[i]['_id']} mean_velocity"].append(avgspeed(data[i]))
      vehicle_seg_dict[f"{data[i]['_id']} segment_velocity"].append(v_per_section(data[i]))

vehicle_dict = {'mean_velocity':vehicle_avg_dict , 'segment_velocity':vehicle_seg_dict}

#print(vehicle_dict)
print(camera_dict)

'''
#panda & load from drive
from google.colab import drive
drive.mount('/content/drive')
data = pd.read_json("/content/drive/MyDrive/Nov22small.json")

def avgspeed1(car_info):
    distance = math.sqrt(pow(car_info.y_position[-1] - car_info.y_position[0],2) + pow(car_info.x_position[-1] - car_info.x_position[0],2))
    time = car_info.last_timestamp - car_info.first_timestamp
    return distance / time * 135 / 198

def v_per_section1(car_info):
    sections = len(car_info.y_position)
    sec_num = sections-1
    velocity = []
    while sec_num > 0:
      distance = math.sqrt(pow(car_info.y_position[sec_num] - car_info.y_position[sec_num-1],2) + pow(car_info.x_position[sec_num] - car_info.x_position[sec_num-1],2))
      time = car_info.timestamp[sec_num]  - car_info.timestamp[sec_num-1] 
      velo = distance / time * 135 / 198
      velocity.append(velo)
      sec_num -= 1
    return velocity

data = pd.read_json('Nov22small.json')
  #camera_dict[data.compute_node_id[i]].append(avgspeed(data[i]))
vehicle_avg_dict = {f"{data.iloc[i]._id} mean_velocity" : avgspeed1(data.iloc[i]) for i in len(data)}
vehicle_seg_dict = {f"{data.iloc[i]._id} segment_velocity" : v_per_section1(data.iloc[i]) for i in len(data)}
vehicle_dict = {'mean_velocity':vehicle_avg_dict , 'segment_velocity':vehicle_seg_dict}

#print(vehicle_dict['segment_velocity'])
'''