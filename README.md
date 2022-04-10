# Hanwha Financial Network 2022 - Global Internship Program
### Younghun Lee



#### 1. Rank price momentum(Q2_result.csv)
- The score is a strategy that yields the score based on the highest peak in last 252 trading days.
- 전고점 대비 현재 종가의 위치를 나타낸다.
- <img src="https://render.githubusercontent.com/render/math?math={(rank(Close, window=252)-1)/251} #gh-light-mode-only"> <img src="https://render.githubusercontent.com/render/math?math={\color{white}(rank(Close, window=252)-1)/251}, window=252)-1)/251 #gh-dark-mode-only">
- 장점:
  - 전고점을 뚫고 상승하는 경우를 파악하기 쉽다
- 단점:
  - 현재의 상태가 하락인지 상승인지 알기 어렵다.


#### 2. Rank Intraday momentum(Q3_result.csv)
-  Rank based on how much a price rose from open to close compared to its movement toward the day.
- 일간 상승분(Close-Open)을 일간 진폭(High-Low)로 나눈 값을, 1년치의 window에서 순위를 매긴다
- <img src="https://render.githubusercontent.com/render/math?math=(rank(\frac{Close-Open}{High-Low}, window=252)-1)/251 #gh-light-mode-only"> <img src="https://render.githubusercontent.com/render/math?math={\color{white}(rank(\frac{Close-Open}{High-Low}, window=252)-1)/251} #gh-dark-mode-only">
- rank방법은 1과 동일하게 진행하였다
- 장점:
  - 중요한 이벤트에 의해 하락 없이 상승하는 경우를 파악하기 쉽다
- 단점:
  - Mean Reversion의 결과로 하락할 가능성이 존재한다.
  - 일간 상승분이 적고 일간 진폭도 적은 경우, 높은 점수를 얻을 수 있지만, momentum과는 무관하다.
