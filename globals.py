class CometStatus:
    DROPPED = 0     # comet no longer live, pier deleted
    MINED = 1       # comet mined, credetials generated, ready to boot
    READY = 2       # comet booted, port recorded
    ASSIGNED = 3    # comet assigned to user
    
URBIT_EXE = '/usr/bin/urbit-king'
HOST = '192.168.0.82:'
PROC_LIST = ['nohup', URBIT_EXE, 'run', '--port-forwarding', '--http-port']

COMET_DIR = '/home/mike/comets/'
LOG_DIR = '/home/mike/Projects/tryurbit/logs/'
COMET_FOUND_STR = 'boot: found comet ~'
CODE_FOUND_STR = 'code: ~'

MAIN_LOOP_DELAY = 1  # Seconds to wait between main loop cycle

APP_SECRET_KEY = 'iF i oNLY hAD a hAMMER, tHE wORLD wOULD bE iN mY oRBIT'