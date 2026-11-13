import http.server, os, re, sys
class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path=self.translate_path(self.path); r=self.headers.get('Range')
        if not r or not os.path.isfile(path): return super().send_head()
        size=os.path.getsize(path); m=re.match(r'bytes=(\d*)-(\d*)',r); a=int(m.group(1) or 0); b=int(m.group(2) or size-1); b=min(b,size-1)
        f=open(path,'rb'); f.seek(a); self.send_response(206); self.send_header('Content-Type',self.guess_type(path)); self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Range',f'bytes {a}-{b}/{size}'); self.send_header('Content-Length',str(b-a+1)); self.end_headers()
        import io; data=f.read(b-a+1); f.close(); return io.BytesIO(data)
    def log_message(self,*a): pass
os.chdir(sys.argv[1]); http.server.ThreadingHTTPServer(('',8765),H).serve_forever()
