# start service
docker-compose build
docker-compose up

#the worker is dockerized but the client created to show off the features isn't
#the important bit is to have or-tools and redis-installed
python -m pip install requirements.txt

#publish a problem
python geo/client.py --problem "[[-45.8102905, 73.459827], [-74.328539, 33.610414], [38.601709, -131.91105], [89.1447085, 167.411816], [78.689627, 6.542714], [88.274427, -44.134373], [73.6308145, 100.656899], [14.7815945, -38.300641], [-87.637856, -14.788132], [81.0695865, 99.567739], [41.8357385, -55.919688], [51.240564, -173.038122], [26.8342485, 121.491091], [69.5143535, -58.135543], [83.6277275, -60.104866], [-85.242164, -31.268344], [40.955635, -1.974146], [-64.550286, -1.867342], [39.7823385, 59.256881], [-43.4951265, -23.198815], [-89.348782, 176.147455], [5.793641, 147.453723], [-70.671387, -110.759804], [2.7472055, -4.879698], [-25.249197, 137.093982]]"

#publish multiple problems 
python geo/client.py --file tests/file.json