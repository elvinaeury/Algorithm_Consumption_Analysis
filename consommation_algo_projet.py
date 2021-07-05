import multiprocessing
import time
from csv import writer
import os
import csv
import numpy as np
import sys
import psutil
from math import factorial


print('Monitoring starting below...')
print('Battery capacity set to',sys.argv[2])

print('Arguments list : ', sys.argv,'Number of arguments : ', len(sys.argv))


if len(sys.argv[1])>2:
    print('Writing data into file',sys.argv[1])

for i in range(1, 3):
    print(sys.argv[i],'end :', end = " ")


# O(n) complexity for both iterative and recursive factorial
def factorial(n):
   result = 1
   for i in range(1, n):
       result *= i 
       #time.sleep(0.5)
   return result

def factorial_rec(n):
    if n == 1:
        return 1
    else:
        return n * factorial_rec(n-1)

# Sequential/ Linear search: complexity O(n)
def sequential_search(li, item):
    position = 0
    is_present = False
    
    while position < len(li) and not is_present:
        if li[position] == item:
            is_present = True
        else:
            position = position + 1
    
    return is_present



# Binary search: complexity O(log n)
def binary_search(li, item):
    first = 0
    last = (len(li) - 1)
    found = False
    
    while first <= last and not found:
        midpoint = ((first + last)//2)
        if li[midpoint] == item:
            found = True
        else:
            if item < li[midpoint]:
                last = (midpoint - 1)
            else:
                first = (midpoint + 1)
    return found


def get_battery_charge():
    battery = psutil.sensors_battery()
    charge = battery.percent
    #print('Battery percent',charge,'%')
    return(charge)










"""
def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    res = []
    for k in range(4):
        res.append(temp['coretemp'][k+1][1])
    #print('Temperature of CPU',res)
    return(res)

def get_cpu_percent():
    #print('Percentage of CPU used',psutil.cpu_percent(percpu=True))
    return(psutil.cpu_percent(percpu=True))
"""

def monitore():
    #res = {'temp':[],'percent':[]}
    k = 0
    periode = 100 #in seconds
    result = []
    study_time = 60/60 #en heure
    previouscharge = 44
    stop_crit = (60/periode)*60*study_time
    while True and k<stop_crit:
        #96000 = 12000*8heures = (60/periode)parminute*60min*8h
        #res['percent'].append(get_percent())
        #res['temp'].append(get_temp())
        currentcharge = get_battery_charge()
        # cpu_temp = get_cpu_temp()
        # print('cpu_temps : ',cpu_temp)
        # cpu_percent = get_cpu_percent()
        # print('cpu_percent : ,', cpu_percent)
        BT_Wh = float(sys.argv[2])#condition of battery in Wh, given by command inxi -B (ubuntu or mac os)
        power_est = 36*(previouscharge - currentcharge)*BT_Wh/periode
        #energy_consumption = 52*(difference/100) (en Wh)
        #power_est = 3600*energy_consumption/periode (en Watt car periode est le temps entre deux mesures en seconde)
        if k>0:
            result.append(power_est)
            print('Current charge',currentcharge,'%')
        #exp_percentage = 100*k/stop_crit
        if k>0:
            print(k,'| Power estimation =',round(power_est,2),'W')
        previouscharge = currentcharge
        k += 1
        time.sleep(periode)
    if len(sys.argv[1])>2:
        np.savetxt(sys.argv[1], result)


if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=monitore)
    p1.start()
    #p2 = multiprocessing.Process(name='p2', target=factorial,args=(100,))
    #p2.start()
    #p3 = multiprocessing.Process(name='p3', target=factorial_rec,args=(100,))
    #p3.start()
    #p4 = multiprocessing.Process(name='p4', target=sequential_search,args=([0,2,3,4,5,8,10,15,17,21,25,32,42,45],45,))
    #p4.start()
    p5 = multiprocessing.Process(name='p4', target=sequential_search,args=([0,2,3,4,5,8,10,15,17,21,25,32,42,45],45,))
    p5.start() 

    # join means wait until finished
    #p1.join()
    #p2.join()
    #p3.join()
    #p4.join()
    p5.join()

    
    