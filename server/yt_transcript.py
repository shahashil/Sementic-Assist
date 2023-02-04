# importing modules
from youtube_transcript_api import YouTubeTranscriptApi
import sementic_search
import funct as f
import hashlib 
import numpy as np  
from annoy import AnnoyIndex
from sklearn.metrics.pairwise import cosine_similarity
import cohere

# Paste your API key here. Remember to not share publicly
api_key = ''
# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(api_key)  

# using the srt variable with the list of dictionaries
# obtained by the .get_transcript() function

def yt_get_transcripts(url):
    #url = 'https://www.youtube.com/watch?v=FM6kHcXpw98'
    yt_id = url[url.index('?v=') + 3:]
    #query = "import dependencies"
    file = str(hashlib.sha256(url.encode()).hexdigest())

    file_list = f.pickle_load('User/filename/filenames')

    if file not in file_list:
        srt = YouTubeTranscriptApi.get_transcript(yt_id)
        subtitle_list = []
        subtitle_list= [x['text'] for x in srt]
        f.pickle_save('User/yt-file/srt'+file,srt)
        f.pickle_save('User/yt-file/subtitle'+file,subtitle_list)
        return (srt,subtitle_list,file)
    else:
        srt           = f.pickle_load('User/yt-file/srt'+file)
        subtitle_list = f.pickle_load('User/yt-file/subtitle'+file)
        return (srt,subtitle_list,file)
        

#
# split = ['or','and','so','which','well','we',"we're",]
#Funcitons

def yt_embedd(file,result,file_list,query):

    filtered_flat_list = result.copy()

    f.pickle_save('User/flat-list/flat_list-'+file, filtered_flat_list)

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
    
    return yt_return_str(file,query)

def yt_return_str(file,query):
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

    index = similar_item_ids[0][0]
    return_sentence = filtered_flat_list[index]          

    return index

def yt_search(url,query):
    srt,subtitle_list,file = yt_get_transcripts(url)
    file_list = f.pickle_load('User/filename/filenames')
    try:
        if file not in file_list:
            print("New File: ",file_list)
            index =  yt_embedd(file,subtitle_list,file_list,query)
            return str(int(srt[index]['start']))
        else:
            pass
            print("Old File")
            index = yt_return_str(file, query)
            return str(int(srt[index]['start']))
    except Exception as e:
        print(e)
        return None    



#Driver  Code


#index = yt_search(file,query,subtitle_list)

#print(srt[index])
#print(int(srt[index]['start']))
