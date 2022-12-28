#/bin/bash

INPUTPATH='./input'
DETAILEDRESULTSNEEDED=$1
INPUTFILES=$(find $INPUTPATH -name '*.csv')

for ff in "${INPUTFILES[@]}"
do
	CASES=$(cat $ff | wc -l)
	IFS=$'\n'
	for line in `cat $ff`
	do
		echo $line | cut -d "," -f 1
	done
	python ./main.py $ff $CASES $DETAILEDRESULTSNEEDED
done

cd ./input/
rm -v input*
cd ../
