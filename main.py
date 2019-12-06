import multiprocessing
import fire
import os
import time
import datetime
import signal
import sys
import recorder
import json

openChannels = {}

def start():
  with open('config.json') as file:
    config = json.load(file)
    for item in config.get('record'):
      host = item.get('host')
      for channel in item.get('channels'):
        scheduleChannel(host, channel, config)

def scheduleChannel(host, channel, config):
  print("[{}] Starting...".format(channel))
  storagePath = config.get('storagePath')
  quality = config.get('quality')
  retryInterval = config.get('retryInterval')
  videoFormat = config.get('videoFormat')
  x = multiprocessing.Process(target=startChannel, args=(host, channel, storagePath, quality, retryInterval, videoFormat))
  x.start()

def startChannel(host, channel, storagePath="storage", quality="720p,480p", retryInterval=60, videoFormat="mp4"):
  openChannels[channel] = recorder.Recorder(host, channel, storagePath, quality, retryInterval, videoFormat)
  openChannels[channel].start()

def signal_handler(sig, frame):
  print('Killing all recorders gracefully...')
  for k in openChannels.keys():
    openChannels[k].stop()
  time.sleep(5)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
  fire.Fire()