#!/usr/bin/env bash

function _() {
    local SH=$(cd `dirname $BASH_SOURCE` && pwd)
    local AH=$(cd "$SH/.." && pwd)
    cd $SH
    # prepare :pipenv binary
    if [[ -f "$HOME/.pyenv/shims/pipenv" ]]; then
      [ -x pipenv ] && pipenv='pipenv' || pipenv="$HOME/.pyenv/shims/pipenv"
    elif [[ -f "$HOME/.local/bin/pipenv" ]]; then
      [ -x pipenv ] && pipenv='pipenv' || pipenv="$HOME/.local/bin/pipenv"
    else
      [ -x pipenv ] && pipenv='pipenv' || pipenv="$HOME/.pyenv/shims/pipenv"
    fi
    mkdir -p "$SH/tmp"
    tee_log="$SH/tmp/$(basename $BASH_SOURCE).log"
    PYTHONPATH=`pwd` $pipenv run pytest -p no:warnings --tb=short --cov=pywallet 2>&1 | tee $tee_log
    min_coverage="50"
    code_coverage=`grep 'TOTAL' $tee_log | awk '{print $NF}'`
    echo "Minimum coverage percentage: ${min_coverage}%"
    echo "Code coverage percentage: ${code_coverage}%"
}
  eval _