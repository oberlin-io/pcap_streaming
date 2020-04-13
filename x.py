import yaml; import os; import pandas as pd; import numpy as np

class DataSet(object):
    '''
    data from
    > http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/
        > GeneratedLabelledFlows
            > Monday-WorkingHours.pcap_ISCX.csv (all benign traffic)
    '''
    def __init__(self, file):
        with open('conf.yaml', 'r') as f:
            self.conf = yaml.safe_load(f.read())
        p = os.path.join(self.conf['storage_p'], file)
        #'/mnt/c/Users/joberlin/Documents/x/data/Monday-WorkingHours.pcap_ISCX.csv'
        # DtypeWarning: Columns (20) have mixed types. Specify dtype option on import or set low_memory=False.
        self.df = pd.read_csv(p)


    def rename_columns(self):
        names = dict()
        for c in df.columns:
            names[c] = c.strip() \
                        .replace(' ', '_') \
                        .replace('/s', '_per_s') \
                        .lower()
        self.df.rename(columns=names, inplace=True)


    def set_timestamps(self):
        self.df.timestamp = pd.to_datetime(self.df.timestamp)

    def get_megabytes_per(self):
        select = ['timestamp', 'flow_id', 'flow_duration', 'flow_bytes_per_s',]
        # get end timestamp
        # assumption: flow_duration is in milliseconds
        df = df[select]
        df.flow_duration = pd.to_timedelta(df.flow_duration, 'milli')
        df['end_timestamp'] = df.timestamp + df.flow_duration
        df['delta'] = df.end_timestamp - df.timestamp
        df.delta = df.delta.dt.total_seconds() * 1e3
        df.delta = df.delta * .001
        # now the delta is in seconds

        drops = ['flow_bytes_per_s']
        df.dropna(subset=drops, inplace=True)

        df.flow_bytes_per_s.astype('float') * df.delta #here
        # gets total bytes for that flow

        ###
        import numpy as np

        timestamp_format = '%Y-%m-%d %H:%M:%S'
        freq = '1S'

        # Make new df for timestamp range freq 1 sec
        start = df.timestamp.min().strftime(timestamp_format)
        end = df.end_timestamp.max().strftime(timestamp_format)
        range = pd.date_range(start=start, end=end, freq=freq)
        flow_bytes_df = pd.DataFrame({'flow_bytes_per_s': np.nan}, index=range)

        # append by adding byte per sec to flow_bytes_df
        for index, flow in df.iterrows():

            print(timestamp_format)
            start = flow['timestamp'].strftime(timestamp_format)
            end = flow['end_timestamp'].strftime(timestamp_format)
            print(start, end)

            range = pd.date_range(start=start, end=end, freq=freq)
            print(range)
            flow_df = pd.DataFrame(index=range)
            flow_df['flow_bytes_per_s'] = flow['flow_bytes_per_s']
            break #here







ts = x.timestamp.unique()
ts = pd.DataFrame({'timestamp':ts})
delta = ts.timestamp.diff()
# Shift delta up
delta = delta.dropna()
s = pd.Series([np.nan])
delta = delta.append(s, ignore_index=True)
ts['delta'] = delta
