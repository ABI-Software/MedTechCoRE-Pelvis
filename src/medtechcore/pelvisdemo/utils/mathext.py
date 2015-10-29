__author__ = 'hsor001'

from math import acos, sqrt, pi

def quaternionToAxisAngle(q):
    x = q[0]
    y = q[1]
    z = q[2]
    w = q[3]
    # print('quaternion: {0}, {1}, {2}, {3}'.format(x, y, z, w))

    angle = 2 * acos(w)
    if angle > pi:
        angle -= pi
    if angle < 0.0:
        angle += pi
    axis = [1.0, 0.0, 0.0]

    s = sqrt(1.0 - w * w)
    if s > 0.001:
        axis[0] = x / s
        axis[1] = y / s
        axis[2] = z / s

    return axis, angle

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

