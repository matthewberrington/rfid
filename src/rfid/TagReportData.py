import datetime
import csv
import os
class TagReportData:
    def __init__(self, config_dict, tag_report, hex_encoding = True):
        if hex_encoding:
            self.EPC = int(tag_report['EPC'], 16)
        else:
            self.EPC = int(tag_report['EPC'])

        for content, enabled in config_dict['tag_content_selector'].items():
            attr = enabler_to_key[content]
            if enabled:
                # if 'Timestamp' in content:
                #     timestamp = datetime.datetime.fromtimestamp(tag_report[attr]/1000000) #convert from us to s
                #     setattr(self, attr, timestamp)
                # else:
                setattr(self, attr, tag_report[attr])
            else:
                setattr(self, attr, None)

    
    def export_to_csv(self, filepath):
        columns = ['EPC',*enabler_to_key.values()]
        if not os.path.isfile(filepath):
            with open(filepath, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)

        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.EPC,
                     self.ROSpecID,
                     self.SpecIndex,
                     self.InventoryParameterSpecID,
                     self.AntennaID,
                     self.PeakRSSI,
                     self.ChannelIndex,
                     self.FirstSeenTimestampUTC,
                     self.LastSeenTimestampUTC,
                     self.TagSeenCount,
                     self.AccessSpecID])

enabler_to_key = {
    'EnableROSpecID': 'ROSpecID',
    'EnableSpecIndex': 'SpecIndex',
    'EnableInventoryParameterSpecID': 'InventoryParameterSpecID',
    'EnableAntennaID': 'AntennaID',
    'EnablePeakRSSI': 'PeakRSSI',
    'EnableChannelIndex': 'ChannelIndex',
    'EnableFirstSeenTimestamp': 'FirstSeenTimestampUTC',
    'EnableLastSeenTimestamp': 'LastSeenTimestampUTC',
    'EnableTagSeenCount': 'TagSeenCount',
    'EnableAccessSpecID': 'AccessSpecID',
}  
