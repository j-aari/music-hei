# Erä 3: Suomen AMK:t ja Ranska (aja: python scripts/programmes/b03.py, sitten python scripts/add_programmes.py data/programmes_batches/03.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "SF HELSINK41"; MP = "https://www.metropolia.fi/fi/opiskelu-metropoliassa/amk-tutkinnot/musiikki"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK): soiton- ja laulunopetus, klassinen tai pop/jazz-musiikki", MP)
R(c, "piano strings guitar woodwind brass vocal-opera", "BA", "Musiikkipedagogi (AMK), klassinen musiikki: piano, jousisoittimet, kitara, puhaltimet, laulu", MP)
R(c, "jazz popular-music", "BA", "Muusikko (AMK): musiikin esittäminen, pop/jazz-musiikki; Musiikkipedagogi (AMK), pop/jazz", MP)
R(c, "music-production composition", "BA", "Muusikko (AMK): musiikin tekeminen ja tuottaminen, pop/jazz-musiikki", MP)
R(c, "music-education", "MA", "Musiikkipedagogi ja muusikko (ylempi AMK)", MP, "Master's degree of a university of applied sciences (ylempi AMK)")

c = "SF KUOPIO08"; SV = "https://www.savonia.fi/opiskele-tutkinto/tutkinnot-ja-hakeminen/amk-ja-yamk-tutkinnot-tarjonta/musiikkipedagogi-amk-paivatoteutus/"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK) – klassisen musiikin tai rytmimusiikin painotus", SV)
R(c, "jazz popular-music", "BA", "Musiikkipedagogi (AMK) – rytmimusiikin painotus (jazz, pop/rock)", SV)

c = "SF JYVASKY11"; JK = "https://www.jamk.fi/fi/hae-opiskelemaan/amk-tutkinto/musiikkipedagogi-on-musiikin-moniosaaja"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK) – klassinen ja pop/jazz", JK)
R(c, "jazz popular-music", "BA", "Musiikkipedagogi (AMK) – pop/jazz-instrumentit", JK)
R(c, "kantele", "BA", "Musiikkipedagogi (AMK) – klassiset instrumentit, mm. kantele", JK)
c = "SF OULU11"; OA = "https://oamk.fi/koulutus/ammattikorkeakoulututkinnot/musiikkipedagogi-amk/"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK)", OA)
R(c, "jazz popular-music", "BA", "Musiikkipedagogi (AMK) – rytmimusiikki: laulu, piano, sähkökitara, sähköbasso, rummut, saksofoni, trumpetti, pasuuna", OA)
R(c, "music-technology music-production", "BA", "Musiikkipedagogi (AMK) – musiikkiteknologian osaamispolku (musiikkituotanto ja studiotyöskentely)", OA)
c = "SF KOKKOLA05"; CE = "https://net.centria.fi/koulutukset/musiikkipedagogi-amk/"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK) – suuntautumisvaihtoehdot klassinen ja rytmimusiikki", CE)
R(c, "jazz popular-music", "BA", "Musiikkipedagogi (AMK) – rytmimusiikki", CE)

c = "SF TURKU05"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK) – soiton- ja laulunopettajat, musiikin hahmotusaineiden opettajat", "https://www.turkuamk.fi/koulutukset/musiikkipedagogi-amk/")
R(c, "music-education", "MA", "Musiikkipedagogi (ylempi AMK)", "https://www.turkuamk.fi/fi/tutkinnot-ja-opiskelu/tutkinnot/musiikkipedagogi-ylempi-amk/", "Master's degree of a university of applied sciences (ylempi AMK)")
c = "SF TAMPERE06"; TM = "https://sites.tuni.fi/tamkmusiikki/"
R(c, "music-education", "BA", "Musiikkipedagogi (AMK): instrumenttipedagogi, musiikin hahmotustaitojen pedagogi", TM + "musiikin-tutkinto-ohjelma-musiikkipedagogi/")
R(c, "conducting", "BA", "Musiikkipedagogi (AMK): kuoronjohtaja tai orkesterinjohtaja", TM + "musiikin-tutkinto-ohjelma-musiikkipedagogi/")
R(c, "composition", "BA", "Muusikko (AMK): esittävä ja luova säveltaide", TM + "tutkinto-ohjelmat/")
R(c, "music-education", "MA", "Musiikin ylempi tutkinto-ohjelma: Musiikkipedagogi (ylempi AMK), Muusikko (ylempi AMK)", TM + "musiikin-ylempi-tutkinto-ohjelma-musiikkipedagogi/", "Master's degree of a university of applied sciences (ylempi AMK)")

c = "F  LYON24"
for n in range(1, 7):
    A(I, c, "https://cnsmd-lyon.fr/formations-musique/" + ("" if n == 1 else f"page/{n}/"), r"/formations-musique/[a-z]", drop=r"Artist Diploma|/page/", quiet=True)
R(c, "composition", "MA", "Master CoPeCo; Master InMICS (composition)", "https://cnsmd-lyon.fr/formations-musique/master-copeco/")

c = "F  STRASBO51"; HE = "https://www.hear.fr/musique/"
R(c, "piano accordion organ guitar harp strings woodwind brass percussion vocal-opera composition", "BA", "Licence CIM / DNSPM (dominantes enseignées)", HE + "licence-dnspm/")
R(c, "piano accordion organ guitar harp strings woodwind brass percussion vocal-opera composition", "MA", "Master CIM (dominantes enseignées)", HE + "master/")
R(c, "jazz", "BA MA", "Jazz et musiques improvisées (DNSPM, Master CIM)", HE + "dominantes-enseignees-3/")
R(c, "early-music", "BA MA", "Musique ancienne: chant baroque, clavecin, claviers historiques, flûte à bec, traverso, luth, viole de gambe, violon et violoncelle baroques", HE + "dominantes-enseignees-3/")
R(c, "music-technology", "BA MA", "Composition et musiques électroniques; Composition électroacoustique et temps réel", HE + "dominantes-enseignees-3/")
R(c, "chamber-music", "MA", "Musique de chambre (master CIM uniquement)", HE + "dominantes-enseignees-3/")
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", HE + "de/")
R(c, "music-education", "MA", "Master Pédagogie (MEEF)", HE + "master-meef/")
c = "F  LILLE71"; ES = "https://www.esmd.fr/musique/"
R(c, "strings woodwind brass piano guitar harp percussion vocal-opera", "BA", "DNSPM classique à contemporain", ES + "diplome-national-superieur-professionnel-de-musicien/")
R(c, "jazz popular-music", "BA", "DNSPM jazz et musiques improvisées; musiques actuelles amplifiées", ES + "diplome-national-superieur-professionnel-de-musicien/")
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", ES + "diplome-d-etat-de-professeur-de-musique/")

c = "F  DIJON32"; DJ = "https://www.esmbourgognefranchecomte.fr/fr/formation-superieure-initiale/"
R(c, "vocal-opera", "BA", "DNSPM domaine classique à contemporain – chanteur et instrumentiste", DJ + "le-diplome-national-superieur-professionnel-de-musicien-dnspm")
R(c, "early-music", "BA", "DNSPM domaine musique ancienne – chanteur et instrumentiste", DJ + "le-diplome-national-superieur-professionnel-de-musicien-dnspm")
R(c, "popular-music", "BA", "DNSPM domaine musiques actuelles amplifiées", DJ + "le-diplome-national-superieur-professionnel-de-musicien-dnspm")
R(c, "conducting", "BA", "DNSPM Direction d'ensembles vocaux", DJ + "le-diplome-national-superieur-professionnel-de-musicien-dnspm")
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", DJ + "le-diplome-detat-de-professeur-de-musique-de")

c = "F  BORDEAU62"; RS = "https://resonances-na.eu/"; RSN = "The school now operates as RésoNAnces (resonances-na.eu)"
R(c, "strings piano guitar percussion", "BA", "DNSPM: cordes frottées, piano, guitare, percussions", RS + "dnspm/", RSN)
R(c, "popular-music", "BA", "DNSPM: musiques actuelles amplifiées", RS + "maa/")
R(c, "early-music", "BA", "DNSPM: musique ancienne", RS + "musique-ancienne/")
R(c, "folk", "BA", "DNSPM: musiques traditionnelles", RS + "musiques-traditionnelles/")
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", RS + "de-musique/")
R(c, "chamber-music", "MA", "Master universitaire : musique, recherche et pratiques d’ensemble", RS + "accueil/master-musique/")
c = "F  BOBIGNY05"; PS = "https://polesup93.fr/"
R(c, "vocal-opera piano guitar strings percussion", "BA", "DNSPM classique à contemporain: chant, piano, guitare, violon, violoncelle, percussions", PS + "dnspm-formation-initiale")
R(c, "jazz", "BA", "DNSPM jazz et musiques improvisées", PS + "dnspm-formation-initiale")
R(c, "conducting", "BA", "DNSPM direction d’ensembles vocaux et instrumentaux", PS + "dnspm-formation-initiale")
R(c, "music-education", "BA", "Diplôme d’État (articulé avec le DNSPM; formation professionnelle)", PS + "diplome-detat-articule-avec-le-dnspm")
c = "F  PARIS365"; PB = "https://www.pspbb.fr/"
R(c, "composition music-technology", "BA", "DNSPM création musicale contemporaine (composition instrumentale, composition électroacoustique)", PB + "musique/diplome-national-superieur-professionnel-de-musicien-dnspm-diplome-d-etat-de")
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", PB + "musique/parcours-de-diplome-d-etat-de-professeur-de-musique-1963")
R(c, "composition", "MA", "Master Improvisation et création musicale", PB + "musique/master/parcours-master-improvisation-et-creation-musicale-niveau-7-du-rncp-1964")
R(c, "strings", "MA", "Master Recherche et Pratique, option pratiques orchestrales cordes", PB + "master-recherche-et-pratique-option-pratiques-orchestrales-cordes-3531")
c = "F  NANTES72"; LP = "https://www.lepontsuperieur.eu/musique/cursus-et-diplomes/"
R(c, "music-education", "BA", "DE professeur de musique (formation initiale)", LP + "de-professeur-de-musique-formation-initiale/")
c = "F  AIX-PRO29"
R(c, "music-education", "BA", "Diplôme d’État de professeur de musique", "https://iesm.fr/diplome-detat-de-professeur-de-musique-de/")
R(c, "folk", "BA", "Diplôme d’État de professeur de musiques et chants traditionnels de Corse et Méditerranée", "https://iesm.fr/formations-inscriptions/")

METHOD = "Field-level collection as in batch 1 (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "03.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
