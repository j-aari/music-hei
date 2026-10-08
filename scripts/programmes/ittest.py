"""ittest.py : aja IT-apuri listaan (code, url, taso) ja tulosta alat + epäilyttävät todisteet."""
import sys,collections,json
sys.stdout.reconfigure(encoding="utf-8")
from auto import IT
P=json.loads(sys.argv[1])
for code,url,lv in P:
    I={}
    try: IT(I,code,url,lv)
    except Exception as e: print("==",code,lv,"ERR",e); continue
    c=collections.defaultdict(set)
    for r in I.get(code,[]): c[r[0]].add(r[2])
    print("==",code,lv,len(c),"alaa |", "; ".join(f"{d}:{len(v)}" for d,v in c.items()))
    odd=[(d,x) for d,v in c.items() for x in v if len(v)<=1]
    if odd: print("   yksittäiset:",odd[:12])
