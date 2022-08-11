import requests
from abc import *

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

        user_tag_id_list=[]
        user_tag_freq=[]
        for tag,freq in tag_frequency[:k]:
            if freq < freq_thresh:
                break
            user_tag_id_list.append((tag,freq))
        
        return user_tag_id_list

    def get_music_id_list_by_user_tag(self,user_tag):
        user_tag_id = [id for id,_ in user_tag]
        user_tag_freq = [freq for _,freq in user_tag]

        music_id_list_by_user_tag=[]
        for user_tag,user_freq in zip(user_tag_id,user_tag_freq):
            music_tag_list = [ music_tag for music_tag,_ in self.tag_has_music_list[str(user_tag)] ]
            music_id_list_by_user_tag.extend(music_tag_list*user_freq)

        return music_id_list_by_user_tag