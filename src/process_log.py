#!/usr/bin/python -tt
# Shanyun Gao, 04/2017

import sys
import re
import os
from datetime import datetime, timedelta
from max_binheap import max_BinHeap
from queue import Queue


""" ultimate generator to generate informations from each line
    line format: IP - - [datetime timezone] "GET resource HTTP/1.0" code bytes

    match1.gr = IP
    match2.gr(1, 2) = datetime, timezone 
    match3.gr(1, 2, 3) = GET, resource, HTTP/1.0
    match4.gr(1, 2) = code, bytes 

    yield: tuple(IP, datetime, timezone, GET, resource, HTTP/1.0, code, bytes)
                  |       |         |       |     |        |        |     |
    yield: tuple( 0  ,    1    ,    2    ,  3 ,   4 ,      5    ,   6 ,   7  )
"""
def gen_info(filename):
    with open(filename, 'rU') as file:
        for row in file:
            match1 = re.search(r'[\w.-]+', row)
            match2 = re.search(r'\[(.*?)\s(-\d\d\d\d)\]', row)
            match3 = re.search(r'\"([A-Z]+)\s(.*?)\s([\/\w.]+)\"', row)
            match4 = re.search(r'(\d+)\s(\d+)', row)
            if match1 and match2 and match3 and match4:
                yield (
                        match1.group(), match2.group(1), match2.group(2),
                        match3.group(1), match3.group(2), match3.group(3),
                        match4.group(1), match4.group(2)
                        )


"""
    FEATURE 1:

    Function 'active_host' return a dictionary 'num_access_dict' from the log
    file.
    num_access_dict = {IP: # requests, ...}
"""
def active_host(filename):
    num_access_dict = {}
    for info in gen_info(filename):
        host = info[0]
        if not host in num_access_dict:
            num_access_dict[host] = 1
        else:
            num_access_dict[host] += 1
    return num_access_dict

"""
    Function 'feature1_write' write feature 1 results to hosts.txt
    1. generate dictionary 'num_access_dict' from log file
    2. generate max binary heap(priority queue) 'activeIP_bh' from the above
       dictionary 
    3. 'activeIP_bh' dequeue 10 times to generate the top 10 active IP and
       write to file 'hosts.txt'
"""
def feature1_write(filename):
    num_access_dict = active_host(filename)
    activeIP_bh = max_BinHeap()
    activeIP_bh.build_heap(num_access_dict)

    with open(os.path.join(os.getcwd(), 'log_output/hosts.txt'), 'w') as ofile:
        counter = 1
        while (counter <= 10) and (activeIP_bh.size() > 0):
            tuple = activeIP_bh.del_max()
            string = tuple[0]+','+str(tuple[1])
            ofile.write('%s\n' % string)
            counter += 1


"""
    FEATURE 2:

    Function 'resource_band': generate dictionary 'resrc_byte'
    dictionary resrc_byte = {resource: sum(bytes), ...}

    Function 'feature2_write' is similar to 'feature1_write'
"""
def resource_band(filename):
    resrc_byte = {}
    
    for info in gen_info(filename):
        resrc = info[4]
        byte = info[7]
        if not resrc in resrc_byte:
            resrc_byte[resrc] = int(byte)
        else:
            resrc_byte[resrc] += int(byte)

    return resrc_byte

def feature2_write(filename):
    resrc_bwth = resource_band(filename)
    resrc_bh = max_BinHeap()
    resrc_bh.build_heap(resrc_bwth)
    with open(os.path.join(os.getcwd(), 'log_output/resources.txt'), 'w') as ofile:
        counter = 1
        while (counter <= 10) and (resrc_bh.size() > 0):
            tuple = resrc_bh.del_max()
            ofile.write('%s\n' % tuple[0])
            counter += 1


"""
    Feature 3, a more regirous approach, but not necessarily better
    time complexity: O(n)
    space complexity: O(n)

    time_queue: a queue to keep track of time
    current_count: integer to count number of visits within one hour from a
                   certain timestamp
    hr_vst_dict = {timestamp: # visits}
"""
def hr_visit(filename):
    time_queue = Queue()
    current_count = int(0)
    hr_vst_dict = {}
    parse_time = '%d/%b/%Y:%H:%M:%S'

    for info in gen_info(filename):
        time = info[1]
        if time_queue.is_empty():
            time_queue.enqueue(time)
            current_count += 1
        elif time_queue.size() > 0:
            time1 = time_queue.front()
            time2 = time
            time1_real = datetime.strptime(time1, parse_time)
            time2_real = datetime.strptime(time2, parse_time)
            interval = int((time2_real - time1_real).total_seconds())
            if interval < 3600:
                time_queue.enqueue(time)
                current_count += 1
            else:
                timestamp = time_queue.dequeue()
                if not timestamp in hr_vst_dict:
                    hr_vst_dict[timestamp] = current_count
                current_count = current_count - 1

    """
        In the last one hour (or less), 60min window start time is every second
        until the very last one. Meaning it is not necessarily when an event
        happened.

        int variable 'counter' means 10 is enough for the purpose, i.e. start
        from the first event at the front of the queue, end at the 10th second.

        funny right?
    """
    counter = 0
    stamp = time_queue.front()
    while (time_queue.size() > 0) and (counter < 10):
        stamp_real = datetime.strptime(stamp, parse_time)
        front_real = datetime.strptime(time_queue.front(), parse_time)

        if (stamp == time_queue.front()) and (not stamp in hr_vst_dict):
            hr_vst_dict[stamp] = current_count
            counter += 1
            time_queue.dequeue()
            current_count = current_count - 1
        elif (stamp == time_queue.front()) and (stamp in hr_vst_dict):
            time_queue.dequeue()
            current_count = current_count - 1
        elif stamp_real < front_real:
            stamp_real = stamp_real + timedelta(seconds=1)
            stamp = stamp_real.strftime(parse_time)
            if (stamp_real < front_real) and (not stamp in hr_vst_dict):
                hr_vst_dict[stamp] = current_count
                counter += 1
            elif (stamp_real == front_real) and (not stamp in hr_vst_dict):
                hr_vst_dict[stamp] = current_count
                counter += 1
                time_queue.dequeue()
                current_count = current_count - 1

    return hr_vst_dict

def feature3_write(filename):

    hrvisit_dict = hr_visit(filename)
    hours_bh = max_BinHeap()
    hours_bh.build_heap(hrvisit_dict)
    
    """
        Function 'feature3_write' differs from the first two in that it
        implements a feature -- in the case of #visits associated with
        different timestamps are same, the printed timestamps are sorted in
        ascending order. For the mere purpose of meeting the test result
        provided by /insight_testsuite

        time_num = [(time, #visits)], a list of tuple records the top 10 busy
        window;

        num_time_dict = {#visits: [time1, time2]}, a dictionary maps the same
        #visits to a list of timestamps. The timestamp list will be sorted
        later;

        num_list = [#visits], is a list of different #visits and becomes sorted
        in descending order later;

        again, funny right? 
    """
    time_num = [] 
    counter = 1
    while (counter <= 10) and (hours_bh.size() > 0):
        tuple = hours_bh.del_max()
        time_num.append(tuple)
        counter += 1

    num_time_dict = {}
    for tup in time_num:
        if not tup[1] in num_time_dict:
            num_time_dict[tup[1]] = [tup[0]]
        else:
            num_time_dict[tup[1]].append(tup[0])

    num_list = []
    parse_time = '%d/%b/%Y:%H:%M:%S'
    for num in num_time_dict:
        num_list.append(num)
        # sort timestamps associated with each #visits
        num_time_dict[num] = (
                sorted(num_time_dict[num], key=lambda x:
                datetime.strptime(x, parse_time))
                )
    num_list.sort(key=int, reverse=True)

    with open(os.path.join(os.getcwd(), 'log_output/hours.txt'), 'w') as ofile:
        for num in num_list:
            for time in num_time_dict[num]:
                string = time + ' -0400' + ','  + str(num)
                ofile.write('%s\n' % string)    
                
                
"""
    FEATURE 3 alternative:

    Function 'hour_visit' returns a dictionary 'hour_visit'
    hour_visit = {timestamp (first event since an hour start): # visits, ...}

    dictionary hr_visit_dict = {hour: [timestamp, # visits]}
    hour format: 'DD/MON/YYYY:HH'; timestamp format: 'DD/MON/YYYY:HH:MM:SS'
    
    Function 'feature3_write' is similar to 'feature1_write' and
    'feature2_write'
"""
def hour_visit(filename):
    hr_visit_dict = {}
    hour_visit = {}

    for info in gen_info(filename):
        time_str = info[1]
        current_hour = time_str[:14]
        if not current_hour in hr_visit_dict:
            hr_visit_dict[current_hour] = [time_str, 1]
        else:
            hr_visit_dict[current_hour][1] += 1

    for values in hr_visit_dict.viewvalues():
        hour_visit[values[0]] = values[1]

    return hour_visit

def feature3_alternative(filename):
    hrvisit_dict = hour_visit(filename)
    hours_bh = max_BinHeap()
    hours_bh.build_heap(hrvisit_dict)
    with open(os.path.join(os.getcwd(), 'log_output/busyhr.txt'), 'w') as ofile:
        counter = 1
        while (counter <= 10) and (hours_bh.size() > 0):
            tuple = hours_bh.del_max()
            string = tuple[0][:18]+'00 -0400'+','+str(tuple[1])
            ofile.write('%s\n' % string)
            counter += 1


"""
    FEATURE 4:

    Function 'block_attempt' returns a list 'log_list' which records attempts
    that would been blocked.

    dictionary IP_counter = {IP: # consecutive failed logins within 20 seconds
    (# <= 3)}. IP_counter = len(fail_attempt[IP]).

    dictionary fail_attempt = {IP : [time1, time2, time3]}, fail_attempt[IP] is
    a list of timestamps when consecutive failed logins within 20 seconds
    occured. len(fail_attempt[IP] <= 3).

    dictionary start_log = {IP: time}, time is the latest time among the 3
    consecutive failed attempts within 20 seconds.

    list log_list = [attempt1, attempt2, ...] records blocked attemtps.

    clock1 = 20-second-window
    clock2 = 5-minute-window
"""
def block_attempt(filename):
    IP_counter = {}
    from collections import defaultdict
    fail_attempt = defaultdict(list)
    start_log = {}
    log_list = []
    clock1 = 20
    clock2 = 300
    parse_time = '%d/%b/%Y:%H:%M:%S'

    for info in gen_info(filename):
        IP = info[0]
        time = info[1]
        code = info[6]
        record = (
                info[0] + ' - - [' + info[1] + ' ' + info[2] + '] "' + info[3]
                + ' ' + info[4] + ' ' + info[5] + '" ' + info[6] + ' ' + info[7]
                )

        failed = (code == str(401))
        if (not IP in fail_attempt) and failed:
            fail_attempt[IP].append(time)
            IP_counter[IP] = len(fail_attempt[IP])
        elif (IP in fail_attempt) and (IP_counter[IP] == 1) and failed:
            time1 = fail_attempt[IP][0]
            time2 = time
            time1_real = datetime.strptime(time1, parse_time)
            time2_real = datetime.strptime(time2, parse_time)
            interval = int((time2_real - time1_real).total_seconds())
            if interval <= clock1:
                fail_attempt[IP].append(time)
                IP_counter[IP] = len(fail_attempt[IP]) 
            else:
                fail_attempt[IP] = time
                IP_counter[IP] = len(fail_attempt[IP])
        elif (IP in fail_attempt) and (IP_counter[IP] == 2) and failed:
            time1 = fail_attempt[IP][0]
            time2 = time
            time1_real = datetime.strptime(time1, parse_time)
            time2_real = datetime.strptime(time2, parse_time)
            interval = int((time2_real - time1_real).total_seconds())
            if interval <= clock1:
                fail_attempt[IP].append(time)
                IP_counter[IP] = len(fail_attempt[IP]) 
            else:
                fail_attempt[IP] = time
                IP_counter[IP] = len(fail_attempt[IP])
                
        if (not IP in start_log) and (IP in IP_counter) and (IP_counter[IP] == 3):
            start_log[IP] = fail_attempt[IP][2]
        elif (IP in start_log) and (IP_counter[IP] == 3):
            time1 = start_log[IP]
            time2 = time
            time1_real = datetime.strptime(time1, parse_time)
            time2_real = datetime.strptime(time2, parse_time)
            interval = int((time2_real - time1_real).total_seconds())
            if interval <= clock2:
                log_list.append(record)
            else:
                if not failed:
                    fail_attempt[IP] = []
                    IP_counter[IP] = len(fail_attempt[IP])
                    del start_log[IP]
                else:
                    fail_attempt[IP] = time
                    IP_counter[IP] = len(fail_attempt[IP])
                    del start_log[IP]

    return log_list

def feature4_write(filename):
    log_list = block_attempt(filename)
    with open(os.path.join(os.getcwd(), 'log_output/blocked.txt'), 'w') as ofile:
        for attempt in log_list:
            ofile.write('%s\n' % attempt)

def main():
    if len(sys.argv) != 3:
        print 'usage: ./process_log.py process file'
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == 'process':
        feature1_write(filename)
        feature2_write(filename)
        feature3_write(filename)
        feature4_write(filename)
        feature3_alternative(filename)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
