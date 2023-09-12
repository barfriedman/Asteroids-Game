SHIP_RADIUS = 1


class Ship:
    """"""
    DEFAULT_LIVES = 3

    def __init__(self, location_x, speed_x, location_y, speed_y, heading):
        """

        this function initiates a ship object
        :param location_x: x coordinate of location (int)
        :param speed_x: ship speed in horizontal axis (int)
        :param location_y: y coordinate of location (int)
        :param speed_y: ship speed in vertical axis (int)
        :param heading: ship's heading orientation in degrees
        :param lives: how many lives the ship have
        """
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__heading = heading
        self.__lives = self.DEFAULT_LIVES

    def get_x_y_location(self):
        """

        :return: x coordinate of location (int) ,  y coordinate of location (int)
        """
        return self.__location_x, self.__location_y

    def get_x_y_speed(self):
        """

        :return: ship speed in horizontal axis (int), ship speed in vertical axis (int)
        """
        return self.__speed_x, self.__speed_y

    def set_x_y_speed(self, new_speed_x_y):
        """

        :param new_speed_x_y: updated speed
        :return: None
        """
        self.__speed_x = new_speed_x_y[0]
        self.__speed_y = new_speed_x_y[1]

    def set_x_y_location(self, location_x, location_y):
        """

        :param location_x: new x coordinate of location (int)
        :param location_y: new y coordinate of location (int)
        :return: None
        """
        self.__location_x = location_x
        self.__location_y = location_y

    def get_heading(self):
        """

        :return: ship's heading in degrees (int)
        """
        return self.__heading

    def set_heading(self, new_heading):
        """

        :param new_heading: new ship's heading in degrees (int)
        :return: None
        """
        self.__heading = new_heading

    def obj_radius(self):
        """

        :return: ship's radius
        """
        return SHIP_RADIUS

    def get_lives(self):
        """

        :return: current ship's lives left
        """
        return self.__lives

    def set_lives(self, new_lives):
        """

        :param new_lives: updated ship's lives
        :return: None
        """
        self.__lives = new_lives
