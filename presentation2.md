## W7 : 머신 러닝 기법 : 회귀
> 분류 모델은 이산적인 `Label` 에 대해 목표를 잡았지만, 회귀 모델은 연속적인 `Label` 에 대해 목표를 잡는다.
>
> ***회귀 문제에선, 원인과 결과의 인과 관계적 사고를 지양해야 한다. `"관계가 존재한다."` --> True or False ... `"~때문에 ~이다."` --> False***
>
> 기본적으로 선형 회귀 모델을 가정하면, $w$ 라는 모델의 파라미터(가중치)가 등장한다. 선형 회귀 모델이 목표한 `Label` 을 잘 맞출 수 있도록 하기 위해선 모델의 파라미터를 최적화시키는 것이 매우 중요하다.
>
> > ### Least Square
> > 예측 값과 실제 값과 차이, 즉 오차를 최소화하는 선형 모델을 찾기 위해 사용되는 것이 **Least Square** 이다.
> >
> > **Least Square** = $(wx_i-y_i)^2$
> >
> > 데이터셋의 모든 *feature* value 는 이 **Least Square** 를 모두 가지고 있으며 선형 모델은 모델 전체의 **Least Square** 를 최소화하는 방향으로 구성되어야 그것이 좋은 선형 회귀 모델이라고 할 수 있는 것이다.
>
> > ### Bias variable
> > 모든 *feature* value 를 선형 회귀 모델에 그대로 사용하게 되면, 그러니까 선형 회귀 모델의 학습에 기존 데이터셋을 그대로 넣어주게 되면 선형 회귀 모델은 무조건 원점을 지나게 된다. 이는 *feature* value 당 하나의 $w$ 를 고려했기 때문이다.
> >
> > ![image](https://github.com/user-attachments/assets/1eb2e46e-8e59-4aca-ae0e-fe7a1975d679)
> >
> > 그래서 선형 회귀 모델에 항 하나(=절편)를 추가해 주어, *feature* value 가 `0` 일때 `Label` 또한 무조건 `0` 이 되는 것을 방지한다.
> >
> > ```
> > X = [ a ]        X = [ a 1 ]
> >     [ b ]   >>>      [ b 1 ]
> >     [ c ]            [ c 1 ]
> > ```
> > 이러면 추가된 `1` 들이 새로운 절편 항 $w$ 를 담당하게 되어 방금의 문제를 해결할 수 있게 된다.
> 
> 선형 회귀 모델의 가장 큰 단점은, 그 형태가 너무 단순해 실제 문제 해결에 사용하기엔 무리가 있다는 점이다. 또한 **Least Square** 는 *Outlier* *feature* value 에 너무 취약하고 학습에 사용될 데이터셋의 크기가 너무 크면 계산 효율이 급격하게 감소하는 단점 등이 존재한다.

## W8 : 회귀 모델을 사용한 분류
> 가장 단순한 회귀를 통한 분류 모델은, 직선 형태의 모델을 두고 그 안에 *threshold* 를 두어 해당 지점을 기준으로 이진 분류를 진행하는 것이다.
> 
> 이진 분류의 `Label` 을 $1$, $-1$ 로 지정한다고 했을 때, 모델의 출력에서 부호를 보고 `Label` 할당이 가능할 것이다. 이 때 *threshold* 는 출력 $= 0$ 인 지점, 즉 $x$ 절편 지점이다. *threshold* 는 *Dicision boundary* 라고 불리기도 한다.
>
> > ### 회귀 모델 분류에서의 Least Square
> > 결론적으로 회귀 모델 분류에서는 **Least Square** 사용이 불가하다.
> >
> > ```
> > (예측 값 : 0.9 , 실제 값 : 1) ... Least Square = 0.01 
> > (예측 값 : -0.9, 실제 값 : 1) ... Least Square = 3.24
> > ...  
> > ```
> > 조금만 값이 틀어져도 오차는 그 값이 매우 커질 수 있기 때문에 **Least Square** 로 최적화를 하지 않는다.
> 
> > ### 0-1 loss function
> > 실제 값과 예측 값의 부호가 서로 같으면 0을 출력하고, 그렇지 않다면 1을 출력하는  새로운 목적 함수이다.
> >
> > $\lVert\hat{y}-y\rVert$
> >
> > ![image](https://github.com/user-attachments/assets/531a1df5-f172-46f9-9993-2115c5298b63)
> >
> > 보통 선형 회귀 모델에서의 파라미터 최적화는 기울기 값이 $0$이 되는 지점을 찾아가는 과정이다. 즉 파라미터에 대해 미분을 했을 때 그 결과가 $0$이 되는 지점을 찾는 것이다. 그런데 **0-1 loss function** 의 그래프를 보면 모든 지점이 상수로 고정되어 있어 파라미터에 대한 미분을 해도 그 값이 0이 나오기 때문에 사실상 파라미터에 대한 최적화 과정이 전부 무의미해진다.
> 
> > ### Max function
> > **0-1 loss function** 에서 발생한 문제, 그러니까 모든 지점에서의 기울기 값이 0인 문제를 해결하기 위해 새롭게 정의한 목적 함수이다.
> > 
> > $\max (0, -(\hat{y}\times y))$
> >
> > 예측 값과 실제 값의 부호가 다르면 $\max (0, +)=+$ 이고,
> > 부호가 다르면 $\max (0, -)=0$ 이라 이렇게 부호가 다른 경우에 한해 파라미터의 최적화가 가능하다.
> >
> > 하지만 **Max function** 또한 실제 값과 예측 값 중 하나라도 0이 나오면 $\max (0, 0)=0$ 이기 때문에 의미있는 추정이었다고 하더라도 그것이 무시가 된다. 이것이 **degenerate solution** 이라는 문제이다.
> 
> > ### Hinge loss function
> > **degenerate solution** 을 해결한, **Max function** 이 개선된 형태의 목적 함수이다.
> >
> > $\max (0, 1-(\hat{y}\times y))$ : *margin* 이라고 하는 1 항 하나가 추가된 별 거 없어보이는 형태이지만, 이 *margin* 을 추가함으로써 **degenerate solution** 문제가 해결된다.
> >
> > **Hinge loss function** 은 **0-1 loss function** 의 *upper bound* : 그 출력이 항상 크거나 같은 포지션이다. **0-1 loss function** 의 출력이 9.8 이면 오차가 발생한 데이터의 개수가 9개라는 것인데, 여기서 **0-1 loss function** 을 **Hinge loss function** 로 그대로 바꿔 넣어도 그 출력은 최소 9.8 이라는 것이다.
> 
> > ### Logistic loss function
> > **0-1 loss function** 의 기본 형태에, `Log - Sum - Exponential` 을 적용해 새로운 형태로 만든 목적 함수이다.
> >
> > $\sum_{i=1}^{n} log(1 + \exp(-(\hat{y}\times y)))$ : 아주 작은 차이를 가진 두 변수에 `Exponential` 을 적용한 결과를 서로 비교해 보면, 그 차이가 매우 커진다. 또한 **Logistic loss function** 의 출력은 모든 지점에서 미분이 가능하기 때문에 목적 함수로서의 가치가 있다.
> >
> > 여기서 발전된 **Sigmoid function** 을 사용해 선형 회귀 모델의 확률적 구분기를 만들 수 있다.

## W9 : 선형 회귀 모델 응용하기
> 이진 분류가 아닌, 다중 클래스로의 분류를 선형 회귀 모델을 통해 수행할 수 있다. 그것의 대표적인 방법 중 **One vs All** : 하나의 클래스와 다른 클래스의 구분을 짓고, 각 클래스 수에 대응하는 만큼의 선형 회귀 모델을 만들어 최종적으로 클래스 간 분류를 진행하는 방법이 있다.
> 
> > $Norm$ : 다중 클래스 분류 시 응용 가능한, 데이터 간 유사도를 측정하는 기법이다.
> > 
> > $L0 \ Norm$ :  *vector* 의 $0$ 이 아닌 *elements* 의 개수 : $0$ 이 아닌 데이터에 집중한다.
> >
> > $L1 \ Norm$ : same as $Taxicab \ Norm$ or $Manhattan \ Norm$ : *vector* 의 *elements* 에 대한 **absolute value** 의 합 : *outlier* 에 강하다.
> >
> > $L2 \ Norm$ : = $\ Euclidean \ Norm$ : $n$ 차원 좌표평면에서의 *vector* 크기를 계산, 어떤 한 지점에서 다른 한 지점까지의 최소 거리를 측정한다.
> >
> > $Infinite \ Norm$ : *outlier* 에 집중하는 $Norm$, 여러 오차 정도 중에 가장 큰 오차 정도에 해당하는 데이터, 즉 *outlier* 에 집중한다.
> >
> > $Frobenius \ Norm$ : 기존 *vector* 에 대한 $Norm$ 연산과 비슷하지만, 연산하는 대상이 *matrix* 인,하나의 *matrix* 내 *vectors* 에 대한 $L2 \ Norm$ 을 계산하고 모두 더한 뒤 $\sqrt{}$ 를 적용해 준 값이다.
>
> **Data augmentation** : 하나의 학습용 데이터를, 특징은 유지한 채 적당히 변환하여 새로운 파생 데이터를 만드는 기술이며, 주로 이미지 데이터에 많이 적용한다.
>

## W10 :선형 회귀 모델의 한계점과 개선 방안
> 선형 회귀 모델은 기본적으로 *outlier* 에 너무나 취약하다. *outlier* 또한 데이터의 일부이니, 선형 회귀 모델은 이 데이터에 모델을 계속 맞추려 할 것이며 이 때문에 오히려 정상적인 범위에 포함된 데이터에 대해선 모델이 잘 맞지 않거나 하는 등의 문제가 발생한다.
>
> > ### Robust Regression
> > **Least Square** 의 경우는 $(예측 값 \- 실제 값)$ 을 제곱한 오차 지표를 사용하기 때문에 그 값이 경우에 따라 매우 커질 가능성이 존재한다. 즉, 줄여야 할 오차 정도가 매우 커진다는 것이다. 
> >
> > 그래서 **Robust Regression** 이라는 방법을 사용한다 : 모델에서 *outlier* 에 대한 비중을 적게 두거나 무시하는 방법, 그리고 오차 정도가 크더라도 줄여야 하는 그것의 크기를 같게 하도록 응용하는 방법이다.
> >
> > 이것의 핵심은 $(예측 값 \- 실제 값)$ 을 제곱하는 것이 아닌 $예측 값 - 실제 값$ 을 그냥 절댓값으로 변환해 결과를 판단하는 것이다.
> 
> > ### Huber loss
> > **Robust Regression** 에서 사용한 절댓값과 **Least Square** 를 함께 사용하는 오차 측정 방식이다. $\epsilon$ 을 기준으로 각 두 방식을 사용하게 된다.
> >
> > $\epsilon$ 은 보통 오차 정도가 낮은 구간에서 **Least Square** 를 사용하도록 설정되고, 오차 정도가 높은 구간에서는 **Robust Regression** 을 사용하도록 설정된다.
> >
> > 이는 모든 구간에서 파라미터의 최적화를 위한 미분을 하기 위해 설정되는 것이다.
>
> > ### Regularization
> > *inlier* 가 많은, 좋은 품질의 데이터라 해도 선형 회귀 모델이 모든 데이터에 대한 깊은 학습을 계속해서 진행한다면 **Overfitting** 이 발생한다. 이를 방지하기 위해 **Regularization** 기법이 사용된다.
> >
> > 여러 **Regularization** 기법이 존재하지만 가장 이해하기 쉬운 **Regularization - Weight Decay** 방법은 오차 정도를 측정하는 수식에 보정 항 하나를 추가해 모델의 파라미터에 영향을 주게 된다.
> > 
> > 보정 항 : $\lambda \times \ Norm \ of \ w$
> >
> > 상수 $\lambda$ 는 그 크기에 따라 모델의 파라미터에 영향을 주게 된다. 이 상수의 값이 크면 모델 파라미터의 크기가 커지는 것을 방지하고, 상수의 값이 작다면 모델 파라미터의 크기가 커지는 것을 그리 많이 방지하지 않는다.
> >
> > 원리는, 하나의 모델 파라미터가 크다는 것은 그것에 해당하는 *feature* value 에 모델이 집중하고 있다는 뜻이기에, 특정 *feature* value 에 대해서만 깊은 학습을 하지 못하도록, 상수 $\lambda$ 를 통해 규제하는 것이다.
> 
> ### RANSAC
> *outlier* 를 무시하고 모델을 만들어 가는 방식이다. *outlier* 의 반대 개념은 *inlier* 인데, 이들 *inlier* 만이 유의미하다고 판단될 때, 이 방법을 사용한다.
>
> > #### 1. 전체 데이터셋 중 일부 데이터만 무작위로 선택한다.
> > #### 2. 선택된 데이터로 초기 상태의 선형 회귀 모델을 구성한다.
> > #### 3. 초기 모델로 기존 데이터셋에 맞추는 과정을 반복해 *inlier*, *outlier* 를 구분한다.
> > #### 4. 가장 많은 *inlier* 를 포함하는 모델을 최종 모델로 선택한다.
> > #### 5. 최종 모델을 전체 데이터셋에 맞춰 본다.

## W11 : 비선형 데이터 다루기
> 비선형 데이터는 선형 회귀 모델로 다룰 수 없다. 선형 회귀 모델을 계속 사용하면서 비선형 데이터를 다루려면 그들을 선형 회귀 모델로 다룰 수 있게 적절히 변형해 줘야 한다. 아니면 선형 회귀 모델을 버리고 곡선 형태의 모델을 사용해야만 한다.
> 
> > ### Convolutions
> > 비선형 데이터의 대표 격인 이미지 데이터를 적절히 변형하는 기술로, 이미지의 각 픽셀의 집합인 복셀을 주로 다루며 변환을 진행한다.
> >
> > **Convolutions** : `Identity filter`, `Translation filiter`, `Local average filter`, `First derivation filter`, `Laplacian filter`, `Gaussian filter`, `Laplacian of Gaussian filter`, `Gabor filter`...
> >  
> > ***Boundary issue*** : 이미지 데이터에 **Convolution** 을 적용할 때 발생할 수 있는 문제로, 픽셀이 없거나 잘린 경우 그 경계에서 발생한다. 
> >
> > ***Boundary issue*** 해결을 위해 `zero padding : 없는 픽셀에 0을 할당`, `replicate : 좌측 끝의 픽셀 값을 할당`, `mirror : 새로운 픽셀 값의 정 반대 값을 할당` 등의 방법을 사용하게 된다.
> 
> > ### Kernel Trick
> > 1차 직선으로 표현 불가능한 특징을 가진 *feature* values 를 1차 직선에 맞게 변환하거나, 다른 곡선 형태의 모델을 사용해 표현하려고 할 때 *feature* value 의 복잡도는 많이 올라가게 된다. 예를 들어 곡선 형태의 모델을 사용하려면 그에 맞는 2차 이상의 *feature* value 를 추가해야 하는데 그들을 추가한다면 그에 대응하는 파라미터 또한 추가되어 추후 머신 러닝에서의 모든 연산 과정이 복잡해진다. **Kernel Trick** 은 선형대수적 수식 정리, 전개, 변환 등을 통해 모델의 결과까지의 과정을 간소화하는 기법이다. 간소화한다고 해서 모델의 결과에 좋지 않은 영향을 주진 않는다.
> >
> > 대표적인 **Kernel Trick** 으로는 `Linear`, `Polynomial`, `Gaussian-RBF` 이 있다.

## W12 : 비지도 학습
>데이터셋의 *feature* value 를 제공함과 동시에 `Label` 을 제공하는 지도 학습과는 다르게, 비지도 학습은 오직 데이터셋의 *feature* value 만을 제공하고 그들의 패턴을 컴퓨터가 직접 학습하게 한다.
> 
> 데이터의 이상치 탐치 시스템, 유사도 기반 평가, 이미지 데이터 특징의 시각화 등에 널리 활용되는 머신 러닝 기법이다.
>
> > ### Clustering
> > 대표적인 비지도 학습 머신 러닝 기법으로, `Label` 이 없는 데이터의 특징만으로, 데이터를 군집화하여 최종적으로 분류하는 가장 이해하기 쉬운 비지도 학습 방법이다.
> >
> > - **parametric clustering** : 군집화 할 그룹의 개수를 미리 정하고 진행한다.
> > - **density-based clustering** : 서로 비슷한 데이터끼리 일단 군집화하고 본다.
> > - **ensemble clustering** : 여러 **clustering** 결과를 합쳐 최종 결과를 낸다.
> > - **hierarchical clustering** : 작은 그룹의 군집화, 조금 큰 그룹의 군집화, 큰 그룹의 군집화, ... 이런 식의 연쇄적 군집화를 진행한다.
>
> > ### K-means Clustering
> > **parametric clustering** 기법 중 대표적인 방법으로, 여기서 $K$ 는 하이퍼 파라미터이며 이 방법은 최소 두 개 이상의 데이터가 존재해야 진행 가능하다.
> >
> > *Initial point* : 초기 상태를 정의하는 매우 중요한 변수로, 데이터 상에서 **index** 를 의미함과 동시에 특정 그룹을 대표하는 값이다.
> >
> > $Norm$ : 데이터의 군집화를 위해 사용되는, 이 문서 상단에서 언급한 알고리즘이며, 이 알고리즘을 통해 그룹의 분류를 수행 가능하다.
> >
> > **K-means Clustering** 은 먼저 데이터셋에서 무작위적으로 데이터를 추출하고, 초기 그룹 상태를 *Initial point* 로 설정 & 구분하게 된다. 이후 초기 상태에서 데이터가 계속해서 유입됨에 따라 *Initial point* 의 값이 갱신된다. 그렇게 되면 몇몇의 데이터는 속한 그룹이 달라지는데, 이러한 재(再)군집화가 더 이상 나타나지 않을 때까지 진행된다.
> 
> > ### K-means ++ Clustering
> > **K-means Clustering** 과 기본 흐름은 유사하지만, *Initial point* 의 변화 방식이 크게 다르다. 확률적으로, 순서대로, 초기 *Initial point* 설정이 이루어지게 되는데 이후엔 서로 다른 그룹을 대표하는 *Initial point* 간 거리가 멀수록 다음 *Initial point* 의 갱신이 각 그룹의 특징을 더욱 잘 반영해 군집화가 될 수 있도록 동작한다. 
