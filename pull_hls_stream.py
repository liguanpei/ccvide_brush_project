#/usr/bin/env python
#-*- coding: utf-8 -*-

##############################
#  Author: liguanpei
#  Email:  ligp@bokecc.com
#  Date:   2018-01-13 14:40:00
#  Func:   拉展视互动hls流
##############################

import os
import sys
import urllib
import commands

def check_ffmpeg_install():
    s = commands.getoutput("ffmpeg")
    if "not found" in s:
        return False
    else:
        return True
        

def detect_ts_audio(dest_url):
    detect_cmd = "ffmpeg -i %s" % dest_url
    detect_result = commands.getoutput(detect_cmd)
    print detect_result
    if "0 channels" in detect_result or " Hz" not in detect_result:
        return False
    else:
        return True
    

def pull_hls_stream_to_mp4(dest_url, output_file):
    cmd = "ffmpeg -i %s -bsf:a aac_adtstoasc -c copy %s" % (dest_url, output_file)
    pull_result = commands.getoutput(cmd)

    if "Not Found" in pull_result:
        return False
    
    return True


def save_ts_to_file(dest_url, dest_ts_filename, ts_content, output_file, output_dir):
    m3u8_file_name = output_file[0: output_file.rfind(".")+1] + "m3u8"

    first = True
    fd = open(m3u8_file_name, "w")
    for i in ts_content:
        if ".ts" in i:
            if first:
                fd.write(output_dir + dest_ts_filename + "\n") 
                first = False
            else: 
                fd.write(dest_url[0: dest_url.rfind("/")+1] + i) 
        else:
            fd.write(i)
    fd.close()
        

def repull_hls_stream(dest_ts_filename, output_file, output_dir):
    m3u8_file_name = output_file[0: output_file.rfind(".")+1] + "m3u8"
    cmd = "ffmpeg -i %s -c:a aac  -bsf:a aac_adtstoasc -strict -2 -y %s" % (m3u8_file_name, output_file) 
    ffmpeg_res = commands.getoutput(cmd)
    os.remove(output_dir + dest_ts_filename)
    os.remove(m3u8_file_name)
    print ffmpeg_res 


def add_audio_in_ts_file(dest_url, first_ts_url, dest_ts_filename, ts_content, output_file, output_dir):
    try:
        cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i %s -shortest -c:v copy -c:a aac -strict -2 -y %s" % (first_ts_url, output_dir + dest_ts_filename)
    
        ffmpeg_res = commands.getoutput(cmd)
        print ffmpeg_res
        save_ts_to_file(dest_url, dest_ts_filename, ts_content, output_file, output_dir)
        repull_hls_stream(dest_ts_filename, output_file, output_dir)
    except Exception, e:
        print str(e)

        
def handle_hls_stream_audio(dest_url, output_file, output_dir):
    try:
        request = urllib.urlopen(dest_url)
        ts_content = request.readlines()
        if ts_content:
            ts_list = [i for i in ts_content if ".ts" in i]
            if ts_list:
                dest_ts_filename = ts_list[0]
                dest_ts_filename = dest_ts_filename.replace("\n", "")
                if "http" not in dest_ts_filename:
                    first_ts_url = dest_url[0: dest_url.rfind("/")+1] + dest_ts_filename
                    first_ts_url = first_ts_url.replace("\n", "")
                    print 'first_ts_url = ' + first_ts_url
                    add_audio_in_ts_file(dest_url, first_ts_url, dest_ts_filename, ts_content, output_file, output_dir)
                    
    except Exception, e:
        print str(e)


def main(dest_url, output_file):
    has_audio = detect_ts_audio(dest_url)
    print 'has_auido = ' + str(has_audio)
    output_dir = output_file[0: output_file.rfind("/")+1]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 
    if has_audio:
        pull_hls_stream_to_mp4(dest_url, output_file)
    else:
        handle_hls_stream_audio(dest_url, output_file, output_dir)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print 'Usage: python pull_stream.py url output_file_name'
        print 'Example: python pull_stream.py "http://zhanshi.com/dest.m3u8" "output.mp4"'
        exit(0)

    is_ffmpeg_install = check_ffmpeg_install()
    if not is_ffmpeg_install:
        print 'Please install ffmpeg first!'
        exit(0) 
   
    main(sys.argv[1], sys.argv[2])
