from datetime import datetime

sched_active = []                                                                                                                                      

state = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 2,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "11:23",                                                                                                                             
    "active": 1,                                                                                                                                       
}   

new_schedule = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 2,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "10:10",                                                                                                                             
    "active": 1,                                                                                                                                       
}

new_schedule1 = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 2,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "10:14",                                                                                                                             
    "active": 1,                                                                                                                                       
}

new_schedule2 = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 1,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "10:12",                                                                                                                             
    "active": 1,                                                                                                                                       
}
new_schedule3 = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 2,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "10:12",                                                                                                                             
    "active": 1,                                                                                                                                       
}
new_schedule4 = {                                                                                                                                              
    "next-cycle": 1,                                                                                                                                   
    "mixer1": 3,                                                                                                                                       
    "mixer2": 2,                                                                                                                                       
    "mixer3": 2,                                                                                                                                       
    "selector": None,                                                                                                                                  
    "pump-in": 2,                                                                                                                                      
    "pump-out": 2,                                                                                                                                     
    "time-start": "10:12",                                                                                                                             
    "active": 1,                                                                                                                                       
}
sched_active.append(state)

# Append new_schedule to sched_active
sched_active.append(new_schedule)
sched_active.append(new_schedule1)
sched_active.append(new_schedule2)
sched_active.append(new_schedule3)
sched_active.append(new_schedule4)

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
    print("current_time", current_time)
    current_time_str = current_time.strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M")

    print("current_time string", current_time)

    # Get the time-start value from the schedule and convert it to a datetime object
    time_start = datetime.strptime(schedule['time-start'], "%H:%M")
    print("time_start", time_start)
    # Calculate the difference between the current time and the time-start value
    time_difference = time_start - current_time

    print("time_difference", time_difference)
    # # Compare the time difference to zero
    # if time_difference.total_seconds() > 0:
    #     print("The time difference is larger than zero.")
    # elif time_difference.total_seconds() < 0:
    #     print("The time difference is less than zero.")
    # else:
    #     print("The time difference is zero.")

    # Convert the time difference to minutes and return it
    return time_difference.total_seconds() / 60

# Sort sched_active based on the time difference in minutes
sched_active.sort(key=get_time_difference_in_minutes)

# Remove duplicate schedules based on the time-start value
sched_active = remove_duplicate_schedules(sched_active)
# Print the sorted sched_active
for schedule in sched_active:
    print(schedule)