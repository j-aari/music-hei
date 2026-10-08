"""probe.py URL... : etsi ohjelmalistasivuja (monikielinen)."""
import sys,re
sys.stdout.reconfigure(encoding="utf-8")
from f import get,links
P=r"bachelor|master|bakalaur|magistr|studij|study|studie|opleiding|programm|degree|course|studiengang|uddannel|utdanning|kierunk|studia|study-programmes|studieprogram|fakult|katedr"
for u in sys.argv[1:]:
    try: L=links(u,get(u))
    except Exception as e: print("==",u,"ERR",e); continue
    S=sorted({(t[:60],l) for t,l in L if re.search(P,t+" "+l,re.I) and "#" not in l and t})
    print("==",u,len(S)); [print("  ",t,"|",l[:150]) for t,l in S[:18]]
