#!/usr/bin/python
import time
import csv
import re
import locations
from locations import parser
import clearances
from clearances import clearance as clear
from sys import argv

#  clearance,description,title,reqid,loclink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
logFile = 'logfile'
csvFile = 'csvWork.csv'
outFile = 'csvFinal.csv'
clearance = ""
doneThis = {}

LOG = open(logFile, 'w')

# Open CSV output stream
output = open(outFile, 'wb')
wr = csv.writer(output, quoting=csv.QUOTE_ALL)

csv.register_dialect(
  'mydialect',
  delimiter=',',
  quotechar='"',
  doublequote=True,
  skipinitialspace=True,
  lineterminator='\r\n',
  quoting=csv.QUOTE_MINIMAL)


wr.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'company_google', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords'])


with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    title  = row[1]
    desc   = row[0]
    req    = row[8]
    travel = row[7]
    loc    = row[5]
    loc    = re.sub("<.+>(.+)<.+>",r'\1',loc)
    title  = re.sub("<.+>(.+)<.+>",r'\1',title)
    appUrl = row[4]
    cl_1   = row[2]
    cl_2   = row[3]
    job_c  = row[6]

    if re.match('location', loc):
      LOG.write("Skipping header field")
    elif len(desc) == 0:
      LOG.write("This one has an empty desc.")
    elif doneThis.has_key(req):
      LOG.write("Already done this crap...")
    else:
      doneThis[req] = "TRUE"
      # This is the final fix for REQ
      req=re.sub(".+ID=(\d+)\&.+",r'\1',req)
      clearance = clear.clear(cl_2)
      clearance_2 = clear.clear(cl_1)
      if re.match("^$|None", clearance):
          clearance = clear.clear(cl_1)
      loc,lat,lon = parser.loc(loc,"leidos")
      if not re.match("None|^$", clearance):
        wr.writerow([title, appUrl, desc, loc, 'Leidos', 'Leidos Description', 'https://leidos.com', 'leidos_logo', 'leidos_facebook', 'leidos_twitter', 'leidos_linkedin', 'leidos_google', req, 'deployment', travel, lat, lon, 'Leidos Benefits', job_c, clearance, 'keywords'])

