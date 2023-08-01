from pathlib import Path
import subprocess

from pydub import AudioSegment
from pydub.silence import split_on_silence

import requests

TIME_GAP = 4000
KEEP_SILENCE = 800
SILENCE_THRESHOLD = -44 # higher is quieter
SEEK_STEP = 5 # Lower is more precise

TIMES = [
  "0000",
  "0030",
  "0100",
  "0130",
  "0200",
  "0230",
  "0300",
  "0330",
  "0400",
  "0430",
  "0500",
  "0530",
  "0600",
  "0630",
  "0700",
  "0730",
  "0800",
  "0830",
  "0900",
  "0930",
  "1000",
  "1030",
  "1100",
  "1130",
  "1200",
  "1230",
  "1300",
  "1330",
  "1400",
  "1430",
  "1500",
  "1530",
  "1600",
  "1630",
  "1700",
  "1730",
  "1800",
  "1830",
  "1900",
  "1930",
  "2000",
  "2030",
  "2100",
  "2130",
  "2200",
  "2230",
  "2300",
  "2330",
]

subprocess.Popen(['mkdir', '-p', './recordings'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait()

streams = []
with open('./streams.txt', 'r') as f:
  streams = [line.strip() for line in f]

p = subprocess.Popen(['date', '-u', '-d', 'yesterday', "+%b-%d-%Y"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
formatted_date = p.stdout.read().decode('ascii').strip()
p.wait()

for stream in streams:

  URL_PREFIX = "https://archive.liveatc.net/{}-{}".format(stream, formatted_date)

  subprocess.Popen(['rm', '-r', './tmp'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait()
  subprocess.Popen(['mkdir', '-p', './tmp'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait()
  time_index = 0
  for TIME in TIMES:
    url = "{}-{}Z.mp3".format(URL_PREFIX, TIME)
    print(url)
    r = requests.get(url, stream=True)
    if r.ok:
      filename = './tmp/{}.mp3'.format(TIME)
      with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 16*1024):
          f.write(chunk)
    time_index += 1

  files = sorted(Path('./tmp').glob('*.mp3'))

  total = AudioSegment.empty()

  file_index = 0
  for file in files:
    print("Chunking {}/{}".format(file_index, len(files)))
    for chunk in split_on_silence(AudioSegment.from_file("./{}".format(file), format="mp3"), min_silence_len=TIME_GAP, keep_silence=KEEP_SILENCE, silence_thresh=SILENCE_THRESHOLD, seek_step=SEEK_STEP):
      total += chunk
    file_index += 1
    
  print("Exporting..")
  filename = "./recordings/{}-{}.mp3".format(stream.replace('/', '-'), formatted_date)
  total.export(filename, format="mp3")
  print("Done.")

  with open("index.html", "a") as f:
    html = "<h4><a href='{}'>{} - {}</h4>\n".format(filename, stream, formatted_date)
    f.write(html)
