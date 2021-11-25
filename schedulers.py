from des import SchedulerDES
from process import ProcessStates
from event import Event, EventTypes


class FCFS(SchedulerDES):
    # scheduler_func is reponsible of selecting which process will run next and return this process so it can be used by the dispatcher_func
    def scheduler_func(self, cur_event):
        for i, process in enumerate(self.processes):
            if (cur_event.process_id) == (process.process_id):
                return process

    # dispatcher_func is reponsible of running the provided process and advance the time (system clock) and return new event with EventTypes.PROC_CPU_DONE or EventTypes.PROC_CPU_REQ depending of if the process needs more CPU processing or not
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        
        actually_run_for = cur_process.run_for(quantum=cur_process.service_time, cur_time=self.time)
        
        finish_time = self.time + actually_run_for

        cur_process.process_state = ProcessStates.TERMINATED
        
        process_id = cur_process.process_id
        eventtype = EventTypes.PROC_CPU_DONE
        
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event
        


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        # choose the process with the shortest service time from processes list:
        process_to_run = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.service_time)
        return process_to_run

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        
        actually_run_for = cur_process.run_for(quantum=cur_process.service_time, cur_time=self.time)
        
        finish_time = self.time + actually_run_for
        
        cur_process.process_state = ProcessStates.TERMINATED
        
        process_id = cur_process.process_id
        eventtype = EventTypes.PROC_CPU_DONE
        
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        # get the process with the same id as cur_event:
        for process in self.processes:
            if (cur_event.process_id == process.process_id) and (process.process_state == ProcessStates.READY):
                return process

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        
        # run the process for a slice of time
        # .run_for will add the execution time tuple to execution list:
        actually_run_for = cur_process.run_for(quantum=self.quantum, cur_time=self.time)
        
        finish_time = self.time + actually_run_for
        
        # if no more CPU processing is required by this process:
        if cur_process.remaining_time == 0:
            cur_process.process_state = ProcessStates.TERMINATED
            eventtype = EventTypes.PROC_CPU_DONE
            
        # if more CPU processing is still required:
        else:
            cur_process.process_state = ProcessStates.READY
            eventtype = EventTypes.PROC_CPU_REQ
            
        process_id = cur_process.process_id
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        process_to_run = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.remaining_time)
        return process_to_run
    
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # will run cur_process until a new event is ready (until next_event_time):
        next_event_time = self.next_event_time()
        # finish time is not known yet so set it to 0:
        finish_time = 0
        
        if (next_event_time > self.time) or (cur_process.remaining_time > 0):
            # choose the min time to run the process for, either until the next event becoming ready or until termination:
            actual_run_for = min(next_event_time-self.time, cur_process.remaining_time)
            
            actually_run_for = cur_process.run_for(quantum=actual_run_for, cur_time=self.time)
        
            finish_time = self.time + actually_run_for
            
        
        if cur_process.remaining_time == 0:
            cur_process.process_state = ProcessStates.TERMINATED
            eventtype = EventTypes.PROC_CPU_DONE
            
        else:
            cur_process.process_state = ProcessStates.READY
            eventtype = EventTypes.PROC_CPU_REQ
        
        process_id = cur_process.process_id
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event
        
        