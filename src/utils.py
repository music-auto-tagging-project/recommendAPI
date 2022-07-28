import pymysql
from pymysql.constants import CLIENT

def get_tag_id_list_by_user_playlist(userid,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            playlist_id_search_sql ="""select id,type from playlist WHERE user_id=%s;"""
            cursor.execute(playlist_id_search_sql,(userid))
            playlist_id_list=[ playlist_id[0] for playlist_id in cursor.fetchall() if playlist_id[1]!="recommended"]

            music_id_list=[]
            music_id_search_sql = """SELECT music_id FROM playlist_has_music WHERE playlist_id=%s"""
            for playlist_id in playlist_id_list:
                cursor.execute(music_id_search_sql,(playlist_id))
                music_id_list.extend([music_id[0] for music_id in cursor.fetchall()])

            tag_id_list=[]
            tag_id_search_sql = """SELECT tag_id FROM tag_has_music WHERE music_id=%s"""
            for music_id in music_id_list:
                cursor.execute(tag_id_search_sql,(music_id))
                tag_id_list.extend([tag_id[0] for tag_id in cursor.fetchall()])

    return tag_id_list

def save_user_tag_in_db(userid,user_tag_list,host,user,db,password,tag_id=True,is_fixed=False):
    """ Save user tag data in DB

        Args:
            tag_id:boolean
                user_tag_list가 user tag id로 이루어져 있는 경우 True,
                user_tag_list가 user tag name으로 이뤙져 있는 경우 False로 설정
            
            is_fixed:boolean
                사용자가 직접 설정한 tag인 경우 is_fixed를 True로,
                사용자의 플레이리스트를 통해 자동으로 설정된 tag의 경우 is_fixed를 False로 설정
                is_fixed가 True인 데이터의 경우 사용자가 해당 태그를 직접 삭제하기 전까지는 바뀌지 않는다.
        Returns:
            None
    """
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            if is_fixed:
                delete_prev_tag_sql = """DELETE FROM user_has_tag WHERE user_id=%s"""
                cursor.execute(delete_prev_tag_sql,(userid))

                if tag_id:
                    sql = """INSERT INTO user_has_tag(user_id,tag_id,is_fixed) 
                                    VALUES(%s,%s,1)"""
                else:
                    sql = """INSERT INTO user_has_tag(user_id,tag_id,is_fixed) 
                                    VALUES(%s,(SELECT id FROM tag WHERE name=%s),1)"""

            else:
                delete_prev_tag_sql = """DELETE FROM user_has_tag WHERE user_id=%s and is_fixed=0"""
                cursor.execute(delete_prev_tag_sql,(userid))

                if tag_id:
                    sql = """INSERT IGNORE INTO user_has_tag(user_id,tag_id,is_fixed) 
                                    VALUES(%s,%s,0)"""
                else:
                    sql = """INSERT IGNORE INTO user_has_tag(user_id,tag_id,is_fixed) 
                                    VALUES(%s,(SELECT id FROM tag WHERE name=%s),0)"""
            
            for user_tag_id in user_tag_list:
                cursor.execute(sql,(userid,user_tag_id))
        db.commit()
    return

def get_user_tag_by_user_id(userid,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    sql = """SELECT tag_id from user_has_tag where user_id=%s"""
    with db:
        with db.cursor() as cursor:
            cursor.execute(sql,(userid))
            user_tag = [music_id[0] for music_id in cursor.fetchall()]
    return user_tag

def get_music_id_list_by_user_tag(user_tag,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    sql = """SELECT music_id from tag_has_music where tag_id=%s"""
    with db:
        with db.cursor() as cursor:
            music_id_list=[]
            for tag in user_tag:
                cursor.execute(sql,(tag))
                music_id_list.extend([music_id[0] for music_id in cursor.fetchall()])
    return music_id_list

def save_recommended_playlist_in_db(userid,recommended_music_id_list,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)

    renew_recommended_playlist_sql="""DELETE FROM playlist_has_music WHERE playlist_id=(SELECT id FROM playlist WHERE user_id=%s and type='recommended');
                                      DELETE FROM playlist WHERE user_id=%s and type='recommended';
                                      INSERT INTO playlist(user_id,type) VALUES(%s,"recommended");
                                      SET @playlist_id=last_insert_id();"""
    insert_playlist_has_music_sql = """INSERT INTO playlist_has_music(playlist_id,music_id) VALUES(@playlist_id,%s);"""
    with db:
        with db.cursor() as cursor:
            cursor.execute(renew_recommended_playlist_sql,(userid,userid,userid))
            for recommended_music_id in recommended_music_id_list:
                cursor.execute(insert_playlist_has_music_sql,(recommended_music_id))
        db.commit()
    return