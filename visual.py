import pandas as pd
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

file_path = './황금티켓 증후군 설문조사(응답).xlsx'
df = pd.read_excel(file_path)

# 문항별 점수 계산
syndrome_cols  = df.columns[3:7]   # D, E, F, G
happiness_cols = df.columns[7:9]   # H, I
value_cols     = df.columns[9:11]  # J, K

df['syndrome_score'] = df[syndrome_cols].mean(axis=1)
df['hi_score']       = df[happiness_cols].mean(axis=1)
df['value_score']    = df[value_cols].mean(axis=1)

# 성적 col 정의
self_col   = '스스로 생각하는 성적 수준 (상, 중, 하)'
actual_col = '본인의 실제 성적 수준 (내신과 모의고사의 평균 성적중 더 높은 쪽으로 선택)'

# 1. 산점도: 증후군 강도 vs 행복·만족도
plt.figure()
plt.scatter(df['syndrome_score'], df['hi_score'])
plt.title('증후군 강도 vs 행복·만족도')
plt.xlabel('황금티켓 증후군 강도')
plt.ylabel('행복·만족도')
plt.grid(True)
plt.show()

# 2. 산점도: 증후군 강도 vs 가치관 점수
plt.figure()
plt.scatter(df['syndrome_score'], df['value_score'])
plt.title('증후군 강도 vs 가치관 점수')
plt.xlabel('황금티켓 증후군 강도')
plt.ylabel('가치관 점수')
plt.grid(True)
plt.show()

# 3. 박스플롯: 스스로 인식한 성적대별 증후군 강도
df.boxplot(column='syndrome_score', by=self_col, grid=True)
plt.title('스스로 생각하는 성적대별 증후군 강도')
plt.suptitle('')
plt.xlabel('스스로 생각하는 성적 수준')
plt.ylabel('증후군 강도')
plt.show()

# 4. 박스플롯: 실제 성적대별 증후군 강도
df.boxplot(column='syndrome_score', by=actual_col, grid=True)
plt.title('실제 성적대별 증후군 강도')
plt.suptitle('')
plt.xlabel('실제 성적 수준')
plt.ylabel('증후군 강도')
plt.xticks(rotation=45, ha='right')
plt.show()
