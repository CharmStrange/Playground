# 딥러닝의 깊이 있는 이해를 위한 머신 러닝
| **@KMOOC**

| **중앙대학교 최종원 교수님**

| **https://lms.kmooc.kr/course/view.php?id=11397**
## W1 : 머신 러닝의 소개 
### *머신 러닝의 핵심은 방대한 데이터 내에서 특징을 자동으로 찾아내는 것!*
> ### 방대한 데이터의 표현 방법
> <**2차원의 행렬**>
> | *feature 1* | *feature 2* | *feature 3* | *feature 4* | *feature 5* |
> |---|---|---|---|---|
> | value | value | value | value | value |
> | value | value | value | value | value |
> | value | value | value | value | value |
> | ... | ... | ... | ... | ... |
>
> **Record** : (행렬에서의 한 행 = **row**)
> | *feature 1* | *feature 2* | *feature 3* | *feature 4* | *feature 5* |
> |---|---|---|---|---|
> | value | value | value | value | value |
>
> **Field** : *feature* 
>
> **Domain** : 중복되지 않는 *feature* value 의 집합

> ### 방대한 데이터의 조작이 필요한 이유
> 일반적으로 *feature* value는 숫자인 것과 숫자가 아닌 것으로 구분, 머신 러닝은 컴퓨터가 데이터 내에서 특징을 찾아가는 방식으로 진행되는데, 컴퓨터는 숫자가 아닌 *feature* value 를 인식하지 못한다. 이것은 큰 문제가 될 수 있고, 또한 *feature* value 가 숫자라고 하더라도, 그 크기가 너무 작거나 너무 크면(*outlier*) 이 역시 문제가 될 수 있다. 마지막으로 있어야 할 *feature* value 가 없는 경우에도 문제가 되기에 방대한 데이터의 조작은 필수적이다.
>
> **조작 없이 사용하면 문제가 될 수 있는 대표적인 데이터의 형태** : 문장 데이터, 음성 데이터, 이미지 데이터, 그래프 데이터, 이상치(*outlier*), *NULL*(*NaN*, *None* 등)

> ### 머신 러닝에 필수적인 수학 개념
> **미적분학**, **선형대수학**, **통계학**, **이산수학**

> ### 머신 러닝의 대분류
> **회귀**, **분류**
> 
## W2 : Decision Tree와 지도 학습
> 일반적인 트리 형태의 그래프 상에서 *feature* value 를 기준으로 특정 조건에 부합하는 노드만을 거쳐 최종 결과에 도달하는 가장 이해하기 쉬운 머신 러닝 기법이다.
> 
> ![image](https://github.com/CharmStrange/Playground/assets/105769152/c467ba40-3eab-4a1c-b91e-591686c23f6b)
>
> 이 그림에서의 Decision Tree는 가장 쉬운 `예-아니오` 이진 분류 형태이고, 최종 결과(목적지)를 **Label** 이라고 부른다.
>
> **Label** 에 대해서 집중적으로 예측을 진행하는 것이 머신 러닝의 **지도 학습** 기법이고, 이 기법은 사용자가 모델에 *fature* value 와 그에 대한 **Label** 을 제공하는 방식으로 진행된다. 그럼 모델은 주어진 **Label** 과 그에 대응하는 *faeture* value 들의 특징을 자동으로 찾아내 학습을 하는 것이다.
> 
> | *feature 1* | *feature 2* | *feature 3* | *feature 4* | **Label** |
> |---|---|---|---|---|
> | value | value | value | value | 1 |
> 
> 일반적으로 하나의 *feature* value 와 **Label** 이 포함된 **Record** 가 모델에 제공된다.
> 

## W3 : 지도 학습의 일반화 성능
> 보통 방대한 데이터가 주어졌을 때, Decision Tree는 수많은 **Record** 에 대해 
