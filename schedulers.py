from des import SchedulerDES
from process import Process, ProcessStates
from event import Event, EventTypes


class FCFS(SchedulerDES):
    # scheduler_func is reponsible of selecting which process will run next and return this process so it can be used by the dispatcher_func
    def scheduler_func(self, cur_event):
        #! cur_event is one event from event_queue and it is an instance if  event
        #! change status to PROC_CPU_REQ or PROC_CPU_DONE (?)
        #! cur_event has event_id(), event_type(), event_time()
        #! cur_event time is always <= self.time
        # print(f"Scheduler: looking for id = {cur_event.process_id}") #! del
        for i, process in enumerate(self.processes):
            if (cur_event.process_id) == (process.process_id):
                # process.process_state = ProcessStates.READY
                return process
                
            # then make a new process
            #     process_to_run = Process(process_id=cur_event.process_id(), arrival_time=self.time, service_time=cur_event.event_time())
            #     self.__update_process_states() # set new process state to READY
            #     #! process_to_run.process_state = ProcessStates.READY

        
    # dispatcher_func is reponsible of running the provided process and advance the time (system clock) and return new event with EventTypes.PROC_CPU_DONE or EventTypes.PROC_CPU_REQ depending of if the process needs more CPU processing or not
    def dispatcher_func(self, cur_process):
        #! your function should make sure to update the process state as it goes.
        #! The returned event should be of type PROC_CPU_REQ if the process needs more time to finish, or PROC_CPU_DONE if the process terminated during the last execution.

        cur_process.process_state = ProcessStates.RUNNING
        finish_time = self.time + cur_process.service_time
        # append duration time: tuple => (start time , finished time)
        cur_process._execution_times.append((self.time, finish_time)) #! is it ok to access _ fields?
        
        # print(f"current time is {self.time}") #! del
        
        cur_process._remaining_time = 0 # will run until completion
        cur_process._process_state = ProcessStates.TERMINATED
        
        process_id = cur_process.process_id
        eventtype = EventTypes.PROC_CPU_DONE
        
        # print("Dispatcher: info of the new event: " , process_id, eventtype, finish_time) #! del
        
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event
        


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        process_to_run = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.service_time)
        # processs =[process.service_time for process in self.processes]
        # print("## SJF process to run service time is:", process_to_run)
        # print("process ids that are ready:", [process.process_id for process in self.processes if process.process_state == ProcessStates.READY])
        # print("process service times:", [process.service_time for process in self.processes])
        
        # print(min([process.service_time for process in process_to_run]))
        # for i, process in enumerate(self.processes):
        #     if (cur_event.process_id) == (process.process_id):
        #         process_to_run = []
        # pass
        return process_to_run

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        finish_time = self.time + cur_process.service_time
        # append duration time: tuple => (start time , finished time)
        cur_process._execution_times.append((self.time, finish_time))
        
        # print(f"current time is {self.time}") #! del
        
        cur_process._remaining_time = 0 # will run until completion
        cur_process._process_state = ProcessStates.TERMINATED
        
        process_id = cur_process.process_id
        eventtype = EventTypes.PROC_CPU_DONE
        
        # print("Dispatcher: info of the new event: " , process_id, eventtype, finish_time) #! del
        
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        # get the process that has the same id as cur_event:
        # process_to_run = [process for process in self.processes if (cur_event.process_id == process.process_id) and (process.process_state == ProcessStates.READY)][0]

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
        if cur_process._remaining_time == 0:
            cur_process._process_state = ProcessStates.TERMINATED
            eventtype = EventTypes.PROC_CPU_DONE
            
        # if more CPU processing is still required:
        else:
            cur_process._process_state = ProcessStates.READY
            eventtype = EventTypes.PROC_CPU_REQ
            
        process_id = cur_process.process_id
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        process_to_run = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.remaining_time)
        return process_to_run

    #! do we run the process for a slice of time then check processes list to run the shortest remaining time process?
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # will run cur_process until a new event is ready (until next_event_time):
        next_event_time = self.next_event_time()
        # finish time is not known yet:
        finish_time = 0
        
        if next_event_time>self.time or cur_process.remaining_time>0:
            # choose the min time to run the process for, either until next event or until termination:
            actual_run_for = min(next_event_time-self.time, cur_process.remaining_time)
        
            cur_process._remaining_time -= actual_run_for #! is ._remaining_time (protected field) same as .remaining_time (the property) ?
        
            finish_time = self.time + actual_run_for
            
            # append duration time: tuple => (start time , finished time)
            cur_process._execution_times.append((self.time, finish_time))
        
        
        
        if cur_process._remaining_time == 0:
            cur_process._process_state = ProcessStates.TERMINATED
            eventtype = EventTypes.PROC_CPU_DONE
            
        else:
            cur_process._process_state = ProcessStates.READY
            eventtype = EventTypes.PROC_CPU_REQ
        
        process_id = cur_process.process_id
        new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        return new_event
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # cur_process.process_state = ProcessStates.RUNNING
        
        # # run the process for a slice of time
        # # .run_for will add the execution time tuple to execution list:
        # actually_run_for = cur_process.run_for(quantum=self.quantum, cur_time=self.time)
        # finish_time = self.time + actually_run_for
        
        # process_id = cur_process.process_id
        
        # # if no more CPU processing is required by this process:
        # if cur_process._remaining_time == 0:
        #     cur_process._process_state = ProcessStates.TERMINATED
        #     eventtype = EventTypes.PROC_CPU_DONE

        # # if this process did not finish executing, return a new event with the remaining time so we can check again (by the scheduler_func) if there is another process with a shorter remaining time in the processes queue available:
        # else:
        #     cur_process._process_state = ProcessStates.READY
        #     eventtype = EventTypes.PROC_CPU_REQ
            
        # new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        # return new_event

        # check that is there is a process with a shorter time than the current process in processes queue:
        # shortest_process = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.remaining_time)
        
        # as long as cur_process is the shortest process in the processes queue:
        # while cur_process == shortest_process:
            
        #     actually_run_for = cur_process.run_for(quantum=self.quantum, cur_time=self.time)
        #     finish_time += actually_run_for
            
            # if cur_process finished its execution, the dispatcher_func will return:
            # if cur_process._remaining_time == 0:
            #     cur_process._process_state = ProcessStates.TERMINATED
            #     process_id = cur_process.process_id
            #     eventtype = EventTypes.PROC_CPU_DONE
            #     new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
            #     return new_event
            
            # # else, calculate the shortest remaining time in the processes queue again:
            # else:
            #     shortest_process = min([process for process in self.processes if process.process_state == ProcessStates.READY], key=lambda x:x.remaining_time)
            
            
        # if more CPU processing is still required, but another process has a shorter remaining time in the processes queue:
        
        # cur_process._process_state = ProcessStates.READY
        # process_id = cur_process.process_id
        # eventtype = EventTypes.PROC_CPU_REQ
            
        # new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        # return new_event
        
        # finish_time = self.time + cur_process.service_time
        # # append duration time: tuple => (start time , finished time)
        # cur_process._execution_times.append((self.time, finish_time))
        # cur_process._remaining_time = 0 # will run until completion
        # cur_process._process_state = ProcessStates.TERMINATED
        
        # process_id = cur_process.process_id
        # eventtype = EventTypes.PROC_CPU_DONE
        
        # new_event = Event(process_id=process_id, event_type=eventtype, event_time=finish_time)
        # return new_event
