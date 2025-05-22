import numpy as np

# 직원 데이터
employee_data = np.array([[101,'사원', 28],
                      [102,'사원', 30],
                      [103,'사원', 28],
                      [104,'사원', 30],
                      [105,'대리', 33],
                      [106,'대리', 35],
                      [107,'대리', 35],
                      [108,'팀장', 40],
                      [109,'팀장', 44],
                      [110,'부장', 55]])

# 상반기/하반기 월급 평균
pay_data = np.array([[101, 260, 280],
                      [102, 280, 290],
                      [103, 270, 280],
                      [104, 270, 290],
                      [105, 300, 320],
                      [106, 330, 330],
                      [107, 320, 330],
                      [108, 370, 380],
                      [109, 360, 375],
                      [110, 400, 430]])

## 1. 직원 개인별 평균 월급을 구하시오.
print('1. 직원 개인별 평균 월급을 구하시오.')
for i in range(len(pay_data)) :
    emp_id = pay_data[i,0]  # 사번
    pay_mean = np.mean(pay_data[i,1:])  # 평균 월급
    print(f'사번 {emp_id}의 평균 월급은 {pay_mean} 만 원입니다.')


## 2. 직급별 나이의 평균과 상반기 평균 월급 합계, 하반기 평균 월급 합계를 구하시오.
# 고유한 직급 리스트
unique_ranks = np.unique(employee_data[:,1])
# print(unique_ranks)
print('\n2. 직급별 나이의 평균과 상반기 평균 월급 합계, 하반기 평균 월급 합계를 구하시오.')
print('직급별 나이 평균 및 상/하반기 평균 월급 합계 :')

# 직급별로 계산 하기
for rank in unique_ranks :
    rank_mask = employee_data[:,1] == rank # 해당 직급을 가진 직원만 선택
    rank_ages = employee_data[rank_mask, 2].astype(int) # 나이 데이터 추출
    rank_ids = employee_data[rank_mask, 0].astype(int) # 해당 직급의 사번

    # 급여 데이터 필터링
    pay_mask = np.isin(pay_data[:,0], rank_ids) # 사번이 해당 직급에 포함되는지 확인
    rank_salaries = pay_data[pay_mask, 1:] # 해당 직원들의 상/하반기 급여 데이터

    avg_age = np.mean(rank_ages)    # 나이 평균
    first_half_sum = np.sum(rank_salaries[:,1]) # 상반기 월급 합
    second_half_sum = np.sum(rank_salaries[:,0]) # 하반기 월급 합

    # 결과값 출력
    print(f'{rank} - 평균 나이 : {avg_age:.1f}세, '
          f'상반기 월급 합계 : {first_half_sum},'
          f'하반기 월급 합계 : {second_half_sum} ')
