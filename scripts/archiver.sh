#/bin/bash

OUTPUTPATH='./output/'
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

tar -cvzf "./archive/output_"$TIMESTAMP".tar.gz" $OUTPUTPATH
tar -cvzf "./archive/econ."$TIMESTAMP".log.gz" "./econ.log"

echo "" > "./econ.log"
rm -Rv $OUTPUTPATH

mkdir -pv $OUTPUTPATH"summary"
mkdir -pv $OUTPUTPATH"detailed"
