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
> 이 그림에서의 **Decision Tree**는 가장 쉬운 `예-아니오` 이진 분류 형태이고, 최종 결과(목적지)를 **Label** 이라고 부른다.
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
> 보통 방대한 데이터가 주어졌을 때, **Decision Tree**는 수많은 **Record** 에 대해 Decision을 하는 Tree 진행 알고리즘을 수행한다. 이를 **Decision Tree** *split* 이라 부르고, 이것이 어떻게 구성되느냐에 따라 **Decision Tree**의 성능이 결정된다. 
>
> 여기서 성능이라는 것은, 기존의 방대한 데이터에 포함되지 않은, 새로운 *feature* value 의 **Record** 가 모델에 주어졌을 때, 지도 학습을 바탕으로 습득한 데이터의 패턴에 따라 **Label** 을 얼마나 잘 예측하느냐의 척도이다.
>
> ### 일반화 개요
> 모델의 성능을 향상시키려면, 즉 새로운 데이터에도 강한 예측력을 보여주는 모델을 만들기 위해선 데이터 학습 단계에서 모델이 데이터의 특징을 일반화할 수 있게 잘 조정해야 한다. 데이터의 특징을 일반화하지 못하고 패턴을 학습한다면 **Overfitting** 또는 **Underfitting** 이라는 문제가 발생한다.
>
> > #### Overfitting
> 학습에 사용된 데이터에 한해서만 **Label** 예측이 정확한, 데이터의 모든 특징을 너무 과도하게 학습하여 발생하는 문제이다. 또한 과도한 학습이 이루어지지 않았더라도 데이터의 양이 너무 적으면 발생하기도 한다.
>
> > #### Underfitting
> 학습에 사용된 데이터의 **Label** 도 제대로 예측하지 못하는, 데이터의 특징을 너무 대충, 적게 학습하여 발생하는 문제이다.
>
> > #### Overfitting & Underfitting 검증 방법
> ![image](https://github.com/CharmStrange/Playground/assets/105769152/7e2c893b-881b-42f4-afea-d5620a6e5116)
>
> **Train Error** & **Test Error** 라는 모델의 정확성 척도를 각각 계산하고, 이 둘의 차이를 비교해, 그 차이가 작은 지점이 일반화가 잘 된 현재로서 최적 상태인 모델이다. 만약 이 차이가 크게 벌어지면 **Overfitting** 이 발생한 것으로 판단한다.
>
> > #### 일반화를 잘 시키는 방법
> - 방대한 양의 데이터를 준비한다.
> - 지도 학습 모델을 너무 복잡하게 구성하지 않는다.
> - 모델 학습 시 데이터의 독립성을 가정하여 데이터를 여러 블록으로 쪼개 따로 학습한다.
> - 모델 학습 시 데이터의 독립성을 가정하여 무작위로 복원추출하는 과정을 사용한다.