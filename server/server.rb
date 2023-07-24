#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

# Visual Studio Code で Code Runner により
# /usr/bin/env ruby を実行しようとしてしまう場合は上の最初の行を削除すること

# どうしても 404 になってしまう場合は以下のコメントアウトを外してみる
# Dir.chdir(File.expand_path(File.dirname(__FILE__)))

require "socket"
server=TCPServer.new(2000) #2000番ポート

def main(client)
    path=nil
    while l=client.gets #1行ずつ読み込み
        l=l.strip #改行削除
        if l.empty?
            if path=="/"
                path="/index.html"
            end
            if File.exist?("data"+path)
                content=open("data"+path,"rb").read
                response="200 OK"
                type="text/html"
            else
                content="Not found"
                response="404 Not Found"
                type="text/html"
            end
            data=<<EOF
HTTP/1.1 #{response}
Content-Type: #{type}

EOF
            data+=content
            print Time.now.to_s+" "+path+" "+response+" "+type+"\n"
            client.write(data)
            break
        elsif l=~/^GET (\S+)/ #GETメソッドからパスを取り出す
            path=$1
        end
    end
    client.close
end

client=server.accept
main(client)

# Local Variables:
# ruby-indent-level: 4
# End:
