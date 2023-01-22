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
    return 2*x - x**2

def m_quadinout(x):
    if x < 1/2: return 1/2 * m_quadin(2*x)
    else: return 1/2 + 1/2 * m_quadout(2*x - 1)