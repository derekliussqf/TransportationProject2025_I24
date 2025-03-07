import pandas as pd
import matplotlib.pyplot as plt
import json
import pickle
import math
from collections import defaultdict
import numpy as np
import time


data = pd.read_json('Nov22small.json')
#test_data = data.head(10)
#test_data = data[data['direction'] == -1].head(10)

def avgspeed(car_info):
    distance = math.sqrt(pow(car_info.y_position[-1] - car_info.y_position[0], 2) +
                         pow(car_info.x_position[-1] - car_info.x_position[0], 2))
    time = car_info.last_timestamp - car_info.first_timestamp
    return distance / time * 135 / 198  #  miles/h

def v_per_section(car_info):
    sections = len(car_info.y_position)
    sec_num = sections - 1
    velocity = []
    while sec_num > 0:
        distance = math.sqrt(pow(car_info.y_position[sec_num] - car_info.y_position[sec_num - 1], 2) +
                             pow(car_info.x_position[sec_num] - car_info.x_position[sec_num - 1], 2))
        time = car_info.timestamp[sec_num] - car_info.timestamp[sec_num - 1]
        velo = distance / time * 135 / 198  #  miles/h
        velocity.append(velo)
        sec_num -= 1
    return velocity


def calculate_flow(data, target_x, start_time, end_time):
    flow_count = 0

    for i in range(len(data)):
        x_positions = data.iloc[i].x_position
        timestamps = data.iloc[i].timestamp
        j = 1
        start_index = -1
        end_index = -1

        while j < len(timestamps) - 1:
            if (start_index == -1) and timestamps[j] >= start_time:
              start_index = j-1
            if timestamps[j] >= end_time:
              end_index = j
            if start_index != -1 and end_index != -1:
              break
            j = j+1

        if start_index == -1:
              continue
        if end_index == -1:
              end_index = len(timestamps)-1
        # have both start & end
        # print('start', start_index)
        # print('end', end_index)
        # print('len x_pos', len(x_positions))

        if x_positions[start_index] <= target_x <= x_positions[end_index] or \
           x_positions[start_index] >= target_x >= x_positions[end_index]:

            flow_count += 1


    # calc flow :veh/h
    time_window = end_time - start_time
    flow = flow_count / (time_window / 3600)

    return flow



# density
def interpolate_position(x1, x2, t1, t2, target_time):
    if t1 == t2:
        return x1
    return x1 + (x2 - x1) * (target_time - t1) / (t2 - t1)
def calculate_density(data, x_start, x_end, target_time):
    density_count = 0
    for i in range(len(data)):

        x_positions = data.iloc[i].x_position
        timestamps = data.iloc[i].timestamp

        for j in range(len(timestamps) - 1):
            if timestamps[j] <= target_time <= timestamps[j + 1]:
                x_interpolated = interpolate_position(
                    x_positions[j], x_positions[j + 1],
                    timestamps[j], timestamps[j + 1],
                    target_time
                )
                if x_start <= x_interpolated <= x_end:
                    density_count += 1
                break
    # density calc
    road_length = (x_end - x_start) / 63360  # in mile
    density = density_count / road_length  #  veh/mile

    return density


#test



#test flow calc

# target_x = 321525
# start_time = float(1669110000)
# end_time =   float(1669130000)


#flow = calculate_flow(test_data, target_x, start_time, end_time)
#flow = calculate_flow(data, target_x, start_time, end_time)

#print(f"The flow in time frame [{start_time}, {end_time}] passing x = {target_x} is: {flow} veh/h")

# test density


# x_start = 321000
# x_end = 321530
# target_time = 1669120000

#density = calculate_density(test_data, x_start, x_end, target_time)
#density = calculate_density(data, x_start, x_end, target_time)
#print(f"Density at [{target_time}] seconds and within x-coord [{x_start}, {x_end}] is: {density} veh/mile")


## avg speed
'''
vehicle_avg_dict = {f"{data.iloc[i]._id} mean_velocity": avgspeed(data.iloc[i]) for i in range(len(data))}
#vehicle_seg_dict = {f"{data.iloc[i]._id} segment_velocity": v_per_section(data.iloc[i]) for i in range(len(data))}
avg_speed = sum(vehicle_avg_dict.values()) / len(vehicle_avg_dict)

#print(f"Average Speed: {avg_speed} miles/h")



##########  process data 
###segment
def segment_list(lst, segment_size):
    res = []
    for i in range(0, len(lst)+1, segment_size):
      if i+segment_size <= len(lst):
        res.append([lst[i],lst[i + segment_size]])
      else: break
    return res

time_list = np.arange(data.timestamp.explode().min(), data.timestamp.explode().max() + 1, step=1).tolist()
time_targets = np.arange(data.timestamp.explode().min(), data.timestamp.explode().max() + 1, step=100).tolist()
### density cal per 100 seconds
print(len(time_list))

segmented_time_list = segment_list(time_list, 200)
#flow cal each for 200s interval 

#print(segmented_time_list[0])
space_list = np.arange(data["x_position"].explode().min(), data["x_position"].explode().max() + 1, step=1).tolist()
space_targets = np.arange(data["x_position"].explode().min(), data["x_position"].explode().max() + 1, step=1000).tolist()
# flow cal per 1000 inches 

segmented_space_list = segment_list(space_list, 2000)
# density cal each for 2000 inches interval 

#####obtain data
density_list = []
flow_list = []
#print(len(time_targets),len(space_targets),len(segmented_time_list),len(segmented_space_list))

## density
for i in range(len(time_targets)):
   for item in segmented_space_list:
    density_list.append(calculate_density(data, item[0], item[1], time_targets[i]))
# start_time = time.time()
#
with open("density.json", "w") as file:
    json.dump(density_list, file)

# end_time = time.time()

# elapsed_time = end_time - start_time

#### flow 
for i in range(len(space_targets)):
  for item in segmented_time_list:
    flow_list.append( calculate_flow(data, space_targets[i], item[0], item[1]))


with open("flow.json", "w") as file:
    json.dump(flow_list, file)


###reload data
with open('density.json', 'r', encoding='utf-8') as file:

    density_list =  json.load(file)
with open('flow.json', 'r', encoding='utf-8') as file:

    flow_list =  json.load(file)
###



## data pre process for graphing 

#print(len(density_list))#,len(flow_list))
#print(len(time_targets),len(space_targets))

d_l = list([] for i in range(int(len(density_list)/len(time_targets))))

f_l = list([] for i in range(int(len(flow_list)/len(space_targets))))

for i in range(len(density_list)):
  d_l[math.floor(i/(len(time_targets)))].append(density_list[i])

for i in range(len(flow_list)):
  f_l[math.floor(i/len(space_targets))].append(flow_list[i])

#### actual draw 


x = range(len(d_l))
t = time_targets
T,X = np.meshgrid(t,x)

space = space_targets
time = range(len(f_l))
sp,ti = np.meshgrid(space, time)


##draw 

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

#：rho(x, t) density
c = ax1.contourf( T,X, d_l, levels=50, cmap='viridis')
ax1.set_ylabel('x / 2000 inches')
ax1.set_xlabel('t / seconds')
ax1.set_title(r'$\hat{\rho}(x,t)$')
fig.colorbar(c, ax=ax1)


# ：u(x, t) : flow
c = ax2.contourf(ti, sp, f_l, levels=50, cmap='plasma')
ax2.set_ylabel('x / inches')
ax2.set_xlabel('t / 200 seconds')
ax2.set_title(r'$\hat{u}(x,t)$')
fig.colorbar(c, ax=ax2)


plt.tight_layout()


plt.show()
'''
#want to make a plot of density vs avg velocity

def generateData(data, x_start, x_end, time_start, time_end):
    totaldata = []
    time = time_start
    increment = (time_end - time_start) / 10000
    while time < time_end:
        dens = calculate_density(data, x_start, x_end, time)
        flow = calculate_flow(data, (x_start+x_end)/2, time - increment * 10, time + increment * 10)
        totaldata.append([time,dens,flow])
        time += increment
    return totaldata

totData = generateData(data, 316136.9561793628, 316284.41535980365, 1669118400,1669148400)

plt.scatter(totData[:,1], totData[:,2])
plt.xlabel("Density")
plt.ylabel("Flow")
plt.show()