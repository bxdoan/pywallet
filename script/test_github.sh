#!/usr/bin/env bash

# shellcheck disable=SC2046
# shellcheck disable=SC2128
# shellcheck disable=SC2006
SH=$(cd `dirname "$BASH_SOURCE"` && pwd)
PH=$(cd "$SH/.." && pwd)
# shellcheck disable=SC2164
cd "$PH"
mkdir -p "$SH/tmp"
tee_log="$SH/tmp/$(basename "$BASH_SOURCE").log"
pytest -p no:warnings --tb=short --cov=pywallet 2>&1 | tee "$tee_log"
min_coverage="50"
# shellcheck disable=SC2006
code_coverage=`grep 'TOTAL' "$tee_log" | awk '{print $NF}'`
echo "Minimum coverage percentage: ${min_coverage}%"
echo "Code coverage percentage: ${code_coverage}%"

has_failed_2nd_run=`grep -c  -E '=+.+failed|=+.+error'  "$tee_log" `  # know if parallel test failed ref. https://github.com/namgivu/pytest-start/commit/a921f9bf2d66519604e5b6846afedfd17198efc1
if [[ $has_failed_2nd_run == '0' ]]; then
    exit 0
else
    echo "All efforts failed"
    exit 1
fi