from math import sqrt


class Asteroid:
    """"""

    def __init__(self, location_x, speed_x, location_y, speed_y, size):
        """
        this function initiates an asteroid object
        :param location_x: x coordinate of location (int)
        :param speed_x: asteroid speed in horizontal axis (int)
        :param location_y: y coordinate of location (int)
        :param speed_y: asteroid speed in vertical axis (int)
        :param size: the size of the asteroid (int)
        """
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__size = size

    def get_x_y_location(self):
        """

        :return: x coordinate of location (int) ,  y coordinate of location (int)
        """
        return self.__location_x, self.__location_y

    def get_x_y_speed(self):
        """

        :return: asteroid speed in horizontal axis (int), asteroid speed in vertical axis (int)
        """
        return self.__speed_x, self.__speed_y

    def set_asteroid_speed(self, new_x_speed, new_y_speed):
        """

        :param new_x_speed: updated speed horizontal
        :param new_y_speed: updated speed vertical
        :return: None
        """
        self.__speed_x = new_x_speed
        self.__speed_y = new_y_speed

    def set_x_y_location(self, location_x, location_y):
        """

        :param location_x: new x coordinate of location (int)
        :param location_y: new y coordinate of location (int)
        :return: None
        """
        self.__location_x = location_x
        self.__location_y = location_y

    def get_asteroid_size(self):
        """

        :return: asteroid size
        """
        return self.__size

    def obj_radius(self):
        """

        :return: asteroid's radius
        """
        radius = self.__size * 10 - 5
        return radius

    def calculate_distance_from_asteroid(self, obj_x, obj_y):
        """

        :param obj_x: x coordinate of object location (int)
        :param obj_y: y coordinate of object location (int)
        :return: object's distance from asteroid
        """
        distance = sqrt((obj_x - self.__location_x) ** 2 + ((obj_y - self.__location_y) ** 2))
        return distance

    def has_intersection(self, obj):
        """
        this function checks if an intersection has occurred between an asteroid and another object
        :param obj: an object to check intersection with
        :return: Trie if there is intersection, False otherwise
        """
        obj_x, obj_y = obj.get_x_y_location()
        distance = self.calculate_distance_from_asteroid(obj_x, obj_y)
        asteroid_radius = self.obj_radius()
        obj_radius = obj.obj_radius()
        if distance <= asteroid_radius + obj_radius:
            return True
        else:
            return False
