#########################################################################################################

This an application in python that can ingest a pdf (postgres), create embeddings, store those in postgres (pgvector), and help retrieve data 
from that pdf while asking a chatbot questions. The daatbase is in a docker container, and the python runs in a virtual environment. Additionally, 
SQLALchemy is used to create a connection between the python code and the postgresdb. 

Ingest process, chunking technique, and retrieval process currently in construction. All other pieces working and code will run. 



COMMANDS TO RUN APP

(with Docker running)

cd ~/your_file_directory
docker compose up -d
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
python db.py
streamlit run streamlit_app.py


to try SQL queries: docker exec -it rag_pg psql -U postgres -d ragdb -c \


The pdf was split into chunks, or segments, and each chunk was embedded (one vector per chunk). those rows were inserted into the chunks table in 
postgres (with vector column populated) and indexed by HNSW.

chunker is character based, 1200 chars per chunk with 150-char overlap

we search the chunks table by vector similarity

top-k chunks are shown/used as context for the answer 

docker commands for DB

docker exec -it rag_pg psql -U postgres -d ragdb -c "SELECT id, title FROM documents ORDER BY id DESC LIMIT 3;"
docker exec -it rag_pg psql -U postgres -d ragdb -c "SELECT COUNT(*) FROM chunks;"
docker exec -it rag_pg psql -U postgres -d ragdb -c "SELECT doc_id, COUNT(*) FROM chunks GROUP BY doc_id ORDER BY doc_id DESC LIMIT 5;"


