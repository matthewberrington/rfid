from .Speedway import Speedway
from . import gui
import os

def run():
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

    host = "speedwayr-12-36-0F.local"
    username = "root"
    password = "impinj"
    export_directory = r'./logs'
    os.makedirs(export_directory, exist_ok=True)
    speedway = Speedway(host, username, password, export_directory)
    gui.gui(speedway, export_directory)

if __name__ == '__main__':
    run()
    