from abc import *
from src.utils import get_user_tag_by_user_id,\
                      get_tag_id_list_by_user_playlist,\
                      get_music_id_list_by_user_tag, \
                      save_user_tag_in_db,\
                      save_recommended_playlist_in_db

class RecommendModel(metaclass=ABCMeta):
    def __init__(self,model):
        self.model = model

    @abstractmethod
    def recommend_music(self,userid):
        pass

    @abstractmethod
    def recommend_user_tag(self,userid):
        pass


from collections import Counter
class FrequencyModel(RecommendModel):
    def __init__(self,host,user,db,password):
        self.host = host
        self.user = user
        self.db = db
        self.password = password

    def recommend_music(self,userid,top_n=10,freq_thresh=2):
        user_tag = get_user_tag_by_user_id(userid,self.host,self.user,self.db,self.password)
        music_id_list = get_music_id_list_by_user_tag(user_tag,self.host,self.user,self.db,self.password)
        music_frequency = Counter(music_id_list).most_common()
        k = min(len(music_frequency),top_n)

        recommended_music_id_list=[]
        for music,freq in music_frequency[:k]:
            if freq < freq_thresh:
                break
            recommended_music_id_list.append(music)

        save_recommended_playlist_in_db(userid,recommended_music_id_list,self.host,self.user,self.db,self.password)

        return recommended_music_id_list        

    def recommend_user_tag(self,userid,top_n=10,freq_thresh=2):
        tag_id_list = get_tag_id_list_by_user_playlist(userid,self.host,self.user,self.db,self.password)
        tag_frequency = Counter(tag_id_list).most_common()
        k = min(len(tag_frequency),top_n)

        user_tag_id_list=[]
        for tag,freq in tag_frequency[:k]:
            if freq < freq_thresh:
                break
            user_tag_id_list.append(tag)

        save_user_tag_in_db(userid,user_tag_id_list,self.host,self.user,self.db,self.password)
        
        return user_tag_id_list
        
        



        