# Star Trader by Dave Kaufman, 1974
# Python version by Peter Sovietov, 2017
# Korean Translation version by CharmStrange, 2024

from __future__ import division
import sys
import math
from random import random as rnd

def say(text):
  sys.stdout.write(str(text))
  sys.stdout.flush()

def get_text():
  while True:
    s = sys.stdin.readline().upper().strip()
    if s != "":
      return s

def get_int():
  try:
    return int(get_text())
  except ValueError:
    return None

def ask(text, checked):
  while True:
    say(text)
    n = get_int()
    if n != None and checked(n):
      return n

in_range = lambda lo, hi: lambda n: lo <= n <= hi

def sgn(x):
  if x < 0:
    return -1
  elif x > 0:
    return 1
  else:
    return 0

rint = lambda x: int(round(x))

INTRO = """
현재는 2070년 1월 1일, 인류는 70년 간 성간 비행을 진행중입니다. 우주 곳곳에는 식민지화된 여러 행성이 있고, 그들 중 일부는 강력한 문명이 존속중이며 다른 일부는 굉장히 오래되어 황폐하거나, 또는 굉장히 발전된 상태입니다.

여러분께선 성간 무역 우주선의 선장입니다. 여러분은 여러 상품과 자원을 사고 팔며 우주 곳곳을 누비게 됩니다. 만약 여러분이 엄청난 기회를 잡아 훌륭한 거래를 성사시킨다면 상상 그 이상의 부를 누릴 겁니다.

시간이 지날수록, 항성계는 천천히 변화할 것이고, 항성계의 무역 상황, 공급과 수요의 흐름 또한 변화할 것입니다. 예를 들어, 어떤 항성계의 우라늄과 강철 원자재 등 자원이 고갈되어 그들 값어치가 높게 상승한다든지, 새로운 기술이 개발되어 어떤 상품의 수요가 증가할 수도 있겠죠. 

여러분의 선박은 일주일에 약 2광년을 여행할 수 있으며 최대 %s톤의 화물을 운반할 수 있습니다. 또한 항성계의 여러 곳엔 은행이 존재하는데, 은행은 I 등급 및 II 등급 항성계에만 존재합니다. 은행 시스템의 이자율은 5%% 이며, 한 행성에 예금한 모든 돈은 은행이 존재하는 다른 행성에서 사용할 수 있게 됩니다.
"""

REPORT = """
항성 등급:
     I  거점 문명 항성
    II  일반 항성
   III  미개발 항성
    IV  외딴 항성

상품 타입:
    UR  우라늄
   MET  강철
    HE  중장비
   MED  의약품
  SOFT  소프트웨어
  GEMS  성광 보석

화물 우주선은 최대 %s 톤의 화물을 운반할 수 있습니다.
성광 보석과 소프트웨어는, 톤 단위로 거래할 수 없습니다.
"""

ADVICE = """
\n모든 우주선은 소르에서 출발합니다.

팁 :  III 등급, IV 등급의 항성을 방문하세요.
소르와 II 등급의 항성은 더 낮은 등급의 항성들을 위한 
많은 양의 중장비와 의약품, 그리고 소프트웨어를 생산합니다.   
또한, 낮은 등급의 항성에선 우라늄, 강철, 성광 보석 등의 
원자재를 생산합니다. 원자재는 거래와 무역을 위해 소르를 
비롯한 다른 II 등급의 항성으로 운반할 수 있습니다.
또한, 항성계의 구조와 여러 자원, 상품의 시세를 항상 잘 알아두세요. 
I 등급과 II 등급의 항성은 더 높은 등급의 항성과 훌륭한 거래 
관계를 만들 수 있습니다.
"""

COSMOPOLITAN = 15
DEVELOPED = 10
UNDERDEVELOPED = 5
FRONTIER = 0

STAR_NAMES = [
  "소르", "요르크", "보옛", "아이반", "리프", "후크", "스탄", "터스크", "싱크",
  "샌드", "퀸", "갤", "퀴르크", "크라이스", "파테"
]

MONTHS = [
  "1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월",
  "11월", "12월"
]

GOODS_NAMES = ["<우라늄>", "<강철>", "<중장비>", "<의약품>", "<소프트웨어>", "<성광 보석>"]
GOODS_TITLE = "%5s %5s %5s %5s %5s %5s" % tuple(GOODS_NAMES)

PRICES = [5000, 3500, 4000, 4500, 3000, 3000]

# *** DATA FOR ECONOMETRIC MODEL FOLLOWS ***
# [k, b], y = k * x + b

ECONOMIC = [
  [[-0.1, 1], [-0.2, 1.5], [-0.1, 0.5]],
  [[0, 0.75], [-0.1, 0.75], [-0.1, 0.75]],
  [[0, -0.75], [0.1, -0.75], [0.1, -0.75]],
  [[-0.1, -0.5], [0.1, -1.5], [0, 0.5]],
  [[0.1, -1], [0.2, -1.5], [0.1, -0.5]],
  [[0.1, 0.5], [-0.1, 1.5], [0, -0.5]]
]

class Record:
  def __init__(self, **kwargs):
    for kw in kwargs:
      setattr(self, kw, kwargs[kw])

def make_game():
  return Record(
    ship_speed = 2 / 7,
    max_distance = 15, # between stars
    ship_delay = 0.1,
    number_of_rounds = 3, # bidding rounds
    max_weight = 30, # ship weight
    margin = 36,
    level_inc = 1.25, # star level increment
    day = 1,
    year = 2070,
    end_year = 5,
    number_of_players = 2,
    half = 1,
    ship = None,
    ships = [],
    stars = [],
    accounts = []
  )

def make_ship(g):
  return Record(
    goods = [0, 0, 15, 10, 10, 0],
    weight = 25,
    day = g.day,
    year = g.year,
    sum = 5000,
    star = None,
    status = 0,
    player_index = 0,
    name = ""
  )

def make_star(g):
  return Record(
    goods = [0, 0, 0, 0, 0, 0],
    prices = [0, 0, 0, 0, 0, 0],
    prods = [0, 0, 0, 0, 0, 0], # star's productivity/month
    x = 0,
    y = 0,
    level = COSMOPOLITAN,
    day = 270,
    year = g.year - 1,
    name = STAR_NAMES[0]
  )

def make_account(g):
  return Record(
    sum = 0,
    day = g.day,
    year = g.year
  )

def make_objects(g, obj, n):
  return [obj(g) for i in range(n)]

def own_game(g):
  g.number_of_players = ask("플레이어 수(2, 3, 4, ..., 12 까지) : ",
    in_range(2, 12))
  n = ask("플레이어 당 소유할 화물 우주선의 수 (최대 12척) : ",
    lambda n: n > 0 and n * g.number_of_players <= 12)
  g.ships = make_objects(g, make_ship, n * g.number_of_players)
  number_of_stars = ask("총 항성의 수 (4, 5, 6, ...,  13 까지) : ",
    in_range(4, 13))
  g.stars = make_objects(g, make_star, number_of_stars)
  length = ask("게임 진행 기간(년) : ", lambda n: n > 0)
  g.end_year = g.year + length
  g.max_weight = ask("최대 화물 적재량(기본 30) : ",
    lambda n: n >= 25)
  say("항성 간 최소 거리")
  g.max_distance = ask("(최소 10, 최대 25, 기본 15) : ",
    in_range(10, 25))
  g.number_of_rounds = ask("입찰 또는 제안 수(기본 3) : ",
    lambda n: n > 0)
  say("이윤 폭(1 ~ 5)...")
  g.margin = ask(": ", in_range(1, 5)) * 18

def distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# *** <TEST STAR CO-ORDS>
# FIRST CONVERT CO-ORDS TO NEXT HALF-BOARD
# SECOND, TEST PROXIMITY
# FINALLY, ENTER CO-ORDS AND INCREMENT HALF-BOARD CTR

def good_coords(g, index, x, y):
  if g.half == 2:
    x, y, = y, x
  elif g.half == 3:
    y = -y
  elif g.half == 4:
    x, y = -y, x
  g.half += 1
  if g.half > 4:
    g.half = 1
  for i in range(index):
    if distance(x, y, g.stars[i].x, g.stars[i].y) < g.max_distance:
      return False
  g.stars[index].x = rint(x)
  g.stars[index].y = rint(y)
  return True

def generate_coords(g, index, bounds):
  while True:
    x = (rnd() - 0.5) * bounds
    y = rnd() * bounds / 2
    if good_coords(g, index, x, y):
      return

def add_star(g, index, level):
  if level == FRONTIER:
    while True:
      x = (rnd() - 0.5) * 100
      y = 50 * rnd()
      if abs(x) >= 25 or y >= 25:
        if good_coords(g, index, x, y):
          break
  elif level == UNDERDEVELOPED:
    generate_coords(g, index, 100)
  elif level == DEVELOPED:
    generate_coords(g, index, 50)
  g.stars[index].level = level

def name_star(g, index):
  while True:
    name = STAR_NAMES[1 + rint(13 * rnd())]
    found = False
    for i in range(1, len(g.stars)):
      if name == g.stars[i].name:
        found = True
        break
    if not found:
      break
  g.stars[index].name = name

def make_stars(g):
  g.half = 1
  add_star(g, 1, FRONTIER)
  add_star(g, 2, FRONTIER)
  add_star(g, 3, UNDERDEVELOPED)
  for i in range(4, len(g.stars)):
    level = i % 3 * 5
    add_star(g, i, level)
  for i in range(1, len(g.stars)):
    name_star(g, i)

def name_ships(g):
  ship_index = 0
  say("\n선장님, 화물 우주선의 이름을 지어주실 차례입니다!\n")
  for i in range(len(g.ships) // g.number_of_players):
    for p in range(g.number_of_players):
      say("  이름을 정해주십시오(플레이어 %s) : " % (
        i + 1))
      g.ships[ship_index].name = get_text()
      g.ships[ship_index].player_index = p
      ship_index += 1
    say("\n")

def finish_setup(g):
  make_stars(g)
  name_ships(g)
  g.accounts = make_objects(g, make_account, g.number_of_players)

def setup(g):
  say("Star Traders 배경 알아보기 ('Y' 또는 'N' 입력) : ")
  if get_text() == "Y":
    say("%s\n" % (INTRO % g.max_weight))
  say("전에 플레이해 본 적이 있나요? ('Y' 또는 'N' 입력) :  ")
  if get_text() == "Y":
    say("커스텀 설정으로 게임을 플레이하실 겁니까? ('Y' 또는 'N' 입력) : ")
    if get_text() == "Y":
      own_game(g)
      finish_setup(g)
      return
  g.number_of_players = ask("총 플레이어 수 (2 ~ 4) : ",
    in_range(2, 4))
  g.ships = make_objects(g, make_ship, 2 * g.number_of_players)
  g.stars = make_objects(g, make_star, 3 * g.number_of_players + 1)
  g.end_year = g.year + 5
  finish_setup(g)

def star_map(g):
  say("                    항성계 구조\n")
  say("                   *************\n")
  for y in range(15, -16, -1):
    line = list("                         1                             ")
    if y == 0:
      line = list("1----1----1----1----1----*소르-1----1----1----1----1    ")
    elif y % 3 == 0:
      line[25] = "-"
    y_hi = y * 10 / 3
    y_lo = (y + 1) * 10 / 3
    for s in range(1, len(g.stars)):
      if g.stars[s].y < y_lo and g.stars[s].y >= y_hi:
        x = rint(25 + g.stars[s].x / 2)
        name = g.stars[s].name
        line[x:x + len(name) + 1] = "*" + name
    say("%s\n" % "".join(line))
  say("\n보이는 이 지도는 가로 세로 100광년이며,\n")
  say("'-' 표시는 10광년을 의미합니다. (지도 상 '1' 또는 '-' 비틀림은 \n항성 배치의 무작위성으로 인해 발생되는 현상이니 \n무시하셔도 됩니다.)\n\n")

def ga():
  say("\n                *** 상태 정보 보고 ***\n\n")

# M AND C DETERMINE A STAR'S PRODUCTIVITY/MONTH
#   PROD/MO. = S(7,J) * M(I,R1)  +  C(I,R1)
#   WHERE J IS THE STAR ID #,I THE MERCHANDISE #,
#   AND R1 IS THE DEVELOPMENT CLASS OF THE STAR

def update_prices(g, star):
  level = 0
  if star.level >= UNDERDEVELOPED:
    level += 1
  if star.level >= DEVELOPED:
    level += 1
  months = 12 * (g.year - star.year) + (g.day - star.day) / 30
  goods, prods, prices = star.goods, star.prods, star.prices
  for i in range(6):
    k, b = ECONOMIC[i][level]
    prods[i] = k * star.level + b
    prods[i] *= 1 + star.level / 15
    if abs(prods[i]) > 0.01:
      goods[i] = sgn(prods[i]) * min(abs(prods[i] * 12),
        abs(goods[i] + months * prods[i]))
      prices[i] = PRICES[i] * (1 - sgn(goods[i]) * abs(
        goods[i] / (prods[i] * g.margin)))
      prices[i] = 100 * rint(prices[i] / 100 + 0.5)
    else:
      prices[i] = 0
  star.day = g.day
  star.year = g.year

def text_level(g, star):
  level = int(star.level / 5)
  if level == 0:
    return "IV"
  elif level == 1:
    return "III"
  elif level == 2:
    return "II"
  else:
    return "I"

def update_account(g, account):
  account.sum = account.sum * (1 + 0.05 * (
    g.year - account.year + (g.day - account.day) / 360))
  account.day = g.day
  account.year = g.year

def price_col(n):
  return "+" + str(n) if n > 0 else str(n)

def report(g):
  ga()
  say("1월 1일, %d%s 연간 보고 # %d\n" % (
    g.year, " " * 35, g.year - 2069))
  if g.year <= 2070:
    say("%s\n" % (REPORT % g.max_weight))
  say("%s[ 시세 표] \n... 여러 문자열의 길이 변동과 CLI의 한계로 표가 지저분할 수 있음!\n\n" % (" " * 20))
  say(" [항성]  [등급]  %s\n" % GOODS_TITLE)
  for i in range(len(g.stars)):
    update_prices(g, g.stars[i])
    prices = g.stars[i].prices
    for j in range(6):
      prices[j] = sgn(g.stars[i].goods[j]) * prices[j]
    say("%4s  %5s      %5s   %5s   %5s   %5s      %5s         %5s\n" % (
      g.stars[i].name,
      text_level(g, g.stars[i]),
      price_col(prices[0]),
      price_col(prices[1]),
      price_col(prices[2]),
      price_col(prices[3]),
      price_col(prices[4]),
      price_col(prices[5])
    ))
    if i % 2 != 0:
      say("\n")
  say("\n('+' 는 공급, '-' 는 수요)\n")
  say("\n%s[ 선장 정보 ]\n\n" % (" " * 22))
  say("[플레이어 번호]  [화물 우주선 잔고]   [은행 잔고]     [적재량]      [총 합]\n")
  for account in g.accounts:
    update_account(g, account)
  for p in range(g.number_of_players):
    say("\n")
    on_ships = 0
    cargoes = 0
    for ship in g.ships:
      if ship.player_index == p:
        on_ships += ship.sum
        for j in range(6):
          cargoes += ship.goods[j] * PRICES[j]
    in_bank = rint(g.accounts[p].sum)
    totals = on_ships + cargoes + in_bank
    say("      %2d           %10d     %10d       %10d    %10d\n" % (
      p + 1, on_ships, in_bank, cargoes, totals
    ))

def get_names(objects):
  return [o.name for o in objects]

def ship_days(g, d):
  g.ship.day += d
  while g.ship.day > 360:
    g.ship.day -= 360
    g.ship.year += 1

def travel(g, from_star):
  d = rint(distance(
    from_star.x, from_star.y, g.ship.star.x, g.ship.star.y) / g.ship_speed)
  if rnd() <= g.ship_delay / 2:
    w = 1 + rint(rnd() * 3)
    if w == 1:
      say("곧 휴일이 다가옵니다!\n")
    elif w == 2:
      say("선원들이 휴가를 원하네요?\n")
    elif w == 3:
      say("선장님! 화물 우주선 점검 결과가 좋지 못하다고 합니다.\n")
    say(" - %d WEEK DELAY.\n" % w)
    d += 7 * w
  ship_days(g, d)
  m = int((g.ship.day - 1) / 30)
  say("THE ETA AT %s IS %s %d, %d\n" % (
    g.ship.star.name, MONTHS[m], g.ship.day - 30 * m, g.ship.year))
  d = rint(rnd() * 3) + 1
  if rnd() <= g.ship_delay / 2:
    d = 0
  ship_days(g, 7 * d)
  g.ship.status = d

def next_eta(g):
  targets = get_names(g.stars)
  while True:
   ans = get_text()
   if ans == "MAP":
     star_map(g)
   elif ans == "REPORT":
     report(g)
   elif ans == g.ship.star.name:
     say("현재 정박중인 항성 말고, 어떤 항성에 가가실 건가요?")
   elif ans in targets:
     from_star = g.ship.star
     g.ship.star = g.stars[get_names(g.stars).index(ans)]
     travel(g, from_star)
     break
   else:
     say("%s 항성계엔 그런 항성이 없습니다만..." % ans)
   say("\n")

def landing(g):
  d, y = g.ships[0].day, g.ships[0].year
  ship_index = 0
  for i in range(1, len(g.ships)):
    if g.ships[i].day > d or g.ships[i].year > y:
      pass
    elif g.ships[i].day == d and rnd() > 0.5:
      pass
    else:
      d, y = g.ships[i].day, g.ships[i].year
      ship_index = i
  g.ship = g.ships[ship_index]
  if g.year < g.ship.year:
    g.day = 1
    g.year = g.ship.year
    report(g)
    if g.year >= g.end_year:
      return False
  g.day = g.ship.day
  m = int((g.day - 1) / 30)
  say("\n%s\n* %s %s, %d\n" % ("*" * 17, MONTHS[m], (g.day - 30 * m), g.year))
  say("* %s HAS LANDED ON %s\n" % (g.ship.name, g.ship.star.name))
  s = g.ship.status + 1
  if s == 2:
    say("1 WEEK LATE - 'OUR COMPUTER MADE A MISTAKE'\n")
  elif s == 3:
    say("2 WEEKS LATE - 'WE GOT LOST.SORRY'\n")
  elif s == 4:
    say("3 WEEKS LATE - PIRATES ATTACKED MIDVOYAGE\n")
  say("\n$ ON BOARD %s   NET WT\n" % GOODS_TITLE)
  say("%10d    %2d    %2d    %2d    %2d    %2d    %2d     %2d\n" % (
    g.ship.sum,
    g.ship.goods[0],
    g.ship.goods[1],
    g.ship.goods[2],
    g.ship.goods[3],
    g.ship.goods[4],
    g.ship.goods[5],
    g.ship.weight
  ))
  return True

def price_window(g, index, units, current_round):
  w = 0.5
  star_units = g.ship.star.goods[index]
  if units < abs(star_units):
    w = units / (2 * abs(star_units))
  return w / (current_round + 1)

def buy_rounds(g, index, units):
  star = g.ship.star
  star_units = rint(star.goods[index])
  if units > 2 * -star_units:
    units = 2 * -star_units
    say("     WE'LL BID ON %d UNITS.\n" % units)
  for r in range(g.number_of_rounds):
    if r != max(g.number_of_rounds - 1, 2):
      say("     WE OFFER ")
    else:
      say("     OUR FINAL OFFER:")
    say(100 * rint(0.009 * star.prices[index] * units + 0.5))
    price = ask(" WHAT DO YOU BID ", in_range(
      star.prices[index] * units / 10,
      star.prices[index] * units * 10
    ))
    if price <= star.prices[index] * units:
      say("     WE'LL BUY!\n")
      g.ship.goods[index] -= units
      if index < 4:
        g.ship.weight -= units
      g.ship.sum += price
      star.goods[index] += units
      return
    elif price > (1 + price_window(g, index, units, r)
      ) * star.prices[index] * units:
      break
    else:
      star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
  say("     WE'LL PASS THIS ONE\n")

def buy(g):
  say("\nWE ARE BUYING:\n")
  for i in range(6):
    star_units = rint(g.ship.star.goods[i])
    if star_units < 0 and g.ship.goods[i] > 0:
      say("     %s WE NEED %d UNITS.\n" % (GOODS_NAMES[i], -star_units))
      while True:
        units = ask("HOW MANY ARE YOU SELLING ", lambda n: n >= 0)
        if units == 0:
          break
        elif units <= g.ship.goods[i]:
          buy_rounds(g, i, units)
          break
        else:
          say("     YOU ONLY HAVE %d" % g.ship.goods[i])
          say(" UNITS IN YOUR HOLD\n     ")

def sold(g, index, units, price):
  say("     SOLD!\n")
  g.ship.goods[index] += units
  if index < 4:
    g.ship.weight += units
  g.ship.star.goods[index] -= units
  g.ship.sum -= price

def sell_rounds(g, index, units):
  star = g.ship.star
  for r in range(g.number_of_rounds):
    if r != max(g.number_of_rounds - 1, 2):
      say("     WE WANT ABOUT ")
    else:
      say("     OUR FINAL OFFER:")
    say(100 * rint(0.011 * star.prices[index] * units + 0.5))
    price = ask(" YOUR OFFER ", in_range(
      star.prices[index] * units / 10,
      star.prices[index] * units * 10
    ))
    if price >= star.prices[index] * units:
      if price <= g.ship.sum:
        sold(g, index, units, price)
        return
      else:
        say("     YOU BID $ %d BUT YOU HAVE ONLY $ %d" % (price, g.ship.sum))
        p = g.ship.player_index
        if star.level >= DEVELOPED and g.ship.sum + g.accounts[p].sum >= price:
          say("     ")
          bank_call(g)
          if price <= g.ship.sum:
            sold(g, index, units, price)
            return
        break
    elif price < (1 - price_window(g, index, units, r)
      ) * star.prices[index] * units:
      break
    star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
  say("     THAT'S TOO LOW\n")

def sell(g):
  say("\nWE ARE SELLING:\n")
  for i in range(6):
    star_units = rint(g.ship.star.goods[i])
    if g.ship.star.prods[i] <= 0 or g.ship.star.goods[i] < 1:
      pass
    elif i <= 3 and g.ship.weight >= g.max_weight:
      pass
    else:
      say("     %s UP TO %d UNITS." % (GOODS_NAMES[i], star_units))
      while True:
        units = ask("HOW MANY ARE YOU BUYING ", in_range(0, star_units))
        if units == 0:
          break
        elif i > 3 or units + g.ship.weight <= g.max_weight:
          sell_rounds(g, i, units)
          break
        else:
          say("     YOU HAVE %d TONS ABOARD, SO %d" % (g.ship.weight, units))
          say(" TONS PUTS YOU OVER\n")
          say("     THE %d TON LIMIT.\n" % g.max_weight)
          say("     ")

def bank_call(g):
  say("DO YOU WISH TO VISIT THE LOCAL BANK ")
  if get_text() != "Y":
    return
  p = g.ship.player_index
  account = g.accounts[p]
  update_account(g, account)
  say("     YOU HAVE $ %d IN THE BANK\n" % account.sum)
  say("     AND $ %d ON YOUR SHIP\n" % g.ship.sum)
  if account.sum >= 0:
    x = ask("     HOW MUCH DO YOU WISH TO WITHDRAW ",
      in_range(0, account.sum))
    account.sum -= x
    g.ship.sum += x
  x = ask("     HOW MUCH DO YOU WISH TO DEPOSIT ",
    in_range(0, g.ship.sum))
  g.ship.sum -= x
  account.sum += x

def update_class(g, star):
  n = 0
  for i in range(6):
    if star.goods[i] >= 0:
      pass
    elif star.goods[i] < star.prods[i]:
      return False
    else:
      n += 1
  if n > 1:
    return False
  star.level += g.level_inc
  if star.level in (UNDERDEVELOPED, DEVELOPED, COSMOPOLITAN):
    ga()
    say("STAR SYSTEM %s IS NOW A CLASS %s SYSTEM\n" % (
      star.name, text_level(g, star)))
  return True

def new_star(g):
  if len(g.stars) == 15:
    return
  n = 0
  for star in g.stars:
    n += star.level
  if n / len(g.stars) < 10:
    return
  g.stars.append(make_star(g))
  add_star(g, len(g.stars) - 1, FRONTIER)
  name_star(g, len(g.stars) - 1)
  g.stars[-1].day = g.day
  g.stars[-1].year = g.year
  ga()
  say("A NEW STAR SYSTEM HAS BEEN DISCOVERED!  IT IS A CLASS IV\n")
  say("AND ITS NAME IS %s\n\n" % g.stars[-1].name)
  star_map(g)

def start(g):
  star_map(g)
  report(g)
  say(ADVICE)
  for ship in g.ships:
    say("\nPLAYER %d, WHICH STAR WILL %s TRAVEL TO " % (
      ship.player_index + 1, ship.name))
    g.ship = ship
    g.ship.star = g.stars[0]
    next_eta(g)
  while landing(g):
    star = g.ship.star
    account = g.accounts[g.ship.player_index]
    update_prices(g, star)
    buy(g)
    sell(g)
    if star.level >= DEVELOPED and g.ship.sum + account.sum != 0:
      bank_call(g)
    say("\nWHAT IS YOUR NEXT PORT OF CALL ")
    next_eta(g)
    if update_class(g, star):
      new_star(g)
  ga()
  say("GAME OVER\n")

def main():
  g = make_game()
  setup(g)
  start(g)

main()
