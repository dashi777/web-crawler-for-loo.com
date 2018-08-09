#encoding:UTF-8
import urllib.request
import re
import os
import sqlite3

"""
程序名称：luowang_crapy.py
设计者：Dash
对落网（http://www.luoo.net/）上所有期刊推荐音乐的歌手，专辑及歌名进行爬取
"""

def get_index(i):
    index = []
    url = r'http://www.luoo.net/tag/?p='+str(i)
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    pattern_index = re.compile(r'<a href="http://www.luoo.net/vol/index/(.*?)" class="name"')
    index_tmp = re.findall(pattern_index, data)
    for j in range(len(index_tmp)):
        index.append(index_tmp[j])
    return index


def get_info(i):
    url = 'http://www.luoo.net/vol/index/'+ str(i)
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    #第几期
    pattern_vol = re.compile(r'<span class="vol-number rounded">(.*?)</span>')
    vol = re.findall(pattern_vol, data)
    #每期期刊名称
    pattern_title = re.compile('<span class="vol-title">(.*?)</span>')
    title = re.findall(pattern_title, data)
    #歌名
    pattern_name = re.compile('<p class="name">(.*?)</p>')
    name = re.findall(pattern_name, data)
    #歌手
    pattern_artist = re.compile('<p class="artist">Artist: (.*?)</p>')
    artist = re.findall(pattern_artist, data)
    #专辑名
    pattern_album = re.compile('<p class="album">Album: (.*?)</p>')
    album = re.findall(pattern_album, data)
        #专辑图片链接
        # pattern_img = re.compile(r'<img src="(.*?)" alt=')
        # img = re.findall(pattern_img, data
        # img = img[0:len(img) - 8]
        # img.pop(1)
    info={}
    for j in range(len(name)):
        info.update({''
               'vol':vol[0],
               'title':title[0],
               'name_'+str(j):name[j],
               'artist_'+str(j):artist[j],
               'album_'+str(j):album[j],
               })
    return info

def dofordb():
	db = 'luoo_song_db.db'
	if os.path.exists(db):
		pass
	else:
		path = os.getcwd()
		path = path + '/' + db
		conn = sqlite3.connect(path)
		conn.close()


def dofortable():
    result = True
    db = 'luoo_song_db.db'
    path = os.getcwd()
    path = path + '/' + db
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    sql = " select * from sqlite_master where type = 'table' and name = 'luoo' "
    YandNO = cursor.execute(sql)
    YandNO = YandNO.fetchall()
    if len(YandNO) == 0:
        sql_create = '''
                  create table luoo(
				  vol NUMERIC (10,1),
				  title VARCHAR(100),
				  song_name VARCHAR(100),
				  song_artist VARCHAR(100),
				  song_album VARCHAR(100)
				  )
				  '''
        try:
            cursor.execute(sql_create)
            result =True
        except IOError:
            print(IOError)
            result = False
    sql_delete = 'delete from luoo;'
    cursor.execute(sql_delete)
    conn.commit
    conn.close()
    return result




#插入数据至二维表中
def insert2table(dict):
    db = 'luoo_song_db.db'
    path = os.getcwd()
    path = path + '/' + db
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    j = int(len(dict.keys()))
    for i in range((j-2)//3):
        string = "'" +dict['vol']+ "',"
        string = string + " '" + dict['title'] + "',"
        string = string + " '" + dict['name_'+str(i)] + "',"
        string = string + " '" + dict['artist_'+str(i)] + "',"
        string = string + " '" + dict['album_'+str(i)] + "'"
        sql_insert = " insert into luoo VALUES (" + string + ")"
        print(sql_insert)
        try:
            cursor.execute(sql_insert)
            conn.commit()
            result = True
        except:
            result = False
        if result:
            print(' --- 数据库导入成功')
        else:
            print(' --- 导入数据库失败')
    cursor.close()
    conn.close()

if __name__ == '__main__':
	# 第一步：检查是否有数据库
    dofordb()
	# 第二步：检查是否有二维表
    dofortable()
    for i in range(1,101):
        index = get_index(i)
        for j in index :
            info = get_info(j)
            insert2table(info)
