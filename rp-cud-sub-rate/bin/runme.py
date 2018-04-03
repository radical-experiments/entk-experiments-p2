import radical.pilot as rp
import sys, time

if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 2:
        print 'usage: python runme.py <bulk size> <number of tasks>'
        sys.exit(1)

    bulk_size = int(args[0])
    num_tasks  = int(args[1])

    session = rp.Session()
    umgr = rp.UnitManager(session=session)

    cuds = list()
    for i in range(0, num_tasks):

        # create a new CU description, and fill it.
        # Here we don't use dict initialization.
        cud = rp.ComputeUnitDescription()
        cud.executable       = '/bin/date'
        cuds.append(cud)


    cur_task_cnt = 0
    f = open('cud_submission.txt','w')
    f.write('start: %f\n'%time.time())
    while(cur_task_cnt < num_tasks):
        workload = list()
        wld_size = 0

        # tasks = copy_tasks
        for cud in cuds[cur_task_cnt:]:
            workload.append(cud)
            # copy_tasks.remove(task)
            wld_size+=1
            if wld_size == bulk_size:
                break   

        cur_task_cnt += wld_size

        umgr.submit_units(workload)

    f.write('end: %f\n'%time.time())



