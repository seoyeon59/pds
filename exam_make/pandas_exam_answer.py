import pandas as pd

df = pd.read_csv('chipotle.csv')
# print(df)

'''
print('>> data basic')
print(df.size, df.shape, df.columns, sep='\n')

df.size : 23110
df.shape : (4622, 5)
df.columns : 'order_id'(주문 번호), 'quantity'(주문 개수),
             'item_name'(음식 이름), 'choice_description'(선택 옵션), 
             'item_price'(음식 가격)
'''

# df.info() # choice_description 결측치 있음

'''
1. 주문 번호이 각각 주문한 음식 별로 총 금액을 구하시오
'''
# item_price 데이터 타입을 소수로 전환
df['item_price'] = df['item_price'].str.replace(r'$', '').astype(float)

# 금액란 추가하기
df['price'] = df['item_price']*df['quantity']

print('1. 주문 번호이 각각 주문한 음식 별로 총 금액을 구하시오')
print(df)
# print(df['choice_description'])

'''
2. 메뉴당 평균 가격과 주문 개수의 합을 구하시오
조건 : 
평균 가격은 소수점 2자리까지 반환
'''
# 음식 별 가격의 평균 구하기
item_price_mean = df.groupby('item_name')['item_price'].mean().reset_index(name='item_price_mean')
# print(item_price_mean)
# 음식 별 합계 세리기
item_count_sum = df.groupby('item_name')['quantity'].sum().reset_index(name='item_count_sum')
# print(item_count_sum)
# 두 결과를 총합
item = pd.merge(item_price_mean, item_count_sum, on='item_name')

# 각 결과를 소수점 2자리까지 반환
item['item_price_mean'] = item['item_price_mean'].round(2)

print('\n2. 메뉴당 평균 가격과 주문 개수의 합을 구하시오')
print(item)

'''
3. 고객들이 자주 원한느 선택 옵션에 등장한 단어 상위 30개로 워드클라우드를 출력하시오
선택 옵션 결측치는 'etc'로 대체
'''
print('\n3. 고객들이 자주 원한느 선택 옵션에 등장한 단어 상위 30개로 워드클라우드를 출력하시오')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 결측치 처리
df.fillna('etc', inplace=True)

# choice_description 전처리 - [] 제거
df['choice_description'] = df['choice_description'].str.replace(r'[', '')
df['choice_description'] = df['choice_description'].str.replace(r']', '')

# 모든 선택 옵션 텍스트를 , 단위로 나누고 리스트에 단어를 추가
all_word = []
for choice in df['choice_description'] :
    words = choice.split(',') # 리뷰 옵션 텍스트를 , 단위로 분리
    all_word.extend(words)  # 모든 단어를 리스트에 추가

# Counter를 사용하여 각 단어의 빈도 계산
word_counts = Counter(all_word)
# print(word_counts)
top_30_words = word_counts.most_common(30) # 상위 30개 자주 등장하는 단어 추출

# Top 30 단어 및 빈도 출력
print('Top 30 frequent words in choice description : ')
for word, count in top_30_words:
    print(f'{word} : {count}')

# 워드클라유두 생성 및 시각화
# 상위 30개 단어의 빈도수를 사용해 워드클라우드 생성
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_30_words))

# 워드클라우드 이미지 시각화
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear') # 워드클라우드 이미지 표시
plt.axis('off') # 축을 숨김
plt.show()
