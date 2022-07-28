from flask import Flask, request, jsonify
from flask_cors import CORS
from src.model import FrequencyModel
from src.utils import save_user_tag_in_db
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",type=str,help='db server endpoint')
    parser.add_argument("--user",type=str,help='db login id')
    parser.add_argument("--db",type=str,help='db name')
    parser.add_argument("--password",type=str,help='db login password')
    parser.add_argument('--port',type=int,default=5001,help='port number to access from middleware or front')
    args = parser.parse_args()
    return args

app = Flask (__name__)
CORS(app)

@app.route('/recommend/<int:userid>',methods=["GET"])
def recommend_music(userid):
    model.recommend_user_tag(userid) # 해당 유저의 현재 플레이리스트로 user tag를 갱신(in DB)
    recommended_music_id_list = model.recommend_music(userid) # 갱신된 user tag를 기반으로 추천 플레이리스트를 갱신(in DB)
    return jsonify({"musicIdList":recommended_music_id_list})

@app.route('/user/tag',methods=["POST"])
def update_user_tag():
    value = request.get_data()
    value = eval(value.decode("utf-8"))

    userid = value['userId']
    tagList = value['tagList']

    save_user_tag_in_db(userid,tagList,host=host,user=user,db=db,password=password,tag_id=False,is_fixed=True)
    return ""    


if __name__ == "__main__":
    args = parse_args()
    host,user,db,password = args.host, args.user, args.db, args.password

    model = FrequencyModel(host=host,user=user,db=db,password=password)

    app.run(host='0.0.0.0',port=args.port)