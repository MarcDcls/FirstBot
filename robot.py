from kinematic import *

class Robot:
    theta = - np.pi / 2
    x = 0
    y = 0

    def odom(self, v, w, dt):
        """
        Takes as parameters linear and angular speed of the robot and the elapsed time, and update the position (m)
        and orientation (rad) of the robot frame

        :param v: linear velocity of the robot
        :param w: angular speed of the robot
        :param dt: time duration
        :return: None

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

        distance = v * dt
        self.theta = self.theta + w * dt
        self.x = self.x + distance * np.cos(self.theta)
        self.y = self.y + distance * np.sin(self.theta)
        return

    # def tick_odom(self, x, y, theta, v, w, dt):
    #     """
    #     Takes as parameters the position and orientation of the robot in the world frame, the variation of the robot
    #     position and orientation in the robot frame, and returns new position and orientation of the robot in the world frame
    #
    #     :param x: current x coordinate of the robot in the world
    #     :param y: current y coordinate of the robot in the world
    #     :param theta: current angle of the robot in the world
    #     :param v: linear velocity of the robot
    #     :param w: angular velocity of the robot
    #     :param dt: time duration
    #     :return: new x, new y, new theta
    #     """
    #     dx, dy, dtheta = odom(v, w, dt)
    #     return x + dx, y + dy, theta + dtheta


################################### TESTS ###################################

if __name__ == "__main__":
    import doctest

    doctest.testmod()
