from model import RoombaModel, TrashAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "green",
                 "r": 0.5}

    if (isinstance(agent, TrashAgent)):
        portrayal['Color'] = 'brown'
        portrayal['Layer'] = 1
        portrayal['r'] = 0.2

    return portrayal


model_params = {"N": UserSettableParameter("slider", "Roomba number", 1, 1, 5),
                "max_time": UserSettableParameter("slider", "Maximum steps", 35, 1, 100),
                "width": 10,
                "height": 10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label": "Steps", "Color": "#AA0000"}],
    scope="agent", sorting="ascending", sort_by="Steps")
pie_chart = PieChartModule(
    [{"Label": "Trash", "Color": "#FFFF00"}, {"Label": "Clean", "Color": "#999999"}])

server = ModularServer(
    RoombaModel, [grid, bar_chart, pie_chart], "Roomba", model_params)

server.port = 8521  # The default
server.launch()
