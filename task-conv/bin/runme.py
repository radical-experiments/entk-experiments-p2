from radical.entk.execman.task_processor import create_cud_from_task
from radical.entk.execman.task_processor import create_task_from_cu
import sys, time
from radical.entk import Task


if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: python runme.py <number of tasks>'
        sys.exit(1)

    num_tasks  = int(args[0])
    tasks_set = set()
    e_dict = dict()

    for cnt in range(num_tasks):

        t = Task()  
        t.name = 't%s'%cnt
        t.executable = ['/bin/bash']   
        t.arguments = ['-l', '-c', 'base64 /dev/urandom | head -c %s > output.txt'%cnt]
        t.input_data = ['abc%s.txt'%cnt]
        t.output_data = ['xyz%s.txt'%cnt]

        tasks_set.add(t)

    f = open('cud_2_task.txt','w')
    f.write('start: %f\n'%time.time())
    for td in tasks_set:
        create_cud_from_task(td, e_dict)
    f.write('end: %f\n'%time.time())