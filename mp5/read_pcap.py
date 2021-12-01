from scapy.all import *
import os
import numpy as np
import argparse
import pandas as pd

def read_pcap_file(filename):
    filepath = os.path.join("pcap_files", filename)
    file = rdpcap(filepath)
    print(file)
    return file


def calculate_totals(packet_list):
    num_out = 0
    num_in = 0
    bytes_out = 0
    bytes_in = 0
    times_out = []
    times_in = []
    for packet in packet_list:
        if IP in packet:
            if packet[IP].src.startswith('192.168'):
                num_out += 1
                bytes_out += packet.len
                times_out.append(packet.time)
            else:
                num_in += 1
                bytes_in += packet.len
                times_in.append(packet.time)
    return dict(num_in=num_in, num_out=num_out, bytes_in=bytes_in, bytes_out=bytes_out,
                times_in=np.array(times_in), times_out=np.array(times_out))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', dest='filename', help='pcap file to read')
    args = parser.parse_args()

    if args.filename is None:
        file_list = os.listdir('pcap_files')
        for file in file_list:
            packet_list = read_pcap_file(file)
            stats = calculate_totals(packet_list)
            tdiff_in = np.diff(stats['times_in'])
            tdiff_out = np.diff(stats['times_out'])
            in_mean = np.mean(tdiff_in)
            in_median = np.median(tdiff_in)
            in_std = np.std(tdiff_in)
            out_mean = np.mean(tdiff_out)
            out_median = np.median(tdiff_out)
            out_std = np.std(tdiff_out)

            # write to dataframe
            df = pd.DataFrame()
            row = {'packets_in': stats['num_in'], 'packets_out': stats['num_out'],
                'bytes_in': stats['bytes_in'], 'bytes_out': stats['bytes_out'],
                'tdiff_in': tdiff_in, 'tdiff_out': tdiff_out, 'in_mean': in_mean,
                'in_median': in_median, 'in_std': in_std, 'out_mean': out_mean,
                'out_median': out_median, 'out_std': out_std}
            df = df.append(row, ignore_index=True)
        df.to_csv('out.csv', index=False)
    else:
        packet_list = read_pcap_file(args.filename)
        stats = calculate_totals(packet_list)
        tdiff_in = np.diff(stats['times_in'])
        tdiff_out = np.diff(stats['times_out'])
        in_mean = np.mean(tdiff_in)
        in_median = np.median(tdiff_in)
        in_std = np.std(tdiff_in)
        out_mean = np.mean(tdiff_out)
        out_median = np.median(tdiff_out)
        out_std = np.std(tdiff_out)

    # write the data to a table

    """   
    total_packets = len(packet_list)
    sources = []
    dests = []
    packet_sizes = []
    packet_times = []
    sources.append(packet[IP].src)
    dests.append(packet[IP].dst)
    packet_sizes.append(len(packet))
    packet_times.append(packet.time)
    """