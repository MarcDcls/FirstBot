import numpy as np

d = 0.014
D = 0.0052


def direct_kinematics(w_l, w_r):
    """
    Takes as parameters wheel speeds (rad/s) and returns linear (m/s) and angular (rad/s) speeds of the robot

    :param w_l: left wheel speed
    :param w_r: right wheel speed
    :return: (v, w) linear and angular speeds of the robot

    >>> abs(direct_kinematics(0, 2 * np.pi)[1] - np.pi * D / d) < 0.0001
    True
    >>> abs(direct_kinematics(2 * np.pi, 2 * np.pi)[0] - np.pi * D) < 0.0001
    True
    >>> abs(direct_kinematics(-1, 1)[0]) < 0.0001
    True
    >>> abs(direct_kinematics(-1, 1)[1] - D / d) < 0.0001
    True
    >>> abs(direct_kinematics(1, 1)[1]) < 0.0001
    True
    >>> abs(direct_kinematics(0, 1)[0] - 0.0013) < 0.0001
    True
    >>> abs(direct_kinematics(0, 1)[1] - 0.1857142) < 0.0001
    True
    >>> abs(direct_kinematics(1, 0)[0] - 0.0013) < 0.0001
    True
    >>> abs(direct_kinematics(1, 0)[1] + 0.1857142) < 0.0001
    True
    >>> abs(direct_kinematics(0, -1)[0] + 0.0013) < 0.0001
    True
    >>> abs(direct_kinematics(0, -1)[1] + 0.1857142) < 0.0001
    True
    >>> abs(direct_kinematics(-1, 0)[0] + 0.0013) < 0.0001
    True
    >>> abs(direct_kinematics(-1, 0)[1] - 0.1857142) < 0.0001
    True
    """
    # Case of a rotation around the middle of the 2 wheels
    if w_l == - w_r:
        return 0, D * w_r / d

    # Case of a straight line
    if w_l == w_r:
        return D * w_l / 2, 0

    # General Case :
    v_r = D * w_r / 2
    v_l = D * w_l / 2
    v = (v_r + v_l) / 2



    direction_w = 1
    side = 1
    if w_r > 0:
        side = - 1
    if w_l > w_r:
        direction_w = - 1
        side = - side

    w = (v_r - v_l) / d

    # if w_r == 0:
    #     r = r_l - d / 2
    #
    # else:
    #     r_r = v_r
    #     r = r_r + side * d / 2

    return v, w # direction_w * abs(v / r)


def odom(v, w, dt):
    """
    Takes as parameters linear and angular speed of the robot, and returns the position (m) and orientation (rad)
    variation in the robot frame

    :param v: linear velocity of the robot
    :param w: angular speed of the robot
    :param dt: time duration
    :return: (dx, dy, dtheta) the variation of x, y, and theta during dt

    >>> abs(odom(0, np.pi / 2, 1)[0]) < 0.0001
    True
    >>> abs(odom(0, np.pi / 2, 1)[1]) < 0.0001
    True
    >>> abs(odom(0, np.pi / 2, 1)[2] - np.pi / 2) < 0.0001
    True
    """
    # Exceptions
    if w == 0:
        if v == 0:
            return 0, 0, 0  # No motion
        return 0, v * dt, 0  # Case of a straight line

    r = v / w
    dtheta = w * dt
    dx = r * np.cos(dtheta)
    dy = r * np.sin(dtheta)
    return dx, dy, dtheta


def tick_odom(x, y, theta, v, w, dt):
    """
    Takes as parameters the position and orientation of the robot in the world frame, the variation of the robot
    position and orientation in the robot frame, and returns new position and orientation of the robot in the world frame

    :param x: current x coordinate of the robot in the world
    :param y: current y coordinate of the robot in the world
    :param theta: current angle of the robot in the world
    :param v: linear velocity of the robot
    :param w: angular velocity of the robot
    :param dt: time duration
    :return: new x, new y, new theta
    """
    dx, dy, dtheta = odom(v, w, dt)
    return x + dx, y + dy, theta + dtheta


def inverse_kinematics(v, w):
    """
    Takes as parameters the linear and angular target speeds, and computes the speed for left and right wheels

    :param v: linear velocity of the robot
    :param w: angular velocity of the robot
    :return: left wheel speed, right wheel speed

    >>> abs(inverse_kinematics(*direct_kinematics(1, 1))[0] - 1) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(1, 1))[1] - 1) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(0, 0))[0]) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(0, 0))[1]) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(-1, 1))[0] + 1) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(-1, 1))[1] - 1) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(0, 1))[0]) < 0.0001
    True
    >>> abs(inverse_kinematics(*direct_kinematics(0, 1))[1] - 1) < 0.0001
    True
    """
    # Exceptions
    if w == 0:
        if v == 0:
            return 0, 0  # No motion
        return 2 * v / D, 2 * v / D  # Case of a straight line
    if v == 0:
        return - w * d / D, w * d / D  # Case of a rotation around the middle of the 2 wheels

    # General case
    r = v / w
    if w > 0:
        r_l = r - d / 2
        r_r = r + d / 2
    else:
        r_l = r + d / 2
        r_r = r - d / 2
    w_l = 2 * v * r_l / (D * r)
    w_r = 2 * v * r_r / (D * r)
    return w_l, w_r


def go_to(x, y, theta):
    """
    Takes the robot to a given position in the world frame

    :param x: target x coordinate
    :param y: target y coordinate
    :param theta:
    :return: None
    """


################################### TESTS ###################################

if __name__ == "__main__":
    import doctest

    doctest.testmod()
