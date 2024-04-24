# tributary

Backend project for Ford's sensor streaming system. 

IN this task we use Python, Flask and Docker,

The /record endpoint is periodically called by embedded sensors within a vehicle to post data to the database. The data is then retrieved by a user facing mobile application using the /collect endpoint.
