#!/usr/bin/env python
import sys, os, re
SCRIPT_NAME = os.path.split(os.path.abspath(sys.argv[0]))[1]
if len(sys.argv) == 1:
    inp = iter(sys.stdin)
elif len(sys.argv) == 2:
    inp = iter(open(sys.argv[1], 'rU'))
else:
    sys.exit(SCRIPT_NAME + ": expecting an input file which should be a paup scorefile produced by LScore with the sitelikes option.\n")
expected_first = "Tree\t-lnL\tSite\t-lnL"
first = inp.next().strip()
if first != expected_first:
    sys.exit('%s: Expecting "%s" as the first line, but found "%s"\n' % (SCRIPT_NAME, expected_first, first))

TREE_LIKE_PAT = re.compile(r'^(\d+)\t([.0-9]+)')
SITE_LIKE_PAT = re.compile(r'^\t\t(\d+)\t([.0-9]+)')
tree_site_ln_like_list = []
curr_site_ln = []
curr_site_ln_sum = 0.0
num_sites = None
for n, line in enumerate(inp):
    m = TREE_LIKE_PAT.match(line)
    if m:
        if len(curr_site_ln) > 0:
            assert(len(tree_site_ln_like_list) + 1 == curr_tree_num)
            if abs(expected_ln_like - curr_site_ln_sum) > 10-4:
                sys.exit('Tree ln L for tree %d disagrees with sum of site lnL.\n')
            tree_site_ln_like_list.append(curr_site_ln)
            if num_sites == None:
                num_sites = len(curr_site_ln)
            elif num_sites != len(curr_site_ln):
                sys.exit('The number of sites for tree %d is %d. Previous tree(s) had %d sites\n' % (curr_tree_num, len(curr_site_ln), num_sites))
            curr_site_ln= []
            curr_site_ln_sum = 0.0
        curr_tree_num = int(m.group(1))
        expected_ln_like = float(m.group(2))
    else:
        m = SITE_LIKE_PAT.match(line)
        if not m:
            sys.exit('%s: Could not parse line %d: "%s"\n' % (SCRIPT_NAME, n + 2, line[:-1]))
        sn = int(m.group(1))
        sls = m.group(2)
        slf = float(sls)
        assert(sn == (1 + len(curr_site_ln)))
        curr_site_ln.append(sls)
        curr_site_ln_sum += slf

if len(curr_site_ln) > 0:
    assert(len(tree_site_ln_like_list) + 1 == curr_tree_num)
    if abs(expected_ln_like - curr_site_ln_sum) > 10-4:
        sys.exit('Tree ln L for tree %d disagrees with sum of site lnL.\n')
    tree_site_ln_like_list.append(curr_site_ln)
    if num_sites == None:
        num_sites = len(curr_site_ln)
    elif num_sites != len(curr_site_ln):
        sys.exit('The number of sites for tree %d is %d. Previous tree(s) had %d sites\n' % (curr_tree_num, len(curr_site_ln), num_sites))

outp = sys.stdout
num_trees = len(tree_site_ln_like_list)
outp.write('Site\ttree%s\n' % '\ttree'.join([str(1 +i) for i in range(num_trees)]))
for i in range(num_sites):
    outp.write('%d\t%s\n' % (1 + i, '\t'.join([x[i] for x in tree_site_ln_like_list])))
