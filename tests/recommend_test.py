import pytest
import importlib
from src import model

def test_recommend_models(playlist_tag_list):
    global model
    for m in model.__dir__():
        if m!="RecommendModel" and "Model" in m:
            model = getattr(model,m)()
            print("model : ",m)
            user_tag_id_list = model.recommend_user_tag(playlist_tag_list)
            assert user_tag_id_list
            print("\tuser tag id list",user_tag_id_list)

            recommended_music_id_list = model.recommend_music(user_tag_id_list)
            assert recommended_music_id_list
            print("\trecommend music id list",recommended_music_id_list)
            print('='*50)
    