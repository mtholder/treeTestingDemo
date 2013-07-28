#!/bin/sh
set -x
mkdir take-m || exit
cd take-m || exit
cp ../macaque-paup.nex . || exit
paup -n macaque-paup.nex || exit 
../parse_paup_sitelike_to_tab_separated.py macaque.likescores.txt macaque.parscores.txt > macaque.score.table.txt || exit
Rscript ../create_site_lnL_plots.R macaque.score.table.txt || exit
echo "Done."
