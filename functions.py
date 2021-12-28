import numpy as np

class Functions:
    def __init__(self):
        pass
    
    def generate_snake_coor(self, n):
        """ Generate snake's coordinate
        :param n: the size of the matrix
        :return self.snake_coor: snake's coordinate
        """
        mid_coor = int((n+1)/2)
        # first index is the snake's head, the rest is the snake's body coordinate
        snake_coor = [[mid_coor, mid_coor]]
        for _ in range(0,7):
            current_coor = snake_coor[-1]
            current_row_coor = current_coor[0]
            current_col_coor = current_coor[1]
            top = [current_row_coor, current_col_coor+1]
            bottom = [current_row_coor, current_col_coor-1]
            left = [current_row_coor-1, current_col_coor]
            right = [current_row_coor+1, current_col_coor]
            neighbor = []
            for v in [top, bottom, left, right]:
                n_row = v[0]
                n_col = v[1]
                if v not in snake_coor and n_row >= 0 and n_row < n and n_col >= 0 and n_col < n:
                    neighbor.append(v)
            rand = np.random.rand(1)
            for r in range(1, len(neighbor)+1):
                compare = r / len(neighbor)
                if rand <= compare:
                    snake_coor.append(neighbor[r-1])
                    break
        self.snake_coor = snake_coor
        return self.snake_coor
    
    def generate_mouse_coor(self, n, snake_coor):
        """ Generate mouse's coordinate
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :return mouse_coor: mouse's coordinate
        """
        while True:
            rand = np.random.rand(1)
            if rand < 0.5:
                rand_row = np.random.randint(0, n)
                rand_col = np.random.randint(-1, 1)
            else:
                rand_row = np.random.randint(-1, 1)
                rand_col = np.random.randint(0, n)   
            mouse_coor = [rand_row, rand_col]
            if mouse_coor not in snake_coor:
                break
        self.mouse_coor = mouse_coor
        return self.mouse_coor
        
    def generate_map(self, n, snake_coor, mouse_coor):
        """ Generate the map that includes snake and mouse
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :return self.map: map that includes snake and mouse
        """
        # empty cells are denoted with number 0
        map = np.zeros((n, n))
        # snake's head are denoted with number 1
        map[snake_coor[0][0], snake_coor[0][1]] = 1
        # snake's body are denoted with number 2
        for body_coor in snake_coor[1:]:
            map[body_coor[0], body_coor[1]] = 2
        # mouse are denoted with number 3
        map[mouse_coor[0], mouse_coor[1]] = 3
        self.map = map
        return self.map

    def snakes_eyesight(self, n, snake_coor):
        """ Generate the coordinate of the snake eyesight, the eyesight's scope is 3x3
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :return self.sights_coor: the coordinates of the snake's eyesight
        """
        head_coor = snake_coor[0]
        head_row_coor = head_coor[0]
        head_col_coor = head_coor[1]
        top = [head_row_coor-3, head_col_coor]
        bottom = [head_row_coor+3, head_col_coor]
        right = [head_row_coor, head_col_coor+3]
        left = [head_row_coor, head_col_coor-3]
        # store ranges with the order top, bottom, right, left
        ranges = []
        for v in [top, bottom, right, left]:
            v_row = v[0]
            v_col = v[1]
            if v_row < 0:
                v_row = 0
            if v_row >= n:
                v_row = n-1
            if v_col < 0:
                v_col = 0
            if v_col >= n:
                v_col = n-1
            ranges.append([v_row, v_col])
        top_span = ranges[0][0]
        bottom_span = ranges[1][0]
        left_span = ranges[3][1]
        right_span = ranges[2][1]
        sights_coor = []
        for r in range(top_span, bottom_span+1):
            for c in range(left_span, right_span+1):
                sights_coor.append([r, c])
        self.sights_coor = sights_coor
        return self.sights_coor

    def snakes_movements_if_mouse_in_sight(self, snake_coor, mouse_coor):
        """ Decide the snake's next move if there's a mouse in sight
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :return self.snake_coor: snake's coordinate
        """
        head_coor = snake_coor[0]
        horizontal_len = head_coor[1] - mouse_coor[1]
        vertical_len = head_coor[0] - mouse_coor[0]
        if np.abs(horizontal_len) > np.abs(vertical_len):
            # mouse is on the left
            if horizontal_len > 0:
                head_coor = [head_coor[0], head_coor[1]-1]
            # mouse is on the right
            elif horizontal_len < 0:
                head_coor = [head_coor[0], head_coor[1]+1]
        elif np.abs(vertical_len) > np.abs(horizontal_len):
            # mouse is on the top
            if vertical_len > 0:
                head_coor = [head_coor[0]-1, head_coor[1]]
            # mouse is on the bottom
            elif vertical_len < 0:
                head_coor = [head_coor[0]+1, head_coor[1]]
        elif np.abs(horizontal_len) == np.abs(vertical_len):
            rand = np.random.rand(1)
            # move vertically
            if rand <= 0.5:
                # mouse is on the top
                if vertical_len > 0:
                    head_coor = [head_coor[0]-1, head_coor[1]]
                # mouse is on the bottom
                elif vertical_len < 0:
                    head_coor = [head_coor[0]+1, head_coor[1]]
            # move horizontally
            elif rand <= 1:
                # mouse is on the left
                if horizontal_len > 0:
                    head_coor = [head_coor[0], head_coor[1]-1]
                # mouse is on the right
                elif horizontal_len < 0:
                    head_coor = [head_coor[0], head_coor[1]+1]
        snake_coor.insert(0, head_coor)
        self.snake_coor = snake_coor
        return self.snake_coor
    
    def snakes_movements_if_no_mouse_in_sight(self, n, snake_coor):
        """ Decide the snake's next move if there's no mouse in sight
        :param snake_coor: snake's coordinate
        :return self.snake_coor: snake's coordinate
        """
        head_coor = snake_coor[0]
        top = [head_coor[0], head_coor[1]+1]
        bottom = [head_coor[0], head_coor[1]-1]
        left = [head_coor[0]-1, head_coor[1]]
        right = [head_coor[0]+1, head_coor[1]]
        neighbor = []
        for v in [top, right, bottom, left]:
            n_row = v[0]
            n_col = v[1]
            if v not in snake_coor and n_row >= 0 and n_row < n and n_col >= 0 and n_col < n:
                neighbor.append(v)
        rand = np.random.rand(1)
        for r in range(1, len(neighbor)+1):
            compare = r / len(neighbor)
            if rand <= compare:
                snake_coor.insert(0, neighbor[r-1])
                break
        self.snake_coor = snake_coor
        return self.snake_coor
    
    def snake_movements_coor(self, n, snake_coor, mouse_coor, map):
        """ Generate the snake's movement based on the information taken from its eyesight
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :param map: map that includes snake and mouse
        :return self.snake_coor: snake's coordinate
        """
        sights_coor = self.snakes_eyesight(n, snake_coor)
        mouse_coor = False
        for s_coor in sights_coor:
            if map[s_coor[0], s_coor[1]] == 3:
                mouse_coor = s_coor
                break 
        if mouse_coor is not False:
            snake_coor = self.snakes_movements_if_mouse_in_sight(snake_coor, mouse_coor)
        else:
            snake_coor = self.snakes_movements_if_no_mouse_in_sight(n, snake_coor)
        self.snake_coor = snake_coor
        return self.snake_coor

    def snake_move(self, map, snake_coor):
        """ Execute the next coordinate of the snake into the map
        :param map: map that includes snake and mouse
        :param snake_coor: snake's coordinate
        :return map: map that includes snake and mouse
        :return snake_coor: snake's coordinate
        """
        head_coor = snake_coor[0]
        for body_coor in snake_coor[1:-1]:
            map[body_coor[0], body_coor[1]] = 2
        last_body_coor = snake_coor[-1]
        map[last_body_coor[0], last_body_coor[1]] = 0
        map[head_coor[0], head_coor[1]] = 1
        self.snake_coor = snake_coor[:-1]
        self.map = map
        return (self.map, self.snake_coor)

    def mouse_movements_coor(self, n, snake_coor, mouse_coor):
        """ Generate the mouses's movement
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :return self.list_mouse_coor: a list containing mouse coordinate before and after it moves
        """
        list_mouse_coor = [mouse_coor]
        top = [mouse_coor[0], mouse_coor[1]+1]
        bottom = [mouse_coor[0], mouse_coor[1]-1]
        left = [mouse_coor[0]-1, mouse_coor[1]]
        right = [mouse_coor[0]+1, mouse_coor[1]]
        neighbor = []
        for v in [top, right, bottom, left]:
            n_row = v[0]
            n_col = v[1]
            if v not in snake_coor and n_row >= 0 and n_row < n and n_col >= 0 and n_col < n:
                neighbor.append(v)
        rand = np.random.rand(1)
        for r in range(1, len(neighbor)+1):
            compare = r / len(neighbor)
            if rand <= compare:
                list_mouse_coor.append(neighbor[r-1])
                break
        self.list_mouse_coor = list_mouse_coor
        return self.list_mouse_coor
     
    def mouse_move(self, n, snake_coor, mouse_coor, map):
        """ Execute the next coordinate of the mouse into the map
        :param map: map that includes snake and mouse
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :return map: map that includes snake and mouse
        :return mouse_coor: mouse's coordinate
        """
        rand = np.random.rand(1)
        if rand < 0.5:
            return (self.map, self.mouse_coor)
        else:
            list_mouse_coor = self.mouse_movements_coor(n, snake_coor, mouse_coor)
            map[list_mouse_coor[0][0], list_mouse_coor[0][1]] = 0
            map[list_mouse_coor[-1][0], list_mouse_coor[-1][1]] = 3
            self.mouse_coor = list_mouse_coor[-1]
            return (self.map, self.mouse_coor)

    def snake_and_mouse_movements(self, n, snake_coor, mouse_coor, map, snakes_property, mouses_property, snake_heat_loss_rate, mouse_heat_loss_rate):
        """ Executes both snake and mouse movements while also undergoing heat loss that can resulting in a hibernation
        :param n: the size of the matrix
        :param snake_coor: snake's coordinate
        :param mouse_coor: mouse's coordinate
        :param map: map that includes snake and mouse
        :param snake_property: list containing informations on snake's body temperature and it current state
        :param snake_property: list containing informations on mouse's body temperature and it current state
        :param snake_heat_loss_rate: snake's heat loss rate for every iterations
        :param mouse_heat_loss_rate: mouse's heat loss rate for every iterations
        :return snake_coor: snake's coordinate
        :return mouse_coor: mouse's coordinate
        :return map: map that includes snake and mouse
        """
        snakes_property[2] = self.heat_reduction(snakes_property[2], snake_heat_loss_rate)
        snakes_property = self.hibernation_time(snakes_property)
        mouses_property[2] = self.heat_reduction(mouses_property[2], mouse_heat_loss_rate)
        mouses_property = self.hibernation_time(mouses_property)
        if snakes_property[4] is False:
            snake_coor = self.snake_movements_coor(n, snake_coor, mouse_coor, map)
            map, snake_coor = self.snake_move(map, snake_coor)    
        if snake_coor[0] == mouse_coor:
            mouse_coor = None
        if mouse_coor is not None:
            if mouses_property[4] is False:
                map, mouse_coor = self.mouse_move(n, snake_coor, mouse_coor, map)
        self.map = map
        self.snake_coor = snake_coor
        self.mouse_coor = mouse_coor
        return (self.map, self.snake_coor, self.mouse_coor)
    
    def generate_snake_mouse_property(self):
        """ Generate snake's and mouse's property
        :return snakes_property: list containing informations on snake's body temperature and it current state
        :return mouses_property: list containing informations on mouse's body temperature and it current state
        """
        # the first index is the initial temperature
        # the second index is the temperature needed to go hibernate
        # the third index is the current body temperature
        # the fourth index is used to track its hibernation time
        # the fifth index is used to know the state of the animal, False means not in a hibernation state
        snakes_property = [22.3, 16, 22.3, 0, False]
        mouses_property = [36.9, 20, 36.9, 0, False]
        return (snakes_property, mouses_property)

    def heat_loss_rate(self, area, env_temperature, body_temp):
        """ Calculate the heat loss rate by its assummed area, the environment's temperature, and its body temperature """
        stefan_boltzman_constant = 5.6703 * 10**(-8)
        # assume that heat emissivity is 0.75
        e = 1
        temp_diff_power_4 = env_temperature**4 - body_temp**4
        heat_loss_rate = stefan_boltzman_constant * e * area * temp_diff_power_4
        return heat_loss_rate

    def heat_reduction(self, body_temp, heat_loss_rate):
        body_temp += heat_loss_rate
        return body_temp
    
    def hibernation_time(self, property):
        # the first index is the initial temperature
        # the second index is the temperature needed to go hibernate
        # the third index is the current body temperature
        # the fourth index is used to track its hibernation time
        # the fifth index is used to know the staste of the animal, False means not in a hibernation state
        if property[2] <= property[1]:
            property[4] = True
        if property[3] == 8:
            property[2] = property[0]
            property[3] = 0
            property[4] = False 
        elif property[4] == True:
            property[3] =  property[3] + 1
        return property


        
    
    
    
    


