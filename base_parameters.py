import pandas as pd
import math
import matplotlib.pyplot as plt
import math



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

vehicle_avg_dict = {f"{data.iloc[i]._id} mean_velocity": avgspeed(data.iloc[i]) for i in range(len(data))}
#vehicle_seg_dict = {f"{data.iloc[i]._id} segment_velocity": v_per_section(data.iloc[i]) for i in range(len(data))}

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

target_x = 321525
start_time = float(1669110000) 
end_time =   float(1669130000)  


#test flow calc
#flow = calculate_flow(test_data, target_x, start_time, end_time)
flow = calculate_flow(data, target_x, start_time, end_time)

print(f"The flow in time frame [{start_time}, {end_time}] passing x = {target_x} is: {flow} veh/h")


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

x_start = 321000
x_end = 321530 
target_time = 1669120000
#test
#density = calculate_density(test_data, x_start, x_end, target_time)
density = calculate_density(data, x_start, x_end, target_time)
print(f"Density at [{target_time}] seconds and within x-coord [{x_start}, {x_end}] is: {density} veh/mile")


## avg speed
avg_speed = sum(vehicle_avg_dict.values()) / len(vehicle_avg_dict)

print(f"Average Speed: {avg_speed} miles/h")





# draw#
def plot_fundamental_diagram(flow, density, avg_speed):
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.scatter(density, flow, color='blue')
    plt.xlabel('Density (veh/mile)')
    plt.ylabel('Flow (veh/h)')
    plt.title('Flow-Density Diagram')

    plt.subplot(1, 2, 2)
    plt.scatter(density, avg_speed, color='red')
    plt.xlabel('Density (veh/mile)')
    plt.ylabel('Speed (km/h)')
    plt.title('Speed-Density Diagram')

    plt.tight_layout()
    plt.show()

plot_fundamental_diagram(flow, density, avg_speed)