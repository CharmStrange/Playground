## Gradient Descent : 경사 하강법
> 머신 러닝에서는 오차를 측정할 때 사용되는 **목적 함수**의 출력을 최소화하는 최적의 포인트를 찾기 위해 이 방법을 사용한다.
>
> 경사 하강법을 사용하지 않고 위의 그것을 적용해야 한다면 매우 비효율적인 연산 과정을 거쳐야 한다.
>
> > ### Local minimum & Global minimum
> > 경사 하강법 진행 중 최적의 포인트라고 판단되는 곳에서 도출되는 **minimum** 은 **Local** 과 **Global** 한 두 성질로 구분된다.
> >
> > ![image](https://github.com/user-attachments/assets/c7bff917-4b9c-444b-abb7-6f8a12903d23)
> >
> > 성질의 이름으로부터 알 수 있듯 어떤 범위 내에 한정해 **minimum** 을 찾는다고 한다면 그 때 **Local minimum**, 범위가 없이 모든 것들에 한한다면 **Global minimum** 이다.
> 
> ### Minimum 을 찾아가는 경사 하강법의 과정
> 1. 초기 시작 포인트를 임의로 설정한다.
> 2. 초기 시작 포인트에서의 **목적 함수** 미분 값을 계산한다.
> 3. 미분 값을 바탕으로 포인트를 갱신한다.
> 4. 갱신된 포인트에서의 **목적 함수** 미분 값을 또 계산한다.
> 5. 3-4 의 과정을, 미분 값이 $0$에 수렴할 때 까지 반복한다.
>
> ![image](https://github.com/user-attachments/assets/ce1454fd-bad0-41ab-ac90-cfca0384686c)
>
> 경사 하강법은 **목적 함수**가 미분 가능한 형태를 띤다면 항상 적용이 가능하며, 또한 ***convex; convexity*** 성질을 지녔다면 **Local minimum** **==** **Global minimum** 이 항상 성립한다.
>
> > ### 경사 하강법의 응용
> > 기본적인 경사 하강법 자체는 전체 데이터 내에서 최적의 포인트를 찾아내기 위해 노력한다. 그리고 경사 하강법은 여러 파생 형태가 존재한다. 그 형태를 구분하는 기준은 먼저 전체 데이터를 어떻게 만지며 경사 하강법을 진행하느냐이다. 
> > 
> > #### Stochastic Gradient Descent
> > 전체 데이터를 전부 만지지 않고, 일부 데이터만 골라 그것들에 대한 경사 하강법을 진행하고, 결과를 보며 어떤 것이 최적의 포인트일지 판단한다.
> >
> > 일부 데이터들에 대한 **목적 함수**의 미분 값이 $0$에 수렴한다고 하더라도, 경사 하강법을 몇 번 더 진행한다. ... 그래서 기본 경사 하강법보단 많은 연산량이 필요하지만 다루는 데이터 크기 자체가 매우 작기 때문에 속도는 빠른 편이다.
> > 
> > #### Mini-batch Gradient Descent
> > 전체 데이터를 몇 조각으로 쪼개, 그 조각 하나하나에 대한 경사 하강법을 진행하는 방법이다. 쪼갠 조각 하나의 단위를 **Mini-batch** 라고 칭하며 이것을 어떻게 설정해 주느냐에 따라 경사 하강법의 성능이 결정된다.
> >
> > **Mini-bacth Gradient Descent** 는 일반 경사 하강법과 **Stochastic Gradient Descent** 중간에 위치한 방법이다.
> > ![image](https://github.com/user-attachments/assets/e6b4f99c-9c10-4bff-95a1-bb76ebebd0e8)