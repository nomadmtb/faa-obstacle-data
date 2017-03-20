![faa](http://i.imgur.com/LINa8X5.jpg)

# faa-obstacle-data
A visual representation of the obstacle data from the FAA.  Tool will calculate the number of obstacles between a set of airports.

You can see development version of the data at dof.itslit.lol

# Routes
| route | params | Desc |
|-------|--------|------|
| /dof/api/calculate_route | route=SEA,SFO,AUS | Get obstacles along route |

# Management Commands
| Command | params | Desc |
|---------|--------|------|
| populatedof | dof_filepath(dat), airport_filepath(csv) | Drop+Reload Obstacles and Airports |


# WIP
1. Build out the airport and obstacle routes.

2. Documentation on routes.

3. Publish code to AWS EC2.

4. Docker deployment scripts.
