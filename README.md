#################################################################################################################################################

This an application in python that can ingest a pdf (postgres), create embeddings, store those in postgres (pgvector), and help retrieve data 
from that pdf while asking a chatbot questions. The daatbase is in a docker container, and the python runs in a virtual environment. Additionally, 
SQLALchemy is used to create a connection between the python code and the postgresdb. 

Ingest process, chunking technique, and retrieval process currently in construction. All other pieces working and code will run. 

#################################################################################################################################################