#!/usr/bin/env node

// Visual Studio Code で Code Runner により
// /usr/bin/env node を実行しようとしてしまう場合は上の最初の行を削除すること

const http = require('http');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = 2000;

const re_type = /\.(css|jpg|ico)/;

function main(req, res){
    var path = req.url;
    var type = 'text/plain';

    type = 'text/html';
    if(result=path.match(re_type)){
        switch(result[1]){
        case 'css':
            type = 'text/css';
            break;
        case 'jpg':
            type = 'image/jpeg';
            break;
        case 'ico':
            type = 'image/x-icon';
            break;
        }
    }

    path='data'+path
    // どうしても 404 になってしまう場合は以下のコメントアウトを外してみる
    // path=require('path').resolve(__dirname,path);
    fs.readFile(path, function(err, data){
        if (err && err.code === 'ENOENT'){
            res.statusCode = 404;
            console.log(Date.now()+" "+req.url+" "+res.statusCode+" "+type);
            res.end(`404 not found: ${req.url}`);
        }else if (err && err.code === 'EISDIR'){
            req.url+='index.html';
            main(req, res);
        }else{
            res.statusCode = 200;
            // type = 'text/html';
            console.log(Date.now()+" "+req.url+" "+res.statusCode+" "+type);
            res.setHeader('Content-Type', type);
            res.end(data);
        }
    })
}

const server = http.createServer(main)

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
