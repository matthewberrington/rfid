class Speedway:
	def __init__(self, host, username, password):
		self.hex_encoding = True
		self.reader = None
		self.ignore_tag = 20
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

	def configure(config_dict):
	    config = llrp.LLRPReaderConfig(self.config_dict)
	    self.reader = llrp.LLRPReaderClient('speedwayr-12-36-0f', config=config)
	    reader.add_tag_report_callback(cb)

	def cb (reader, tag_reports):
	    for tag_report in tag_reports:
	        report = TagReportData(config_dict, tag_report)
	        if not report.EPC in ignore_until.keys():
	            report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
	            ignore_until[report.EPC] = report.FirstSeenTimestampUTC + ignore_tag_time*1e6
	        if ignore_until[report.EPC] < report.FirstSeenTimestampUTC:
	            report.export_to_csv(r'C:\Users\pfber\Downloads\tmp.csv')
	            ignore_until[report.EPC] = report.FirstSeenTimestampUTC + ignore_tag_time*1e6