import sys,re
sys.stdout.reconfigure(encoding="utf-8")
from f import get,links
P=r"especialidad|especialitat|estudios|estudis|enseñanzas|ensenyaments|t[ií]tulo superior|grau|grado|m[aá]ster|interpretaci|itinerari|oferta"
for u in sys.argv[1:]:
    try: L=links(u,get(u))
    except Exception as e: print("==",u,"ERR",str(e)[:80]); continue
    S=sorted({(t[:55],l) for t,l in L if re.search(P,t+" "+l,re.I) and "#" not in l and t and not re.search(r"noticia|news|evento|calendar|matr[ií]cula|tasas|beca",t+l,re.I)})
    print("==",u,len(S)); [print("  ",t,"|",l[:140]) for t,l in S[:12]]
