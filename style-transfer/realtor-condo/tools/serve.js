const http=require('http'),fs=require('fs'),path=require('path');const root=process.argv[2];
const T={'.html':'text/html','.mp4':'video/mp4','.mp3':'audio/mpeg','.js':'text/javascript','.json':'application/json'};
http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(!fs.existsSync(f)){r.writeHead(404);return r.end();}
const st=fs.statSync(f),ty=T[path.extname(f)]||'application/octet-stream',rg=q.headers.range;
if(rg){const [a,b]=rg.replace('bytes=','').split('-');const s=+a,e=b?+b:st.size-1;r.writeHead(206,{'Content-Range':`bytes ${s}-${e}/${st.size}`,'Accept-Ranges':'bytes','Content-Length':e-s+1,'Content-Type':ty});fs.createReadStream(f,{start:s,end:e}).pipe(r);}
else{r.writeHead(200,{'Content-Length':st.size,'Content-Type':ty,'Accept-Ranges':'bytes'});fs.createReadStream(f).pipe(r);}}).listen(8765);
