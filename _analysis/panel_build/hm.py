import pandas as pd, numpy as np, json, re

UP = '/mnt/user-data/uploads/'
_cmap_raw = json.load(open('/home/claude/panel/cmap.json'))
def _n(s): return re.sub(r'\s+',' ',str(s).strip())
# FIX: normalize mapping keys (double-space keys like 'kwantagora  Goussaoua')
cmap = {_n(k): v for k, v in _cmap_raw.items()}
cmap['AtchidaKofoto bilingue'] = 'Atchidakofoto Bilingue'   # session fix (case variant)

xw = pd.read_csv('/home/claude/panel/status_xw.csv')
xw = xw[~xw['family'].astype(str).str.startswith('#')]
EOY = {_n(k):v for k,v in zip(xw[xw.family=='EOY_Status'].raw_value, xw[xw.family=='EOY_Status'].canonical_status)}
COL = {_n(k):v for k,v in zip(xw[xw.family=='College_Tracking'].raw_value, xw[xw.family=='College_Tracking'].canonical_status)}
COL['Elle reprend la classe du CM2'] = 'NOT_TRANSITIONED'   # session addition (flagged)

DROP_ROWS = {'total','totaux','ensemble'}

def canon(s):
    if pd.isna(s): return np.nan
    v = _n(s)
    if v.lower() in DROP_ROWS: return np.nan
    return cmap.get(v, v)

def stat(v, table):
    if pd.isna(v) or _n(v) in ('','nan'): return np.nan
    v = _n(v)
    if v in table: return table[v]
    lo = {k.lower():c for k,c in table.items()}
    if v.lower() in lo: return lo[v.lower()]
    if re.fullmatch(r'[\d.%]+', v) or re.fullmatch(r'\?+', v): return 'INVALID'
    return 'UNMAPPED:'+v

def num(s): return pd.to_numeric(s, errors='coerce')

def dz(df):
    for a,b in [('pre_math','pre_fr'),('post_math','post_fr')]:
        if a in df and b in df:
            z = (df[a]==0)&(df[b]==0)
            df.loc[z,[a,b]] = np.nan

def find_header(f, sh, kw='ecole', maxr=10):
    d0 = pd.read_excel(f, sheet_name=sh, header=None, nrows=maxr)
    for i in range(len(d0)):
        if d0.iloc[i].astype(str).str.lower().str.contains(kw).any(): return i
    return 0

def read(f, sh, hdr=None, kw='ecole'):
    if hdr is None: hdr = find_header(f, sh, kw)
    d = pd.read_excel(f, sheet_name=sh, header=hdr)
    d.columns = [_n(c) for c in d.columns]
    ec = [c for c in d.columns if c.lower().startswith('ecole') or c.lower()=='ecoles' or 'school' in c.lower()]
    if ec:
        d = d[d[ec[0]].notna()].copy()
        d['school'] = d[ec[0]].map(canon)
        d = d[d['school'].notna()]
    return d

VALID_EXCL = {'INVALID','REVIEW_NEEDED','DECEASED'}

def agg_eoy_counts(ser):
    c = ser.value_counts().to_dict()
    valid = {k:v for k,v in c.items() if k not in VALID_EXCL and not str(k).startswith('UNMAPPED')}
    n = sum(valid.values())
    passed = valid.get('PASSED_EXAM',0)+valid.get('TRANSITIONED_SECONDARY',0)
    return pd.Series({'n_eoy_valid':n,'n_dropout':valid.get('DROPOUT',0),'n_passed':passed,
        'n_repeated':valid.get('REPEATED',0),'n_cfm':valid.get('TRANSFERRED_CFM',0),
        'taux_abandon': 100*valid.get('DROPOUT',0)/n if n else np.nan,
        'taux_reussite': 100*passed/n if n else np.nan})

def agg_college(g, eoy_col='eoy', col_col='college'):
    el = g[g[eoy_col].isin(['PASSED_EXAM','TRANSITIONED_SECONDARY'])] if eoy_col in g else g
    c = el[col_col].value_counts().to_dict()
    enr, nt = c.get('ENROLLED_SECONDARY',0), c.get('NOT_TRANSITIONED',0)
    den = enr+nt
    return pd.Series({'n_eligible':len(el),'n_enrolled_sec':enr,'n_not_trans':nt,
        'taux_inscription': 100*enr/den if den else np.nan})

def agg_scores(g):
    return pd.Series({'n_girls': len(g),
        'pre_math': g.pre_math.mean() if 'pre_math' in g else np.nan,
        'pre_fr': g.pre_fr.mean() if 'pre_fr' in g else np.nan,
        'post_math': g.post_math.mean() if 'post_math' in g else np.nan,
        'post_fr': g.post_fr.mean() if 'post_fr' in g else np.nan,
        'cfepd': g.cfepd.mean() if 'cfepd' in g else np.nan,
        'n_pre': g.pre_math.notna().sum() if 'pre_math' in g else 0,
        'n_post': g.post_math.notna().sum() if 'post_math' in g else 0})

def report_unmapped(df, cols=('eoy','college')):
    for c in cols:
        if c in df:
            u = df[c][df[c].astype(str).str.startswith('UNMAPPED')].value_counts()
            if len(u): print(f'UNMAPPED {c}:'); print(u.head(15).to_string())
