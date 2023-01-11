#!/usr/bin/env bash
STARTTIME=$(date +%s)
#Do not allow commit code if fail flake8
#As of nowTotal LOC: 137413
#Not compile with flake8: 51959 ~ 37%
#Setup circleci so that it will fail when % of code that not compile with flake8 > 33%
PWD=`cd $(dirname "$BASH_SOURCE") && pwd`; CODE=`cd $PWD/.. && pwd`

#region printing util
EC='\033[0m'    # end coloring
HL='\033[0;33m' # high-lighted color
ER='\033[0;31m' # red color

CM='\033[0;32m' # comment color
GR='\033[0;32m' # green color
WH='\033[0;37m' # white color
expected=20

function print_res() {
    printf "
Flake8 check information
Line of code:               ${GR}${1}${EC}
Line code isn't coverage:   ${GR}${2}${EC}
Percentage of non-coverage: ${GR}${3}%%${EC}
Expected percentage of non-coverage less than ${GR}${expected}%%${EC}"
}

function print_exe_time() {
    STARTTIME=${1}
    ENDTIME=$(date +%s)
    EXE_TIME=$((${ENDTIME} - ${STARTTIME}))
    printf "
It takes ${GR}${EXE_TIME}${EC} seconds to complete this script...\n"
}

# loc aka line of code
loc=$(git ls-files   |   grep '\.py'       | grep -Ev __boneyard__ | xargs wc -l | awk '{w=$1} END{print w}')
# list all file git     only python file     exclude __boneyard__    count line         get result

# flake with exclude dir in $pywallet/.flake8
# l_cover aka number line coveragetest_record_visits
l_cover=$(flake8 | wc -l)

# calculate percentage of coverage pep8
percent=$((${l_cover} * 100 / ${loc}))

print_res ${loc} ${l_cover} ${percent}
print_exe_time ${STARTTIME}

if [[ ${percent} -gt ${expected} ]]; then
    printf "Check flake8 ${ER}failed${EC}"
    exit 1
else
    exit 0
fi


