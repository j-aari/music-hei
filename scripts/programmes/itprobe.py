"""itprobe.py URL... : etsi italialaisen konservatorion triennio/biennio-listasivut."""
import sys,re
sys.stdout.reconfigure(encoding="utf-8")
from f import get,links
for u in sys.argv[1:]:
    try: L=links(u,get(u))
    except Exception as e: print("==",u,"ERR",e); continue
    S=sorted({(t[:60],l) for t,l in L if re.search(r"triennio|biennio|trienni|bienni|offerta formativa|corsi accademici|diploma accademico|ordinamentali|corsi di studio|didattica/corsi",t+" "+l,re.I) and "#" not in l and t})
    print("==",u,len(S)); [print("  ",t,"|",l) for t,l in S[:14]]
