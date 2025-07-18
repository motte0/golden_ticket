import os
import pandas as pd
import matplotlib.pyplot as plt

# plt.rc('font', family='Malgun Gothic') # 윈도우 폰트
plt.rc('font', family='AppleGothic')  # 맥북 폰트
plt.rc('axes', unicode_minus=False)

# 그래프 저장 폴더 생성
output_dir = './graph'
os.makedirs(output_dir, exist_ok=True)

# 데이터 불러오기
file_path = './황금티켓 증후군 설문조사(응답).xlsx'
df = pd.read_excel(file_path)

# 점수 계산
syndrome_cols  = df.columns[3:7]   # D, E, F, G
happiness_cols = df.columns[7:9]   # H, I
value_cols     = df.columns[9:11]  # J, K

df['syndrome_score'] = df[syndrome_cols].mean(axis=1)
df['hi_score']       = df[happiness_cols].mean(axis=1)
df['value_score']    = df[value_cols].mean(axis=1)

# 성적 열 이름
self_col   = '스스로 생각하는 성적 수준 (상, 중, 하)'
actual_col = '본인의 실제 성적 수준 (내신과 모의고사의 평균 성적중 더 높은 쪽으로 선택)'

# 실제 성적 문자 줄이기
df[actual_col] = df[actual_col].str.split('(').str[0].str.strip()

# 산점도: 증후군 강도 vs 행복·만족도
plt.figure()
plt.scatter(df['syndrome_score'], df['hi_score'])
plt.title('증후군 강도 vs 행복·만족도')
plt.xlabel('황금티켓 증후군 강도')
plt.ylabel('행복·만족도')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '증후군강도_vs_행복만족도.png'))
plt.close()

# 산점도: 증후군 강도 vs 가치관 점수
plt.figure()
plt.scatter(df['syndrome_score'], df['value_score'])
plt.title('증후군 강도 vs 가치관 점수')
plt.xlabel('황금티켓 증후군 강도')
plt.ylabel('가치관 점수')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '증후군강도_vs_가치관점수.png'))
plt.close()

# 박스플롯: 스스로 인식한 성적대별 증후군 강도
plt.figure()
df.boxplot(column='syndrome_score', by=self_col, grid=True)
plt.title('스스로 생각하는 성적대별 증후군 강도')
plt.suptitle('')
plt.xlabel('스스로 생각하는 성적 수준')
plt.ylabel('증후군 강도')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '상상_성적별_증후군강도.png'))
plt.close()

# 박스플롯: 실제 성적대별 증후군 강도
plt.figure()
df.boxplot(column='syndrome_score', by=actual_col, grid=True)
plt.title('실제 성적대별 증후군 강도')
plt.suptitle('')
plt.xlabel('실제 성적 수준')
plt.ylabel('증후군 강도')
# plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '실제_성적별_증후군강도.png'))
plt.close()

print("시각화 파일이 저장되었습니다.")