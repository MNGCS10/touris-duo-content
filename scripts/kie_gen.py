#!/usr/bin/env python3
"""kie.ai image helper. Key is read from kie-config.json (never committed).
usage: kie_gen.py "<prompt>" out.png [--ref URL ...] [--ratio 2:3] [--quality medium]"""
import sys, json, time, urllib.request, argparse, os
p = argparse.ArgumentParser(); p.add_argument("prompt"); p.add_argument("out")
p.add_argument("--ref", action="append", default=[]); p.add_argument("--ratio", default="2:3")
p.add_argument("--quality", default="medium"); p.add_argument("--model", default="gpt-image/1.5-image-to-image")
a = p.parse_args()
key = json.load(open(os.environ.get("KIE_CONFIG", "kie-config.json")))["api_key"]
H = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
def call(url, body=None):
    r = urllib.request.Request(url, json.dumps(body).encode() if body else None, H)
    return json.load(urllib.request.urlopen(r, timeout=60))
inp = {"prompt": a.prompt, "aspect_ratio": a.ratio, "quality": a.quality}
if a.ref: inp["input_urls"] = a.ref
t = call("https://api.kie.ai/api/v1/jobs/createTask", {"model": a.model, "input": inp})["data"]["taskId"]
for _ in range(120):
    time.sleep(5)
    d = call("https://api.kie.ai/api/v1/jobs/recordInfo?taskId=" + t)["data"]
    if d["state"] == "success":
        u = json.loads(d["resultJson"])["resultUrls"][0]
        urllib.request.urlretrieve(u, a.out); print("saved", a.out); sys.exit(0)
    if d["state"] == "fail": print("fail", d.get("failMsg")); sys.exit(1)
print("timeout", t); sys.exit(2)
