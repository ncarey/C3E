import csv
from optparse import OptionParser
import subprocess
import os
import sys
import time
from datetime import datetime
from datetime import timedelta


#script that generates histograms for each client for:
#   hour of day of request
#   duration between requests

#zero_micro = timedelta(0,0,0)
#ten_micro = timedelta(0,0,10)
#hundred_micro = timedelta(0,0,100)
#thousand_micro = timedelta(0,0,1000)
#tenthou_micro = timedelta(0,0,10000)
#hundredthou_micro = timedelta(0,0,100000)
#second = timedelta(0,1,0)
#five_sec = timedelta(0,5,0)
#ten_sec = timedelta(0,10,0)
#thirty_sec = timedelta(0,30,0)
#minute = timedelta(0,0,0,0,1)
#two_min = timedelta(0,0,0,0,2)
#five_min = timedelta(0,0,0,0,5)
#ten_min = timedelta(0,0,0,0,10)
#thirty_min = timedelta(0,0,0,0,30)
#hour = timedelta(0,0,0,0,0,1)
#three_hour = timedelta(0,0,0,0,0,3)
#six_hour = timedelta(0,0,0,0,0,6)
#twelve_hour = timedelta(0,0,0,0,0,12)
#day = timedelta(1)
#two_day = timedelta(2)
#week = timedelta(7)
#month = timedelta(30)

#hist_dict[x] = [0:prev_req_time, 1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:20, 22:21, 23:22, 24:23, 25:0u, 26:10u, 27:100u, 28:1000u, 29:10000u, 30:100000u, 31:1s, 32:5s, 33:10s, 34:30s, 35:1m, 36:2m, 37:5m, 38:10m, 39:30m, 40:1h, 41:3h, 42:6h, 43:12h, 44:1d, 45:2d, 46:7d, 47:30d, 48:>30d]


time_deltas = [timedelta(0,0,0), timedelta(0,0,10), timedelta(0,0,100), timedelta(0,0,1000), timedelta(0,0,10000), timedelta(0,0,100000), timedelta(0,1,0), timedelta(0,5,0), timedelta(0,10,0), timedelta(0,30,0), timedelta(0,0,0,0,1), timedelta(0,0,0,0,2), timedelta(0,0,0,0,5), timedelta(0,0,0,0,10), timedelta(0,0,0,0,30), timedelta(0,0,0,0,0,1), timedelta(0,0,0,0,0,3), timedelta(0,0,0,0,0,6), timedelta(0,0,0,0,0,12), timedelta(1), timedelta(2), timedelta(7), timedelta(30)]

def hist_dict_pretty(hist_dict):
  for src_ip in hist_dict:
    print "IP Addr: {0}".format(src_ip)
    print "  Hour of Requests Histogram: "
    for i in range(0,24):
      print "    {0}-{1} : {2}".format(i, i+1, hist_dict[src_ip][i+1])
    print "  Inter-request duration Histogram: "
    print "    x <= {0} : {1}".format(time_deltas[0], hist_dict[src_ip][25])
    for i in range(1, len(time_deltas) - 1):
      print "    {0} < x <= {1} : {2}".format(time_deltas[i], time_deltas[i+1], hist_dict[src_ip][i+25])
    print "    {0} < x : {1}".format(time_deltas[len(time_deltas) - 1], hist_dict[src_ip][len(time_deltas) + 25])

def hist_dict_ugly(hist_dict):
  for src_ip in hist_dict:
    ret = ""
    ret += "{0},".format(src_ip)
    ret += "{0},".format(hist_dict[src_ip][0])
    for i in range(0,24):
      ret += "{0},".format(hist_dict[src_ip][i+1])
    ret += "{0},".format(hist_dict[src_ip][25])
    for i in range(1, len(time_deltas) - 1):
      ret += "{0},".format(hist_dict[src_ip][i+25])
    ret += "{0}".format(hist_dict[src_ip][len(time_deltas) + 25])
    print ret

def update_hist_dict(hist_dict, src_ip, dt):

  if src_ip not in hist_dict:
    hist_dict[src_ip] = [dt,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    hour = dt.hour
    hist_dict[src_ip][hour+1] += 1

  else:

    hour = dt.hour
    hist_dict[src_ip][hour+1] += 1

    prev_dt = hist_dict[src_ip][0]
    dif = dt - prev_dt  

    for i in range(0,len(time_deltas) + 1):
      if i == len(time_deltas):
        hist_dict[src_ip][i + 25] += 1
        break
      if dif <= time_deltas[i]:
        hist_dict[src_ip][i + 25] += 1
        break
    
    hist_dict[src_ip][0] = dt    


def parse_dns(dns_path_list):
 
  hist_dict = {}

  total_count = 0;
  for dns_path in dns_path_list:
    with open(dns_path, 'rb') as dns_file:
      
      line = dns_file.readline()
      while line != '': #total_count < 20: #line != '':
        if line.startswith("2013"):
          
          split_line = line.split(',')    
	  date_time = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S.%f")
          src_ip = split_line[1]
          dest_ip = split_line[2]
          size = split_line[3]
          proto = split_line[4]
          q_r = split_line[5]
 
          #only care about queries right now, not responses so much
          if q_r == "q":
            update_hist_dict(hist_dict, src_ip, date_time)
            total_count += 1


        line = dns_file.readline()

  hist_dict_ugly(hist_dict)
  print "Total DNS requests : {0}".format(total_count)
  print "Total unique IP addr : {0}".format(len(hist_dict))

def filter_dns(dns_path_list):

  dns_servers = {}
  for dns_path in dns_path_list:
    with open(dns_path, 'rb') as dns_file:
      line = dns_file.readline()

      while line != '':
        if line.startswith("2013"):
          split_line = line.split(',')
          dest_ip = split_line[2]
          src_ip = split_line[1]
          q_r = split_line[5]
     
          if q_r == "r":
            dns_servers[src_ip] = 1
          if q_r == "q":
            dns_servers[dest_ip] = 1
        line = dns_file.readline() 
            
    print "Done populating DNS server list, starting filter"
    with open(dns_path, 'rb') as dns_file:
      with open(dns_path + ".filtered", 'w') as dns_file_filtered:
        line = dns_file.readline()
        while line != '':
          if line.startswith("2013"):
            split_line = line.split(',')
            src_ip = split_line[1]
            q_r = split_line[5]
            if q_r == "q" and src_ip not in dns_servers:
              dns_file_filtered.write(line)
          line = dns_file.readline()




def combine_hist(log_fn_list, agg_hist, to_print):

  tot_req = 0
  tot_ip = 0

  for log_fn in log_fn_list:
    with open(log_fn, 'rb') as log:
      line = log.readline()
      while line != '':
        if line.startswith("Total DNS"):
          to_add = line.split(' : ')[1]
          tot_req += int(to_add)
        elif line.startswith("Total unique"):
          to_add = line.split(' : ')[1]
          tot_ip += int(to_add)

        else:
          hist_list = line.split(',')
          src_ip = hist_list[0]

          if src_ip not in agg_hist:
            agg_hist[src_ip] = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
 
          #TODO account for prev_datetime
          for i in range(2,len(hist_list)):
            agg_hist[src_ip][i-1] += int(hist_list[i])

        line = log.readline()

  if to_print != 0:
    #hist_dict_ugly(agg_hist)
    print "Total DNS requests : {0}".format(tot_req)
    print "Total unique IP Addr : {0}".format(tot_ip)

def print_summary(agg_hist):
  avg_entry = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for src_ip in agg_hist:
    for i in range(1, len(agg_hist[src_ip])):
      avg_entry[i] += agg_hist[src_ip][i]
  for i in range(1, len(avg_entry)):
    avg_entry[i] = float(float(avg_entry[i]) / float(len(agg_hist)))

  tmp_hist = {"Average Client" : avg_entry}
  hist_dict_pretty(tmp_hist)
  hist_dict_ugly(tmp_hist)

if __name__=='__main__':

  usage = "Usage: "
  parser = OptionParser(usage=usage)


  parser.add_option("-f", "--filter", type="int", dest="filt", 
                    default="0", 
                    help="Specify 0 or 1 for filter mode", metavar="#FILT") 

  parser.add_option("-x", "--diagnostic", type="int", dest="diag", 
                    default="0", 
                    help="Specify 0 or 1 for diagnostic mode", metavar="#DIAG") 
  parser.add_option("-s", "--summary", type="int", dest="summary", 
                    default="0", 
                    help="Specify 0 or 1 for summary statistics mode", metavar="#SUMMARY") 

  parser.add_option("-l", "--hist", type="string", dest="hist_log_path", 
                    default="/damsl/projects/C3E_Challenge/histograms/march_02-06.hist", 
                    help="Specify comma-separated paths to DNS logs to examine", metavar="#DNSPATH") 
  parser.add_option("-d", "--dns", type="string", dest="dns_path", 
                    default="/damsl/projects/C3E_Challenge/data/ftp.lanl.gov/public/pflarr/fixed.2013-02-01.txt", 
                    help="Specify comma-separated paths to DNS logs to examine", metavar="#DNSPATH") 


  (options, args) = parser.parse_args()
  if options.diag == 1:
    for i in time_deltas:
      print i
  
  elif options.filt == 1:
    dns_paths = options.dns_path
    dns_path_list = dns_paths.split(",")

    filter_dns(dns_path_list)  

  elif options.summary == 1:
    hist_paths = options.hist_log_path.split(',')
    agg_hist = {}
    combine_hist(hist_paths, agg_hist, 0)
    print_summary(agg_hist)
  else:
    dns_paths = options.dns_path
    dns_path_list = dns_paths.split(",")
  
    parse_dns(dns_path_list)



