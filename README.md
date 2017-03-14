# faa-obstacle-data
A visual representation of the obstacle data from the FAA.  Tool will calculate the number of obstacles between a set of airports.

# Routes
| route | params | Desc |
|-------|--------|------|
| /dof/api/calculate_route | route=SEA,SFO,AUS | Get obstacles along route |

# Management Commands
| Command | params | Desc |
|---------|--------|------|
| populatedof | dof_filepath(dat), airport_filepath(csv) | Drop+Reload Obstacles and Airports |


# WIP
1. Generate the set of distances between each point. 26 miles split with 5 miles will be 5,5,5,5,1.

2. With the above list of distances we can compute the coordinates for all of these. With slope and trig functions.

3. Query the backend to see what points are within x distance from each point. Not sure about this yet.
