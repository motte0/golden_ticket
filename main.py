import pandas as pd
from scipy.stats import pearsonr, f_oneway, spearmanr

# 1. 데이터 불러오기
file_path = './황금티켓 증후군 설문조사(응답).xlsx'
df = pd.read_excel(file_path)

# 2. 설문 문항 컬럼 추출
#    – DEFG: 황금티켓 증후군적 사고 강도 문항 4개
#    – HI  : 행복도 및 삶 만족도 문항 2개
#    – JK  : 가치관 문항 2개
syndrome_cols  = df.columns[3:7]   # D, E, F, G번째 컬럼
happiness_cols = df.columns[7:9]   # H, I번째 컬럼
value_cols     = df.columns[9:11]  # J, K번째 컬럼

# 2-1. 문항 점수 역코딩
all_items = list(syndrome_cols) + list(happiness_cols) + list(value_cols)
df[all_items] = df[all_items].apply(pd.to_numeric, errors='coerce')
df[all_items] = df[all_items].applymap(lambda x: 6 - x)

# 3. 점수 계산 (각 문항 1~5, 5가 동의 강도 높음)
weights = [3, 1, 1, 1]
df['syndrome_score'] = (
    df[syndrome_cols].multiply(weights, axis=1)
    .sum(axis=1)
    / sum(weights)
)
df['hi_score']       = df[happiness_cols].mean(axis=1)
df['value_score']    = df[value_cols].mean(axis=1)

# 4. 1) 상관분석: syndrome_score vs hi_score
clean_hi = df[['syndrome_score', 'hi_score']].dropna()
r_hi, p_hi = pearsonr(clean_hi['syndrome_score'], clean_hi['hi_score'])
print(f"Pearson | 증후군 강도 vs 행복·만족도 → r = {r_hi:.3f}, p = {p_hi:.3f}")

rho_hi, p_s_hi = spearmanr(clean_hi['syndrome_score'], clean_hi['hi_score'])
print(f"Spearman | 증후군 강도 vs 행복·만족도 → p = {rho_hi:.3f}, p = {p_s_hi:.3f}")

print()

# 5. 2) 상관분석: syndrome_score vs value_score
clean_val = df[['syndrome_score', 'value_score']].dropna()
r_val, p_val = pearsonr(clean_val['syndrome_score'], clean_val['value_score'])
print(f"Pearson | 증후군 강도 vs 가치관 점수 → r = {r_val:.3f}, p = {p_val:.3f}")

rho_val, p_s_val = spearmanr(clean_val['syndrome_score'], clean_val['value_score'])
print(f"Spearman | 증후군 강도 vs 가치관 점수 → p = {rho_val:.3f}, p = {p_s_val:.3f}")

# 6. 3-1) 스스로 생각하는 성적대별 syndrome_score 분석
self_col   = '스스로 생각하는 성적 수준 (상, 중, 하)'
groups_self = [grp.dropna() for _, grp in df.groupby(self_col)['syndrome_score']]

print("\n=== 스스로 생각하는 성적대별 황금티켓 증후군 강도 요약 ===")
print(df.groupby(self_col)['syndrome_score'].describe())

f_s, p_s = f_oneway(*groups_self)
print(f"ANOVA (스스로 성적) → F = {f_s:.3f}, p = {p_s:.3f}")

# 7. 3-2) 실제 성적대별 syndrome_score 분석
actual_col = '본인의 실제 성적 수준 (내신과 모의고사의 평균 성적중 더 높은 쪽으로 선택)'
groups_act = [grp.dropna() for _, grp in df.groupby(actual_col)['syndrome_score']]

print("\n=== 실제 성적대별 황금티켓 증후군 강도 요약 ===")
print(df.groupby(actual_col)['syndrome_score'].describe())

f_a, p_a = f_oneway(*groups_act)
print(f"ANOVA (실제 성적) → F = {f_a:.3f}, p = {p_a:.3f}")
