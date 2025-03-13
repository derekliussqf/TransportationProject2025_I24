import numpy

def speedOnSegment(data, x_start, x_end, time):
    for i in range(len(data)):
        x_positions = data.iloc[i].x_position
        timestamps = data.iloc[i].timestamp

def generateData(data, x_start, x_end, time_start, time_end):
    totaldata = []
    time = time_start
    increment = (time_end - time_start) / 10000
    while time < time_end:
        dens = calculate_denity(data, x_start, x_end, time)
        flow = calculate_flow(data, (x_start+x_end)/2, time - increment * 10, time + increment * 10)
        totaldata.append([time,dens,flow])
        time += increment
