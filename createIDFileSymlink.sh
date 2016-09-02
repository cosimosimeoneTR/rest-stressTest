#!/bin/bash

if [ $# -ne 1 ]; then
   echo "Please pass:"
   echo "* File containing IDs"
   exit 1
fi

cd queries

idFile=$1

find -type f -name "*json" -exec ln --symbolic -- "$idFile" "{}.idList" \;

cd -