#!.\env\Scripts\python.exe
import sys

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press enter to exit.")
    sys.exit(-1)
    
from sllurp import llrp
import logging
import time
import keyboard
import atexit
from datetime import datetime



sys.excepthook = show_exception_and_exit

#####################################
countdown_timer_seconds = 10
ignore_tag_time = 30 #in seconds
HEX_encoding = True
enabled_antennas = [1]
#####################################

def OnExitApp():
    print("Exit Python application")
    tag_logs.info("Exit Python application") 
    reader.disconnect()
 
now = datetime.now()
datestring = now.strftime('%Y-%m-%d')
atexit.register(OnExitApp)

formatter = logging.Formatter('%(asctime)s %(message)s')
formatter.default_time_format = "%H:%M:%S"
handler = logging.FileHandler('llrp_{}.log'.format(datestring)) 
handler.setFormatter(formatter)
logger = logging.getLogger()   
logger.setLevel(logging.DEBUG)  
logger.addHandler(handler)


handler2 = logging.FileHandler('tag_logs_{}.log'.format(datestring)) 
handler2.setFormatter(formatter)
tag_logs = logging.getLogger('test')   
tag_logs.setLevel(logging.INFO)  
tag_logs.propagate = False
tag_logs.addHandler(handler2)

lastseen = {}

def read_EPC(tag):
    if HEX_encoding:
        EPC = int(tag['EPC'],16)
    else:
        try:
            EPC = int(tag['EPC'])
        except ValueError:
            EPC = None
    return EPC

def cb (_,tags):
    #print(tags)
    for tag in tags:    
        EPC = read_EPC(tag)
        # print(EPC)
        timestamp = tag['FirstSeenTimestampUTC']

        if EPC == None:
            return

        if EPC not in lastseen or timestamp > lastseen[EPC] + ignore_tag_time*1e6:
            print("read tag " + str(EPC))
            tag_logs.info(EPC)
            keyboard.write(str(EPC)+'\r\n')
            lastseen[EPC] = tag['FirstSeenTimestampUTC']

lastseen = {}

config_dict = {
    'antennas': enabled_antennas,
    'report_every_n_tags': 1000,
    'report_timeout_ms': 100,
    # 'start_trigger_type': 'Periodic',
    # 'offset': 0,
    'period': 1, #ms to wait before start inventory again
    'tag_content_selector':{
        'EnableROSpecID': False,
        'EnableSpecIndex': False,
        'EnableInventoryParameterSpecID': False,
        'EnableAntennaID': False,
        'EnableChannelIndex': False,
        'EnablePeakRSSI': False,
        'EnableFirstSeenTimestamp': True,
        'EnableLastSeenTimestamp': False,
        'EnableTagSeenCount': True,
        'EnableAccessSpecID': False,}}

if __name__ == '__main__':
    config = llrp.LLRPReaderConfig(config_dict)
    reader = llrp.LLRPReaderClient('speedwayr-12-36-0f', config=config)
    reader.add_tag_report_callback(cb)

    print('Starting antenna and wedge in')
    for i in range(countdown_timer_seconds,0,-1):
        print(i)
        time.sleep(1)
  
    reader.connect()
    print('Started')    

    #Wait until keyboard interrupt to kill program
    try:
        while True:
            time.sleep(10)
    except  :
        reader.disconnect()
