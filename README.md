# About the project:

 1. This was part of my Notworking and Operating Systems Essentials (NOSE2 COMPSCI2024) course in Level 2.
 2. Implemented the most popular OS scheduling algorithms only: First Come First Serve - FCFS, Shortest Job First - SJF, Round Robin - RR and Shortest Remaining Time First - SRTF.
 3. I only implemented the algorithms; I did not design the Discrete Event Simulator - DES.
 4. 

# About the scheduling algorithms:

 1. **FCFS** (non-pre-emptive): Processes should be executed in the
    order in which they arrived at the system. Conceptually, when a
    process arrives at the system, it is added to a queue. The
    scheduling algorithm will always pick the first process in the queue
    and will execute it to completion. It will then proceed with the
    next process in the queue, and so on.
 2. **SJF** (non-pre-emptive): Processes are prioritised based on their
    service time. Conceptually, on arrival, processes are added to a
    priority queue, which is sorted in ascending order of service time.
    The scheduling algorithm will then always pick the first process in
    the queue and will execute it to completion. It will then proceed
    with the next process in the queue, and so on.
 3. **RR** (pre-emptive): On arrival, processes are added to a queue.
    Conceptually, the algorithm will pick the first process in the
    queue, execute it for a specified amount of time (also known as a
    time-slice or quantum), and if the process needs more time it will
    then be added to the end of the queue.
 4. **SRTF** (pre-emptive): This is a pre-emptive version of the SJF
    algorithm above. Conceptually, whenever a change occurs in the
    system (i.e., a new process arrives, a running process terminates,
    etc.), the scheduler is called to select the process among those in
    the READY state with the minimum remaining execution time. This
    process will then be pre-empted when a new change occurs that
    results in some other process having a lower remaining execution
    time than the currently executing one.

# How to use:

 1.  Make sure you are in the right directory. If not, use  `cd <YOUR/FOLDER/PATH>`  to navigate to the correct folder.
 2. Use the following command to test the algorithms using a random seed:

    python main.py

  3. To specify the seed:

    python main.py -S <SEED>
  4. To get help:

    python main.py -h

# Thing I learnt when developing this:

 1. OS scheduling algorithms and how they work exactly.
 2. Developed my skills on OOP in Python.
 3. Improved my problem-solving and critical-thinking skills.
