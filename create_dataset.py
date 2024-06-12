import kaggle
import pandas as pd
import zipfile

def download_and_save_dataset():
    kaggle.api.authenticate()
    dataset = "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"
    kaggle.api.dataset_download_files(dataset)

    with zipfile.ZipFile(
        "imdb-dataset-of-top-1000-movies-and-tv-shows.zip", "r"
    ) as zip_ref:
        zip_ref.extractall(".")
    






def return_dataframe():
    download_and_save_dataset()
    df = pd.read_csv("imdb_top_1000.csv")
    print("Downloaded and saved dataset")
    return df

if __name__=="__main__":
    df=return_dataframe()
    print(df)


