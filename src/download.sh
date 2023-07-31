#!/bin/env bash

TIMES=( "0000" "0030" "0100" "0130" "0200" "0230" "0300" "0330" "0400" "0430" "0500" "0530" "0600" "0630" "0700" "0730" "0800" "0830" "0900" "0930" "1000" "1030" "1100" "1130" "1200" "1230" "1300" "1330" "1400" "1430" "1500" "1530" "1600" "1630" "1700" "1730" "1800" "1830" "1900" "1930" "2000" "2030" "2100" "2130" "2200" "2230" "2300" "2330" )

while read stream; do
  rm ./tmp/*.mp3
  DATE_PREFIX=$(date -u -d "yesterday" '+%b-%d-%Y')
  URL_PREFIX="https://archive.liveatc.net/$stream-$DATE_PREFIX"
  for TIME_KEY in "${!TIMES[@]}"; do
    TIME="${TIMES[$TIME_KEY]}"
    URL="$URL_PREFIX-${TIME}Z.mp3"
    echo "$URL"
    wget -O "./tmp/$(printf %02d $TIME_KEY).mp3" "$URL"
  done
done <../streams.txt
