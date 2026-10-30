# YouTube の公開ページから再生数を読み、data.json を更新する（APIキー不要）。
# 締め切りを過ぎたら値を確定（final）にして、それ以降は書き換えない。
import json, re, urllib.request
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
cfg = json.load(open("config.json", encoding="utf-8"))
data = json.load(open("data.json", encoding="utf-8"))
now = datetime.now(JST)

if data.get("final"):
    raise SystemExit(0)

req = urllib.request.Request(
    f"https://www.youtube.com/watch?v={cfg['videoId']}",
    headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "ja"},
)
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
m = re.search(r'"viewCount":"(\d+)"', html)
if not m:
    raise SystemExit("viewCount not found")

data = {
    "views": int(m.group(1)),
    "updated": now.isoformat(timespec="seconds"),
    "final": now >= datetime.fromisoformat(cfg["deadline"]),
}
json.dump(data, open("data.json", "w", encoding="utf-8"), ensure_ascii=False)
print(data)
