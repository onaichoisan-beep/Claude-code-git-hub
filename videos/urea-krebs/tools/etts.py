import asyncio, json, os, ssl, sys
import edge_tts, edge_tts.communicate as ec
ec._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
async def main(voice, text, out, rate="+0%", pitch="+0Hz"):
    c = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=os.environ.get("HTTPS_PROXY"), boundary="WordBoundary")
    words = []
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"text": ch["text"], "start": ch["offset"] / 1e7, "end": (ch["offset"] + ch["duration"]) / 1e7})
    json.dump(words, open(out + ".words.json", "w"), ensure_ascii=False, indent=0)
a = sys.argv
asyncio.run(main(a[1], open(a[2]).read().strip(), a[3], *(a[4:6])))
