"""
- Prepare the text to embed for each reccord of your dataset.
    - Create the reccord.
        - Clean the text.
        - Concatenate fields.
- Choose a Sentence Embedding Model.
- Embed the text generated in the previous step for each reccord.
- Store the embeddings in a vector database (i.e. elasticsearch).
"""
from sentence_transformers import SentenceTransformer
from clean_data import preprocess
from elasticsearch import Elasticsearch
import yaml
from indexMapping import indexMapping




def read_yaml(path_to_yaml:str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)

        return content

def check_coonection():
    password=read_yaml("./constants.yaml")['password']



    es=Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic",str(password)),
        ca_certs="C:/elasticsearch-8.13.0/config/certs/http_ca.crt"
    )
    if es.ping()==True:
        print("Connection Build")
        return es
    else:
        print("Not connected to Elastic Search database.....")
        print("Returning None")

        return None

# Embedd the Dataset
def embed_dataset(input_keyword):
    es=check_coonection()
    if es==None:
        exit()
    

    new_df=preprocess()
    

    model3 = SentenceTransformer('all-mpnet-base-v2')
    new_df["Overview_newVector"] = new_df["Overview_new"].apply(lambda x: model3.encode(x))

    # print("For Overview_newVector ")
    # print()


    # print(new_df.columns)
    if es.indices.exists(index="all_moviess"):
    # Delete the existing index with same name
        es.indices.delete(index="all_moviess")
    es.indices.create(index="all_moviess", mappings=indexMapping)
    record_list = new_df.to_dict("records")
    # print()
    # print("Record List :",end="")
    # print(record_list[0])

    for record in record_list:
        try:
            es.index(index="all_moviess", document=record, id=record["MovieID"])
        except Exception as e:
            print(e,"Here.................................")



# Embed the User_input

    vector_of_input_keyword = model3.encode(input_keyword)

    n=read_yaml("./constants.yaml")
    num_candidates=n['no_of_rows_to_be_used']
    no_outputs_to_show=n['no_outputs_to_show']


    query = {
        "field" : "Overview_newVector",
        "query_vector" : vector_of_input_keyword,
        "k" : 3,
        "num_candidates" : 100
    }

    res = es.knn_search(index="all_moviess", knn=query , source=["Series_Title","Overview"])
    abc=res["hits"]["hits"]
    return abc
    




if __name__=="__main__":
    input_keyword="Good Movie"#input("Enter the text to be searched :")

    results = embed_dataset(input_keyword)
    print(results)

