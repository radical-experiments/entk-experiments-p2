import os
import sys
import pika
from radical.entk import Task
from multiprocessing import Process, Event
import traceback
import json
import time

def sendr(qname, bulk_size, num_tasks):


    try:

        tasks = list()
        for cnt in range(num_tasks):

            task = Task()
            task.name = str(cnt)
            tasks.append(task)

        connection = pika.BlockingConnection(pika.ConnectionParameters( host=hostname, 
                                                                        port=port,
                                                                        heartbeat=0))
        channel = connection.channel()

        cur_task_cnt = 0
        f = open('sendr.txt','w')
        f.write('start: %f\n'%time.time())
        while(cur_task_cnt < num_tasks):
            workload = list()
            wld_size = 0

            # tasks = copy_tasks
            for task in tasks:
                workload.append(task.to_dict())
                # copy_tasks.remove(task)
                wld_size+=1
                if wld_size == bulk_size:
                    break

            cur_task_cnt += wld_size

            wld_as_json = json.dumps(workload)

            channel.basic_publish(  exchange = '',
                                    routing_key = qname,
                                    body = wld_as_json,
                                    # properties=pika.BasicProperties(
                                    #     delivery_mode = 2, # make message persistent
                                    #     )
                                )
        f.write('stop: %f\n'%time.time())

    except Exception as ex:
        print 'Error in sendr: %s'%ex
        print traceback.format_exc()



def recvr(qname, bulk_size, num_tasks):
    
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters( host=hostname, 
                                                                        port=port,
                                                                        heartbeat=0))
        channel = connection.channel()

        cur_task_cnt = 0
        f = open('recvr.txt','w')
        f.write('start: %f\n'%time.time())
        while(cur_task_cnt < num_tasks):
            method_frame, header_frame, body = channel.basic_get(queue=qname)
            if body:

                wld_as_json = json.loads(body)
                assert len(wld_as_json) == bulk_size
                cur_task_cnt+=bulk_size 
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        f.write('stop: %f\n'%time.time())
        f.close()
                

    except Exception as ex:
        print 'Error in recvr: %s'%ex
        print traceback.format_exc()


hostname = 'localhost'
port = 5672
qname = 'task_queue'

if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 2:
        print 'usage: python runme.py <bulk size> <number of tasks>'
        sys.exit(1)

    bulk_size = int(args[0])
    num_tasks  = int(args[1])

    connection = pika.BlockingConnection(pika.ConnectionParameters( host=hostname, 
                                                                    port=port,
                                                                    heartbeat=0))
    channel = connection.channel()
    channel.queue_delete(queue=qname)
    channel.queue_declare(queue=qname)

    # task_as_dict = json.dumps(executable_task.to_dict())
    p_sendr = Process(target=sendr, args=(qname, bulk_size, num_tasks))
    p_recvr = Process(target=recvr, args=(qname, bulk_size, num_tasks))

    p_sendr.start()
    p_recvr.start()
    p_sendr.join()
    p_recvr.join()

    channel.queue_delete(queue=qname)  

    connection.close()