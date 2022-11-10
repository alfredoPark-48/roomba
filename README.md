# Roomba
Using the code provided in the [TC2008B course repository](https://github.com/octavio-navarro/TC2008B/tree/main/mesaExamples/randomAgents), we created a simple roomba simulation that cleans up trash objects in the grid.

Mesa and Flask is required in order to run, install both using:

    pip install mesa && pip install flask
To run the simulation use:

    python3 server.py

## Simulation Behaviour
- Five roombas are initilized at position (1,1) and trash is initialized in random cells throughout the grid. All five roombas will move in different directions throughout the grid and cleaning up trash in the way.
- The roombas will not pick the same position twice in order for it to not be repeating the same directions, however if it were to get stuck due to all possible directions being visited the roomba will simply choose a random position to move from all it's possible directions.
- If one of it's possible directions to move to happens to contain trash, the roomba will prioritize that direction and move towards it, cleaning it once it moves.

#### Collaborators
- Alfredo Jeong Hyun Park
- Diego Mellado Oliveros