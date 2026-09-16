"""C4 school-level outcomes, corrected sourcing:
  scores/CFEPD:  Marcus CM1 file; Marcus AllComplete CM2 (main + 4 extra ctrl sheets)
  CM1 EOY:       Marcus CM1 file
  CM2 EOY+college: AlmostComplete (both arms; ctrl 846 INCLUDES the 4 extras),
                   Tarna college backfilled from 2022-12-12 Base Suivi 6e if empty.
School-level join (analysis is school-level; avoids fragile girl-ID merges).
"""
import pandas as pd, numpy as np, json, re

UP = '/mnt/user-data/uploads/'
cmap = json.load(open('cmap.json'))
xw = pd.read_csv('status_xw.csv'); xw = xw[~xw['family'].astype(str).str.startswith('#')]
def _n(s): return re.sub(r'\s+',' ',str(s).strip())
EOY = {_n(k):v for k,v in zip(xw[xw.family=='EOY_Status'].raw_value, xw[xw.family=='EOY_Status'].canonical_status)}
COL = {_n(k):v for k,v in zip(xw[xw.family=='College_Tracking'].raw_value, xw[xw.family=='College_Tracking'].canonical_status)}
# session addition, FLAG for Antoine (2 girls, Base Suivi 6e): repeating CM2 = not transitioned
COL['Elle reprend la classe du CM2'] = 'NOT_TRANSITIONED'

def canon(s):
    if pd.isna(s): return np.nan
    return cmap.get(_n(s), _n(s))
def stat(v, table):
    if pd.isna(v) or _n(v)=='' or _n(v)=='nan': return np.nan
    v = _n(v)
    if v in table: return table[v]
    lo = {k.lower():c for k,c in table.items()}
    if v.lower() in lo: return lo[v.lower()]
    if re.fullmatch(r'[\d.]+', v) or re.fullmatch(r'\?+', v): return 'INVALID'
    return 'UNMAPPED:'+v
def num(s): return pd.to_numeric(s, errors='coerce')
def dz(df):
    z = (df['pre_math']==0)&(df['pre_fr']==0)
    df.loc[z,['pre_math','pre_fr']] = np.nan
    z2 = (df['post_math']==0)&(df['post_fr']==0)
    df.loc[z2,['post_math','post_fr']] = np.nan

def read(f, sh, hdr=None):
    if hdr is None:
        d0 = pd.read_excel(f, sheet_name=sh, header=None, nrows=8)
        hdr = next(i for i in range(8) if d0.iloc[i].astype(str).str.lower().str.contains('ecole').any())
    d = pd.read_excel(f, sheet_name=sh, header=hdr)
    d.columns = [_n(c) for c in d.columns]
    ecol = [c for c in d.columns if c.lower().startswith('ecole')][0]
    d = d[d[ecol].notna()].copy()
    d['school'] = d[ecol].map(canon)
    return d

# ============ SCORES ============
score_rows = []
# CM1
f = UP+'C4_CM1_Marcus_BaseDeDonnees_IntCtrl_3_.xlsx'
for sh, side in [('1. Base de donnée Intervention','Int'),('2. Base de données Control','Ctrl')]:
    d = read(f, sh, hdr=3)
    m = [c for c in d.columns if c.lower().startswith('math')]
    fr = [c for c in d.columns if c.lower().startswith('fran')]
    s = [c for c in d.columns if c.startswith("Situation (fin")][0]
    o = pd.DataFrame({'level':'CM1','side':side,'school':d['school'],
        'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
        'post_math':num(d[m[1]]),'post_fr':num(d[fr[1]]),
        'eoy':d[s].map(lambda v: stat(v,EOY)),'cfepd':np.nan})
    dz(o); score_rows.append(o)
# CM2 scores from Marcus (EOY here NOT used for CM2 — comes from AlmostComplete)
f = UP+'C4_CM2_Marcus_AllComplete_4ExtraSchools_5_.xlsx'
xl = pd.ExcelFile(f)
sheets = [('1. Base de donnée Intervention','Int'),('2. Base de données Control','Ctrl')] + \
         [(s,'Ctrl') for s in xl.sheet_names if s not in
          ['1. Base de donnée Intervention','2. Base de données Control','Explication des identifiants']]
for sh, side in sheets:
    d = read(f, sh)
    m = [c for c in d.columns if c.lower().startswith('math')]
    fr = [c for c in d.columns if c.lower().startswith('fran')]
    cc = [c for c in d.columns if 'compo' in c.lower()]
    o = pd.DataFrame({'level':'CM2','side':side,'school':d['school'],
        'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
        'post_math':num(d[m[1]]) if len(m)>1 else np.nan,
        'post_fr':num(d[fr[1]]) if len(fr)>1 else np.nan,
        'eoy':np.nan,
        'cfepd':pd.concat([num(d[c]) for c in cc],axis=1).mean(axis=1) if cc else np.nan})
    dz(o); score_rows.append(o)
scores = pd.concat(score_rows, ignore_index=True)

# ============ CM2 EOY + COLLEGE (AlmostComplete) ============
f = UP+'HilinMu_C4_CM2_All_AlmostComplete_4_.xlsx'
eoy_rows = []
for sh, side in [('1. Base de donnée Intervention','Int'),('2. Base de données Control','Ctrl')]:
    d = read(f, sh)
    e22 = [c for c in d.columns if c.startswith("Situation fin d'année 2022")][0]
    col = [c for c in d.columns if 'college' in c.lower()][0]
    eoy_rows.append(pd.DataFrame({'level':'CM2','side':side,'school':d['school'],
        'eoy':d[e22].map(lambda v: stat(v,EOY)),
        'college':d[col].map(lambda v: stat(v,COL))}))
cm2s = pd.concat(eoy_rows, ignore_index=True)

# Tarna college backfill from Base Suivi 6e
tarna_fill = cm2s[(cm2s.school=='Tarna')]['college'].notna().sum()
print('Tarna college non-null in AlmostComplete:', tarna_fill, '/', (cm2s.school=='Tarna').sum())
if tarna_fill < 10:
    d = read(UP+'2022-12-12_Base_Suivi_6_e_2_.xlsx','1. Base de donnée Intervention', hdr=3)
    col = [c for c in d.columns if 'college' in c.lower()][0]
    t = d[d.school=='Tarna']
    tt = pd.DataFrame({'level':'CM2','side':'Int','school':'Tarna',
        'eoy':t[[c for c in d.columns if c.startswith("Situation fin d'année 2022")][0]].map(lambda v: stat(v,EOY)),
        'college':t[col].map(lambda v: stat(v,COL))})
    print('Base Suivi 6e Tarna: n=',len(tt),' college non-null=',tt.college.notna().sum())
    cm2s = pd.concat([cm2s[cm2s.school!='Tarna'], tt], ignore_index=True)

# unmapped audit
for nm, ser in [('EOY(sc)',scores.eoy),('EOY(cm2)',cm2s.eoy),('COL',cm2s.college)]:
    u = ser[ser.astype(str).str.startswith('UNMAPPED')].value_counts()
    if len(u): print('UNMAPPED', nm, ':\n', u.to_string())

# ============ AGGREGATE ============
VALID_EXCL = {'INVALID','REVIEW_NEEDED','DECEASED'}
def agg_scores(g):
    return pd.Series({
        'n_girls': len(g),
        'pre_math': g.pre_math.mean(), 'pre_fr': g.pre_fr.mean(),
        'post_math': g.post_math.mean(), 'post_fr': g.post_fr.mean(),
        'cfepd': g.cfepd.mean(),
        'n_pre': g.pre_math.notna().sum(), 'n_post': g.post_math.notna().sum()})
S = scores.groupby(['level','side','school']).apply(agg_scores, include_groups=False).reset_index()

def agg_eoy(ser):
    c = ser.value_counts().to_dict()
    valid = {k:v for k,v in c.items() if k not in VALID_EXCL and not str(k).startswith('UNMAPPED')}
    n = sum(valid.values())
    passed = valid.get('PASSED_EXAM',0)+valid.get('TRANSITIONED_SECONDARY',0)
    return pd.Series({'n_eoy_valid':n,
        'n_dropout':valid.get('DROPOUT',0),'n_passed':passed,
        'n_repeated':valid.get('REPEATED',0),'n_cfm':valid.get('TRANSFERRED_CFM',0),
        'taux_abandon': 100*valid.get('DROPOUT',0)/n if n else np.nan,
        'taux_reussite': 100*passed/n if n else np.nan})
E1 = scores[scores.level=='CM1'].groupby(['level','side','school'])['eoy'].apply(agg_eoy).unstack().reset_index()
E2 = cm2s.groupby(['level','side','school'])['eoy'].apply(agg_eoy).unstack().reset_index()

def agg_col(g):
    # eligible-only: among girls with EOY in {PASSED_EXAM, TRANSITIONED_SECONDARY}
    el = g[g.eoy.isin(['PASSED_EXAM','TRANSITIONED_SECONDARY'])]
    c = el.college.value_counts().to_dict()
    enr, nt = c.get('ENROLLED_SECONDARY',0), c.get('NOT_TRANSITIONED',0)
    den = enr+nt
    return pd.Series({'n_eligible':len(el),'n_enrolled_sec':enr,'n_not_trans':nt,
        'n_college_missing': len(el)-sum(v for k,v in c.items() if not str(k).startswith('UNMAPPED')),
        'taux_inscription': 100*enr/den if den else np.nan})
C = cm2s.groupby(['level','side','school']).apply(agg_col, include_groups=False).reset_index()

out = S.merge(pd.concat([E1,E2]), on=['level','side','school'], how='outer') \
       .merge(C, on=['level','side','school'], how='left')
out.insert(0,'cohort','C4'); out.insert(1,'year',2022)
out.to_csv('c4_school_outcomes.csv', index=False)
scores.to_csv('c4_girls_scores.csv', index=False); cm2s.to_csv('c4_girls_cm2_eoy_college.csv', index=False)
print('\nschools by level/side:\n', out.groupby(['level','side']).size())
print('\nsummary (girl-weighted means):')
for lv in ['CM1','CM2']:
    for sd in ['Int','Ctrl']:
        o = out[(out.level==lv)&(out.side==sd)]
        w = o.n_girls
        def wm(c): 
            v=o[c].notna()&w.notna()
            return np.average(o[c][v],weights=w[v]) if v.sum() else np.nan
        print(f'{lv} {sd}: schools={len(o)} girls={int(w.sum())} '
              f'abandon={wm("taux_abandon"):.1f}% reussite={wm("taux_reussite"):.1f}% '
              f'inscription={wm("taux_inscription"):.1f}% pre_math={wm("pre_math"):.1f} post_math={wm("post_math"):.1f}')
