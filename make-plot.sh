#!/bin/sh
set -x
if test -z $3
then
    echo Expecting 3 args:
    echo likescore parscores tag
    exit 1
fi
../parse_paup_sitelike_to_tab_separated.py "$1" "$2" > "$3.score.table.txt" || exit
Rscript ../create_site_lnL_plots.R "$3.score.table.txt" || exit
echo "Done."
