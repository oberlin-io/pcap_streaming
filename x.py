import yaml; import os; import pandas as pd; import numpy as np

class DataSet(object):
    '''
    data from
    > http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/
        > GeneratedLabelledFlows
            > Monday-WorkingHours.pcap_ISCX.csv (all benign traffic)
    '''
    def __init__(self, file):
        '''
        files:
            Monday-WorkingHours.pcap_ISCX.csv
        '''
        with open('conf.yaml', 'r') as f:
            self.conf = yaml.safe_load(f.read())
        p = os.path.join(self.conf['storage_p'], file)
        #'/mnt/c/Users/joberlin/Documents/x/data/Monday-WorkingHours.pcap_ISCX.csv'
        # DtypeWarning: Columns (20) have mixed types. Specify dtype option on import or set low_memory=False.
        self.df = pd.read_csv(p)


    def rename_columns(self):
        names = dict()
        for c in self.df.columns:
            names[c] = c.strip() \
                        .replace(' ', '_') \
                        .replace('/s', '_per_s') \
                        .lower()
        self.df.rename(columns=names, inplace=True)


    def set_timestamps(self):
        self.df.timestamp = pd.to_datetime(self.df.timestamp)

    def get_bytes_per_s(self):
        # get end timestamp
        # assumption: flow_duration is in milliseconds
        select = ['timestamp', 'flow_id', 'flow_duration', 'flow_bytes_per_s',]
        df = self.df[select].copy()

        # Bring in portion from in the morning
        filter = (df.timestamp >= pd.datetime(2017, 3, 7, 9)) & \
            (df.timestamp < pd.datetime(2017, 3, 7, 9, 30))
        df = df[filter]

        df.flow_duration = pd.to_timedelta(df.flow_duration, 'milli')
        df['end_timestamp'] = df.timestamp + df.flow_duration
        df['delta'] = df.end_timestamp - df.timestamp
        df.delta = df.delta.dt.total_seconds() # in sec as float # not * 1e3
        drops = ['flow_bytes_per_s']
        df = df.dropna(subset=drops)

        timestamp_format = '%Y-%m-%d %H:%M:%S'
        freq = '1S'
        # Make new df for timestamp range freq 1 sec
        def x():
            start = df.timestamp.min().strftime(timestamp_format)
            end = df.end_timestamp.max().strftime(timestamp_format)
            range = pd.date_range(start=start, end=end, freq=freq)
            df_ = pd.DataFrame({'flow_bytes': 0}, index=range) # or np.nan
            return df_
        df_ = x()

        # adding byte per sec to flow_bytes_df
        sh = df.shape[0]
        c = 0
        for index, flow in df.iterrows(): # test like df[-4:] or df.sample(n=4)
            try:
                start = flow['timestamp'].strftime(timestamp_format)
                end = flow['end_timestamp'].strftime(timestamp_format)
                range = pd.date_range(start=start, end=end, freq=freq)
                flow_df = pd.DataFrame({'flow_bytes': 0}, index=range)
                if flow_df.shape[0] > 0: # Why would flow_df have no range? Are the start and end stamps same?
                    b = float(flow['flow_bytes_per_s']) * flow['delta']
                    b = b / flow_df.shape[0]
                    flow_df.flow_bytes = b
                    df_.flow_bytes = df_.flow_bytes.add(flow_df.flow_bytes.astype('float'), fill_value=0)
                    print(round(c/sh, 2))
                    c += 1
            except Exception as e:
                x = str(index) + ': ' + str(e) + '\n'
                print(x)
                with open('errors', 'a') as f: f.write(x)

        p = os.path.join(self.conf['storage_p'], 'bytes_timeseries.csv')
        df_.to_csv(p)

        #test
        #df_[df_.flow_bytes>0]



if __name__ == '__main__':
    DS = DataSet('Monday-WorkingHours.pcap_ISCX.csv')
    DS.rename_columns()
    DS.set_timestamps()
    DS.get_bytes_per_s()




'''
ts = x.timestamp.unique()
ts = pd.DataFrame({'timestamp':ts})
delta = ts.timestamp.diff()
# Shift delta up
delta = delta.dropna()
s = pd.Series([np.nan])
delta = delta.append(s, ignore_index=True)
ts['delta'] = delta
'''
