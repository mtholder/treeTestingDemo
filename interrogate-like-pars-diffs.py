#!/usr/bin/env python
import sys
max_t_1_ld = [0, '']
max_t_2_ld = [0, '']
max_t_1_pd = [0, '']
max_t_2_pd = [0, '']
max_t_1_disagd = [0, '']
max_t_2_disagd = [0, '']
max_t_1_same = [0, '']
max_t_2_same = [0, '']

li = iter(open(sys.argv[1], 'rU'))
pref = 'Site\tLTree1\tLTree2\tPTree1\tPTree2'
assert li.next().startswith(pref)
for line in li:
    line = line.strip()
    s = line.split()
    index, l1, l2, p1, p2 = [float(i) for i in s]
    dl1 = l1 -l2
    dl2 = -dl1
    dp1 = p1 - p2
    dp2 = -dp1
    if dl1 > max_t_1_ld[0]:
        max_t_1_ld[0], max_t_1_ld[1] = dl1, line
    if dl2 > max_t_2_ld[0]:
        max_t_2_ld[0], max_t_2_ld[1] = dl2, line
    if dp1 > max_t_2_pd[0]:
        max_t_2_pd[0], max_t_2_pd[1] = dp1, line
    if dp2 > max_t_1_pd[0]:
        max_t_1_pd[0], max_t_1_pd[1] = dp2, line
    if dp1 > 0: # tree 2 preferred
        if dl1 > max_t_1_disagd[0]:
            max_t_1_disagd[0], max_t_1_disagd[1] = dl1, line
    elif dp2 > 0: # tree 1 preferred
        if dl2 > max_t_2_disagd[0]:
            max_t_2_disagd[0], max_t_2_disagd[1] = dl2, line
    else:
        if dl1 > max_t_1_same[0]:
            max_t_1_same[0], max_t_1_same[1] = dl1, line
        if dl2 > max_t_2_same[0]:
            max_t_2_same[0], max_t_2_same[1] = dl2, line

print '                \tDiff\t{}'.format(pref)
frag = '{t}\t{d:.2f}\t{l}'
for i in [('max-like-for--T1', max_t_1_ld),
          ('max-like-for--T2', max_t_2_ld),
          ('max-pars-for--T1', max_t_1_pd),
          ('max-pars-for--T2', max_t_2_pd),
          ('max-like-dis--T1', max_t_1_disagd),
          ('max-like-dis--T2', max_t_2_disagd),
          ('max-like-same-T1', max_t_1_same),
          ('max-like-same-T2', max_t_2_same),
          ]:
    print frag.format(t=i[0], d=i[1][0], l=i[1][1])
