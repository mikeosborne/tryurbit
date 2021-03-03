class CometStatus:
    DROPPED = 0     # comet no longer live, pier deleted
    MINED = 1       # comet mined, credetials generated, ready to boot
    READY = 2       # comet booted, port recorded
    ASSIGNED = 3    # comet assigned to user
    
URBIT_EXE = '/usr/bin/urbit-king'

COMET_DIR = '/home/mike/comets/'
LOG_DIR = '/home/mike/Projects/tryurbit/logs/'
COMET_FOUND_STR = 'boot: found comet ~'
CODE_FOUND_STR = 'code: ~'

MAIN_LOOP_DELAY = 1  # Seconds to wait between main loop cycle