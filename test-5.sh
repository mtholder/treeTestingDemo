#!/bin/sh
set -x
mkdir take5 || exit
cd take5 || exit
cp ../5-taxa-paup-batch.nex . || exit
paup -n 5-taxa-paup-batch.nex || exit 
../parse_paup_sitelike_to_tab_separated.py hcg.likescores.txt hcg.parscores.txt > hcg.score.table.txt || exit
Rscript ../create_site_lnL_plots.R hcg.score.table.txt || exit
echo "Done."
