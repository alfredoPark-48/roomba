from mesa import Model, agent
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RandomAgent, TrashAgent


class RoombaModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """

    def __init__(self, N, width, height, max_time):
        self.num_agents = N
        self.height = height
        self.width = width
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivationByType(self)
        self.running = True
        self.Time = 0
        self.max_time = max_time
        self.grid_size = (height - 2) * (width - 2)

        self.datacollector = DataCollector(
            agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(
                a, RandomAgent) else 0},
            model_reporters={
                "Trash": lambda a: a.countTrash(a, self.grid),
                "Clean": lambda a: a.countFloor(a, self.grid)
            })

        # Adds random trash in the grid
        for (contents, x, y) in self.grid.coord_iter():
            trash = TrashAgent((x, y), self)
            if self.random.random() < 0.1:
                self.grid.place_agent(trash, (x, y))

        # Add the roombas
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self)
            self.schedule.add(a)

            def pos_gen(w, h): return (
                self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, (1, 1))

        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.Time += 1
        self.schedule.step()
        self.datacollector.collect(self)

        # If the number of steps have been reached, the simulation stops
        if self.Time >= self.max_time or self.countTrash(self, self.grid) == 0:
            print("Ya estuvo ferras")
            self.running = False

    @staticmethod
    def countFloor(model, grid):
        count = 0

        for (contents, x, y) in grid.coord_iter():
            if len(contents) == 0:
                count += 1
                print("Clean", count)
            for i in contents:
                if isinstance(i, RandomAgent):
                    count += 1
                    print("Clean_", count)
        return count
    
    @staticmethod
    def countTrash(model, grid):
        count = 0 

        for (contents, x, y) in grid.coord_iter():
            for i in contents:
                if isinstance(i, TrashAgent):
                    count += 1
                    print("Trash", count)
        return count

