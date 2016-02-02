#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil
import operator
from optparse import OptionParser
from datetime import datetime

RUNNING_FILE = "runningrecord.dat"
LINE_FORMAT = "日期:%-12s 时长:%-6d 距离:%-8.2f 配速:%-10s"

def formatdatestr(str):
    return datetime.strftime(datetime.strptime(str,"%Y-%m-%d"),"%Y-%m-%d")

def calcspeed(during,distance):
    dursecond = during*60
    hour = int(dursecond/(distance*60))
    second = int((dursecond/distance)%60)
    return str(hour)+":"+str(second)

def addrun():
    running_day = formatdatestr(input("Running date(yyyy-mm-dd):"))
    running_during = int(input("Running during(minutes):"))
    running_distance = float(input("Runing distance(kilometre):"))
    running_record = running_day+","+str(running_during)+","+str(running_distance)
    running_speed = calcspeed(running_during,running_distance)
    with open(RUNNING_FILE,"a") as f:
        print(running_record,file=f)
    print("Save record success!")
    print("-"*40)
    print(LINE_FORMAT%(running_day,running_during,running_distance,running_speed))

def delrun(options):
    deldate = formatdatestr(options.delrun)
    with open(RUNNING_FILE,"r") as r:
        with open("temp.dat","w") as t:
            for line in r.readlines():
                running_day = line.split(',')[0]
                if running_day!=deldate:
                    t.write(line)
    shutil.move("temp.dat",RUNNING_FILE)
    print("delete success!")

def listrun():
    run_array = []
    with open(RUNNING_FILE) as f:
        for line in f.readlines():
            run_array.append(line.split(','))
    run_array.sort(key=operator.itemgetter(0),reverse=True)

    totalduring = 0
    totaldistance = 0.0
    monthtag = " "

    for run_rec in run_array:
        running_day = run_rec[0]
        running_during = int(run_rec[1])
        running_distance = float(run_rec[2])
        running_speed = calcspeed(running_during,running_distance)

        if monthtag == running_day[0:7]:
            totalduring = totalduring + running_during
            totaldistance = totaldistance + running_distance
        elif monthtag == " ":
            monthtag = running_day[0:7]
            totalduring =  running_during
            totaldistance = running_distance
        else:
            print("   %-12s 总时长:%-5d总距离:%-7.2f  配速:%-10s"%("",totalduring,totaldistance,calcspeed(totalduring,totaldistance)))
            print("-"*55)
            monthtag = running_day[0:7]
            totalduring =  running_during
            totaldistance = running_distance

        print(LINE_FORMAT%(running_day,running_during,running_distance,running_speed))

parser = OptionParser()
parser.add_option("-a","--add",
                  action="store_true",
                  dest="addrun",
                  help="add a running record")

parser.add_option("-d","--delete",
                  action="store",
                  dest="delrun",
                  help="delete a day running record,delete yyyy-mm-dd")

parser.add_option("-l","--list",
                  action="store_true",
                  dest="listrun",
                  help="list runing record")

parser.add_option("-v","--version",
                  action="store_true",
                  dest="version",
                  help="running record version")

(options,args) = parser.parse_args()

if options.addrun:
    addrun()
if options.delrun:
    delrun(options)
if options.listrun:
    listrun()
if options.version:
    print("Version 0.0.1")
