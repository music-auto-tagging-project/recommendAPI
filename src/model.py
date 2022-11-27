import requests
from abc import *
from src.utils import softmax
import numpy as np

class RecommendModel(metaclass=ABCMeta):
    def __init__(self,server):
        self.server=server

    @abstractmethod
    def recommend_music(self):
        pass

    @abstractmethod
    def recommend_user_tag(self):
        pass

    def get_tag_has_music(self,server="http://10.1.3.30:5000/music/tag/all"):
        return requests.get(server).json()

class EmbeddingModel(RecommendModel):
    def __init__(self):
        self.tag_embedding_dict = self.get_tag_embedding_dict()
        self.music_embedding_dict = self.get_music_embedding_dict()

        self.music_embeddings = np.stack([music_embedding for music_embedding in self.music_embedding_dict.values()],axis=0)
        self.music_idx2id = {idx : id for idx,id in enumerate(self.music_embeddings.keys())}

    def recommend_music(self,user_tag,top_n=10,sim_tresh=0.2):
        user_embedding = self.get_user_embedding(user_tag)

        embedding_similarity = np.einsum("AD,BD->AB",user_embedding, self.music_embeddings)

        k = min(embedding_similarity.shape[1],self.top_n)
        indices = embedding_similarity.argsort()[:-k:-1].flatten().tolist()

        recommended_music_id_list=[]
        for index in indices:
            if embedding_similarity[0][index] < sim_tresh:
                break
            music_id = self.musicidx2id[index]
            recommended_music_id_list.append(music_id)

        return recommended_music_id_list
        
    def recommend_user_tag(self):
        raise Exception("Embedding model couldn't recommend user tag")

    def get_user_embedding(self,user_tag):
        user_tag_id = user_tag["tagIdList"]
        user_tag_freq = user_tag['frequency']
        
        filtered = [(self.tag_embedding_dict[tag_id],freq) for tag_id,freq in zip(user_tag_id,user_tag_freq) if self.tag_embedding_dict[tag_id]!=-1]
        user_tag_embeddings, user_tag_freq = list(zip(*filtered))
        user_tag_embeddings = np.stack(user_tag_embeddings,axis=0)
        user_tag_weights = softmax(user_tag_freq)
        user_embedding = np.average(user_tag_embeddings,axis=0,weights=user_tag_weights,keepdims=True) # (1,D)

        return user_embedding
        
    def get_tag_embedding_dict(self,server="http://10.1.3.30:5000/tag/embedding/all"):
        tag_embedding_dict = requests.get(server).json()
        tag_embedding_dict = {id:value for id,value in tag_embedding_dict.items() if value!=-1}
        return tag_embedding_dict

    def get_music_embedding_dict(self,server="http://10.1.3.30:5000/music/embedding/all"):
        music_embedding_dict = requests.get(server).json()
        music_embedding_dict = {id:value for id,value in music_embedding_dict.items() if value!=-1}
        return music_embedding_dict

from collections import Counter
class FrequencyModel(RecommendModel):
    def __init__(self):
        self.tag_has_music_list = self.get_tag_has_music()

    def recommend_music(self,user_tag,top_n=10,freq_thresh=3):
        music_id_list = self.get_music_id_list_by_user_tag(user_tag)
        music_frequency = Counter(music_id_list).most_common()
        k = min(len(music_frequency),top_n)

        recommended_music_id_list=[]
        for music,freq in music_frequency[:k]:
            if freq < freq_thresh:
                break
            recommended_music_id_list.append(music)

        return recommended_music_id_list        

    def recommend_user_tag(self,playlist,top_n=10,freq_thresh=3):
        tag_frequency = Counter(playlist).most_common()
        k = min(len(tag_frequency),top_n)

        user_tag_id_list={
            "tagIdList":[],
            "frequency":[]
        }
        for tag,freq in tag_frequency[:k]:
            if freq < freq_thresh:
                break
            user_tag_id_list["tagIdList"].append(tag)
            user_tag_id_list["frequency"].append(freq)
        
        return user_tag_id_list

    def get_music_id_list_by_user_tag(self,user_tag):
        user_tag_id = user_tag["tagIdList"]
        user_tag_freq = user_tag["frequency"]

        music_id_list_by_user_tag=[]
        for user_tag,user_freq in zip(user_tag_id,user_tag_freq):
            music_tag_list = self.tag_has_music_list[str(user_tag)]
            music_id_list_by_user_tag.extend(music_tag_list*user_freq)

        return music_id_list_by_user_tag