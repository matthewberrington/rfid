import sys
from TagReportData import TagReportData

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press enter to exit.")
    sys.exit(-1)
    
from sllurp import llrp
import time
import atexit
from datetime import datetime

sys.excepthook = show_exception_and_exit

def OnExitApp():
    print("Exit Python application")
    reader.disconnect()
 
atexit.register(OnExitApp)

ignore_until = {}
def cb (reader, tag_reports):
    for tag_report in tag_reports:
        report = TagReportData(config_dict, tag_report)
        if not report.EPC in ignore_until.keys():
            report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
            ignore_until[report.EPC] = report.FirstSeenTimestampUTC + ignore_tag_time*1e6
        if ignore_until[report.EPC] < report.FirstSeenTimestampUTC:
            report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
            ignore_until[report.EPC] = report.FirstSeenTimestampUTC + ignore_tag_time*1e6



if __name__ == '__main__':
    config_dict = {
    'antennas': [1],
    'report_every_n_tags': 1000,
    'report_timeout_ms': 1000,
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
    config = llrp.LLRPReaderConfig(config_dict)
    reader = llrp.LLRPReaderClient('speedwayr-12-36-0f', config=config)
    reader.add_tag_report_callback(cb)

    reader.connect()
    print('Started')    

    #Wait until keyboard interrupt to kill program
    try:
        while True:
            time.sleep(1)
    except  :
        reader.disconnect()
