#!/bin/bash

shopt -s expand_aliases
alias echoi='echo `date +%Y-%m-%d\ %H:%M.%S` - '

if [ $# -le 2 ]; then
   echo "Please pass:"
   echo "* server IP address/URL and port, eg http://52.36.128.125:7001 "
   echo "* test file to run (ALL for... well... all) "
   echo "* (OPTIONAL) output file name "
   exit 1
fi

serverAdress=$1
serverIP=`echo $1 | sed  's,http://,,g' | sed 's,:7001,,g'`

echoi "Calling curl to check server is alive"
curl $serverAdress > /dev/null 2>/dev/null
if [ $? -ne 0 ]; then
   echoi "ERROR calling server $serverAdress";
   exit 2
fi



export myDate=`date +%Y%m%d-%H%M%S`

if [ 'x'$3 == 'x' ]; then
  outFileName=zzusersnumzzUSERS_zztimesnumzzQUERIES_$myDate.csv
else
  outFileName=$3
fi

export EXECME_PROTO="./perfTest.py --connectTo $serverAdress  --idFile queries/_validTargetIds.csv -o Y --runTillSomethingFound N --printShortRestAnswer Y  --truncateOutFile N zzfileToRunzz "
export EXECME_RUN="$EXECME_PROTO --loopsToRun zztimesnumzz --csvLead zzusersnumzzUSERS_zztimesnumzzQUERIES_$myDate --outFile $outFileName "


if [ $2 == 'ALL' ]; then
  export EXECME_RUN=` echo $EXECME_RUN | sed "s,zzfileToRunzz,,g" `
else
  export EXECME_RUN=` echo $EXECME_RUN | sed "s,zzfileToRunzz,--testFileToRun $2,g" `
fi


export numUsers=1
export numTimes=25
echoi "Executing $numUsers user, $numTimes times"
EXECME=`echo $EXECME_RUN --printHeader Y | sed "s,zzusersnumzz,$numUsers,g" | sed "s,zztimesnumzz,$numTimes,g" | sed "s,zzthreadnumzz,1,g" `
# Run Forrest, RUN!
#echo $EXECME
$EXECME


function runmeMulti {

  export numUsers=$1
  export numTimes=$2
  echoi "Executing $numUsers user, $numTimes times"
  EXECME_THREAD=`echo $EXECME_RUN | sed "s,zzusersnumzz,$numUsers,g" | sed "s,zztimesnumzz,$numTimes,g" `

  export pids=""
  i=1
  while [[ $i -le $numUsers ]]
  do
    EXECMENOW=`echo $EXECME_THREAD | sed "s,zzthreadnumzz,$i,g"`
    # Run Forrest, RUN!
    #echo $EXECMENOW
    nohup $EXECMENOW > /dev/null 2>&1 &
    pids="$pids $!"
    ((i = i + 1))
    sleep 0.1
  done
  wait $pids

}

runmeMulti   2 25
runmeMulti   5 25
runmeMulti  10 25
runmeMulti  15 25
runmeMulti  20 25
runmeMulti  30 25
runmeMulti  40 25
runmeMulti  50 25
runmeMulti  60 25
runmeMulti  70 25
runmeMulti  80 25
runmeMulti  90 25
runmeMulti 100 25

echoi "Thanks all!"
