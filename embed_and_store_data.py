from sentence_transformers import SentenceTransformer
from clean_data import preprocess
from elasticsearch import Elasticsearch
import yaml
import time
from indexMapping import indexMapping

def read_yaml(path_to_yaml:str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)

        return content


def final(input_keyword):
    # print("Checking Connection")


    password=read_yaml("./constants.yaml")['password']

    es=Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic",str(password)),
        ca_certs="C:/elasticsearch-8.13.0/config/certs/http_ca.crt"
    )

    if es.ping()==True:
        print("Connected")
    else:
        print("Not connected to Elastic Search database.....")
        print("Returning")
        return 


# Embedding the dataset
    model = SentenceTransformer('all-mpnet-base-v2')
    new_df=preprocess()
    new_df["Overview_newVector"] = new_df["Overview_new"].apply(lambda x: model.encode(x))


    print(new_df['Overview_newVector'][0].shape)

    if es.indices.exists(index="all_moviess"):
        es.indices.delete(index="all_moviess")
        es.indices.create(index="all_moviess", mappings=indexMapping)
    record_list = new_df.to_dict("records")

    for record in record_list:
        try:
            es.index(index="all_moviess", document=record, id=record["MovieID"])
        except Exception as e:
            print(e)

    # Add a delay to allow indexing to complete
    time.sleep(30)  # Adjust the sleep time as needed

    print(es.count(index="all_moviess"))


    n=read_yaml("./constants.yaml")
    num_candidates=n['no_of_rows_to_be_used']
    no_outputs_to_show=n['no_outputs_to_show']


# Embed user_input
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "Overview_newVector",
        "query_vector" : vector_of_input_keyword,
        "k" : int(no_outputs_to_show),
        "num_candidates" : int(num_candidates)
    }

    res = es.knn_search(index="all_moviess", knn=query , source=["Series_Title","Overview_new"])
    results=res["hits"]["hits"]
    return results






if __name__=="__main__":
    input_keyword=input("Enter the text to be searched :")

    results = final(input_keyword)
    print(results)