import requests
import time
import csv
import math
import json
import pandas as pd
import random


# 请求头
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360SE/13.1.5600.0'}


# 获取该用户关注列表中的认证用户
def getNextUsers(userId):
    follow_text = requests.get("https://api.bilibili.com/x/relation/followings?vmid={}&pn=1".format(userId),
                               headers=header).text
    follow_json = json.loads(follow_text)
    # 筛选未设置隐私的用户
    if follow_json['code'] != 0:
        return []
    else:
        # 关注人数
        follow_num = follow_json['data']['total']
        # 获取pn数
        pns = math.ceil(follow_num / 50)
        urls = ["https://api.bilibili.com/x/relation/followings?vmid={}&pn={}".format(userId, i) for i in
                range(1, pns + 1)]
        follow_data = []
        for url in urls:
            text = requests.get(url, headers=header).text
            j = json.loads(text)
            try:
                user_list = j['data']['list']
                for user in user_list:
                    # 判断是否为认证用户
                    if user['official_verify']['type'] == 0:
                        mid = user['mid']
                        uname = user['uname']
                        sign = user['sign']
                        follow_data.append([mid, uname, sign])
            except:
                follow_data += []
        return follow_data


# 获取关注数和粉丝数
def getRelations(userId):
    relation_text = requests.get("https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(userId),
                                 headers=header).text
    relation_json = json.loads(relation_text)
    fans, follows = relation_json['data']['follower'], relation_json['data']['following']
    return fans, follows


# 获取视频数、音频数、专栏数、相簿数
def getNum(userId):
    num_text = requests.get("https://api.bilibili.com/x/space/navnum?mid={}".format(userId), headers=header).text
    num_json = json.loads(num_text)
    videoNum, audioNum, articleNum, albumNum = num_json['data']['video'], num_json['data']['audio'], num_json['data'][
        'article'], num_json['data']['album']
    return videoNum, audioNum, articleNum, albumNum


# 获取投稿视频(前5)标题
def getVideos(userId):
    video_text = requests.get(
        'https://api.bilibili.com/x/space/masterpiece?vmid={}&jsonp=jsonp'.format(userId),
        headers=header).text
    video_json = json.loads(video_text)
    videos = video_json['data']
    titles = []
    for item in videos[:3]:
        # 播放量 play4
        # 评论条数 video_review
        titles.append(item['title'])
    return ";".join(titles)


def getTypes(userId):
    type_text = requests.get(
        'https://api.bilibili.com/x/space/masterpiece?vmid={}&jsonp=jsonp'.format(userId),
        headers=header).text
    video_json = json.loads(type_text)
    videos = video_json['data']
    videotypes = []
    for item in videos[:3]:
        # 播放量 play4
        # 评论条数 video_review
        videotypes.append(item['tname'])

    return ";".join(videotypes)
##########开始爬取##########
# ['userId','userName','userDescription']
with open("three_fields.csv", 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['userId', 'userName', 'userDescription', 'tname'])
    # 第一层
    first = getNextUsers("10119428")  # 10119428 入口账号
    csv_writer.writerows(first)
    # 第二层
    second = []
    for user in first:
        time.sleep(3)
        second += getNextUsers(user[0])
    csv_writer.writerows(second)
    # 第三层
    third = []
    for user in second:
        print(user[0])
        third += getNextUsers(user[0])
    csv_writer.writerows(third)
    print("写入完毕")

# ['userId','userName','userDescription','videos','follows','fans','videoNum','audioNum','articleNum','albumNum']
# 去重
df = pd.read_csv("three_fields.csv").drop_duplicates().reset_index()
userIds = list(df['userId'])

# 获取投稿视频(前5条视频的标题信息)
for id in userIds:
    try:
        time.sleep(random.random())
        df.loc[df['userId'] == id, ['videos', '']] = getVideos(id)
        df.loc[df['userId'] == id, ['tname', '']] = getTypes(id)
        print("1")
    except:
        print("2")

# 获取关注数、粉丝数、视频数、音频数、专栏数、相簿数
# 新增多列['fans','follows','videoNum','audioNum','articleNum','albumNum']
df[['fans', 'follows', 'videoNum', 'audioNum', 'articleNum', 'albumNum']] = pd.DataFrame(
    columns=['fans', 'follows', 'videoNum', 'audioNum', 'articleNum', 'albumNum'])
for id in userIds:
    time.sleep(random.random())
    df.loc[df['userId'] == id, ['fans', 'follows', 'videoNum', 'audioNum', 'articleNum', 'albumNum']] = list(
        getRelations(id)) + list(getNum(id))
df.to_csv("final_result.csv", index=False)
