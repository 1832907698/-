#!/usr/bin/env python
# --coding:utf-8--

import requests
import json
import os
import base64
from Crypto.Cipher import AES
import time
import sys
from math import ceil

userId = ''
results = []
playList_ids = []
url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_29393669/?csrf_token='


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey.encode(), AES.MODE_CBC, b'0102030405060708')
    ciphertext = encryptor.encrypt(text.encode())
    ciphertext = base64.b64encode(ciphertext).decode()
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(text.encode('utf-8').hex(), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return base64.b16encode(os.urandom(size)).decode()[:16]


def dataGenerator(limit, offset):
    text = {
        'limit': limit,
        'offset': offset
    }
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    return {
        'params': encText,
        'encSecKey': encSecKey
    }


def pre_steps(userId):
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    text = {
        'uid': userId,
        'type': '0'
    }
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    req = requests.post('http://music.163.com/weapi/v1/play/record?csrf_token=', headers=headers, data=data)
    for song in req.json().get('allData', []):
        playList_ids.append({'id': song['song']['id'], 'name': song['song']['name']})
    print("列表共{}条\n".format(len(playList_ids)))


def number_of_comments(url):
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    data = dataGenerator(1, 0)
    req = requests.post(url, headers=headers, data=data)
    print("总评论数:{}".format(req.json()['total']))
    return req.json()['total']


def search_start(limit, offset):
    for song in playList_ids:
        comments_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token='.format(song['id'])
        song_name = song['name']
        _offset = offset

        totalComments = number_of_comments(comments_url)

        while _offset < totalComments:
            time.sleep(2)
            sys.stdout.write("\r正在查询歌曲: {}, 进度: {}/{}, 当前共找到评论: {}条".format(
                song_name, _offset, totalComments, len(results)))
            sys.stdout.flush()

            headers = {
                'Cookie': 'appver=1.5.0.75771;',
                'Referer': 'http://music.163.com/'
            }
            data = dataGenerator(limit, _offset)
            try:
                req = requests.post(comments_url, headers=headers, data=data)
            except requests.exceptions.ConnectionError as e:
                print('\n网络异常,自动重试..\n')
                continue

            index = 0
            for content in req.json().get('comments', []):
                index += 1
                if content['user']['userId'] == int(userId):
                    ab_path = os.path.abspath('.')
                    full_path = os.path.join(ab_path, 'results.txt')
                    with open(full_path, 'a+', encoding='utf-8') as fil:
                        fil.write('{}说: {}, 位于歌曲: {}({}页)\n'.format(
                            content['user']['nickname'], content['content'], song_name, ceil((_offset + index) / 20)))
                    results.append(content['content'])
            _offset += limit
        print("\n\n")
    print("全部完成! 结果总数 = {}".format(len(results)))


if __name__ == '__main__':
    userId = input("请输入网易云用户ID: ")
    pre_steps(userId)
    search_start(1000, 0)
