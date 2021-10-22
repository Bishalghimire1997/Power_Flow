from matplotlib import pyplot as plt
import numpy as np
import math as m

Tperiod=100
percentage=0.6
angle=140


def time_period_calculation(Tperiod,percentage,angle,less):
    print("Given Angle= ",angle,"New_Angle= ",angle-less)
    t1=Tperiod*percentage*np.sin(m.radians(60-(angle-less)))
    t2=Tperiod*percentage*np.sin(m.radians(angle-less))
    t0=Tperiod-t1-t2
    print("T1= ",t1,"T2= ",t2,"T0= ",t0)
    return[t0/4,t1/2,t2/2,t0/4]
def state_identifier(a,b):
    state=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,1,1]]
    return[state[0],state[a],state[b],state[7]]
    
def swap(a):
    b=a[1]
    a[1]=a[2]
    a[2]=b
    return a
def sector_identifier(angle):
    base_vector=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]]
    if angle>0 and angle<=60:
        index=0
        less_angle=0
    elif angle>60 and angle<=120:
        index=1
        less_angle=60
    elif angle>120 and angle<=180:
        index=2
        less_angle=120
    elif angle>180 and angle<=240:
        index=3
        less_angle=180
    elif angle>240 and angle<=300:
        index=4
        less_angle=240
    elif angle>300 and angle<=360:
        index=4
        less_angle=240

    return base_vector[index],less_angle

def plot():
    for i in  U_matrix:
        plt.plot(i)
        plt.show()
        
Base_vector,Less_angle=sector_identifier(angle)
if Base_vector[0]%2==0:
    time=time_period_calculation(Tperiod,percentage,angle,Less_angle)
    U_matrix=state_identifier(Base_vector[0],Base_vector[1])
    time=swap(time)
    U_matrix=swap(U_matrix)
    
else:
    time=time_period_calculation(Tperiod,percentage,angle,Less_angle)

    U_matrix=state_identifier(Base_vector[0],Base_vector[1])

for i in range(len(U_matrix)):
    print("Stage",i+1)
    print("L1 is ",U_matrix[i][0]," for ",time[i],"micro Second")
    print("L2 is ",U_matrix[i][1]," for ",time[i],"micro Second")
    print("L3 is ",U_matrix[i][2]," for ",time[i],"micro Second")
    
    
        
        



    

    
    
    
    
    


