#!/usr/bin/env bash

SH=$(cd `dirname $BASH_SOURCE` && pwd)
PH=$(cd "$SH/.." && pwd)
cd $PH
mkdir -p "$SH/tmp"
tee_log="$SH/tmp/$(basename $BASH_SOURCE).log"
pytest -p no:warnings --tb=short --cov=pywallet 2>&1 | tee $tee_log
min_coverage="50"
code_coverage=`grep 'TOTAL' $tee_log | awk '{print $NF}'`
echo "Minimum coverage percentage: ${min_coverage}%"
echo "Code coverage percentage: ${code_coverage}%"
