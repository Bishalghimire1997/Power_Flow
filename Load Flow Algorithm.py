
#____________________________________________________________________________________________________________________________________________________________________________
#function to extract any data from ecxel

def get_bus_data(bus_number,column):#gets the data from excel in the list,n bus Number=int,column=string
    parameter=[]
    for i in range(bus_number):
        temp1=all_data.at[i,column]
        parameter.append(temp1)
    return parameter
#___________________________________________________________________________________________________________________________________________________________________________
#function to refine extracted data
def refine(bus_data):
    for i in range(total_number_of_buses):
        bus_data[i]=float(bus_data[i])
    return bus_data
#__________________________________________________________________________________________________________________________________________________________


#_____________________________________________________________________________________________________________________________________________________________________________
#function to create ADMITANCE MATRIX
def create_line():
    first_admitance=[]
    admitance_temp=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    admitance=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    tap_diag=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    imp_temp=np.full((total_number_of_buses,1),complex(0,0))
    from_bus_no=get_bus_data(total_number_of_connection,"from_bus_no")
    to_bus_no=get_bus_data(total_number_of_connection,"to_bus_no")
    from_bus_no_temp=get_bus_data(total_number_of_connection,"from_bus_no")
    to_bus_no_temp=get_bus_data(total_number_of_connection,"to_bus_no")
    r=get_bus_data(total_number_of_connection,"r")
    x=get_bus_data(total_number_of_connection,"x")
    c=get_bus_data(total_shunt_capacitance,"s_c")
    tap=get_bus_data(total_number_of_connection,"tap")
    for i in range(total_number_of_connection):
        if from_bus_no[i]>to_bus_no[i]:
            temp_imp=from_bus_no[i]
            from_bus_no[i]=to_bus_no[i]
            to_bus_no[i]=temp_imp
    for i in range(total_shunt_capacitance):
        cap=float(c[i])
        cap=complex(0,cap)
        if cap==0:
            imp_temp[i]=complex(0,0)
        else:
            imp=1/cap
            imp_temp[i]=imp
            for i in range(total_number_of_buses):
                for j in range(total_number_of_buses):
                    if i==j:
                        a=imp_temp[i]
                        admitance_temp[i][j]=a
    for i in range(total_number_of_connection):
        a=float(r[i])
        b=float(x[i])
        impedance=complex(a,b)
        #print(tap[i])
        if tap[i]==1:
            y=-1*(1/impedance)
            first_admitance.append(y)
        else:
            y=1*(1/impedance)
            y_temp=-y/tap[i]
            first_admitance.append(y_temp)
            non_tap_side=(1-1/tap[i])*y
            tap_side_admitance=(((1/tap[i])-1)/tap[i])*y
            tap_diag[int(from_bus_no_temp[i]-1)][int(from_bus_no_temp[i]-1)]=tap_side_admitance+tap_diag[int(from_bus_no_temp[i]-1)][int(from_bus_no_temp[i]-1)]
            tap_diag[int(to_bus_no_temp[i]-1)][int(to_bus_no_temp[i]-1)]=non_tap_side+tap_diag[int(to_bus_no_temp[i]-1)][int(to_bus_no_temp[i]-1)]
            
            
    for i in range(total_number_of_connection):
        from_bus=int(from_bus_no[i]-1)
        to_bus=int(to_bus_no[i]-1)
        val=first_admitance[i]
        admitance[from_bus][to_bus]=val
    for i in range(total_number_of_buses):
        for j in range(total_number_of_buses):
            if i!=j:
                admitance[j][i]=admitance[i][j]
    for i in range(total_number_of_buses):
        for j in range(total_number_of_buses):
            if i!=j:
                admitance[i][i]=admitance[i][i]+admitance[i][j]
    for i in range(total_number_of_buses):
        for j in range(total_number_of_buses):
            if i==j:
                admitance[i][i]=admitance[i][i]*-1
    admitance=admitance+admitance_temp+tap_diag
    diagonal_element=admitance_temp+tap_diag
    #print(admitance)

    return admitance,diagonal_element
#__________________________________________________________________________________________________________________________________________________________________________________
#function to create Bus Data
def create_bus_data():
    v=np.full((total_number_of_buses),0.000)
    p=np.full((total_number_of_buses),0.000)
    q=np.full((total_number_of_buses),0.000)
    delta=np.full((total_number_of_buses),0.000)
    bus_number=np.full((total_number_of_buses),0.000)
    pv_bus_no=get_bus_data(total_pv_bus,"pv_bus_number")
    pq_bus_no=get_bus_data(total_load_bus,"pq_bus_number")
    bus_number=get_bus_data(total_number_of_buses,"bus_no")
    v=get_bus_data(total_number_of_buses,"voltage_pu")
    delta=get_bus_data(total_number_of_buses,"voltage_angle")
    p=get_bus_data(total_number_of_buses,"real_power")
    q=get_bus_data(total_number_of_buses,"reactive_power")
    return v,p,q,delta,pv_bus_no,pq_bus_no
#______________________________________________________________________________________________________________________________________________________________________________________________________
# 
def create_jacobian():
    r=2*total_number_of_buses-2-total_pv_bus
    c=r
    jacob=np.full((r,c),0.000000)
    for i in range(r1):
        for j in range(c1):
            jacob[i][j]=j1[i][j]
    for i in range(r2):
        for j in range(c2):
            jacob[i][j+c1]=j2[i][j]
    for i in range(r3):
        for j in range(c3):
            jacob[i+r1][j]=j3[i][j]
    for i in range(r4):
        for j in range(c4):
            jacob[i+r1][j+c3]=j4[i][j]
    return jacob
#_________________________________________________________________________________________________________________________________________________________________________
def create_j1():
    r=total_number_of_buses
    r_ret= total_number_of_buses-1
    c_ret=r_ret
    c=r
    j1=np.full((r,c),0.000000)
    j1_temp_1=np.full((r,c),0.000000)
    j1_temp_2=np.full((r,c),0.000000)
    second_element=np.full((c),0.000000)
    difference=np.full((c),0.000000)
    for i in range(r):
        for j in range(c):
            a=abs(y[i][j])
            b=cmath.phase(y[i][j])
            if i!=j:
               j1_temp_1[i][j]=-1* v[i]*v[j]*a*np.sin(b-delta[i]+delta[j])       
    for i in range(r):
        for j in range(c):
            if i!=j:
                second_element[i]=second_element[i]+(-1*j1_temp_1[i][j])      
    for i in range(c):
        difference[i]=second_element[i]
    for i in range(r):
        for j in range(c):
            if i==j:
                j1_temp_2[i][j]=difference[i]
    j1_temp_3=j1_temp_1+j1_temp_2        
    j1_temp_5=np.delete(j1_temp_3,0,1)
    j1=np.delete(j1_temp_5,0,0)
    return j1,r_ret,c_ret
#_________________________________________________________________________________________________________________________________________________________________________
def create_j2():
    r=total_number_of_buses
    r_ret=total_number_of_buses-1
    c_ret=total_number_of_buses-1-total_pv_bus
    c=total_number_of_buses
    j2=np.full((r,c-total_number_of_buses),0.000000)
    j2_temp_1=np.full((r,c),0.000000)
    j2_temp_2=np.full((r,c),0.000000)
    pv_bus=np.full(total_pv_bus,0)
    temp=0
    d=total_ref_bus
    first_element=np.full((r),0.000000)
    third_element=np.full((r),0.000000)
    all_sum=np.full((r),0.000000)
    temp=0
    for i in range(r):
        for j in range(c):
            if i!=j:
                a=abs(y[i][j])
                b=cmath.phase(y[i][j])
                j2_temp_1[i][j]=v[i]*a*np.cos(b-delta[i]+delta[j])         
    for i in range(r):
        for j in range(c):
            if i==j:
             first_element[i]=2*v[i]*abs(y[i][i])*np.cos(cmath.phase(y[i][j]))
   
    for i in range(c):
        for j in range(r):
                if r==1:
                    third_element[temp]=v[1+d]*abs(y[1][1+d])*np.cos(cmath.phase(y[1][1+d])-delta[1]+delta[1+d])
                else:
                    if i!=j:
                        third_element[temp]=third_element[temp]+j2_temp_1[j][i]*np.cos(cmath.phase(y[i][j])-delta[i]+delta[j])/np.cos(cmath.phase(y[j][i])-delta[j]+delta[i])
        temp=temp+1
    for i in range(r):
        all_sum[i]=first_element[i]+third_element[i]
    for i in range(r):
        for j in range(c):
            if i==j:
                j2_temp_2[i][j]=all_sum[i]   
    j2_temp_3=j2_temp_1+j2_temp_2   
    for i in range(total_pv_bus):
        pv_bus[i]=pv_bus_no[i]-1
    j2_temp_4=np.delete(j2_temp_3,pv_bus,1)
    j2_temp_5=np.delete(j2_temp_4,0,1)
    j2=np.delete(j2_temp_5,0,0)
    #print((len(j2),len(j2[0])))

    #print(j2)
    return j2,r_ret,c_ret
#___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_j3():
    r=total_number_of_buses
    r_ret=total_number_of_buses-1-total_pv_bus
    c_ret=total_number_of_buses-1
    c=total_number_of_buses
    j3=np.full((r-total_pv_bus,c),0.000000)
    j3_temp_1=np.full((r,c),0.000000)
    j3_temp_2=np.full((r,c),0.000000)
    pv_bus=np.full(total_pv_bus,0)
    j3_temp_3=np.full((r,c),0.000000)
    second_element=np.full((c),0.000000)
    difference=np.full((c),0.000000)
    for i in range(r):
        for j in range(c):
            a=abs(y[i][j])
            b=cmath.phase(y[i][j])
            if i!=j:
               j3_temp_1[i][j]=-1* v[i]*v[j]*a*np.cos(b-delta[i]+delta[j])
    for i in range(r):
        for j in range(c):
            if i!=j:
                second_element[i]=(second_element[i]+(-1*j3_temp_1[i][j]))
    for i in range(c):
        difference[i]=second_element[i]

    for i in range(r):
        for j in range(c):
             if i==j:
                 j3_temp_2[i][j]=difference[i]
    j3_temp_3=j3_temp_1+j3_temp_2
    for i in range(total_pv_bus):
        pv_bus[i]=pv_bus_no[i]-1
    j3_temp_4=np.delete(j3_temp_3,pv_bus,0)
    j3_temp_5=np.delete(j3_temp_4,0,0)
    j3=np.delete(j3_temp_5,0,1)
    return j3,r_ret,c_ret
#_______________________________________________________________________________________________________________________________________________________________________
def create_j4():
    r=total_number_of_buses
    c=r
    r_ret=total_number_of_buses-1-total_pv_bus
    c_ret=total_number_of_buses-1-total_pv_bus
    j4=np.full((r-total_pv_bus,c-total_pv_bus),0.000000)
    j4_temp_1=np.full((r,c),0.000000)
    j4_temp_2=np.full((r,c),0.000000)
    pv_bus=np.full(total_pv_bus,0)
    j4_temp_3=np.full((r,c),0.000000)
    temp=0
    first_element=np.full((r),0.000000)
    third_element=np.full((r),0.000000)    
    all_sum=np.full((r),0.000000)
    temp=0
    for i in range(r):
        for j in range(c):
            if i!=j:
                a=abs(y[i][j])
                b=cmath.phase(y[i][j])
                j4_temp_1[i][j]=-v[i]*a*np.sin(b-delta[i]+delta[j])    
    for i in range(r):
        for j in range(c):
            if i==j:
             first_element[i]=-2*v[i]*abs(y[i][i])*np.sin(cmath.phase(y[i][j]))             
    for i in range(c):
        for j in range(r):                
                    if i!=j:                        
                        b=np.sin(cmath.phase(y[j][i])-delta[j]+delta[i])
                        if b==0:
                            third_element[temp]=0
                        else:
                            third_element[temp]=third_element[temp]+(-1*j4_temp_1[j][i]*np.sin(cmath.phase(y[i][j])-delta[i]+delta[j])/np.sin(cmath.phase(y[j][i])-delta[j]+delta[i]))                            
        temp=temp+1 
    for i in range(r):
        all_sum[i]=first_element[i]-third_element[i]
    for i in range(r):
        for j in range(c):
            if i==j:
                j4_temp_2[i][j]=all_sum[i]
    for i in range(total_pv_bus):
        for j in range(total_number_of_buses):
            h=int(pv_bus_no[i]-1)
            j4_temp_1[h][j]=0
    for i in range(total_pv_bus):
        for j in range(total_number_of_buses-1):
            h=int(pv_bus_no[i]-1)
            j4_temp_1[j][h]=0
    for i in range(total_pv_bus):
        for j in range(total_number_of_buses-1):
            h=int(pv_bus_no[i]-1)
            j4_temp_2[h][j]=0
    for i in range(total_pv_bus):
        for j in range(total_number_of_buses):
            h=int(pv_bus_no[i]-1)
            j4_temp_1[j][h]=0
    j4_temp_3=j4_temp_1+j4_temp_2
    for i in range(total_pv_bus):
        pv_bus[i]=pv_bus_no[i]-1
    j4_temp_4=np.delete(j4_temp_3,pv_bus,1)
    j4_temp_5=np.delete(j4_temp_4,pv_bus,0)
    j4_temp_6=np.delete(j4_temp_5,0,1)
    j4=np.delete(j4_temp_6,0,0)
    return j4,r_ret,c_ret
#-------------------------------------------------------------------------------------------
#def create_j4_nul():
    
def create_j2_null():
    r=total_number_of_buses
    r_ret=total_number_of_buses-1
    c_ret=total_number_of_buses-1-total_pv_bus
    j2=np.full((r_ret,c_ret),0.000000)
    #print((len(j2),len(j2[0])))
    return j2,r_ret,c_ret

def create_j3_null():
    r=total_number_of_buses
    r_ret=total_number_of_buses-1-total_pv_bus
    c_ret=total_number_of_buses-1
    j3=np.full((r_ret,c_ret),0.000000)
    
    return j3,r_ret,c_ret
    
#________________________________________________________________________________________________________________________________________________________________________________________
#function to calculate P and Q
def calculate_pk_qk():
    a=total_number_of_buses
    pk=np.full((a),0.000000)
    qk=np.full((a),0.000000)
    aeiou=np.full((a),0.000000)
    a=total_number_of_buses
   
    for i in range(a):
        for j in range(a):
            pk[i]=pk[i]+v[i]*v[j]*abs(y[i][j])*np.cos(cmath.phase(y[i][j])-delta[i]+delta[j])
            aeiou[j]=v[i]*v[j]*abs(y[i][j])*np.cos(cmath.phase(y[i][j])-delta[i]+delta[j])
    for i in range(a):
        for j in range(a):
            qk[i]=qk[i]-v[i]*v[j]*abs(y[i][j])*np.sin(cmath.phase(y[i][j])-delta[i]+delta[j])
    return pk,qk

#_________________________________________________________________________________________________________________________________________________________________________________________________________
#function to dalculate del(Pi) del(Qi)
def calculate_pi_qi():  
    del_pi=p-pk
    del_qi=q-qk
    return del_pi,del_qi  
#_____________________________________________________________________________________________________________________________________________________________________________
#function to arrange del pi and del qi in a calculable matrix
def arrange_del_matrix():
    real_power_to_be_taken=total_number_of_buses-1
    reactive_power_to_be_taken=total_number_of_buses-1-total_pv_bus
    d=total_ref_bus
    e=real_power_to_be_taken+reactive_power_to_be_taken
    del_matrix=np.full((e,1),0.000000)
    del_pi_arranged=np.full(real_power_to_be_taken,0.0000000)
    del_qi_arranged=np.full(reactive_power_to_be_taken,0.000000)
    for i in range(real_power_to_be_taken):
        del_pi_arranged[i]=del_pi[i+d]
    for i in range(total_number_of_buses):
        for j in range(total_load_bus):
            if i==int(pq_bus_no[j]-1):
                del_qi_arranged[j]=del_qi[i]
    for i in range(real_power_to_be_taken):
        del_matrix[i][0]=del_pi_arranged[i]
    for i in range(reactive_power_to_be_taken):
        del_matrix[i+real_power_to_be_taken][0]=del_qi_arranged[i]
    return del_matrix
#_____________________________________________________________________________________________________________________________________________________________________________________________
#function to arrange del and v
def arrange_del_and_v():
    number_of_del_to_be_taken=total_number_of_buses-1
    number_of_v_to_be_taken=total_number_of_buses-1-total_pv_bus
    v_arr=np.full((total_number_of_buses),0.000000)
    v_arr_temp=np.full((number_of_v_to_be_taken),0.000000)
    del_arr=np.full((total_number_of_buses),0.000000)
    for i in range(number_of_del_to_be_taken):
        del_arr[i+total_ref_bus]=c[i][0]
    for i in range(number_of_v_to_be_taken):
        v_arr_temp[i]=c[i+number_of_del_to_be_taken][0]
    for i in range(total_number_of_buses):
        for j in range(total_load_bus):
            if i==int(pq_bus_no[j]-1):
                v_arr[i]=v_arr_temp[j]
    return del_arr,v_arr
#_____________________________________________________________________________________________________________________________________________________________________________________

#function to check the specefied accuracy
def check_accuracy(del_matrix,error,count,sum1,check):
    run_permission=0
    for i in range(2*total_number_of_buses-total_pv_bus-2):
        if abs(del_matrix[i][0])<error[i][0]:
            check[i]=0
    for i in range(2*total_number_of_buses-total_pv_bus-2):
        sum1=sum1+check[i]
    if sum1==0:
        return sum1
    #__________________________________________________________________________________________________________________________________________________________________________________________________
#function to print results
def print_result(i,admitance):
    print("")
    print("LOAD FLOW CONVERSED IN "+str(i)+" ITERRATION")
    pk,qk=calculate_pk_qk()
    print("")    
    for i in range(total_number_of_buses):
        print("BUS NUMBER "+str(i+1))
        print("VOLTAGE= "+str(v[i]))         
        print("LOAD ANGLE(RADIAN)="+str(delta[i]))        
        print("LOAD ANGLE(DEGREE)="+str(delta[i]*180/np.pi))       
        print("REAL POWER= "+str(pk[i]))        
        print("REACTIVE POWER= "+str(qk[i]))
        print("")
           
    if total_number_of_connection<total_number_of_buses:
        power_flow,current_flow,losses=calculate_line_flow_and_losses_radial()
    else:
        power_flow,current_flow,losses=calculate_line_flow_and_losses()
    print("")
    print("")
    decision=input("Do you wish to export the output?? YES=1,NO=press any key")
       
    if decision==str(1):
        export(power_flow,current_flow,losses)
        print("")
        print("**********DATA EXPORTED SUCESSFULLY*****************")
        print("")
    else:
        print("")
        print("*********NOT EXPORTED********************************")
       
          

        
        
        
#__________________________________________________________________________________________________________________________________________________________________________________________________
#function to calculate line flow and losses for ring feed
def calculate_line_flow_and_losses():
    from_bus_number=get_bus_data(total_number_of_connection,"from_bus_no")
    to_bus_number=get_bus_data(total_number_of_connection,"to_bus_no")
    current_1=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    current_1_conj=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    current_2_conj=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    power_1=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    power_2=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    power_2_for_loss_calculation=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    current_2=np.full((total_number_of_connection,total_number_of_connection),complex(0,0))
    v_rect=np.full((total_number_of_buses),complex(0,0))
    s_flow=v_rect=np.full((total_number_of_connection),complex(0,0))
    i_flow=np.full((total_number_of_connection),complex(0,0))
    loss_flow=np.full((total_number_of_connection),complex(0,0))
    from_no=np.full((total_number_of_connection),complex(0,0))
    to_no=np.full((total_number_of_connection),complex(0,0))
    count=0
    
    for i in range(total_number_of_buses):
        v_rect[i]=cmath.rect(v[i],delta[i])
    #print("")
    #print(v_rect)
    #print("")
        
    for i in range(total_number_of_connection):
            #current[from_bus_number[i]-1][to_bus_number[j]-1]=-1*y[from_bus_number[i]-1][to_bus_number[j]-1]*(v[from_bus_number[i]-1]-v[to_bus_number[i]-1])+diag_ele[from_bus_number[i]-1][from_bus_number[i]-1]*v[from_bus_number[i]-1]
        current_1[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=-1*y[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]*(v_rect[int(from_bus_number[i]-1)]-v_rect[int(to_bus_number[i]-1)])+diag_ele[int(from_bus_number[i]-1)][int(from_bus_number[i]-1)]*v_rect[int(from_bus_number[i]-1)]
        current_2[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]=-1*y[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]*(v_rect[int(to_bus_number[i]-1)]-v_rect[int(from_bus_number[i]-1)])+diag_ele[int(to_bus_number[i]-1)][int(to_bus_number[i]-1)]*v_rect[int(to_bus_number[i]-1)]
    for i in range(total_number_of_connection):
        for j in range(total_number_of_connection):
            current_1_conj[i][j]=np.conj(current_1[i][j])
            current_2_conj[i][j]=np.conj(current_2[i][j])
    for i in range(total_number_of_connection):
        for j in range(total_number_of_connection):
            power_1[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=v_rect[int(from_bus_number[i]-1)]*current_1_conj[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]
            power_2[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]=v_rect[int(to_bus_number[i]-1)]*current_2_conj[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]
            power_2_for_loss_calculation[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=v_rect[int(to_bus_number[i]-1)]*current_2_conj[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]
    current_flow=current_1+current_2
    power_flow=power_1+power_2
    loss=power_1+power_2_for_loss_calculation
    for i in range(total_number_of_connection):
        for j in range(total_number_of_connection):
            if i!=j:
                loss[j][i]=loss[i][j]
    for i in range(total_number_of_connection):
            #print("FROM BUS NUMBER: "+str(from_bus_number[i])+" TO BUS NUMBER: "+str(to_bus_number[i]))
        for j in range(total_number_of_connection):
            if i!=j:
                if current_flow[i][j]!=0:
                    
                    print("FROM BUS NUMBER: "+str(i+1)+" TO BUS NUMBER: "+str(j+1))
                    print("CURRENT= "+str(current_flow[i][j]))
                    
                    print("POWER= "+str(power_flow[i][j]))
                    
                    print("LOSSES= "+str(loss[i][j]))
                   
                    print("")
    return s_flow,i_flow,loss_flow
               
                                                             
#__________________________________________________________________________________________________________________________________________________________________________________________________
#function to calculate line flow and losses for radial feed
def calculate_line_flow_and_losses_radial():
    from_bus_number=get_bus_data(total_number_of_connection,"from_bus_no")
    to_bus_number=get_bus_data(total_number_of_connection,"to_bus_no")
    current_1=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    current_1_conj=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    current_2_conj=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    power_1=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    power_2=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    power_2_for_loss_calculation=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    current_2=np.full((total_number_of_buses,total_number_of_buses),complex(0,0))
    v_rect=np.full((total_number_of_buses),complex(0,0))
    for i in range(total_number_of_buses):
        v_rect[i]=cmath.rect(v[i],delta[i])
    print("")
    #print(v_rect)
    print("")
     
    for i in range(total_number_of_connection):
        #current[from_bus_number[i]-1][to_bus_number[j]-1]=-1*y[from_bus_number[i]-1][to_bus_number[j]-1]*(v[from_bus_number[i]-1]-v[to_bus_number[i]-1])+diag_ele[from_bus_number[i]-1][from_bus_number[i]-1]*v[from_bus_number[i]-1]
        current_1[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=-1*y[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]*(v_rect[int(from_bus_number[i]-1)]-v_rect[int(to_bus_number[i]-1)])+diag_ele[int(from_bus_number[i]-1)][int(from_bus_number[i]-1)]*v_rect[int(from_bus_number[i]-1)]
        current_2[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]=-1*y[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]*(v_rect[int(to_bus_number[i]-1)]-v_rect[int(from_bus_number[i]-1)])+diag_ele[int(to_bus_number[i]-1)][int(to_bus_number[i]-1)]*v_rect[int(to_bus_number[i]-1)]
    for i in range(total_number_of_buses):
        for j in range(total_number_of_buses):
            current_1_conj[i][j]=np.conj(current_1[i][j])
            current_2_conj[i][j]=np.conj(current_2[i][j])
    for i in range(total_number_of_connection):
        for j in range(total_number_of_connection):
            power_1[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=v_rect[int(from_bus_number[i]-1)]*current_1_conj[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]
            power_2[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]=v_rect[int(to_bus_number[i]-1)]*current_2_conj[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]
            power_2_for_loss_calculation[int(from_bus_number[i]-1)][int(to_bus_number[i]-1)]=v_rect[int(to_bus_number[i]-1)]*current_2_conj[int(to_bus_number[i]-1)][int(from_bus_number[i]-1)]
    current_flow=current_1+current_2
    power_flow=power_1+power_2
    loss=power_1+power_2_for_loss_calculation
    for i in range(total_number_of_buses):
        for j in range(total_number_of_buses):
            if i!=j:
                loss[j][i]=loss[i][j]
    for i in range(total_number_of_buses):
            #print("FROM BUS NUMBER: "+str(from_bus_number[i])+" TO BUS NUMBER: "+str(to_bus_number[i]))
        for j in range(total_number_of_buses):
            if i!=j:
                if current_flow[i][j]!=0:
                    print("FROM BUS NUMBER: "+str(i+1)+" TO BUS NUMBER: "+str(j+1))
                    print("CURRENT= "+str(current_flow[i][j]))
                    print("POWER= "+str(power_flow[i][j]))
                    print("LOSSES= "+str(loss[i][j]))
                    print("")
    return power_flow,current_flow,loss
    
    
 #______________________________________________________________________________________________________________________
  # function to export data to spreadsheet
def export(power_flow,current_flow,losses):
    print("")
    print("Seleect a spreadsheet to export data afer calculation WARNING: ALL THE DATA OF THE SPREADSHEET WILL BE LOST")
    root.filename=filedialog.askopenfilename(initialdir="c:/",title="select a spreadsheet to export data")
    print("")
    file_location_1=root.filename
    print("Destination file set")
    from_bus_number=get_bus_data(total_number_of_connection,"from_bus_no")
    to_bus_number=get_bus_data(total_number_of_connection,"to_bus_no")
    for i in range(total_number_of_buses):
        delta[i]=delta[i]*180/np.pi
    raw_data={"Voltage":v,"Angle":delta,"Real Power":p,"Reactive Power":q}
    df=pd.DataFrame(raw_data,columns=["Voltage","Angle","Real Power","Reactive Power"])
    df.to_excel(file_location_1,"Bus Data Output")
    #raw_data_1={"From Bus":from_bus_number,"To Bus":to_bus_number,"Power Flow":power_flow,"Current Flow":current_flow,"Losses":losses}
    #df_1=pd.DataFrame(raw_data_1,columns=["From Bus","To Bus","Real POwer Flow","Current Flow","Losses"])
    #df_1.to_excel(file_location_1,"Line Flow and Losses")
    
          
          
#____________________________________________________________________________________________________________________________________________________________________________    
#Function  to select spreadsheet
def set_location():
    print("Select a spreadsheet to upload data")
    while True:
            root.filename=filedialog.askopenfilename(initialdir="c:/",title="Select a spreadsheet to upload data")
            file_location=root.filename
            break
            
    return file_location
    
def select_sheet():
    print("")
    print("***************************************************************************************************************")
    print("")
    print("")
    
    while True:
        all_data=pd.read_excel(file_location,sheet_name="To python",header=15)
        try:
            all_data=pd.read_excel(file_location,sheet_name="To python",header=15)
            break
        except:
            print("")
            print("OOPS!!! Looks like you have  uploaded an invalid file or haven't uploaded any file at all")
            input("Please change the file and try again: PRESS ANY KEY TO CONTINUE")
            set_location()
            continue
       
   
               
    return all_data
        
    
#_______________________________________________________________________________________________________________________________________________________________________
#main_program

import sys
import pandas as pd
import numpy as np
import cmath
import time
#timer=pd.DataFrame()
pre_data=pd.read_excel("D://load flow//paper//Reserch Data//IEEE 30//Precision VS Number of Iterrattion.xlsx",sheet_name="IEEE 30 Lower Precision")
pre_data=pre_data.dropna()
print(pre_data)
precision=pre_data["precision"]
#print(precision)

precision_1=precision[0]
    
timer=[]
iterration=[]
precision=[]

for j in range(1000):
    file_location="D://load flow//IEEE 9 Bus.xlsx"
    all_data=pd.read_excel(file_location,sheet_name="To python",header=15)
    #file_location_1="C://Users//Bishal ghimire//Desktop//load flow//Load flow.xlsx"
     #sheet name=sheet number, header= from which row data begains to import
    total_number_of_buses=int(all_data.at[0,"total_number_of_buses"])
    #from_bus_number=all_data.at[0,"from_bus_no"]
    #to_bus_number=all_data.at[0,"to_bus_no"]
    total_number_of_connection=int(all_data.at[0,"total_number_of_connection"])
    total_ref_bus=int(all_data.at[0,"total_ref_bus"])
    total_pv_bus=int(all_data.at[0,"total_pv_bus"])
    total_load_bus=int(all_data.at[0,"total_load_bus"])
    total_shunt_capacitance=int(all_data.at[0,"total_shunt_capacitance"])
    error=np.full((2*total_number_of_buses-total_pv_bus-2,1),5.970297e-02)
    #print(error)
    sum1=0
    check=np.full((2*total_number_of_buses-total_pv_bus-2,),1)
    y,diag_ele=create_line()
    v,p,q,delta,pv_bus_no,pq_bus_no=create_bus_data()
    elapsed_time=[]
    
    

    a=0
    b=0
    for i in range(100):
        #print(i+1)
        start=time.time()
        j1,r1,c1=create_j1()
        if i==0:        
            j2,r2,c2=create_j2_null()
            j3,r3,c3=create_j3_null()
        if i==2:
            j2,r2,c2=create_j2_null()
            j3,r3,c3=create_j3_null()
####        if i==4:
####            j2,r2,c2=create_j2()
####            j3,r3,c3=create_j3()
        else:
            j2,r2,c2=create_j2()
            j3,r3,c3=create_j3()
        j4,r4,c4=create_j4()
        jacob=create_jacobian()
        pk,qk=calculate_pk_qk()
        del_pi,del_qi=calculate_pi_qi()
        #print(del_pi)
        del_matrix=arrange_del_matrix()
        a=np.array(jacob)
        #print(del_matrix)
        b=np.array(del_matrix)
        inv_jacob=np.linalg.inv(a)
        c=np.dot(inv_jacob,b)
        delta_arr,v_arr=arrange_del_and_v()
        v=v+v_arr
        delta=delta+delta_arr
        check_temp=check_accuracy(del_matrix,error,i,sum1,check)
        
        if check_temp==0:
            print(j)
            #print(len(iterration))
            #print(j,i)
            elapsed_time.append(time.time()-start)
            #iterration.append(i)
            #precision.append(j)
            timer.append(elapsed_time)
            #print(timer)
            break
        elapsed_time.append(-start+time.time())
        #print(timer)
        #print(i)
        #print(elapsed_time)
        continue
timer_data=pd.DataFrame(timer)
print(timer_data)
timer_data.to_csv("C://Users//DELL//Desktop//December-2019.csv")
##pre_data["new_iterration_1"]=iterration
##pre_data.to_csv("C://Users//DELL//Desktop//December-2019.csv")
##    
   

        

    






