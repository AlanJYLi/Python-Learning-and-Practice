import simpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
%matplotlib inline

class AirportCheck(object):
    '''
    In the ID/boarding-pass check process, the resources are regarded as one block with several counters.
    Passengers wait in one queue.
    
    In the personal scanner process, each counter is regarded as individual queues.
    Passengers choose the shortest one and wait in that queue.
    '''  
    def __init__(self, env, number_IDcheck, number_scanner):
        self.env = env
        self.idcheck_resource = simpy.Resource(env, number_IDcheck)
        self.scanner_resource = []
        for j in range(number_scanner):
            self.scanner_resource.append(simpy.Resource(env, 1))

    def idcheck(self, name, checktime):
        # The ID checking process. Passenger's "name" and the service time are the function's arguements
        # The reason why use name as a argument is that when debugging, it's easier to identify each passenger's state via print(). And same reason for the following part
        yield self.env.timeout(checktime)
        #print("{}'s ID checking time is: {:.2f}".format(name, checktime))
    
    def scancheck(self, name, scantime):
        # The scanner checking process. Passenger's "name" and the service time are the function's arguements
        yield self.env.timeout(scantime)
        #print("{}'s scanner checking time is: {:.2f}".format(name, scantime))


def shortestqueue(queuelist):
    '''
    find the queue with least people
    '''
    lengthlist = [len(line.queue)+len(line.users) for line in queuelist]
    for m in range(len(lengthlist)):
        if lengthlist[m] == 0 or lengthlist[m] == min(lengthlist):
            return m
            break
        

def person(env, name, passenger, checktime, scantime, results):
    '''
    The general process for a passenger to finish the whole process.
    
    ID/boarding-pass check process
    The passenger arrives, waits for ID checking, spends some time in the checking and leaves there.
    
    Personal scanner process
    The passenger chooses the shortest queue, waits for checking, spends some time in the checking and leaves there.
    
    arguement "results" is a empty dict to store the time point
    '''
    # the arrival time of a passenger
    # name also used as key for storing the time points for each passenger
    results[name] = [env.now]
    #print("{} comes at: {:.2f}".format(name, results[name][0]))
    
    # waiting for ID checking
    with passenger.idcheck_resource.request() as request1:
        yield request1
        
        # the time point of starting ID checking
        results[name].append(env.now)
        #print("{} starts ID checking: {:.2f}".format(name, results[name][1]))
        
        # the time spended in checking
        yield env.process(passenger.idcheck(name, checktime))
        
        # the time point of finishing ID checking
        results[name].append(env.now)
        #print("{} finishes ID checking at: {:.2f}".format(name, results[name][2]))
        
    # find the shortest queue
    m = shortestqueue(passenger.scanner_resource)
    #results[name].append(m)
    #print("{} enter queue: {:.0f}".format(name, m))
        
    # waiting for scanning
    with passenger.scanner_resource[m].request() as request2:
        yield request2
        
        #print([len(line.queue)+len(line.users) for line in passenger.scanner_resource])
        # the time point of starting scanner checking
        results[name].append(env.now)
        #print("{} starts scanner checking at: {:.2f}".format(name, results[name][3]))
        #print([len(line.queue)+len(line.users) for line in passenger.scanner_resource])
            
        # the time spended in personal scanner checking
        yield env.process(passenger.scancheck(name, scantime))

        # the time point of finishing scanner checking
        results[name].append(env.now)
        #print("{} finishes scanner checking at: {:.2f}".format(name, results[name][4]))


def setup(env, number_IDcheck, number_scanner, average_time_IDcheck, passengers_per_minute, time_scanner_lower, time_scanner_upper ,initial_passengers, results):

    passeger = AirportCheck(env, number_IDcheck, number_scanner)
    
    # Create initial passengers
    i = 1
    if initial_passengers > 0:
        while i <= initial_passengers:
            checktime = np.random.exponential(scale=average_time_IDcheck*60)
            scantime = np.random.uniform(time_scanner_lower*60, time_scanner_upper*60)
            env.process(person(env, 'Passenger %d' % i, passeger, checktime, scantime, results))
            i += 1

    # Create more passengers while the simulation is running
    while True:
        time_interval = np.random.exponential(scale=60/passengers_per_minute)
        yield env.timeout(time_interval)
        checktime = np.random.exponential(scale=average_time_IDcheck*60)
        scantime = np.random.uniform(time_scanner_lower*60, time_scanner_upper*60)
        env.process(person(env, 'Passenger %d' % i, passeger, checktime, scantime, results))
        i += 1


# Initial trail
# We set the simulation time as 12 hours (43200 seconds) in order to get enough data points.
# The parameters are set below. Besides the parameters given in the question, we also set an initial number of passengers to make our simulation closer to realistic situation.
# When the average number of passengers arrives per minute is 5, we set the initial number of passengers to 0. The number of servers at ID checking is 5 and the number of personal scanner checking queues is 5, too.
AVERGAE_TIME_IDCHECK = 0.75 # average service time at ID checking, in minute
TIME_SCANNER_LOWER = 0.5 # uniform distribution bound of service time at scanner checking, in minute
TIME_SCANNER_UPPER = 1 # uniform distribution bound of service time at scanner checking, in minute

# key parameters we explore
PASSENGERS_PER_MINUTE = 5 # lambda 1, average number of passengers arrives per minute
NUMBER_IDCHECK = 4 # number of servers at ID checking
NUMBER_SCANNER = 4 # number of personal scanner checking queues
INITIAL_PASSENGERS = 0 # initial number of passengers

timestore={} # store the time point for each passenger

# Setup and start the simulation
SIM_TIME = 43200 # simulation endding time
env = simpy.Environment()
env.process(setup(env, NUMBER_IDCHECK, NUMBER_SCANNER, AVERGAE_TIME_IDCHECK, PASSENGERS_PER_MINUTE, TIME_SCANNER_LOWER, TIME_SCANNER_UPPER, INITIAL_PASSENGERS, timestore))
env.run(until=SIM_TIME)


# calculate and visualize results
totaltime = []
waitingtime = []
idt = []
st = []
count = 0 # record how many passengers finish the security check
for p in timestore:
    if len(timestore[p]) == 5:
        count += 1
        totaltime.append(timestore[p][4]-timestore[p][0])
        waitingtime.append(timestore[p][1]-timestore[p][0]+timestore[p][3]-timestore[p][2])
        idt.append(timestore[p][2]-timestore[p][1])
        st.append(timestore[p][4]-timestore[p][3])

print('Average time of security process: {:.2f}'.format(sum(totaltime)/len(totaltime)))
print('Average waiting time in the queue: {:.2f}'.format(sum(waitingtime)/len(waitingtime)))
print('Average ID cheking time: {:.2f}'.format(sum(idt)/len(idt)))
print('Average scanner checking time: {:.2f}'.format(sum(st)/len(st)))
print('Number of passengers arrive at airport:{}'.format(len(timestore)))
print('Number of passengers finish secure check: {}'.format(count))



fig = plt.figure(figsize=(15,5))
x1 = range(0,(math.ceil(max(totaltime)/100)+1)*100,50)
x2 = range(0,(math.ceil(max(waitingtime)/100)+1)*100,50)

plt.subplot2grid((1,2),(0,0))
plt.hist(totaltime, bins=x1, rwidth=0.9, density=True, color='grey', alpha=0.3)
sns.kdeplot(totaltime, shade=True)
plt.title('Distribution of Total Time for each Passenger')

plt.subplot2grid((1,2),(0,1))
plt.hist(waitingtime, bins=x2, rwidth=0.9, density=True, color='grey', alpha=0.3)
sns.kdeplot(waitingtime, shade=True)
plt.title('Distribution of Waiting Time for each Passenger')


# Then we change the average number of passengers arrives per minute to 50, while the number of servers at ID checking and the number of personal scanner checking queues are changed to 20. And the initial number of passengers change to 30. The situation goes severely bad. In the simulation trail illustrate below, 36109 passengers arrive at airport but only 19150 of them finish the whole checking process. And for the passengers who finish the process, average total time is around 3 hours.


# key parameters we explore
PASSENGERS_PER_MINUTE = 50 # lambda 1, average number of passengers arrives per minute
NUMBER_IDCHECK = 20 # number of servers at ID checking
NUMBER_SCANNER = 20 # number of personal scanner checking queues
INITIAL_PASSENGERS = 30 # initial number of passengers

timestore={} # store the time point for each passenger

# Setup and start the simulation
env = simpy.Environment()
env.process(setup(env, NUMBER_IDCHECK, NUMBER_SCANNER, AVERGAE_TIME_IDCHECK, PASSENGERS_PER_MINUTE, TIME_SCANNER_LOWER, TIME_SCANNER_UPPER, INITIAL_PASSENGERS, timestore))
env.run(until=SIM_TIME)

totaltime = []
waitingtime = []
idt = []
st = []
count = 0 # record how many passengers finish the security check
for p in timestore:
    if len(timestore[p]) == 5:
        count += 1
        totaltime.append(timestore[p][4]-timestore[p][0])
        waitingtime.append(timestore[p][1]-timestore[p][0]+timestore[p][3]-timestore[p][2])
        idt.append(timestore[p][2]-timestore[p][1])
        st.append(timestore[p][4]-timestore[p][3])

print('Average time of security process: {:.2f}'.format(sum(totaltime)/len(totaltime)))
print('Average waiting time in the queue: {:.2f}'.format(sum(waitingtime)/len(waitingtime)))
print('Average ID cheking time: {:.2f}'.format(sum(idt)/len(idt)))
print('Average scanner checking time: {:.2f}'.format(sum(st)/len(st)))
print('Number of passengers arrive at airport:{}'.format(len(timestore)))
print('Number of passengers finish secure check: {}'.format(count))

fig = plt.figure(figsize=(15,5))
x1 = range(0,(math.ceil(max(totaltime)/100)+1)*100,200)
x2 = range(0,(math.ceil(max(waitingtime)/100)+1)*100,200)

plt.subplot2grid((1,2),(0,0))
plt.hist(totaltime, bins=x1, rwidth=0.9, density=True, color='grey', alpha=0.3)
sns.kdeplot(totaltime, shade=True)
plt.title('Distribution of Total Time for each Passenger')

plt.subplot2grid((1,2),(0,1))
plt.hist(waitingtime, bins=x2, rwidth=0.9, density=True, color='grey', alpha=0.3)
sns.kdeplot(waitingtime, shade=True)
plt.title('Distribution of Waiting Time for each Passenger')


# How many security resource are needed to keep waiting time under 15 minutes?
# In the following session, we will explore how many resources are needed when the number of average arrival per minute equal to 5 or 50 in order to keep the average total time under 15 mintes. Because there are randomness in each simulation, we run the simulation under one condition for 100 times. The matric we use is the maximum average total time and maximum average waiting time in 100 trails.

# Number of average arrival per minute = 5
parameters = [str(num) for num in range(3,6)]

data_total = pd.DataFrame(index=parameters, columns=parameters)
data_waiting = pd.DataFrame(index=parameters, columns=parameters)

for a in range(len(parameters)):
    for b in range(len(parameters)):
        # key parameters we explore
        PASSENGERS_PER_MINUTE = 5 # lambda 1, average number of passengers arrives per minute
        INITIAL_PASSENGERS = 0 # initial number of passengers
        NUMBER_IDCHECK = int(data_total.index[a]) # number of servers at ID checking
        NUMBER_SCANNER = int(data_total.columns[b]) # number of personal scanner checking queues
    
        simulationtimes = 100
    
        total = 0
        waiting = 0
    
        for c in range(simulationtimes):
            timestore={}
            env = simpy.Environment()
            env.process(setup(env, NUMBER_IDCHECK, NUMBER_SCANNER, AVERGAE_TIME_IDCHECK, PASSENGERS_PER_MINUTE, TIME_SCANNER_LOWER, TIME_SCANNER_UPPER, INITIAL_PASSENGERS, timestore))
            env.run(until=SIM_TIME)
        
            totaltime = []
            waitingtime = []
            for p in timestore:
                if len(timestore[p]) == 5:
                    totaltime.append(timestore[p][4]-timestore[p][0])
                    waitingtime.append(timestore[p][1]-timestore[p][0]+timestore[p][3]-timestore[p][2])
        
            # store the results of one simulation
            if total < sum(totaltime)/len(totaltime):
                total = sum(totaltime)/len(totaltime)
            if waiting < sum(waitingtime)/len(waitingtime):
                waiting = sum(waitingtime)/len(waitingtime)
    
        data_total.loc[data_total.index[a], data_total.columns[b]] = total
        data_waiting.loc[data_total.index[a], data_total.columns[b]] = waiting


data_total = data_total[data_total.columns].astype(float)
data_total = data_total[data_total.columns]/60
fig=plt.figure(figsize=(10,6))
sns.heatmap(data_total, annot=True, fmt='.1f')
plt.xlabel("Number of Scanner Checking Queues")
plt.ylabel("Number of ID checking Servers")
plt.title("Heatmap of Average Total Security Checking Time (min)")

data_waiting = data_waiting[data_waiting.columns].astype(float)
data_waiting = data_waiting[data_waiting.columns]/60
fig=plt.figure(figsize=(10,6))
sns.heatmap(data_waiting, annot=True, fmt='.1f')
plt.xlabel("Number of Scanner Checking Queues")
plt.ylabel("Number of ID checking Servers")
plt.title("Heatmap of Average Waiting Time (min)")


# Number of average arrival per minute = 50
parameters = [str(num) for num in range(33,42,3)]

data_total = pd.DataFrame(index=parameters, columns=parameters)
data_waiting = pd.DataFrame(index=parameters, columns=parameters)

for a in range(len(parameters)):
    for b in range(len(parameters)):
        # key parameters we explore
        PASSENGERS_PER_MINUTE = 50 # lambda 1, average number of passengers arrives per minute
        INITIAL_PASSENGERS = 30 # initial number of passengers
        NUMBER_IDCHECK = int(data_total.index[a]) # number of servers at ID checking
        NUMBER_SCANNER = int(data_total.columns[b]) # number of personal scanner checking queues
    
        simulationtimes = 100
    
        total = 0
        waiting = 0
    
        for c in range(simulationtimes):
            timestore={}
            env = simpy.Environment()
            env.process(setup(env, NUMBER_IDCHECK, NUMBER_SCANNER, AVERGAE_TIME_IDCHECK, PASSENGERS_PER_MINUTE, TIME_SCANNER_LOWER, TIME_SCANNER_UPPER, INITIAL_PASSENGERS, timestore))
            env.run(until=SIM_TIME)
        
            totaltime = []
            waitingtime = []
            for p in timestore:
                if len(timestore[p]) == 5:
                    totaltime.append(timestore[p][4]-timestore[p][0])
                    waitingtime.append(timestore[p][1]-timestore[p][0]+timestore[p][3]-timestore[p][2])
        
            # store the results of one simulation
            if total < sum(totaltime)/len(totaltime):
                total = sum(totaltime)/len(totaltime)
            if waiting < sum(waitingtime)/len(waitingtime):
                waiting = sum(waitingtime)/len(waitingtime)
    
        data_total.loc[data_total.index[a], data_total.columns[b]] = total
        data_waiting.loc[data_total.index[a], data_total.columns[b]] = waiting


data_total = data_total[data_total.columns].astype(float)
data_total = data_total[data_total.columns]/60
fig=plt.figure(figsize=(10,6))
sns.heatmap(data_total, annot=True, fmt='.1f')
plt.xlabel("Number of Scanner Checking Queues")
plt.ylabel("Number of ID checking Servers")
plt.title("Heatmap of Average Total Security Checking Time (min)")

data_waiting = data_waiting[data_waiting.columns].astype(float)
data_waiting = data_waiting[data_waiting.columns]/60
fig=plt.figure(figsize=(10,6))
sns.heatmap(data_waiting, annot=True, fmt='.1f')
plt.xlabel("Number of Scanner Checking Queues")
plt.ylabel("Number of ID checking Servers")
plt.title("Heatmap of Average Waiting Time (min)")