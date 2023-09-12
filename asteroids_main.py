from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random
from math import cos, sin, radians, sqrt

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    # Ship parameters
    ORIENT_SHIP_HEAD_LEFT = 7
    ORIENT_SHIP_HEAD_RIGHT = -7
    DEFAULT_SHIP_LIVES = 3

    # Asteroid parameters
    MAX_SPEED = 4
    MIN_SPEED = -4
    DEFAULT_ASTEROID_SIZE = 3

    # Torpedo parameters
    MAX_TORPEDOS = 10
    DEFAULT_TORPEDO_LIFETIME = 200

    # Game messages
    TITLE_CRUSH_ASTEROID_SHIP = "An intersection occurred!"
    MSG_CRUSH__ASTEROID_SHIP = "OOPS! your ship crushed an asteroid"
    MSG_WIN_ASTEROIDS = "WELL DONE! all asteroids are crushed"
    MSG_YOU_LOSE = "OH NO! you ran out of lives"
    MSG_QUIT = "BYE BYE"
    TITLE_GAME_OVER = "game over"

    # Game defaults
    HORIZONTAL_AXIS = "x"
    VERTICAL_AXIS = "y"
    POINTS_DICT = {3: 20, 2: 50, 1: 100}
    DEFAULT_INIT_POINTS = 0

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """
        This initializes the screen passed is the screen controlling the game, the game ship, asteroids and points.
         set different attributes to new Gamerunner objects
        """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount
        self.__ship = Ship(self.initiate_location(self.HORIZONTAL_AXIS), 0, self.initiate_location(self.VERTICAL_AXIS),
                           0, 0)
        self.__asteroids = []
        self.add_asteroids()
        self.__torpedos = []
        self.__points = self.DEFAULT_INIT_POINTS
        self.__count = 0
        self.__ship.set_lives(self.DEFAULT_SHIP_LIVES)

    def initiate_location(self, axis):
        """
        This randomly sets the initiate location of an object according to a specific axis.
        :param axis: X or Y (str)
        :return: random coordinates on the given axis within the screen borders.
        """
        if axis == self.HORIZONTAL_AXIS:
            return random.randint(self.__screen_min_x, self.__screen_max_x)
        if axis == self.VERTICAL_AXIS:
            return random.randint(self.__screen_min_y, self.__screen_max_y)

    def initiate_asteroid_speed(self):
        """
        This randomly sets the initiate location of an asteroid object.
        :return: random coordinates within the screen borders.
        """
        random_speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        while random_speed == 0:
            random_speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        return abs(random_speed)

    def add_asteroids(self):
        """
        This methods creates, register and draw new asteroids according to asteroids amount.
        """
        for i in range(self.__asteroids_amount):
            asteroid = Asteroid(self.initiate_location(self.HORIZONTAL_AXIS),
                                self.initiate_asteroid_speed(),
                                self.initiate_location(self.VERTICAL_AXIS),
                                self.initiate_asteroid_speed(), self.DEFAULT_ASTEROID_SIZE)
            while asteroid.has_intersection(self.__ship):
                asteroid = Asteroid(self.initiate_location(self.HORIZONTAL_AXIS),
                                    self.initiate_asteroid_speed(),
                                    self.initiate_location(self.VERTICAL_AXIS),
                                    self.initiate_asteroid_speed(), self.DEFAULT_ASTEROID_SIZE)
            self.__asteroids.append(asteroid)
            self.__screen.register_asteroid(asteroid, asteroid.get_asteroid_size())

    def calculate_torpedo_speed_direction(self):
        """
        This method calculates the speed of a torpedo object according to the firing ship
        :return: torpedo speed (X,Y coordinates) and heading (int)
        """
        # Parameters
        ship = self.__ship
        ship_heading = ship.get_heading()
        x_speed_ship, y_speed_ship = ship.get_x_y_speed()

        # Calculation
        x_torpedo_speed = x_speed_ship + 2 * cos(radians(ship_heading))
        y_torpedo_speed = y_speed_ship + 2 * sin(radians(ship_heading))
        return x_torpedo_speed, y_torpedo_speed, ship_heading

    def initiate_torpedo(self):
        """
        This crates a new torpedo (according to the firing ship) with defaults attributes
        """
        # Parameters
        ship = self.__ship
        x_cord_torpedo, y_cord_torpedo = ship.get_x_y_location()
        x_torpedo_speed, y_torpedo_speed, torpedo_heading = self.calculate_torpedo_speed_direction()
        # Initialize
        torpedo = Torpedo(x_cord_torpedo, x_torpedo_speed, y_cord_torpedo, y_torpedo_speed, torpedo_heading)
        torpedo.set_born_time(self.__count)  # game_loop
        # Initialize in game
        self.__torpedos.append(torpedo)
        self.__screen.register_torpedo(torpedo)
        self.__screen.draw_torpedo(torpedo, x_cord_torpedo, y_cord_torpedo, torpedo_heading)

    def shoot_torpedo(self):
        """
        This methods check if a torpedo can be fired according to the conditions.
        """
        if self.__screen.is_space_pressed() and len(self.__torpedos) <= self.MAX_TORPEDOS:
            self.initiate_torpedo()

    def run(self):
        """
        This method is a default function which runs the game.
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        This method is a default function which overloop the running of the game.
        """
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def move_object(self, obj):
        """
        This method causes the given object to move throughout the game.
        :param obj: object type (Ship, Asteroid and Torpedo)
        """
        # Parameters
        old_spot = obj.get_x_y_location()
        screen_mini = (self.__screen_min_x, self.__screen_min_y)
        screen_max = (self.__screen_max_x, self.__screen_max_y)
        speed = obj.get_x_y_speed()
        delta = (screen_max[0] - screen_mini[0], screen_max[1] - screen_mini[1])

        # Calculates new spot for i\in {x,y}
        new_spot = []
        for i in range(2):
            new_spot_i = screen_mini[i] + (old_spot[i] + speed[i] - screen_mini[i]) % delta[i]
            new_spot.append(new_spot_i)
        obj.set_x_y_location(new_spot[0], new_spot[1])

    def orient_ship_head(self, orientation, ship):
        """
        this function updating the ship's heading according to given orientation.
        :param orientation: the change in degrees (int)
        :param ship: ship object
        """
        new_heading = ship.get_heading() + orientation
        ship.set_heading(new_heading)

    def change_ship_heading(self):
        """
        This changes the heading of the ship according to the player's movements.
        """
        ship = self.__ship
        if self.__screen.is_left_pressed():
            self.orient_ship_head(self.ORIENT_SHIP_HEAD_LEFT, ship)
        elif self.__screen.is_right_pressed():
            self.orient_ship_head(self.ORIENT_SHIP_HEAD_RIGHT, ship)

    def calculate_ship_acceleration(self):
        """
        This calculates the new speed of the ship.
        :return: new speed (x,y)
        """
        # Parameters
        ship = self.__ship
        heading = ship.get_heading()
        old_speed_x, old_speed_y = ship.get_x_y_speed()
        # Calculation
        new_speed_x = old_speed_x + cos(radians(heading))
        new_speed_y = old_speed_y + sin(radians(heading))
        return new_speed_x, new_speed_y

    def accelerate_ship(self):
        """
        This set the speed of the ship according to the player's movements.
        """
        if self.__screen.is_up_pressed():
            self.__ship.set_x_y_speed(self.calculate_ship_acceleration())

    def crush_asteroid_ship(self):
        """
        If there was a collision between the ship and an asteroid, the function removes the asteroid
        from the game and decreases player's life in the game.
        """
        ship = self.__ship
        lives = ship.get_lives()

        for asteroid in self.__asteroids:
            if asteroid.has_intersection(ship):
                self.__screen.show_message(self.TITLE_CRUSH_ASTEROID_SHIP, self.MSG_CRUSH__ASTEROID_SHIP)
                ship.set_lives(lives - 1)
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroids.remove(asteroid)

    def calculate_new_asteroids_speed(self, torpedo, asteroid):
        """
        This calculates the new speed of a given asteroid.
        :param torpedo: Torpedo object
        :param asteroid: Asteroid object
        :return: Asteroid new speed and location (x,y, x,y)
        """
        # Parameters
        x_torpedo_speed, y_torpedo_speed = torpedo.get_x_y_speed()
        x_old_asteroid_speed, y_old_asteroid_speed = asteroid.get_x_y_speed()
        x_asteroid_location, y_asteroid_location = asteroid.get_x_y_location()

        # Calculations
        partial_calculate = sqrt(x_old_asteroid_speed ** 2 + y_old_asteroid_speed ** 2)
        new_asteroid_speed_x = (x_torpedo_speed + x_old_asteroid_speed) / partial_calculate
        new_asteroid_speed_y = (y_torpedo_speed + y_old_asteroid_speed) / partial_calculate
        return new_asteroid_speed_x, new_asteroid_speed_y, x_asteroid_location, y_asteroid_location

    def split_asteroid(self, torpedo, asteroid):
        """
        This responsible for splitting the asteroid and adding the new asteroids to the game
        (if an asteroid was hit by a torpedo).
        :param torpedo: Torpedo object
        :param asteroid: Asteroid object
        """
        size_old_asteroid = asteroid.get_asteroid_size()
        if size_old_asteroid > 1:
            asteroid_minus, asteroid_plus, size_new_asteroid = self.new_asteroids_size(size_old_asteroid, torpedo,
                                                                                       asteroid)
            self.__asteroids.append(asteroid_plus)
            self.__asteroids.append(asteroid_minus)
            self.__screen.register_asteroid(asteroid_plus, size_new_asteroid)
            self.__screen.register_asteroid(asteroid_minus, size_new_asteroid)

        self.remove_asteroid(asteroid)
        torpedo.set_torpedo_dead(True)

    def new_asteroids_size(self, size_old_asteroid, torpedo, asteroid):
        """
        This creates new asteroids according to the size of the asteroid which was hit.
        :param size_old_asteroid: (int)
        :param torpedo: Torpedo object
        :param asteroid: Asteroid object
        :return: asteroid1 (minus), asteroid2 (plus), sizes of the new asteroids
        """
        size_new_asteroid = size_old_asteroid - 1
        new_asteroid_speed_x, new_asteroid_speed_y, x_asteroid_location, y_asteroid_location =\
            self.calculate_new_asteroids_speed(torpedo, asteroid)
        asteroid_minus = Asteroid(x_asteroid_location, -new_asteroid_speed_x, y_asteroid_location,
                                  -new_asteroid_speed_y, size_new_asteroid)
        asteroid_plus = Asteroid(x_asteroid_location, new_asteroid_speed_x, y_asteroid_location,
                                 new_asteroid_speed_y, size_new_asteroid)
        return asteroid_minus, asteroid_plus, size_new_asteroid

    def add_points(self, asteroid):
        """
        This adds to the player's score according to the size of the asteroid hit by torpedo.
        :param asteroid:Asteroid object
        """
        size_asteroid = asteroid.get_asteroid_size()
        how_many_points = self.POINTS_DICT[size_asteroid]
        self.__points += how_many_points

    def remove_asteroid(self, asteroid):
        """
        This unregister and remove the given asteroid from the game.
        :param asteroid: type object Asteroid
        """
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def set_torpedos(self, alive_torpedos):
        """

        :param alive_torpedos: a list of all currently living torpedos
        :return: None
        """
        self.__torpedos = alive_torpedos

    def remove_dead_torpedos(self):
        """
        this function creates a new list of torpedos-only the living ones and sets it to the list of torpedos
        :return: None
        """
        alive_torpedos = []
        for torpedo in self.__torpedos:
            if not torpedo.get_torpedo_dead():
                alive_torpedos.append(torpedo)
            else:
                self.__screen.unregister_torpedo(torpedo)
        self.set_torpedos(alive_torpedos)

    def crush_asteroid_torpedo(self, torpedo):
        """
        If there was a collision between an Asteroid and a Torpedo, the function split the asteroid
        and add to the player's score in the game.
        :param torpedo: Torpedo object
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(torpedo):
                self.split_asteroid(torpedo, asteroid)  # todo run over a changing list - torpedo
                self.add_points(asteroid)
                break
        self.__screen.set_score(self.__points)

    def torpedo_life_time(self, torpedo):  # todo
        """
        This removes the Torpedo from the game according to the conditions.
        :param torpedo: Torpedo object
        """
        if torpedo.get_born_time() + self.DEFAULT_TORPEDO_LIFETIME == self.__count:
            torpedo.set_torpedo_dead(True)

    def game_over(self):
        """
        This checks if the game should end.
        :return: boolean expression - True if so, False- otherwise.
        """
        if not self.__asteroids:
            self.__screen.show_message(self.TITLE_GAME_OVER, self.MSG_WIN_ASTEROIDS)
            return True
        if self.__ship.get_lives() == 0:
            self.__screen.show_message(self.TITLE_GAME_OVER, self.MSG_YOU_LOSE)
            return True
        if self.__screen.should_end():
            self.__screen.show_message(self.TITLE_GAME_OVER, self.MSG_QUIT)
            return True
        return False

    def ship_game(self):
        """
        the ship's actions during a game loop
        :return: None
        """
        x_cord_ship, y_cord_ship = self.__ship.get_x_y_location()
        self.__screen.draw_ship(x_cord_ship, y_cord_ship, 0)
        self.move_object(self.__ship)
        self.change_ship_heading()
        self.__screen.draw_ship(x_cord_ship, y_cord_ship, self.__ship.get_heading())
        self.accelerate_ship()

    def asteroid_game(self):
        """
        the asteroids' actions during a game loop
        :return: None
        """
        for asteroid in self.__asteroids:
            x_cord_asteroid, y_cord_asteroid = asteroid.get_x_y_location()
            self.__screen.draw_asteroid(asteroid, x_cord_asteroid, y_cord_asteroid)
            self.move_object(asteroid)
        self.crush_asteroid_ship()

    def torpedo_game(self):
        """
        the torpedos' actions during a game loop
        :return: None
        """
        self.shoot_torpedo()
        for torpedo in self.__torpedos:
            self.move_object(torpedo)
            x_cord_torpedo, y_cord_torpedo = torpedo.get_x_y_location()
            direction_torpedo = torpedo.get_direction()
            self.__screen.draw_torpedo(torpedo, x_cord_torpedo, y_cord_torpedo, direction_torpedo)
            self.torpedo_life_time(torpedo)
            self.crush_asteroid_torpedo(torpedo)
        self.remove_dead_torpedos()

    def _game_loop(self):
        """
        The main function of the game. responsible for operating the overall game process.
        """
        self.ship_game()
        self.asteroid_game()
        self.torpedo_game()
        self.__count += 1  # loop counter
        if self.game_over():
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
