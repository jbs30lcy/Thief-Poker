import math

def easing(pos0, pos1, func, t, wt):
    x0, y0 = pos0
    x1, y1 = pos1
    k = func(t/wt)
    x = (1-k)*x0 + k*x1
    y = (1-k)*y0 + k*y1

    return (x, y)

def m_linear(x):
    return x

def m_quadin(x):
    return x**2

def m_quadout(x):
    return 2 * x - x**2

def m_quadinout(x):
    if x < 1/2: return 1/2 * m_quadin(2*x)
    else: return 1/2 + 1/2 * m_quadout(2*x - 1)

def m_cubicin(x):
    return x**3

def m_cubicout(x):
    return 3 * x - 3 * x**2 + x**3

def m_cubicinout(x):
    if x < 1/2: return 1/2 * m_cubicin(2*x)
    else: return 1/2 + 1/2 * m_cubicout(2*x - 1)

def m_sinein(x):
    pi = math.pi
    return math.sin(pi/2 * (x-1)) + 1

def m_sineout(x):
    pi = math.pi
    return math.sin(pi/2 * x)

def m_sineinout(x):
    if x < 1/2: return 1/2 * m_sinein(2*x)
    else: return 1/2 + 1/2 * m_sineout(2*x - 1)

def m_backin(x):
    a = 0.78387 # 반동 최대 거리가 0.2가 되도록 계산 => 100a^3 - 27a - 27 = 0의 해
    return x * ( (a+1)*x**2 - a )

def m_backout(x):
    a = 0.78387
    return (x-1) * ((a+1) * (x-1)**2 - a) + 1

def m_backinout(x):
    if x < 1/2: return 1/2 * m_backin(2*x)
    else: return 1/2 + 1/2 * m_backout(2*x - 1)

def m_bounceout(x):
    g = 7 + 3 * math.sqrt(5)
    x += math.sqrt(2/g)
    xmax = math.sqrt(8/g)
    co = 1
    for i in range(10):
        if x < xmax:
            return 1 - co*math.sqrt(2*g)*x + 1/2 * g * x**2
        x -= xmax
        xmax *= math.sqrt(1/5)
        co *= math.sqrt(1/5)
    return 1