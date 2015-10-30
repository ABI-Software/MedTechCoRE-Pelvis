__author__ = 'hsor001'

from math import acos, sqrt, pi, atan2


def quaternionToAxisAngle(q):
    x = q[0]
    y = q[1]
    z = q[2]
    w = q[3]
    # print('quaternion: {0}, {1}, {2}, {3}'.format(x, y, z, w))

    mag_x = sqrt(x*x + y*y + z*z)
    # angle = 2 * acos(w)
    angle = 2 * atan2(mag_x, w)
    # if angle > pi:
    #     angle -= pi
    # if angle < 0.0:
    #     angle += pi
    axis = [1.0, 0.0, 0.0]

    s = sqrt(1.0 - w * w)
    if s > 0.001:
        axis[0] = x / s
        axis[1] = y / s
        axis[2] = z / s

    return axis, angle


def quaternionMultiply(a, b):
    q = [0.0, 0.0, 0.0, 0.0]

    a1 = a[3]
    a2 = a[0]
    a3 = a[1]
    a4 = a[2]
    b1 = b[3]
    b2 = b[0]
    b3 = b[1]
    b4 = b[2]

    q[0] = a1 * b2 + a2 * b1 + a3 * b4 - a4 * b3
    q[1] = a1 * b3 - a2 * b4 + a3 * b1 + a4 * b2
    q[2] = a1 * b4 + a2 * b3 - a3 * b2 + a4 * b1
    q[3] = a1 * b1 - a2 * b2 - a3 * b3 - a4 * b4

    if q[3] < 0.0:
        q[3] += pi
    elif q[3] > pi:
        q[3] -= pi

    return q


def quaternionToMatrix(q):
    mx = [0.0] * 9
    x = q[0]
    y = q[1]
    z = q[2]
    w = q[3]

    x2 = x + x
    y2 = y + y
    z2 = z + z
    xx = x * x2
    xy = x * y2
    xz = x * z2
    yy = y * y2
    yz = y * z2
    zz = z * z2
    wx = w * x2
    wy = w * y2
    wz = w * z2

    mx[0] = 1 - yy - zz
    mx[1] = xy - wz
    mx[2] = xz + wy

    mx[3] = xy + wz
    mx[4] = 1 - xx - zz
    mx[5] = yz - wx

    mx[6] = xz - wy
    mx[7] = yz + wx
    mx[8] = 1 - xx - yy

    return mx
