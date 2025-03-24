from sllurp import llrp
from rshell_commands import get_time_UTC, set_time_UTC
from TagReportData import TagReportData
import keyboard
import datetime

class Speedway:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.keyboard_wedge_enabled = False
        self.hex_encoding = True
        self.reader = None
        self.ignore_tag_time = 20
        self.ignore_until = {}
        self.config_dict = {
            'antennas': [],
            'report_every_n_tags': 1000,
            'report_timeout_ms': 1000,
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
                'EnableAccessSpecID': False}}

    def configure(self):
        config = llrp.LLRPReaderConfig(self.config_dict)
        self.reader = llrp.LLRPReaderClient('speedwayr-12-36-0f', config=config)
        self.reader.add_tag_report_callback(self.cb)

    def cb (self, reader, tag_reports):
        for tag_report in tag_reports:
            report = TagReportData(tag_report, self.hex_encoding)
            if not report.EPC in self.ignore_until.keys():
                report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
                self.ignore_until[report.EPC] = report.FirstSeenTimestampUTC + self.ignore_tag_time*1e6
                if self.keyboard_wedge_enabled:
                    t = datetime.datetime.fromtimestamp(report.FirstSeenTimestampUTC/1e6)
                    keyboard.write(str(report.EPC))
                    keyboard.press_and_release('tab')
                    keyboard.write(t.strftime("%H:%M:%S.%f"))
                    keyboard.press_and_release('enter')
            if self.ignore_until[report.EPC] < report.FirstSeenTimestampUTC:
                report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
                self.ignore_until[report.EPC] = report.FirstSeenTimestampUTC + self.ignore_tag_time*1e6
                if self.keyboard_wedge_enabled:
                    t = datetime.datetime.fromtimestamp(report.FirstSeenTimestampUTC/1e6)
                    keyboard.write(str(report.EPC))
                    keyboard.press_and_release('tab')
                    keyboard.write(t.strftime("%H:%M:%S.%f"))
                    keyboard.press_and_release('enter')

    def synchronise(self):
        return set_time_UTC(self.host, self.username, self.password)

    def get_timestamp(self):
        return get_time_UTC(self.host, self.username, self.password)