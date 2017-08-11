#-*- encoding=UTF-8 -*-

import os
from celery import Celery
from celery_app import app
import struct
import encode_decode
import time
import binascii
from write_db import write_db
from private_key_gene import private_key_gene
import rsa
from reg_limit import limit_ip
from exe_limit import exe_limit
import traceback
import logging
import multiprocessing
from tasks_db import add_tasks, get_tasks, get_a_task, delete_tasks, count_tasks
import subprocess


@app.task
def Execution(casename, Username, task_id, filetype): 
    try:
        Database = '/usr/local/' + Username + '/' + Username + '_exe.db'
        user_cwd = '/'.join(casename.split('/')[:-1])
        if(filetype == 'exe_py'):
            command_line = 'cd ' + user_cwd + ';' + 'python3 ' + casename + ';exit 0'
        elif(filetype == 'exe_c'):
            command_line = 'cd ' + user_cwd + ';' + 'gcc -o ' + casename[:-2] + ' ' + casename + ';' + casename[:-2]
        elif(filetype == 'exe_pbin'):
            command_line = r'echo 1 > /sys/devices/soc0/amba@0/f8007000.ps7-dev-cfg/is_partial_bitstream;'+ 'cat '+ casename + ' > /dev/xdevcfg'+ ';exit 0'
        t = time.ctime()
        delete_tasks(task_id, casename, Username, 'inqueue',  r'/usr/local', Database = '/usr/local/' + Username + '/'  + 'tasks.db')
        task_id = add_tasks(casename, 'processing', t, Username, r'/usr/local', Database = '/usr/local/' + Username + '/'  + 'tasks.db')
        #开始执行就解除inqueue状态
        try:
            #print(command_line)
            cmd_res = subprocess.check_output(command_line, shell=True)
            time.sleep(5)
            if(not cmd_res):
                with open(casename + '_res.txt', 'wb') as fres:
                    fres.write(cmd_res)
        except subprocess.CalledProcessError as err:
            print('error run', str(err))
            add_tasks(casename, 'error', t, Username, r'/usr/local', result_filedir = casename + '_res.txt' , Database = '/usr/local/' + Username + '/'  + 'tasks.db')
        else:
            exe_info = casename + ' executed.'
            print(exe_info)
        
            logging.info(exe_info)    #执行完毕后记录执行信息

            t = time.ctime()
        
            add_tasks(casename, 'finished', t, Username, r'/usr/local', result_filedir = casename + '_res.txt' , Database = '/usr/local/' + Username + '/'  + 'tasks.db')
        
        print('task id:',task_id)
        #执行完毕就解除processing状态
        res = delete_tasks(task_id, casename, Username, 'processing',  r'/usr/local', Database = '/usr/local/' + Username + '/'  + 'tasks.db')
        print(res)
        exe_limit(casename, Database, pid = 1)

        print("delete limit")
    except Exception as e:
        traceback.print_exc()
        t = time.ctime()
        exe_limit(casename, Database, pid = 1)
        add_tasks(casename, 'error', t, Username, r'/usr/local', Database = '/usr/local/' + Username + '/'  + 'tasks.db')

	
