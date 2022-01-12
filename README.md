# pub-sub python
A wrapper for converting sets of lat-lon coordinates to pairwise distance.

![Architecture](/resources/architecture.png)
 
 ## Design
 The publishe/subscribe queues are literally represented using Redis PubSub capabilities.

 The "worker" (wrapping service) subscribes to "problems" channel (inbound queue) containing the IDs of problems that "clients" have submitted. When the ID is received, the problem with that ID is retrieved from Redis and solved. Once solved, the problem is placed back under the same ID but marked as a solution and then the worker publishes the solved ID to the "solutions" channel (outbound queue)

 Client desiring to use the system need to subscribe to the solutions channel, generate an ID for each problem, store the problem under that ID and then publish the ID to the problems channel.

 The reason for this is to allow clients to check the status of their problem independently of whether or not it is being processed. They can check if it's done at any time or pull it multiple times to get the solution.

 The problems are stored as dictionnaries with four attributes:
 * id : str - a random uuid generated at the start of the process to identify the problem, returned by the function for tracking purposes
 * problem : List[Tuple[int, int]] - the problem to be solved, a list of lont/lat coordinates
 * solution : List[int] - the solution to the problem, empty until the problem is solved and can remain empty even after, represents the pairwise distances
 * solved : bool - indicated whether the problem has been processed, set to True even if no solution is found as it represents that the worker is done processing it.

 worker.py is the "service", client.py is a example of how to connect to the service and how to publish problem and receive solutions. solver.py is mostly code from the or-tool example to be used as the underlying optmization engine.

 Transactions from the client to the worker are done through redis, the only thing is contained within docker.

 client.py uses command line argument, you can either pass a JSON-compliant list or the path to a json file containing a list of problems to solve.


## Deployment
The worker is dockerized, run docker-compose build, docker-compose up and it'll take care of itself.

The client created for the purpose of showing off the service is not dockerized and requires the python redis library and OR-tools. Those are specified in the requirements.txt so simply running that through pip should install everything you need.

The client can publish problems in two ways through command line arguments.

For single problems using the `--problem` argument followed by a list of tuples (here represented as lists cause json doesn't have tuples) of ints representing a list of lat/lon coordinates.
```
python geo/client.py --problem "[[-45.8102905, 73.459827], [-74.328539, 33.610414], [38.601709, -131.91105], [89.1447085, 167.411816], [78.689627, 6.542714], [88.274427, -44.134373], [73.6308145, 100.656899], [14.7815945, -38.300641], [-87.637856, -14.788132], [81.0695865, 99.567739], [41.8357385, -55.919688], [51.240564, -173.038122], [26.8342485, 121.491091], [69.5143535, -58.135543], [83.6277275, -60.104866], [-85.242164, -31.268344], [40.955635, -1.974146], [-64.550286, -1.867342], [39.7823385, 59.256881], [-43.4951265, -23.198815], [-89.348782, 176.147455], [5.793641, 147.453723], [-70.671387, -110.759804], [2.7472055, -4.879698], [-25.249197, 137.093982]]"
```

For multiple problems using the `--file` argument followed by the path to a json file containing a list of lists of tuples of ints represneting lat/lon coordinates. 

```
python geo/client.py --file tests/file.json
```

Either way, the contents must be JSON-compliant.

## Results
The client currently prints the results to the screen with the ID of the problem but this is completely customisable.

## Documentation
Importnant functions have docstrings, the rest is explained in this ReadME.

## Pictures

![Results](/resources/example_results.png)

