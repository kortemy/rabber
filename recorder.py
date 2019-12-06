import datetime
import time
import subprocess
import threading

class Recorder:
  
  def __init__(self, host, channel, storagePath, quality, retryInterval, videoFormat):
    self.host = host
    self.channel = channel
    self.storagePath = storagePath
    self.quality = quality
    self.retryInterval = retryInterval
    self.videoFormat = videoFormat

  def start(self):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    tmpl = 'streamlink {host}/{channel} \"{quality}\" --quiet -o {storage}/{channel}_{timestamp}.{format}'
    cmd = tmpl.format(host=self.host, channel=self.channel, quality=self.quality, storage=self.storagePath, timestamp=timestamp, format=self.videoFormat)
    self.running = True
    self.proc = subprocess.Popen(cmd, shell=True)
    self.proc.wait()
    if self.running:
      time.sleep(self.retryInterval)
      self.start()

  def stop(self):
    self.running = False
    self.proc.terminate()
    self.proc.wait()