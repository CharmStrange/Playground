-- 삼각형 소속 함수
function triangular_membership(x, a, b, c)
    if x <= a or x >= c then
        return 0
    elseif x > a and x <= b then
        return (x - a) / (b - a)
    elseif x > b and x < c then
        return (c - x) / (c - b)
    end
end

-- "덥다" 소속 함수: a = 20, b = 30, c = 40
local a, b, c = 20, 30, 40

-- 예제 입력 온도
local temperatures = {15, 25, 30, 35, 45}

-- 소속도 계산
for _, temp in ipairs(temperatures) do
    local membership = triangular_membership(temp, a, b, c)
    print(string.format("Temperature: %d°C, Membership: %.2f", temp, membership))
end

-- 간단한 퍼지 제어기
function fuzzy_controller(temperature)
    -- 덥다 소속 함수
    local membership = triangular_membership(temperature, 20, 30, 40)
    -- 에어컨 출력 (0% ~ 100%)
    return membership * 100
end

-- 테스트
local test_temperatures = {25, 30, 35}
for _, temp in ipairs(test_temperatures) do
    local ac_output = fuzzy_controller(temp)
    print(string.format("Temperature: %d°C, AC Output: %.1f%%", temp, ac_output))
end
