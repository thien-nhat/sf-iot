from datetime import datetime                                                                                                                          
from rs485 import *                                                                                                                                    
from timer import *                                                                                                                                    
import json                                                                                                                                            
import time                                                                                                                                            
                                                                                                                                                       
PHYSIC = Physic()                                                                                                                                      

def remove_duplicate_schedules(schedules):
    seen = set()
    unique_schedules = []

    for schedule in schedules:
        time_start = schedule['time-start']

        if time_start not in seen:
            seen.add(time_start)
            unique_schedules.append(schedule)

    return unique_schedules

# Define a function to calculate the time difference in minutes
def get_time_difference_in_minutes(schedule):
    # Get the current time
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M")
    # Get the time-start value from the schedule and convert it to a datetime object
    time_start = datetime.strptime(schedule['time-start'], "%H:%M")
    # Calculate the difference between the current time and the time-start value
    time_difference = time_start - current_time
    return time_difference.total_seconds() / 60
                                                                                                                                                       
class FarmScheduler():                                                                                                                                 
    def __init__(self, debug=True):                                                                                                                    
        self.debug = debug                                                                                                                             
        self.schedules = []                                                                                                                            
        self.current_schedule = None                                                                                                                   
        self.current_state = IdleState(debug=self.debug)                                                                                               
                                                                                                                                                       
    def run(self):                                                                                                                                     
        # while True:                                                                                                                                    
        #     self.print_schedules()                                                                                                                     
        #     if not self.current_schedule:                                                                                                              
        #         self.current_schedule = self.check_schedule()                                                                                          
        #         if not self.current_schedule:                                                                                                          
        #             time.sleep(1)  # Sleep briefly to avoid busy waiting                                                                               
        #             continue                                                                                                                           
                                                                                                                                                       
        #     self.current_state = self.current_state.execute(self.current_schedule)                                                                     
        #     if isinstance(self.current_state, IdleState) and self.current_schedule['next-cycle'] <= 0:                                                 
        #         self.schedules.pop(0)                                                                                                                  
        #         print("Cycle complete, checking for new schedules.")                                                                                   
        #         self.current_schedule = None                                                                                                           
        #         break                                                                                                                                  
                                                                                                                                                       
        #     time.sleep(1)  # Main loop tick rate
        self.print_schedules()                                                                                                                  
        if not self.current_schedule:                                                                                                              
            self.current_schedule = self.check_schedule()                                                                                          
            if not self.current_schedule:                                                                                                          
                time.sleep(1)  # Sleep briefly to avoid busy waiting                                                                               
                return True                                                                                                                                                                                                                                                                      
        self.current_state = self.current_state.execute(self.current_schedule)                                                                     
        if isinstance(self.current_state, IdleState) and self.current_schedule['next-cycle'] <= 0:                                                 
            self.schedules.pop(0)                                                                                                                  
            print("Cycle complete, checking for new schedules.")                                                                                   
            self.current_schedule = None                                                                                                           
            return False                                                                                                                                 
                                                                                                                                                       
    def print_schedules(self):                                                                                                                         
        print("Current schedules:")                                                                                                                    
        for idx, schedule in enumerate(self.schedules, start=1):                                                                                       
            print(f"Schedule {idx}: {schedule}")                                                                                                       
    def add_schedule(self, schedule):                                                                                                                  
        self.schedules.append(schedule)
        current_time = datetime.now()
        print("Current time:", current_time)
        self.schedules.sort(key=get_time_difference_in_minutes)
        self.schedules = remove_duplicate_schedules(self.schedules)
        print("New schedule added:", schedule)
        print("# Print the sorted sched_active taht already in FSM")
        for schedule in self.schedules:
            print("Schedule:", schedule)                                                                                                                
                                                                                                                                                       
    def check_schedule(self):                                                                                                                          
        # Find a schedule with start time in the future                                                                                                
        now = datetime.now().strftime("%H:%M")                                                                                                         
        for schedule in self.schedules:                                                                                                                
            start_time = schedule['time-start']                                                                                                        
            if start_time <= now:                                                                                                                      
                return schedule                                                                                                                        
        return None                                                                                                                                    
                                                                                                                                                       
class State:                                                                                                                                           
    def __init__(self, debug=True):                                                                                                                    
        self.debug = debug                                                                                                                             
                                                                                                                                                       
    def execute(self, schedule):                                                                                                                       
        raise NotImplementedError                                                                                                                      
                                                                                                                                                       
    def wait_for_timer(self, timer_id):                                                                                                                
        while timer_counters[timer_id] > 0:                                                                                                            
            timerRun()                                                                                                                                 
            time.sleep(1)  # Sleep to simulate time passing                                                                                            
                                                                                                                                                       
class IdleState(State):                                                                                                                                
    def execute(self, schedule):                                                                                                                       
        if self.debug:                                                                                                                                 
            print("IDLE STATE")                                                                                                                        
        if schedule['next-cycle'] > 0:                                                                                                                 
            schedule['next-cycle'] = schedule['next-cycle'] -1                                                                                         
            return Mixer1State(debug=self.debug)                                                                                                       
        else:                                                                                                                                          
            print("FINISHED !!!")                                                                                                                      
            return self                                                                                                                                
                                                                                                                                                       
class Mixer1State(State):                                                                                                                              
    def execute(self, schedule):                                                                                                                       
        PHYSIC.setActuators(MIXER1,"ON")                                                                                                               
        setTimer(0, int(schedule['mixer1']))                                                                                                           
        self.wait_for_timer(0)                                                                                                                         
        PHYSIC.setActuators(MIXER1,"OFF")                                                                                                              
        if self.debug:                                                                                                                                 
            print("MIXER1 STATE - Complete")                                                                                                           
        return Mixer2State(debug=self.debug)                                                                                                           
                                                                                                                                                       
class Mixer2State(State):                                                                                                                              
    def execute(self, schedule):                                                                                                                       
        PHYSIC.setActuators(MIXER2,"ON")                                                                                                               
        setTimer(0, int(schedule['mixer2']))                                                                                                           
        self.wait_for_timer(0)                                                                                                                         
        PHYSIC.setActuators(MIXER2,"OFF")                                                                                                              
        if self.debug:                                                                                                                                 
            print("MIXER2 STATE - Complete")                                                                                                           
        return Mixer3State(debug=self.debug)                                                                                                           
                                                                                                                                                       
class Mixer3State(State):                                                                                                                              
    def execute(self, schedule):                                                                                                                       
        PHYSIC.setActuators(MIXER3,"ON")                                                                                                               
        setTimer(0, int(schedule['mixer3']))                                                                                                           
        self.wait_for_timer(0)                                                                                                                         
        PHYSIC.setActuators(MIXER3,"OFF")                                                                                                              
        if self.debug:                                                                                                                                 
            print("MIXER3 STATE - Complete")                                                                                                           
        return PumpInState(debug=self.debug)                                                                                                           
                                                                                                                                                       
class PumpInState(State):                                                                                                                              
    def execute(self, schedule):                                                                                                                       
        PHYSIC.setActuators(PUMPIN,"ON")                                                                                                               
        setTimer(0, int(schedule['pump-in']))                                                                                                          
        self.wait_for_timer(0)                                                                                                                         
        PHYSIC.setActuators(PUMPIN,"OFF")                                                                                                              
        if self.debug:                                                                                                                                 
            print("PUMP IN STATE - Complete")                                                                                                          
        return PumpOutState(debug=self.debug)                                                                                                          
                                                                                                                                                       
class PumpOutState(State):                                                                                                                             
    def execute(self, schedule):                                                                                                                       
        PHYSIC.setActuators(PUMPOUT,"ON")                                                                                                              
        setTimer(0, int(schedule['pump-out']))                                                                                                         
        self.wait_for_timer(0)                                                                                                                         
        PHYSIC.setActuators(PUMPOUT,"OFF")                                                                                                             
        if self.debug:                                                                                                                                 
            print("PUMP OUT STATE - Complete")                                                                                                         
        return IdleState(debug=self.debug)                                                                                                             
                                                                                                                                                       
                                                                                                                                                       
                                                                                                                                                       
def convert_schedule_json_to_dict(json_data):                                                                                                          
    return json.loads(json_data)                                                                                                                       
                                                                                                                                                       
            