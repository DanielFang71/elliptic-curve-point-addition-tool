from collections import namedtuple
from tabulate import tabulate

Point = namedtuple("Point", "x y")

# The point at infinity (identity element in group).
identity = 'Point(x=inf, y=inf)'
# Choose a particular curve and prime.  We assume that p > 3.
# elliptic curve y^2 = x^3 + ax + b
p = 5
a = 1
b = 1


def valid(P):
    """
    Determine whether we have a valid representation of a point
    on our curve.  We assume that the x and y coordinates
    are always reduced modulo p, so that we can compare
    two points for equality with a simple ==.
    """
    if P == identity:
        return True
    else:
        return (
                (P.y ** 2 - (P.x ** 3 + a * P.x + b)) % p == 0 and
                0 <= P.x < p and 0 <= P.y < p)


def inv_mod_p(x):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p - 2, p)


def ec_inv(P):
    """
    Inverse of the point P on the elliptic curve y^2 = x^3 + ax + b.
    """
    if P == identity:
        return P
    return Point(P.x, (-P.y) % p)


def ec_add(P, Q):
    """
    Sum of the points P and Q on the elliptic curve y^2 = x^3 + ax + b.
    """
    if not (valid(P) and valid(Q)):
        raise ValueError("Invalid inputs")

    # Deal with the special cases where either P, Q, or P + Q is
    # the origin.
    if P == identity:
        result = Q
    elif Q == identity:
        result = P
    elif Q == ec_inv(P):
        result = identity
    else:
        # Cases not involving the origin.
        if P == Q:
            dydx = (3 * P.x ** 2 + a) * inv_mod_p(2 * P.y)
        else:
            dydx = (Q.y - P.y) * inv_mod_p(Q.x - P.x)
        x = (dydx ** 2 - P.x - Q.x) % p
        y = (dydx * (P.x - x) - P.y) % p
        result = Point(x, y)

    # The above computations *should* have given us another point
    # on the curve.
    assert valid(result)
    return result


def compute_n_P(P, n):
    Q = P
    temp = 0
    for i in range(n - 1):
        temp = ec_add(P, Q)
        P = temp
    return "compute" + str(n) + "P=", temp


def compute_all_valid_points():
    # print(identity)
    res = []
    for x in range(p):
        for y in range(p):
            if valid(Point(x, y)):
                # print((x, y))
                res.append(Point(x, y))
    return res


# Question 2 (a) Part 1 Prove: P + Q = W belongs to E(Z5)
res = compute_all_valid_points()
res.append(identity)
table = []
table.append(["Addition Table"] + res)
for i1 in res:
    temp = [i1]
    for i2 in res:
        count = ec_add(i1, i2)
        temp.append(count)
        # print("Add", i1, i2, "=",count)
    table.append(temp)
print(tabulate(table, tablefmt='fancy_grid'))

# Question 2 (a) Part 2 Prove: P + e = e + P = P
res = compute_all_valid_points()
res.append(identity)
table = []
table.append(["Addition Table"] + res)
temp = ["p+e"]
for i1 in res:
    count = ec_add(i1, identity)
    temp.append(count)
table.append(temp)
temp = ["e+p"]
for i1 in res:
    count = ec_add(identity, i1)
    temp.append(count)
table.append(temp)
print(tabulate(table, tablefmt='fancy_grid'))

# Question 2 (a) Part 3 Prove: P + Q + R = P + (Q + R)
res = compute_all_valid_points()
res.append(identity)
for i1 in res:
    for i2 in res:
        for i3 in res:
            count_1 = ec_add(ec_add(i1, i2), i3)
            count_2 = ec_add(i1, ec_add(i2, i3))
            assert count_1 == count_1
            if count_1 != count_2:
                print("Unequal!!!")

# Question 2 (b) Compute N*P for all P in E(Z5) until adding to identity element.
res = compute_all_valid_points()
for item in res:
    print("Computation for point", item)
    i = 2
    count = compute_n_P(item, i)
    print(count)
    while count[1] != identity:
        i += 1
        count = compute_n_P(item, i)
        print(count)
    print("i=", i, item, compute_n_P(item, i))
    print()

# Question 7
# Steps for find order of Point P(2,3)
m = 7
P = Point(2, 3)
res = []
for k in range(-7, 8):
    for j in range(0, 8):
        n1 = 558 + 2 * k * m + j
        n2 = 558 + 2 * k * m - j
        if compute_n_P(P, n1)[1] == identity:
            res.append(["n1", n1, k, j])
        if compute_n_P(P, n2)[1] == identity:
            res.append(["n2", n2, k, j])
print(res)

print(compute_n_P(P, 567 // 3))
print(compute_n_P(P, 567 // 7))

print(compute_n_P(P, 189 // 3))
print(compute_n_P(P, 189 // 7))
