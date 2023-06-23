from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

# Conexão com o MongoDB
cluster_url = os.getenv("CLUSTER_URL")
cluster = MongoClient(cluster_url)


# Bancos
db_provas = cluster["provas"]