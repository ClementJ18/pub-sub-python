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
