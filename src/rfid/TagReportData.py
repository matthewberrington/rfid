import datetime
import csv
import os

TAG_PARAMETERS = [
    'ROSpecID',
    'SpecIndex',
    'InventoryParameterSpecID',
    'AntennaID',
    'PeakRSSI',
    'ChannelIndex',
    'FirstSeenTimestampUTC',
    'LastSeenTimestampUTC',
    'TagSeenCount',
    'AccessSpecID']


class TagReportData:
    def __init__(self, tag_report, hex_encoding):
        for parameter in TAG_PARAMETERS:
            if parameter in tag_report.keys():
                setattr(self, parameter, tag_report[parameter])
            else:
                setattr(self, parameter, None)
        if hex_encoding:
            self.EPC = int(tag_report['EPC'], 16)
        else:
            self.EPC = int(tag_report['EPC'])
    
    def export_report(self, filepath):
        columns = ['EPC',*TAG_PARAMETERS]
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
            
    def export_report_simple(self, filepath):
        dt = datetime.datetime.fromtimestamp(self.FirstSeenTimestampUTC/1e6)
        columns = ['EPC', 'Time', 'Date']
        if not os.path.isfile(filepath):
            with open(filepath, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)

        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.EPC,
                    dt.strftime("%H:%M:%S.%f"),
                    dt.strftime("%d/%m/%Y")])