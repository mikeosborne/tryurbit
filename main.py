#!/usr/bin/env python3

'''
    main.py - server side script for tryurbit web site
        runs all background services for tryurbit web site
        mine() - ensures minimum number of mined comets exists
        ready() - ensures minimum number of comets are ready
        drop() - kills comet, deletes pier after use
'''



import subprocess
import logging
from datetime import datetime, timedelta
import time
import os
import shutil
from pathlib import Path
from database import SessionLocal, engine
from sqlalchemy.sql import func

from globals import *
from model import *


#  Set up logging  
LOGFILE = 'main.log'
logging.basicConfig(filename=LOG_DIR+LOGFILE, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


#  Set up database    
db = SessionLocal()
Base.metadata.create_all(bind=engine)

# Get app globals
appglobals = db.query(AppGlobals).first()

'''
# Set up port lists
ports_available = [
    '8080',
    '8081',
    '8082',
    '8083',
    '8084',
    '8085',
    '8086',
    '8087',
    '8088',
    '8089',
    '8090'
]
ports_used = []
'''
procs_active = []

# Comet process class
class Comet_Process():
    proc = None
    pid = None
    
    def __init__(self, port, pier):
        self.proc = subprocess.Popen(['nohup', URBIT_EXE, 'run', '-d', '--http-port', port, pier], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.pid = self.proc.pid
        
    def __repr__(self):
        return('<PID {}>'.format(self.pid))
        
    
    
############################################################################################
###                                                                                      ###
###  mine() - compares number of mined comets to minimum required, mines them as needed  ###
###                                                                                      ###
############################################################################################

def mine():
    
    #  Get data
    act_mined_comets = db.query(Comet).filter(Comet.status == CometStatus.MINED).count()
    curcometid = db.query(func.max(Comet.id).label("maxid")).one().maxid + 1
    os.chdir(COMET_DIR)
    min_mined_comets = appglobals.min_mined_comets
    
    # Mine comets
    
    while act_mined_comets < min_mined_comets:
    
        pier = 'c' + str(curcometid).zfill(5)  # create zero filled comet pier
        
        # mine single comet
        poutput = subprocess.run([URBIT_EXE,'new','--comet',pier,'-x'], capture_output=True, text=True)
        
        # get comet name and code
        outstr = poutput.stdout.split('\n')
        tstr = [line for line in outstr if COMET_FOUND_STR in line]
        if not tstr:
            logging.error('No comet mined')
            return
        comet_name = tstr[0].split(COMET_FOUND_STR)[1]   # extract comet name from list
        
        tstr = [line for line in outstr if CODE_FOUND_STR in line]
        if not tstr:
            logging.error('No code found')
            return
        code = tstr[0].split(CODE_FOUND_STR)[1]          # extract code from list
        
        # add comet to db
        newcomet = Comet(comet_name, code, pier)
        db.add(newcomet)
        db.commit()
        
        # increment counters
        act_mined_comets += 1
        curcometid += 1 
        
        logging.info('{} mined code: {} pier: {}'.format(comet_name, code, pier))
        
    return



############################################################################################
###                                                                                      ###
###  ready() - compares number of mined comets to minimum required to be ready, boots    ###
###            them as needed                                                            ###
###                                                                                      ###
############################################################################################

def ready(): 
    
    #  get data
    act_ready_comets = db.query(Comet).filter(Comet.status == CometStatus.READY).count()
    act_mined_comets = db.query(Comet).filter(Comet.status == CometStatus.MINED).count()
    min_ready_comets = appglobals.min_ready_comets
    os.chdir(COMET_DIR)
    
    if act_ready_comets >= min_ready_comets:
        return
    
    if act_mined_comets + act_ready_comets < min_ready_comets:
        min_ready_comets = act_mined_comets + act_ready_comets
        logging.warning('{} ready comets needed, only {} available'.format(min_ready_comets, act_mined_comets + act_ready_comets))
        
    while act_ready_comets < min_ready_comets:       
        cur_comet = db.query(Comet).filter(Comet.status == CometStatus.MINED).first()
        if not cur_comet:
            logging.error('No mined comets avaiable!')
            return
        pier = cur_comet.pier
        
        # get availble port
        port = db.query(Ports).filter(Ports.available == True).first()
        if not port:
            logging.error('No avaiable ports!')
            return
        port.available = False 
               
        # boot up the comet    
        proc = Comet_Process(port.port, pier)
        procs_active.append(proc)
        
        # update the record
        cur_comet.port = port.port
        cur_comet.pid = proc.pid
        cur_comet.status = CometStatus.READY
        cur_comet.ready_ts = datetime.now()
        db.commit()
        logging.info('{} now ready on port: {} pid: {}'.format(cur_comet.name, cur_comet.port, cur_comet.pid))
        
        # increment counter
        act_ready_comets += 1
        
    return


############################################################################################
###                                                                                      ###
###  drop() - checks assigned timestamp for exiration time, kills processes and deletes  ###
###           pier as needed                                                             ###
###                                                                                      ###
############################################################################################
           
def drop():
    #  get assigned comets
    assigned_comets = db.query(Comet).filter(Comet.status == CometStatus.ASSIGNED).all()
    
    for comet in assigned_comets:
        if comet.assigned_ts < datetime.now() - timedelta(minutes=appglobals.max_time):
            # kill proc
            for proc in procs_active:
                if proc.pid == comet.pid:
                    try:
                        proc.proc.terminate()
                    except:
                        logging.error('error trying to terminate pid {}'.format(comet.pid))
                        break
                    procs_active.remove(proc)
                    break
                         
            # delete pier
            shutil.rmtree(COMET_DIR+comet.pier, ignore_errors=True) 
            
            #update db
            comet.dropped_ts = datetime.now()
            comet.status = CometStatus.DROPPED
            dbport = db.query(Ports).filter(Ports.port == comet.port).first()
            if not dbport:
                logging.error('couldn\'t find port {}'.format(comet.port))
            else:
                dbport.available = True
            
            db.commit()
            
    
    return
    

############################################################################################
###                                                                                      ###
###  main() - main loop                                                                  ###
###                                                                                      ###
############################################################################################

if __name__ == '__main__':
    
    logging.info('main script started')
    
    # Main loop
    while(True):
        mine()
        ready()
        drop()
        time.sleep(MAIN_LOOP_DELAY)

    db.close()
    logging.info('main script completed')

