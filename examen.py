import datetime
import time
import threading

tank_capacity = 0
motor = 0
wheel = 0

class scheduler():

    tasks = None

    def __init__(self, tasks):

        self.tasks = tasks

    def run(self):
    
        for thread in self.tasks:
            
            if(thread.name =="pump_1" or thread.name == "pump_2"):

                while(thread.period != 0):
                    if(thread.production + tank_capacity >= 50 ):
                        print(thread.name + " job has been done discarding task")
                        break
                    else:
                        thread.run()

            elif(thread.name == "wheel_1" or thread.name == "wheel_2"):
                if(thread.production - tank_capacity >= 0):
                    print(thread.name + " job has been done discarding task")
                    break
                else:
                    thread.run()




class thread(threading.Thread):

    name = None
    period = None
    exec_time = None
    priority = None
    
    def __init__(self, name, period, exec_time, production, discarding, motor = None, wheel = None, ):

        self.name = name
        self.period = period
        self.exec_time = exec_time
        self.production = production
        self.motor = motor
        self.wheel = wheel
        self.discarding = discarding

        threading.Thread.__init__(self)

    def run(self):

        global tank_capacity
        global motor
        global wheel
        global discarding

        if(self.name =="pump_1" or self.name == "pump_2"):

            print(self.name + " status : filling tank")
            print("tank capacity = "+ str(tank_capacity) + "%")
            time.sleep(self.exec_time)
            self.period = self.period - 1
            tank_capacity = tank_capacity + (self.production * self.exec_time)
            
        elif(self.name =="wheel_1" or self.name == "wheel_2"):

            print(self.name + " status : emptying tank and making motor")
            print("tank capacity = "+ str(tank_capacity) + "%")
            time.sleep(1)
            self.period = self.period - 1
            self.exec_time = self.exec_time - 1
            tank_capacity = tank_capacity - self.production
            if(self.name =="wheel_1"):
                motor = motor + 1
                print("1 motor built : " + str(motor))

            if(self.name =="wheel_2"):
                wheel = wheel + 1
                print("1 wheel built : " + str(wheel))
        
        
task_list = []
task_list.append(thread(name="pump_1", period=5,exec_time=2, production=10, discarding = 0))
task_list.append(thread(name="pump_2", period=15,exec_time=3, production=20, discarding = 0))
task_list.append(thread(name="wheel_1", period=5,exec_time=5, production=25, discarding = 0, motor = 1, ))
task_list.append(thread(name="wheel_2", period=5,exec_time=3, production=5, discarding = 0, wheel = 1, ))

if __name__ == '__main__':
    while(True):
        schedule = scheduler(task_list)
        schedule.run()