#!/usr/bin/python
import time
import csv
import re
import companyinfo
from companyinfo import infofiller
import locations
from locations import parser
import clearances
from clearances import clearance as clear
from sys import argv
import datetime
#  clearance,description,title,reqid,loclink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
logFile = 'logfile'
csvFile = 'csvWork.csv'
outFile = 'csvFinal.csv'
clearance = ""
doneThis = {}

LOG = open(logFile, 'w')

# Open CSV output stream
logDate= datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
companyName = 'Leidos'
output = open('/home/jbaker/Desktop/'+companyName+'_'+logDate+'_'+outFile, 'wb')
output2 = open('/home/jbaker/Desktop/'+companyName+'_2_'+logDate+'_'+outFile, 'wb')
wr = csv.writer(output, quoting=csv.QUOTE_ALL)
wr2 = csv.writer(output2, quoting=csv.QUOTE_ALL)

csv.register_dialect(
  'mydialect',
  delimiter=',',
  quotechar='"',
  doublequote=True,
  skipinitialspace=True,
  lineterminator='\r\n',
  quoting=csv.QUOTE_MINIMAL)


wr.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords'])

wr2.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords'])

infoComp,infoDesc,infoSite,infoLogo,infoFace,infoTwit,infoLinked,infoBeni=companyinfo.infofiller(companyName)

with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    keyw   = ''
    keywordsLoc = ''
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
    title = re.sub('^\s+|\s+$', '',title)
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
      clearance,keywords = clear.clear(cl_2)
      clearance_2,keywords_2 = clear.clear(cl_1)
      if re.match("^$|None", clearance):
          clearance = clearance_2
          keywords = keywords_2
      for i in keywords:
        keyw=keyw+' '+i
      keyw=re.sub('^ ','',keyw)
      loc,lat,lon,keywordsLoc = parser.loc(loc,"leidos")
      keyw = keyw + ' ' + keywordsLoc
      #print loc + ' ||||||||||||| THIS IS FUCKED UP ||||||||||||| ' + keywordsLoc
      if not re.match("None|^$", clearance):
        wr.writerow([title, appUrl, desc, loc, infoComp, infoDesc, infoSite, infoLogo, infoFace, infoTwit, infoLinked, req, 'UNKNOWN', travel, lat, lon, infoBeni, job_c, clearance, keyw])

