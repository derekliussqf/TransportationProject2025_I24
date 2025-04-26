# TransportationProject2025_I24

Collaboration Space & Weekly Report for Zach and Derek

Week 3  Feb.7 - Feb.13 (Count startde from first meeting) 

Review & conclude important transportation related knowledges and models.
Take first look at the dataset.



Week 4 Feb.14 - Feb.20

Calculated vehicle velocity ( mean and for each camera section )



Week 5 Feb.21 - Feb.28

Figure how to configure format 
*For each ramp, vehicle number entering / exiting ramp at certain time, count total number of vehicle for each timestep.

Read Paper to understand further goal of the project

Next : fit fundamental diagram -> fit novel model

Week 6 Feb.28 - Mar.7
Do this
![image](https://github.com/user-attachments/assets/6298089d-0271-4cf2-a6b6-90d078cf2dc4)

Week 7 Mar.8 - Mar.14
Wait for Qi to look at the graph & make it looks better & prepare for application(fitting other models)

Week 8 & 9 Mar.15 - Mar.27
irregular :  vehicle stops : straight horizontal line
only on the road for a short time : short lines

roughly estimate the ramp, plot for that region 

Week 10 Mar.28 - Apr.3
Try to figure out how to clean the data and x vs. y at exit.

Week 11 Apr.4 - Apr.11
-Go over whole highway and check how many cars are passing over the center datapoint

-Clean data of not moving cars and cars that pass over centerline / normalize data by dividing by mean value (y_pos)

-Segment the highway, calc avg. velocity & vehicle count for each direction for each 5 seconds

-For each time interval, calc the ratio of vehicle goes out  vs. total vehicle , for each exit.

Week 12 Apr.12 - Apr.18

Week 13 Apr.19 - Apr.25
-visualize by plot the in and out vehicles in different colors, wait for qi's code
