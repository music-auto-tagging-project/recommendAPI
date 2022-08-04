from flask import Flask, request, jsonify
from flask_cors import CORS
from src.model import FrequencyModel
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=5000,help='port number to access from middleware or front')
    args = parser.parse_args()
    return args

app = Flask (__name__)
CORS(app)

@app.route('/recommend/music',methods=["POST"])
def recommend_music():
    user_tag = request.get_json()['userTagList']
    recommended_music_id_list = model.recommend_music(user_tag)
    return jsonify({"musicIdList":recommended_music_id_list})
    
@app.route('/recommend/user-tag',methods=["POST"])
def recommend_user_tag():
    playlist = request.get_json()['playlistTagList']
    user_tag = model.recommend_user_tag(playlist)
    return jsonify({"userTagList":user_tag})

@app.route('/recommend/user-tag-music',methods=["POST"])
def recommend_user_tag_music():
    playlist = request.get_json()['playlistTagList']
    user_tag = model.recommend_user_tag(playlist)
    recommended_music_id_list = model.recommend_music(user_tag)

    return jsonify({"userTagList":user_tag,"musicIdList":recommended_music_id_list})

if __name__ == "__main__":
    args = parse_args()

    model = FrequencyModel()

    app.run(host='0.0.0.0',port=args.port)