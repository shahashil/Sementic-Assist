import cohere
import numpy as np
import pandas as pd
from nltk import sent_tokenize
from annoy import AnnoyIndex
from sklearn.metrics.pairwise import cosine_similarity
import re 
import requests
from bs4 import BeautifulSoup
import funct as f
import hashlib    


# Paste your API key here. Remember to not share publicly
api_key = ''
# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(api_key)  


def embedd(file,url,file_list,query):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser') 
    result = list(soup.findAll('p')) 

    raw = []
    filtered = []
    raw_map = {}

    for x in result:

        raw.append(x.text)
        filtered.append(sent_tokenize(f.remove_brac(x.text)))
    

    filtered_flat_list = []
    last_number = -1

    for count1,x in enumerate(filtered):
        members = []
        for count2,y in enumerate(x):
            last_number = last_number + 1
            members.append(last_number)
            filtered_flat_list.append(y)
        raw_map.update({count1:members})


    f.pickle_save('User/flat-list/flat_list-'+file, filtered_flat_list)
    f.pickle_save('User/raw/raw-'+file, raw)
    f.pickle_save('User/raw-map/raw_map-'+file, raw_map)

    # Get the embeddings
    embeds = co.embed(texts=filtered_flat_list,
                  model="large",
                  truncate="LEFT").embeddings
    embeds = np.array(embeds)
    # Create the search index, pass the size of embedding
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    # Add all the vectors to the search index
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])

    search_index.build(10) # 10 trees
    search_index.save("User/Annoy/"+file+'.ann')
    
    file_list.append(file)
    f.pickle_save('User/filename/filenames',file_list)
    f.pickle_save('User/embed/embed-'+file,embeds)
    
    return return_str(file,query)


#################################################################

def return_str(file,query):
    embeds = f.pickle_load('User/embed/embed-'+file)
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    search_index.load("User/Annoy/"+file+'.ann')
    
    # Get the query's embedding
    query_embed = co.embed(texts=[query],
                  model="large",
                  truncate="LEFT").embeddings

    # Retrieve the nearest neighbors
    similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
                                                include_distances=True)


    filtered_flat_list = f.pickle_load('User/flat-list/flat_list-'+file)
    raw     = f.pickle_load('User/raw/raw-'+file)
    raw_map = f.pickle_load('User/raw-map/raw_map-'+file)

    index = similar_item_ids[0][0]
    filtered_flat_list[index]
    
    for count,x in enumerate(list(raw_map.values())):
        if index in x:
            index = count
            break
    return_sentence = raw[index][:25]        

    return return_sentence

    
####################################################################

def search(url,query):
    file_list = f.pickle_load('User/filename/filenames')
    file = str(hashlib.sha256(url.encode()).hexdigest())
    try:
        if file not in file_list:
            print("New File: ",file_list)
            return embedd(file,url,file_list,query)
        else:
            print("Old File")
            return return_str(file, query)
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    print(search('https://en.wikipedia.org/wiki/Ir_David_Foundation', 'when did he retire'))




