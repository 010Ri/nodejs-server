#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Visual Studio Code で Code Runner により
# /usr/bin/env python を実行しようとしてしまう場合は上の最初の行を削除すること

import socket, re, os, datetime, time, threading

# どうしても 404 になってしまう場合は以下のコメントアウトを外してみる
# os.chdir(os.path.dirname(__file__))

re_get=re.compile(r"^GET (\S+)")
re_type=re.compile(r"\.(css|jpg|ico)$")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # おまじない
server.bind(('127.0.0.1', 2000))
server.listen(1)

######################################################################
# main
######################################################################
def main(client):
    fp=client.makefile()
    path=""
    for l in fp: #1行読み込み
        l=l.strip() #改行削除
        if len(l)==0:
            if path=="/":
                path="/index.html"
            if os.path.isfile("data"+path):
                with open("data"+path, 'rb') as f:
                    content = f.read()
                response="200 OK"
                type="text/html"
            else:
                content=bytes("Not found","ascii")
                response="404 Not Found"
                type="text/html"
            data="HTTP/1.1 "+response+"\n"
            data+="Content-Type: "+type+"\n"
            data+="\n"
            data=data.encode("ascii") + content
            client.send(data)
            print(datetime.datetime.now().isoformat(" ")+" "+path+" "+response+" "+type)
            path=""
            break
        else:
            match=re_get.search(l)
            if match:
                path=match.groups()[0]
    client.close()
######################################################################

client, addr = server.accept()
main(client)
