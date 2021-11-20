from des import SchedulerDES
from process import Process, ProcessStates
from event import Event, EventTypes


class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        #! cur_event is one event from event_queue and it is an instance if  event
        #! change status to PROC_CPU_REQ or PROC_CPU_DONE (?)
        #! cur_event has event_id(), event_type(), event_time()
        #! cur_event time is always <= self.time
        print(f"Scheduler: looking for id = {cur_event.process_id}")
        for i, process in enumerate(self.processes):
            if (cur_event.process_id) == (process.process_id):
                process.process_state = ProcessStates.READY
                return process
                
            # then make a new process
            #     process_to_run = Process(process_id=cur_event.process_id(), arrival_time=self.time, service_time=cur_event.event_time())
            #     self.__update_process_states() # set new process state to READY
            #     #! process_to_run.process_state = ProcessStates.READY

        

    def dispatcher_func(self, cur_process):
        #! your function should make sure to update the process state as it goes.
        #! The returned event should be of type PROC_CPU_REQ if the process needs more time to finish, or PROC_CPU_DONE if the process terminated during the last execution.

        # add the time this process took to the execution time list:
        cur_process.process_state = ProcessStates.RUNNING
        # append duration time: (start time , finished time)
        finish_time = self.time + cur_process.service_time
        cur_process._execution_times.append((self.time, finish_time))
        print(f"current time is {self.time}")
        
        cur_process._remaining_time = 0 #! cur_process.service_time() - runtime
        cur_process._process_state = ProcessStates.TERMINATED
        
        processid = cur_process.process_id
        # print(processid == )
        eventtype = EventTypes.PROC_CPU_DONE
        
        print("Dispatcher: info of the new event: " , processid, eventtype, finish_time)
        
        new_event = Event(process_id=processid, event_type=eventtype, event_time=finish_time)
        return new_event
    
        # for i, event in enumerate(self.events_queue):
        #     if event.process_id == cur_process.process_id:
        #         # the event must be finished according how FCFS works:
        #         event._event_type = EventTypes.PROC_CPU_DONE #! how to set this? there is not setter!
        #         return event
        


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass
