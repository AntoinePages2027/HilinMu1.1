import sys; sys.path.insert(0,'/home/claude/panel')
from hm import *

rows=[]
# ---- C5 CM1: EXAMENS file (per COMPLETENESS; not the 931_743 candidate) ----
f = UP+'HILIN_MU_C5_CM1_EXAMENS_08_08_2023.xlsx'
xl = pd.ExcelFile(f)
for sh, side in [(s,'Int' if 'intervention' in s.lower() else 'Ctrl')
                 for s in xl.sheet_names if 'base' in s.lower()]:
    d = read(f, sh)
    m = [c for c in d.columns if c.lower().startswith('math')]
    fr = [c for c in d.columns if c.lower().startswith('fran')]
    sc = [c for c in d.columns if c.lower().startswith('situation')]
    print('C5 CM1', sh[:30], side, '| n', len(d), '| sit cols:', sc, '| math:', m[:3])
    o = pd.DataFrame({'cohort':'C5','level':'CM1','side':side,'school':d['school'],
        'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
        'post_math':num(d[m[1]]) if len(m)>1 else np.nan,
        'post_fr':num(d[fr[1]]) if len(fr)>1 else np.nan,
        'eoy':d[sc[0]].map(lambda v: stat(v,EOY)) if sc else np.nan,
        'college':np.nan,'cfepd':np.nan})
    dz(o); rows.append(o)

# ---- C5 CM2: pilot file ----
f = UP+'C5_CM2_BasePhasePilote_EOY_CollegeTracking_5_.xlsx'
for sh, side in [('Groupe Intervention ','Int'),('Groupe Temoin ','Ctrl')]:
    d = read(f, sh)
    d = d.loc[:, [c for c in d.columns if not str(c).startswith('Unnamed')]]
    m = [c for c in d.columns if c.lower().startswith('math')]
    fr = [c for c in d.columns if c.lower().startswith('fran')]
    cc = [c for c in d.columns if 'compo' in c.lower()]
    sc = [c for c in d.columns if 'situation' in c.lower() or 'suivi' in c.lower() or 'college' in c.lower()]
    print('C5 CM2', sh[:24], side, '| n', len(d), '| cols:', list(d.columns)[:26])
    eoyc = [c for c in sc if 'fin' in c.lower() or ('situation' in c.lower() and 'college' not in c.lower() and 'suivi' not in c.lower())]
    colc = [c for c in sc if 'college' in c.lower() or 'suivi' in c.lower()]
    o = pd.DataFrame({'cohort':'C5','level':'CM2','side':side,'school':d['school'],
        'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
        'post_math':num(d[m[1]]) if len(m)>1 else np.nan,
        'post_fr':num(d[fr[1]]) if len(fr)>1 else np.nan,
        'eoy':d[eoyc[0]].map(lambda v: stat(v,EOY)) if eoyc else np.nan,
        'college':d[colc[0]].map(lambda v: stat(v,COL)) if colc else np.nan,
        'cfepd':pd.concat([num(d[c]) for c in cc],axis=1).mean(axis=1) if cc else np.nan})
    dz(o); rows.append(o)

g = pd.concat(rows, ignore_index=True)
report_unmapped(g)
g.to_csv('/home/claude/panel/c5_girls.csv', index=False)
S = g.groupby(['cohort','level','side','school']).apply(agg_scores, include_groups=False).reset_index()
E = g.groupby(['cohort','level','side','school'])['eoy'].apply(agg_eoy_counts).unstack().reset_index()
C = g[g.level=='CM2'].groupby(['cohort','level','side','school']).apply(agg_college, include_groups=False).reset_index()
out = S.merge(E, on=['cohort','level','side','school'], how='outer').merge(C, on=['cohort','level','side','school'], how='left')
out.insert(1,'year',2023)
out.to_csv('/home/claude/panel/c5_school_outcomes.csv', index=False)
print(out.groupby(['level','side'])[['n_girls']].sum())
print(out.groupby(['level','side']).size())
