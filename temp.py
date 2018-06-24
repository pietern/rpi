#!/usr/bin/env python3

import argparse
import statistics
from statsd import StatsClient
from time import time, sleep


def load_temp():
  with open('/sys/class/thermal/thermal_zone0/temp') as f:
    return float(f.read()) / 1000.0


# Average a large number of samples to get a more accurate measurement
def sample_temp(average=10, delay=1.0):
    tick = time() + delay
    while True:
        temps = []
        while len(temps) < average:
            temps.append(load_temp())
            sleep(tick - time())
            tick = tick + delay
        yield statistics.mean(temps)


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

statsd = StatsClient()
for temp in sample_temp():
    statsd.gauge('pi.temp', temp)
    if args.verbose:
        print(temp)
