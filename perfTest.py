#!/usr/bin/python


import logging

from pprint import pprint
import requests, json, urllib2
import time, datetime
import gzip, sys, os, getopt
import random

########## Input params
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'c:l:v:d:t:r:m:f:i:o:h:x:s:y:z:a:', \
  [   'connectTo=',
      'loopsToRun=',
      'csvLead=',
      'debugLevel=',
      'testFileToRun=',
      'runTillSomethingFound=',
      'runTillSomethingFoundMaxLoops=',
      'idFile=',
      'id=',
      'printRestAnswer=',
      'printHeader=',
      'outFile=',
      'printShortRestAnswer=',
      'truncateOutFile=',
      'flushSpoolEvery=',
      'exitIfException=',
  ])
# ARGS Default values
parConnectTo = parRunTillSomethingFound = -1
parRunTillSomethingFoundMaxLoops = 10
parLoopsToRun =  1
parIdFile = parCsvLead = ''
parId = 'X'
parDebugLevel = 0
parTestFileToRun = '___ALL___'
parRunTillSomethingFound = parPrintShortRestAnswer = parExitIfException = 'N'
parPrintRestAnswer = parPrintShoreRestAnswer = parPrintHeader = parTruncateOutFile = 'N'
parOutFile = ''
parFlushSpoolEvery = 30

locExceptionFound=False
parRunTillSomethingFoundMaxLoopsSpecified=False
parRunTillSomethingFoundSpecified=False
parIdSpecified=False
parIdFileSpecified=False
flgUseIndividualIdFile=False
parTruncateOutFileSpecified=False


for opt, arg in options:
    if opt in ('-c', '--connectTo'):
      # Where to go
      parConnectTo = arg

    elif opt in ('-l', '--loopsToRun'):
      # How many times run the same query
      parLoopsToRun = int(arg)

    elif opt in ('-v', '--csvLead'):

      # a CSV of your convenience you want to print it out in results
      parCsvLead = arg

    elif opt in ('-d', '--debugLevel'):
      # 1: you want debug infos in console, 0 you don't want it
      parDebugLevel = int(arg)

    elif opt in ('-t', '--testFileToRun'):
      # json file containing call to run; do not pass it to run all tests
      parTestFileToRun = arg

    elif opt in ('-r', '--runTillSomethingFound'):
      # IDs are choosen randomly between a file; passing Y means
      #  "Run the same query, over and over again till you find something
      parRunTillSomethingFound = arg
      parRunTillSomethingFoundSpecified=True

    elif opt in ('-m', '--runTillSomethingFoundMaxLoops'):
      parRunTillSomethingFoundMaxLoops = int(arg)
      parRunTillSomethingFoundMaxLoopsSpecified = True

    elif opt in ('-f', '--idFile'):
      # File with valid IDs
      parIdFile = arg
      parIdFileSpecified=True

    elif opt in ('-i', '--id'):
      # Or, ID to pass to rest call
      parId = arg
      parIdSpecified=True

    elif opt in ('-o', '--printRestAnswer'):
      # Do you want me to spool restOutput in CSV file? Y/N
      parPrintRestAnswer = arg

    elif opt in ('-h', '--printHeader'):
      # Should i print header? Y/N
      parPrintHeader = arg

    elif opt in ('-x', '--outFile'):
      # File name i should spool (default=stdOut)
      parOutFile = arg

    elif opt in ('-o', '--printShortRestAnswer'):
      # Do you want me to spool first 50 characters of rest answer in CSV file? Y/N
      parPrintShortRestAnswer = arg

    elif opt in ('-y', '--truncateOutFile'):
      # Should i trincate output file? Y/N
      parTruncateOutFile = arg
      parTruncateOutFileSpecified=True

    elif opt in ('-z', '--flushSpoolEvery'):
      # How often to flush spool
      parFlushSpoolEvery = int(arg)

    elif opt in ('-a', '--exitIfException'):
      parExitIfException = arg


if parConnectTo == -1:
  print 'Parameter error:'
  print '--connectTo is mandatory'
  sys.exit(1)

if parIdFileSpecified==False and parIdSpecified==False:
  #print 'Parameter error:'
  #print 'Please specify at least one option between --id and --idFile'
  #sys.exit(2)
  flgUseIndividualIdFile = True

if parIdFileSpecified==True and parIdSpecified==True:
  print 'Parameter error:'
  print 'Please specify just one option between --id and --idFile'
  sys.exit(3)

if parRunTillSomethingFoundSpecified == False and parRunTillSomethingFoundMaxLoopsSpecified == True:
  print 'Parameter error:'
  print 'You cannot specify --runTillSomethingFoundMaxLoop if dont set --runTillSomethingFound to Y '
  sys.exit(4)

if parRunTillSomethingFoundSpecified == True and parRunTillSomethingFoundMaxLoops < 1:
  print 'Parameter error:'
  print 'Please check --runTillSomethingFoundMaxLoop (maybe you set 0 or negative value?)'
  sys.exit(5)

if parRunTillSomethingFoundSpecified == True and parIdSpecified==True:
  print 'Parameter error:'
  print 'Are you sure on what you are doing? You specified --runTillSomethingFound with --id! Maybe you have not clear what those mean.'
  sys.exit(6)

if parTruncateOutFileSpecified==True and parOutFile == '':
  print 'Parameter error:'
  print 'Are you sure on what you are doing? You specified --truncateOutFile with specifying the outFile! Maybe you have not clear what those mean.'
  sys.exit(7)

########## Input params end here



# outFile handling
if parOutFile:
  fileMode = 'a'
  if parTruncateOutFile <> 'N': fileMode = 'w'
  spoolFile = open(parOutFile,fileMode)
  sys.stdout = spoolFile


# Debugging
if parDebugLevel <> 0:
  logging.basicConfig(level=logging.DEBUG)
  handler=urllib2.HTTPHandler(debuglevel=1)
else:
  logging.basicConfig(level=logging.CRITICAL)
  handler=urllib2.HTTPHandler(debuglevel=0)

opener = urllib2.build_opener(handler)
logger = logging.getLogger(__name__)
urllib2.install_opener(opener)


# Murphy's law of output:
#  "The value of a program is inversely proportional to the weight of its output."
logger = logging.getLogger('Input Params')
logger.debug('parConnectTo: %s', parConnectTo)
logger.debug('parLoopsToRun: %s', parLoopsToRun)
logger.debug('parCsvLead: %s', parCsvLead)
logger.debug('parDebugLevel: %s', parDebugLevel)
logger.debug('parTestFileToRun: %s', parTestFileToRun)
logger.debug('parRunTillSomethingFound: %s', parRunTillSomethingFound)
logger.debug('parRunTillSomethingFoundMaxLoops: %s', parRunTillSomethingFoundMaxLoops)
logger.debug('parIdFile: %s', parIdFile)
logger.debug('parId: %s', parId)
logger.debug('parPrintRestAnswer: %s', parPrintRestAnswer)
logger.debug('parPrintHeader: %s', parPrintHeader)
logger.debug('parOutFile: %s', parOutFile)
logger.debug('parPrintShortRestAnswer: %s', parPrintShortRestAnswer)
logger.debug('parTruncateOutFile: %s', parTruncateOutFile)
logger.debug('parFlushSpoolEvery: %s', parFlushSpoolEvery)
logger.debug('parExitIfException: %s', parExitIfException)


logger = logging.getLogger(__name__)

# Get all valid Target IDs
logger.debug('Getting valid IDs from file')
validTargetIds = []
# If i passed a ID File
if parIdFileSpecified==True:
  logger.debug('Using '+ str(parIdFile)+ ' for IDs')
  validTargetIdsFile  = open(parIdFile, 'r')
  for currValidTargetId in validTargetIdsFile:
    validTargetIds.append(int(currValidTargetId))
  validTargetIdsFile.close()

  logger.debug('len(validTargetIds): %i', len(validTargetIds))
  logger.debug('validTargetIds[0]: %i', validTargetIds[0])


# If i passed a specific ID
elif parIdSpecified == True:
  logger.debug('Specified ID:'+ parId)
  validTargetIds.append(parId)

  logger.debug('len(validTargetIds): %i', len(validTargetIds))
  logger.debug('validTargetIds[0]: %i', validTargetIds[0])


# ELSE No ID specified
# later on, will try to open .idList file for each operation.
# Catch you later





# What should i test?
if parTestFileToRun == "___ALL___":
  jsonFilesArray = ['queries/'+f for f in os.listdir('queries') if f.endswith('.json')]
else:
  jsonFilesArray = parTestFileToRun.split(',')
logger.debug('jsonFilesArray='+' | '.join(jsonFilesArray))



# Should I print the header?
if parPrintHeader <> 'N':
  print "%s,,%s,%s,%s,,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"   % \
        ('CustomCsv','DataTimeString','DataTimeStringUTC','DataTimeEpoch', 'QueryExecuted', 'ID(s)', 'LoopNumber', 'TentativeNumber', 'RequestStatusCode', 'Time(seconds)', 'QuerySize(Bytes)', 'QuerySize(Chars)', 'AnswerSize(Bytes)', 'AnswerSize(Chars)','AnswerFromService')


writesNum=0


# Rock 'n' Roll!
for jsonFile in jsonFilesArray:
  logger = logging.getLogger('--- jsonFilesArray LOOP ---')

  # REST call file
  fileIn  = open(jsonFile, 'r')
  queryFromFile = fileIn.read()
  fileIn.close()

  # REST call entry point
  fileEndPoint  = open(jsonFile+'.entryPoint', 'r')
  urlEndPoint   = fileEndPoint.read()
  fileEndPoint.close()

  if flgUseIndividualIdFile == True:
    logger.debug('Using '+ jsonFile+'.idList'+ ' for IDs')
    validTargetIdsFile  = open(jsonFile+'.idList', 'r')
    for currValidTargetId in validTargetIdsFile:
      validTargetIds.append(int(currValidTargetId))
    validTargetIdsFile.close()


  logger.debug('jsonFile.lower(): %s', jsonFile.lower())
  logger.debug('urlEndPoint: %s', urlEndPoint)
  logger.debug('len(validTargetIds): %i', len(validTargetIds))
  logger.debug('validTargetIds[0]: %i', validTargetIds[0])


  # This is to answer when QA asks "How many operations?"
  for sameQueryLoop in range(0,parLoopsToRun):
    restAnswer = ''

    logger = logging.getLogger('--- sameQueryLoop LOOP ---')
    logger = logging.debug('sameQueryLoop: %i', sameQueryLoop)

    # Check if i should loop until i find something or not
    if parRunTillSomethingFound == 'N':
      minDataLen=1
    else:
      minDataLen=3  # Rest call returns "{}" if nothing found


    thisTentativeLoop=0
    while ( len(restAnswer) < minDataLen ):
      logger = logging.getLogger('--- WHILE LOOP ---')

      thisTentativeLoop=thisTentativeLoop+1
      restRequestStatusCode = 0
      answerSizeInBytes = answerSizeInChars = startTime = endTime = 0

      # Here i pick the ID to send
      idToSearch=str(validTargetIds[random.randint(0, len(validTargetIds)-1)])


      queryToRun = queryFromFile.replace('##PARAM_ID##',idToSearch)
      querySizeInBytes = sys.getsizeof(queryToRun)
      querySizeInChars = len(queryToRun)


      # Murphy's law of output:
      #  "The value of a program is inversely proportional to the weight of its output."
      #  (again :-D)
      logger.debug('-------------------------------------')
      logger.debug('thisTentativeLoop: %i', thisTentativeLoop)
      logger.debug('len(restAnswer): %i',len(restAnswer))
      logger.debug('minDataLen: %i',minDataLen)
      logger.debug('idToSearch: %s',idToSearch)
      logger.debug('parConnectTo+urlEndPoint=#'+parConnectTo+urlEndPoint+'#')
      logger.debug('queryToRun=#'+queryToRun+'#')


      # REST call built here
      restRequest = urllib2.Request(parConnectTo + urlEndPoint )
      restRequest.add_header('Content-Type', 'application/json')
      restRequest.add_header('Cache-Control', 'no-cache')
      locExceptionFound=False

      startTime = time.time()
      try:
        # After a looong way, time to call the freaking rest service!
        response = urllib2.urlopen(restRequest, queryToRun)
        restAnswer = response.read()
        endTime = time.time()

        restRequestStatusCode = response.code

        answerSizeInBytes = sys.getsizeof(restAnswer)
        answerSizeInChars = len(restAnswer)

      except urllib2.HTTPError as e:
        restRequestStatusCode = e.code
        restAnswer='---EXCEPTION--- '+str(e.code)+':'+e.reason
        endTime = startTime-1
        answerSizeInBytes=answerSizeInChars=querySizeInBytes=querySizeInChars=-99999999
        locExceptionFound=True
        time.sleep( 0.5 )


      # Sad to realize: all this mess, to get this simeple information... In one line... :-D
      deltaTime=(endTime-startTime)


      # Have i got to the maximum tentative i have to find something?
      if locExceptionFound==False:
        if (parIdFileSpecified==True) and (parRunTillSomethingFoundMaxLoops <> -1) and (thisTentativeLoop >=  parRunTillSomethingFoundMaxLoops):
          # Yep
          restAnswer='MaxTentativeExausted'
          restRequestStatusCode=-1
          deltaTime=answerSizeInBytes=answerSizeInChars=querySizeInBytes=querySizeInChars=-99999999


      # Printing time!
      #  Well, IF and WHAT i have to...
      if (  (parRunTillSomethingFound <> 'N' and len(restAnswer) >= minDataLen) or  (parRunTillSomethingFound == 'N')  ):

        logger.debug('--- PRINTING! ')
        restAnswerToPrint=''

        if parPrintRestAnswer <> 'N':
          #restAnswerToPrint = json.dumps(restAnswer)
          restAnswerToPrint = restAnswer

        if parPrintShortRestAnswer <> 'N':
          #restAnswerToPrint = json.dumps(restAnswer)
          restAnswerToPrint = restAnswer[:50]

        outCsv = "%s,,%s,%s,%f,,%s,\"%s\",%i,%i,%i,%f,%i,%i,%i,%i,' %s ' ,"   % \
              (parCsvLead,datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S'), float(time.time()), jsonFile, idToSearch, sameQueryLoop, thisTentativeLoop, restRequestStatusCode, deltaTime, querySizeInBytes, querySizeInChars, answerSizeInBytes, answerSizeInChars,restAnswerToPrint)

        print outCsv
        writesNum = writesNum+1
        if writesNum > parFlushSpoolEvery:
          sys.stdout.flush()
          writesNum=0

      if locExceptionFound==True and parExitIfException <> 'N':
        logger.debug('-- Exception found, exiting')
        sys.stdout.flush()
        sys.exit(99)


      logger.debug('--------- restAnswer=#'+restAnswer+'#')
      logger.debug('-------------------------------------')
      logger.debug('-------------------------------------\n\n\n')

  sys.stdout.flush()

sys.stdout.flush()
#devNull.close()

# That's all Folks!
