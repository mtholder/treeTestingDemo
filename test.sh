#!/bin/sh
set -x
mkdir take2 || exit
cd take2 || exit
cp ../paup-batch.nex . || exit
paup -n paup-batch.nex || exit 
../parse_paup_sitelike_to_tab_separated.py hcg.likescores.txt hgc.parscores.txt > hcg.score.table.txt || exit
Rscript ../create_site_lnL_plots.R hcg.score.table.txt || exit
echo "Done."
