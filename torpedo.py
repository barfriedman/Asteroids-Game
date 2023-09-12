TORPEDO_RADIUS = 4


class Torpedo:
    """"""

    def __init__(self, location_x, speed_x, location_y, speed_y, direction):
        """
        this function initiates a torpedo object
        :param location_x: x coordinate of location (int)
        :param speed_x: torpedo speed in horizontal axis (int)
        :param location_y: y coordinate of location (int)
        :param speed_y: torpedo speed in vertical axis (int)
        :param direction: movement direction in degrees
        """
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__direction = direction
        self.__born_time = 0
        self.__is_dead = False

    def get_x_y_location(self):
        """

        :return: x coordinate of location (int) ,  y coordinate of location (int)
        """
        return self.__location_x, self.__location_y

    def get_x_y_speed(self):
        """

        :return: torpedo speed in horizontal axis (int), torpedo speed in vertical axis (int)
        """
        return self.__speed_x, self.__speed_y

    def set_x_y_location(self, location_x, location_y):
        """

        :param location_x: new x coordinate of location (int)
        :param location_y: new y coordinate of location (int)
        :return: None
        """
        self.__location_x = location_x
        self.__location_y = location_y

    def obj_radius(self):
        """

        :return: torpedo's radius
        """
        return TORPEDO_RADIUS

    def get_direction(self):
        """

        :return: torpedo's moving direction(in degrees)
        """
        return self.__direction

    def set_born_time(self, born_time):
        """
        :param born_time: time shooting the torpedo(creation) (how many loops in game loop so far)
        :return: None
        """
        self.__born_time = born_time

    def get_born_time(self):
        """

        :return: time shooting the torpedo(creation)
        """
        return self.__born_time

    def get_torpedo_dead(self):
        """

        :return: the "is_dead" flag of the torpedo
        """
        return self.__is_dead

    def set_torpedo_dead(self, is_dead):
        """

        :param is_dead: updated value for torpedo's life- Boolean value
        :return: None
        """
        self.__is_dead = is_dead
