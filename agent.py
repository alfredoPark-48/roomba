from mesa import Agent


class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        self.visited = []
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Using get_neighbors method we store the neighbors that are trash to clean
        trash = [trash_agent for trash_agent in self.model.grid.get_neighbors(
            self.pos, moore=True
        ) if isinstance(trash_agent, TrashAgent)]

        if len(trash) > 0:
            # If we have trash agents in the trash list we move to the trash's position
            next_move = trash[-1].pos
            self.model.grid.move_agent(self, next_move)
            # We use remove_agent method to remove the trash agent
            self.model.grid.remove_agent(trash[-1])
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                moore=True,
                include_center=True)

            # Checks which grid cells are empty
            freeSpaces = list(
                map(self.model.grid.is_cell_empty, possible_steps))

            next_moves = [p for p, f in zip(
                possible_steps, freeSpaces) if f == True]
            next_move = self.random.choice(next_moves)

            empty = not self.visited
            nextMove = next_move not in self.visited
            allVisited = all(cell in self.visited for cell in next_moves)

            # escapes if roomba is traped
            if allVisited:
                next_move = self.random.choice(next_moves)
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                # if there is none cell visited it moves wherever
            if empty:
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.visited.append(next_move)
                # if the selected cell is not visited it moves
            if nextMove:
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.visited.append(next_move)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()


class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class TrashAgent(Agent):
    """
    Trash agent for our random agent remove from grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self._isTrash = True

    def step(self):
        pass
