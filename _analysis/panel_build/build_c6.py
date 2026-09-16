import sys; sys.path.insert(0,'/home/claude/panel')
from hm import *
from hm import _n
EOY['Decedée'] = 'DECEASED'  # session addition (1 girl C5)

# ---------- CM1: girl-level EOY, both arms ----------
f = UP+'C6_CM1_SituationFinAnnee_AllCommunes_2_.xlsx'
d = pd.read_excel(f, sheet_name='Sheet1')
d.columns = [_n(c) for c in d.columns]
d['school'] = d["Nom d'ecole"].map(canon)
d['side'] = d['Int/Controle'].map(lambda v: 'Int' if 'interv' in _n(v).lower() else 'Ctrl')
d['eoy'] = d['Situation Finale'].map(lambda v: stat(v, EOY))
cm1 = pd.DataFrame({'cohort':'C6','level':'CM1','side':d['side'],'school':d['school'],'eoy':d['eoy']})
print('CM1 girls:', len(cm1), cm1.side.value_counts().to_dict())
report_unmapped(cm1, ('eoy',))
E1 = cm1.groupby(['cohort','level','side','school'])['eoy'].apply(agg_eoy_counts).unstack().reset_index()
E1['n_girls'] = cm1.groupby(['cohort','level','side','school']).size().values

# CM1 intervention scores (partial, Marcus)
d = read(UP+'C6_CM1_Marcus_BaseDeDonnees_3_.xlsx','1. Base de donnée Hilin Mu CM1')
m = [c for c in d.columns if c.lower().startswith('math')]
fr = [c for c in d.columns if c.lower().startswith('fran')]
print('C6 CM1 Marcus n:', len(d), '| math cols:', m[:3])
o = pd.DataFrame({'school':d['school'],'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
                  'post_math':num(d[m[1]]) if len(m)>1 else np.nan,
                  'post_fr':num(d[fr[1]]) if len(fr)>1 else np.nan})
dz(o)
S1 = o.groupby('school').agg(pre_math=('pre_math','mean'),pre_fr=('pre_fr','mean'),
    post_math=('post_math','mean'),post_fr=('post_fr','mean'),
    n_pre=('pre_math','count'),n_post=('post_math','count')).reset_index()
S1[['cohort','level','side']] = ['C6','CM1','Int']
OUT1 = E1.merge(S1, on=['cohort','level','side','school'], how='left')

# ---------- CM2 (and CM1 cross-check) from Metrics tabs ----------
metrics_files = {
 ('Tibiri','Int'):'C6_CM2_Tibiri_Interv_EOY_Status_GovScores_5_.xlsx',
 ('Tibiri','Ctrl'):'C6_CM2_Tibiri_Control_EOY_Status_GovScores_3_.xlsx',
 ('Djirataoua','Int'):'C6_CM2_Djirataoua_Interv_EOY_Status_GovScores_2_.xlsx',
 ('Djirataoua','Ctrl'):'C6_CM2_Djirataoua_Control_EOY_Status_GovScores_1_.xlsx',
 ('Safo','Int'):'C6_CM2_Safo_Interv_EOY_Status_GovScores_1_.xlsx',
 ('Safo','Ctrl'):'C6_CM2_Safo_Control_EOY_Status_GovScores_1_.xlsx',
 ('Sae Saboua','Int'):'C6_CM2_Sae_Saboua_Interv_EOY_Status_GovScores_2_.xlsx',
 ('Sae Saboua','Ctrl'):'C6_CM2_Sae_Saboua_Control_EOY_Status_GovScores_2_.xlsx'}

mrows = []
for (com, side), fn in metrics_files.items():
    try:
        d = pd.read_excel(UP+fn, sheet_name='CM1 & CM2 Metrics', header=None)
    except Exception as ex:
        print('NO METRICS TAB:', fn, ex); continue
    level = None; cols = None
    for i in range(len(d)):
        row = d.iloc[i]
        joined = ' '.join(str(x) for x in row.tolist())
        c0 = _n(row[0])
        if re.search(r'\bCM1\b', joined) and 'CM2' not in joined and c0 in ('nan',''): level='CM1'; cols=None; continue
        if re.search(r'\bCM2\b', joined) and 'CM1' not in joined and c0 in ('nan',''): level='CM2'; cols=None; continue
        if c0.lower().startswith('ecole'):
            cols = [_n(x).lower() for x in row.tolist()]; continue
        if cols and c0 not in ('nan','') and level:
            def get(kw):
                idx = [j for j,c in enumerate(cols) if kw in c and '%' not in c and 'pourcent' not in c]
                return num(pd.Series([row[idx[0]]]))[0] if idx else np.nan
            ins = get('insrite') or get('inscrite')
            mrows.append({'cohort':'C6','level':level,'side':side,'commune':com,
                'school':canon(c0),'n_inscrites':ins,'n_dropout':get('abandon'),
                'n_presentes':get('presente'),'n_passed':get('admise')})
mt = pd.DataFrame(mrows).dropna(subset=['school'])
mt = mt[mt.n_inscrites.notna()]
mt['n_eoy_valid'] = mt['n_inscrites']
mt['taux_abandon'] = 100*mt.n_dropout/mt.n_inscrites
mt['taux_reussite'] = 100*mt.n_passed/mt.n_inscrites
print('\nMetrics rows by level/side:\n', mt.groupby(['level','side']).size())

# CM2 intervention scores
d = read(UP+'C6_CM2_Interv_Pre_Post_TestScores_2_.xlsx','1. Base de donnée HILIN MU CM2 ')
m = [c for c in d.columns if c.lower().startswith('math')]
fr = [c for c in d.columns if c.lower().startswith('fran')]
cc = [c for c in d.columns if 'compo' in c.lower()]
print('C6 CM2 interv scores n:', len(d), '| math:', m[:3])
o = pd.DataFrame({'school':d['school'],'pre_math':num(d[m[0]]),'pre_fr':num(d[fr[0]]),
    'post_math':num(d[m[1]]) if len(m)>1 else np.nan,
    'post_fr':num(d[fr[1]]) if len(fr)>1 else np.nan,
    'cfepd':pd.concat([num(d[c]) for c in cc],axis=1).mean(axis=1) if cc else np.nan})
dz(o)
S2 = o.groupby('school').agg(pre_math=('pre_math','mean'),pre_fr=('pre_fr','mean'),
    post_math=('post_math','mean'),post_fr=('post_fr','mean'),cfepd=('cfepd','mean'),
    n_pre=('pre_math','count'),n_post=('post_math','count')).reset_index()
S2[['cohort','level','side']] = ['C6','CM2','Int']

M2 = mt[mt.level=='CM2'].drop(columns=['n_presentes'])
OUT2 = M2.merge(S2, on=['cohort','level','side','school'], how='outer')
OUT2['n_girls'] = OUT2['n_inscrites']

# CM1 Metrics kept as cross-check file
mt[mt.level=='CM1'].to_csv('/home/claude/panel/c6_cm1_metrics_crosscheck.csv', index=False)

out = pd.concat([OUT1, OUT2], ignore_index=True)
out.insert(1,'year',2024)
out.to_csv('/home/claude/panel/c6_school_outcomes.csv', index=False)
print('\nC6 schools by level/side:\n', out.groupby(['level','side']).size())
w = out[out.level=='CM2'].groupby('side').apply(
    lambda g: pd.Series({'abandon':np.average(g.taux_abandon.dropna()),
                         'reussite':np.average(g.taux_reussite.dropna())}), include_groups=False)
print('\nC6 CM2 simple means:\n', w.round(1))
