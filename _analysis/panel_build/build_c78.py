import sys; sys.path.insert(0,'/home/claude/panel')
from hm import *
from hm import _n
EOY.update({'Decedée':'DECEASED','Redouble au CM1':'REPEATED','rédble le CM1':'REPEATED'})

# ================= C7 =================
# CM1: canonical prepost+status file
f = UP+'C7_CM1_TX_CTRL_prepost_status_CANONICAL_3_.xlsx'
d = pd.read_excel(f, sheet_name='HMCM1C7')
d.columns = [_n(c) for c in d.columns]
print('C7 CM1 cols:', list(d.columns))
sc = [c for c in d.columns if 'ecole' in c.lower() or 'school' in c.lower()][0]
d['school'] = d[sc].map(canon)
grp = [c for c in d.columns if 'group' in c.lower()][0]
st  = [c for c in d.columns if 'status' in c.lower()][0]
mb = [c for c in d.columns if 'basemath' in c.lower().replace(' ','')][0]
me = [c for c in d.columns if 'endmath' in c.lower().replace(' ','')][0]
fb = [c for c in d.columns if 'basefran' in c.lower().replace(' ','')][0]
fe = [c for c in d.columns if 'endfran' in c.lower().replace(' ','')][0]
print('C7 CM1 group counts:', d[grp].value_counts().to_dict())
c7cm1 = pd.DataFrame({'cohort':'C7','level':'CM1',
    'side': d[grp].map({1:'Int',0:'Ctrl'}),
    'school': d['school'],
    'pre_math':num(d[mb]),'pre_fr':num(d[fb]),'post_math':num(d[me]),'post_fr':num(d[fe]),
    'status25':num(d[st])})
dz(c7cm1)
def agg7cm1(g):
    n_ab = (g.status25==0).sum(); n_pr = (g.status25==1).sum(); n = n_ab+n_pr
    return pd.Series({'n_girls':len(g),
        'pre_math':g.pre_math.mean(),'pre_fr':g.pre_fr.mean(),
        'post_math':g.post_math.mean(),'post_fr':g.post_fr.mean(),
        'n_pre':g.pre_math.notna().sum(),'n_post':g.post_math.notna().sum(),
        'n_eoy_valid':n,'n_dropout':n_ab,
        'taux_abandon':100*n_ab/n if n else np.nan})
O71 = c7cm1.groupby(['cohort','level','side','school']).apply(agg7cm1, include_groups=False).reset_index()

# CM2: consolidated
f = UP+'C7_CM2_All_Pre_Post_TestScores_GovScores_EOY_1_.xlsx'
d = pd.read_excel(f, sheet_name='CM2_Consolidated')
d.columns = [_n(c) for c in d.columns]
print('C7 CM2 cols:', list(d.columns))
sc = [c for c in d.columns if 'ecole' in c.lower() or 'school' in c.lower()][0]
d['school'] = d[sc].map(canon)
grp = [c for c in d.columns if c.lower() in ('group','groupe') or 'group' in c.lower()][0]
yeo = [c for c in d.columns if 'yearend' in c.lower().replace(' ','') or 'outcome' in c.lower()][0]
cf  = [c for c in d.columns if 'cfepd' in c.lower()]
mb = [c for c in d.columns if 'basemath' in c.lower().replace(' ','') or ('pre' in c.lower() and 'math' in c.lower())]
me = [c for c in d.columns if 'endmath' in c.lower().replace(' ','') or ('post' in c.lower() and 'math' in c.lower())]
fb = [c for c in d.columns if 'basefran' in c.lower().replace(' ','') or ('pre' in c.lower() and 'fran' in c.lower())]
fe = [c for c in d.columns if 'endfran' in c.lower().replace(' ','') or ('post' in c.lower() and 'fran' in c.lower())]
print('C7 CM2 group counts:', d[grp].value_counts().to_dict(), '| yeo sample:', d[yeo].dropna().unique()[:8])
c7cm2 = pd.DataFrame({'cohort':'C7','level':'CM2',
    'side': d[grp].map(lambda v: 'Int' if str(v).strip() in ('1','Int','Intervention') else 'Ctrl'),
    'school': d['school'],
    'pre_math':num(d[mb[0]]) if mb else np.nan,'pre_fr':num(d[fb[0]]) if fb else np.nan,
    'post_math':num(d[me[0]]) if me else np.nan,'post_fr':num(d[fe[0]]) if fe else np.nan,
    'cfepd':num(d[cf[0]]) if cf else np.nan,
    'eoy': d[yeo].map(lambda v: stat(v,EOY))})
dz(c7cm2)
report_unmapped(c7cm2, ('eoy',))
S = c7cm2.groupby(['cohort','level','side','school']).apply(agg_scores, include_groups=False).reset_index()
E = c7cm2.groupby(['cohort','level','side','school'])['eoy'].apply(agg_eoy_counts).unstack().reset_index()
O72 = S.merge(E, on=['cohort','level','side','school'], how='outer')

# CM2 college: X-matrix sheets
f = UP+'C7_CM2_All_CollegeTracking_2_.xlsx'
crows = []
for sh, side in [('FILLES INTERVENTION','Int'),('FILLES CONTROLE','Ctrl')]:
    d = read(f, sh)
    xcols = [c for c in d.columns if _n(c).upper() in
             ('PRESENTE','PRESENTES','INSCRITE','INSCRITES','ABANDONNER','ABANDON',
              'TRANSFERER','TRANSFEREE','DECEDER','DECEDEE')]
    print('C7 college', sh, '| n', len(d), '| xcols:', xcols)
    def rowstat(r):
        marks = [c for c in xcols if str(r[c]).strip().lower() in ('x','xx','1','oui')]
        return stat(marks[0], COL) if len(marks)==1 else ('INVALID' if len(marks)>1 else np.nan)
    crows.append(pd.DataFrame({'cohort':'C7','level':'CM2','side':side,'school':d['school'],
        'college': d.apply(rowstat, axis=1)}))
c7col = pd.concat(crows)
C = c7col.groupby(['cohort','level','side','school']).apply(
    lambda g: agg_college(g.assign(eoy='PASSED_EXAM'), 'eoy','college'), include_groups=False).reset_index()
O72 = O72.merge(C, on=['cohort','level','side','school'], how='left')
c7 = pd.concat([O71, O72], ignore_index=True); c7.insert(1,'year',2025)
c7.to_csv('/home/claude/panel/c7_school_outcomes.csv', index=False)
print('C7 by level/side:\n', c7.groupby(['level','side']).size())

# ================= C8 =================
sheets = [('Base_des_données_Hilin_Mu_INTERVENTION_COHORTE8_MISE_A_JOUR_2025-2026_4_.xlsx','CM1 INTERVENTION','CM1','Int'),
          ('Base_des_données_Hilin_Mu_INTERVENTION_COHORTE8_MISE_A_JOUR_2025-2026_4_.xlsx','CM2 INTERVENTION','CM2','Int'),
          ('Base_des_données_controles_Cohorte8_2025-2026_4_.xlsx','CM1 CONTROLE','CM1','Ctrl'),
          ('Base_des_données_controles_Cohorte8_2025-2026_4_.xlsx','CM2 CONTROLE','CM2','Ctrl')]
rows8 = []
for fn, sh, lvl, side in sheets:
    d = read(UP+fn, sh)
    pre_f = [c for c in d.columns if 'pre' in c.lower() and 'fran' in c.lower()]
    pre_m = [c for c in d.columns if 'pre' in c.lower() and 'math' in c.lower()]
    post_f = [c for c in d.columns if 'post' in c.lower() and 'fran' in c.lower()]
    post_m = [c for c in d.columns if 'post' in c.lower() and 'math' in c.lower()]
    sit = [c for c in d.columns if 'situation' in c.lower()]
    cf = [c for c in d.columns if 'cfepd' in c.lower()]
    o = pd.DataFrame({'cohort':'C8','level':lvl,'side':side,'school':d['school'],
        'pre_math':num(d[pre_m[0]]) if pre_m else np.nan,
        'pre_fr':num(d[pre_f[0]]) if pre_f else np.nan,
        'post_math':num(d[post_m[0]]) if post_m else np.nan,
        'post_fr':num(d[post_f[0]]) if post_f else np.nan,
        'cfepd':num(d[cf[0]]) if cf and lvl=='CM2' else np.nan,
        'eoy':d[sit[0]].map(lambda v: stat(v,EOY)) if sit else np.nan})
    if lvl=='CM2' and side=='Ctrl':
        # DATA-ENTRY DUPLICATION (French==Math for 100%): subject scores unusable;
        # keep composite pre-test average only
        o['pre_comp'] = (o.pre_math+o.pre_fr)/2
        o[['pre_math','pre_fr']] = np.nan
    dz(o)
    print('C8', sh, '| n', len(o), '| eoy col:', sit[:1], '| eoy top:',
          o.eoy.value_counts().head(4).to_dict())
    rows8.append(o)
g8 = pd.concat(rows8, ignore_index=True)
report_unmapped(g8, ('eoy',))
S = g8.groupby(['cohort','level','side','school']).apply(agg_scores, include_groups=False).reset_index()
S['pre_comp'] = g8.groupby(['cohort','level','side','school'])['pre_comp'].mean().values if 'pre_comp' in g8 else np.nan
E = g8.groupby(['cohort','level','side','school'])['eoy'].apply(agg_eoy_counts).unstack().reset_index()
c8 = S.merge(E, on=['cohort','level','side','school'], how='outer')
c8.insert(1,'year',2026)
c8.to_csv('/home/claude/panel/c8_school_outcomes.csv', index=False)
print('C8 by level/side:\n', c8.groupby(['level','side']).size())
