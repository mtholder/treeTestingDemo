#!/usr/bin/env python
import sys, os, re
SCRIPT_NAME = os.path.split(os.path.abspath(sys.argv[0]))[1]

def parse_paup_site_like_file(inp, score_type, is_parsimony=False):

    if is_parsimony:
        expected_first = re.compile(r"Tree\tLength\tCharacter\tLength")
    else:
        expected_first = re.compile(r"Tree\t-lnL\t.*Site\t-lnL")

    first = inp.next().strip()
    if not expected_first.match(first):
        sys.exit('%s: Unexpected first line found "%s"\n' % (SCRIPT_NAME, first))

    TREE_LIKE_PAT = re.compile(r'^(\d+)\t([-.0-9eE]+)\s.*')
    SITE_LIKE_PAT = re.compile(r'^\t+(\d+)\t([-.0-9eE]+)')
    tree_site_ln_like_list = []
    curr_site_ln = []
    curr_site_ln_sum = 0.0
    num_sites = None
    for n, line in enumerate(inp):
        m = TREE_LIKE_PAT.match(line)
        if m:
            if len(curr_site_ln) > 0:
                assert(len(tree_site_ln_like_list) + 1 == curr_tree_num)
                sys.stderr.write('expected_ln_like = ' + str(expected_ln_like) + '    curr_site_ln_sum = ' + str(curr_site_ln_sum) + '\n')
                if abs(expected_ln_like - curr_site_ln_sum) > 0.0001:
                    sys.exit('Tree ln L for tree %d disagrees with sum of site lnL.\n' % curr_tree_num)
                tree_site_ln_like_list.append(curr_site_ln)
                if num_sites == None:
                    num_sites = len(curr_site_ln)
                elif num_sites != len(curr_site_ln):
                    sys.exit('The number of sites for tree %d is %d. Previous tree(s) had %d sites\n' % (curr_tree_num, len(curr_site_ln), num_sites))
                curr_site_ln= []
                curr_site_ln_sum = 0.0
            curr_tree_num = int(m.group(1))
            expected_ln_like = score_type(m.group(2))
        else:
            m = SITE_LIKE_PAT.match(line)
            if not m:
                sys.exit('%s: Could not parse line %d: "%s"\n' % (SCRIPT_NAME, n + 2, line[:-1]))
            sn = int(m.group(1))
            sls = m.group(2)
            slf = score_type(sls)
            if abs(slf) < 1.0e-9:
                sls = '0.0'
            assert(sn == (1 + len(curr_site_ln)))
            curr_site_ln.append(sls)
            curr_site_ln_sum += slf
    if len(curr_site_ln) > 0:
        assert(len(tree_site_ln_like_list) + 1 == curr_tree_num)
        sys.stderr.write('expected_ln_like = ' + str(expected_ln_like) + '    curr_site_ln_sum = ' + str(curr_site_ln_sum) + '\n')
        if abs(expected_ln_like - curr_site_ln_sum) > 0.0001:
            sys.exit('Tree ln L for tree %d disagrees with sum of site lnL.\n' % curr_tree_num)
        tree_site_ln_like_list.append(curr_site_ln)
        if num_sites == None:
            num_sites = len(curr_site_ln)
        elif num_sites != len(curr_site_ln):
            sys.exit('The number of sites for tree %d is %d. Previous tree(s) had %d sites\n' % (curr_tree_num, len(curr_site_ln), num_sites))
    return tree_site_ln_like_list, num_sites

if __name__ == '__main__':
    if len(sys.argv) == 1:
        inp = iter(sys.stdin)
    else:
        like_filename = sys.argv[1]
        inp = iter(open(like_filename, 'rU'))
        if len(sys.argv) > 3:
            sys.exit(SCRIPT_NAME + ": expecting an input file which should be a paup scorefile produced by LScore with the sitelikes option.\n")

    tree_site_ln_like_list, num_sites = parse_paup_site_like_file(inp, float)
    pars_filename = None
    if len(sys.argv) == 3:
        pars_filename = sys.argv[2]
        inp = iter(open(pars_filename, 'rU'))
        tree_site_parsimony_list, num_sitesp = parse_paup_site_like_file(inp, int, is_parsimony=True)
        assert(num_sites == num_sitesp)
        assert(len(tree_site_ln_like_list) == len(tree_site_parsimony_list))
    outp = sys.stdout
    num_trees = len(tree_site_ln_like_list)
    if pars_filename:
        suffix = '\tPTree%s' % '\tPTree'.join([str(1 +i) for i in range(num_trees)])
    else:
        suffix = ""
    lsc_part = '\tLTree'.join([str(1 +i) for i in range(num_trees)])
    outp.write('Site\tLTree%s%s\n' % (lsc_part, suffix))
    if tree_site_ln_like_list[0][0] < 0.0:
        js = '\t'
    else:
        js = '\t-'
    for i in range(num_sites):
        if pars_filename:
            suffix = '\t' + ('\t'.join([x[i] for x in tree_site_parsimony_list]))
        else:
            suffix = ""
        lsc_part = js.join([x[i] for x in tree_site_ln_like_list])
        outp.write('%d%s%s%s\n' % (1 + i, js, lsc_part, suffix))
