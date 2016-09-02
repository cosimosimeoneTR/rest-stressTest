# rcs-neo4j-stressTest
``perfTest.py`` parameter list:
<li>``--connectTo - string - *mandatory*`` Where to go
<li>``--loopsToRun - int - Default: 1`` How many times run the same query
<li>``--csvLead - string`` a CSV of your convenience you want to print it out in results
<li>``--debugLevel - 0/1 - Default: 0`` 1: you want debug infos in console, 0 you dont want it
<li>``--testFileToRun - string - Default: run all files in query/ directory`` json file containing call to run; do not pass it to run all tests
<li>``--runTillSomethingFound - Y/N - Default: N`` IDs are choosen randomly between a file; passing Y means  "Run the same query, over and over again till you find something"
<li>``--runTillSomethingFoundMaxLoops - int - Default: 10`` Given previous statement, with this param you avoid waiting forever for something to be found. "try to find something for maximum X times"
<li>``--idFile - string - Default: <testFileToRun>.idList`` File with valid IDs
<li>``--id - int[,int,int,...]`` Specific ID(s if comma separated) to pass to rest call;<br>
            If no ``--idFile`` and no ``--id`` is passed, code will try to open ``<testFileToRun>.idList``, or fail
<li>``--printRestAnswer - Y/N - Default: N`` Do you want me to spool restOutput in CSV file?
<li>``--printHeader - Y/N - Default: N`` Should i print header?
<li>``--outFile - string - Default: standard output`` File name i should spool (default=stdOut)
<li>``--printShortRestAnswer - Y/N - Default: N`` Do you want me to spool first 50 characters of rest answer in CSV file?
<li>``--truncateOutFile - Y/N - Default: N`` Should i truncate output file?
<li>``--flushSpoolEvery - int - Default: 30`` How often to flush spool
<li>``--exitIfException - Y/N - Default: N`` Stop and exit if an exception is found in REST call


Header file:<br>
``CustomCsv (multiple values here!),,DataTimeString,DataTimeStringUTC,DataTimeEpoch,, QueryExecuted, ID(s), LoopNumber, TentativeNumber, RequestStatusCode, Time(seconds), QuerySize(Bytes), QuerySize(Chars), AnswerSize(Bytes), AnswerSize(Chars),AnswerFromService``
