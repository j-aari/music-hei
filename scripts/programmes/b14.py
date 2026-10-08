# Erä 14: Espanja (aja: python scripts/programmes/b14.py, sitten python scripts/add_programmes.py data/programmes_batches/14.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T, IT
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---
IT_PAGES = [
]
for code, ba, ma in IT_PAGES:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

CL = "strings woodwind brass percussion piano vocal-opera"; CLN = "Classical music programme; the page does not list the instruments, which are recorded as the usual orchestral instruments, piano and voice"

PI = "strings woodwind brass percussion piano organ guitar harp accordion"

for code, url, lv in [
    ("E  MADRID252", "https://katarinagurska.com/oferta-academica/grado-superior/", "BA"), ("E  MADRID252", "https://katarinagurska.com/oferta-academica/master/", "MA"),
    ("E  VALENCI67", "https://www.csmvalencia.es/grado/", "BA"),
    ("E  MALAGA02", "https://www.conservatoriosuperiormalaga.com/pages/especialidades", "BA"),
    ("E  BADAJOZ39", "https://csmbadajoz.es/?page_id=275", "BA"),
    ("E  MURCIA02", "https://csmmurcia.com/interpretacion/", "BA"),
    ("E  ZARAGOZ05", "https://csma.es/estudios-de-nivel-grado/", "BA")]:
    IT(I, code, url, lv)
R("E  VALENCI67", "music-technology", "MA", "Máster en Sonología aplicada y creación sonora", "http://www.sonologiacsmv.com/master.html")
for slug, d in [("composicion", "composition"), ("direccion", "conducting"), ("musicologia", "musicology"), ("pedagogia", "music-education")]:
    R("E  MURCIA02", d, "BA", slug.capitalize(), "https://csmmurcia.com/" + slug + "/")
R("E  CASTELL13", "early-music", "MA", "Màster en interpretació de música antiga i investigació de patrimoni", "https://www.conservatorisuperiorcastello.com/master-en-ensenyaments-artistics-en-interpretacio-de-musica-antiga-i-investigacio-de-patrimoni-")
R("E  CASTELL13", "composition music-technology", "MA", "Màster en ensenyaments artístics de composició multimèdia", "https://www.conservatorisuperiorcastello.com/master-en-ensenyaments-artistics-de-composicio-multimedia/")

c = "E  CASTELL13"; CA = "https://www.conservatorisuperiorcastello.com/es/planes-estudio-titulo-superior/"
R(c, "composition music-education conducting", "BA", "Grado: Composición, Pedagogía, Dirección", CA)
R(c, "vocal-opera piano guitar strings woodwind brass percussion", "BA", "Grado – Interpretación: Canto, Instrumentos Orquesta Sinfónica, Piano, Guitarra", CA)
R(c, "early-music", "BA", "Grado – Música Antigua; Interpretación: Clave", CA)
R(c, CL, "MA", "Máster en Interpretación Musical e Investigación Aplicada", "https://www.conservatorisuperiorcastello.com/master-interpretacio-musical-i-recerca-aplicada/", CLN)
c = "E  CORDOBA04"; CD = "https://csmcordoba.com/saludo-del-director/"
R(c, "composition", "BA", "Composición", CD)
R(c, CL + " guitar", "BA", "Interpretación (incl. itinerario de guitarra)", "https://www.csmcordoba.com/especialidad-interpretaci%C3%B3n-itinerario-de-guitarra", CLN)
R(c, "global-music", "BA", "Flamenco: Cante flamenco, Guitarra flamenca, Flamencología", "https://csmcordoba.com/wp-content/uploads/2025/07/Guitarraflamenca2526GD.pdf")
c = "E  SEVILLA04"; SE = "https://consev.es/wp-content/uploads/2015/03/folleto-puertas-abiertas-consev-2015.pdf"
R(c, "composition conducting musicology", "BA", "Composición; Dirección de coro; Musicología", SE)
R(c, "vocal-opera guitar organ strings woodwind brass percussion", "BA", "Interpretación: Canto, Guitarra, Instrumentos sinfónicos, Órgano", "https://consev.es/wp-content/uploads/2012/06/Plan-Estudios-LOE-Consev-2012.pdf")
R(c, "early-music", "BA", "Interpretación: Instrumentos de la música antigua", "https://consev.es/wp-content/uploads/2012/06/Plan-Estudios-LOE-Consev-2012.pdf")
c = "E  OVIEDO03"; OV = "http://www.consmupa.es/index.php/planes-de-estudios"
R(c, "accordion vocal-opera organ strings woodwind brass percussion guitar piano", "BA", "Interpretación: Acordeón, Canto, Clave-Órgano, Cuerda de arco-Viento-Percusión, Guitarra, Piano", OV)
R(c, "early-music", "BA", "Interpretación: Clave", OV)
R(c, "folk", "BA", "Interpretación: Instrumentos de la música tradicional y popular de Asturias (gaita)", OV)
R(c, "composition music-education conducting", "BA", "Composición; Pedagogía; Dirección", OV)
c = "E  JAEN07"; JA = "https://www.csmjaen.es/es/"
R(c, "global-music", "BA", "Flamenco: Guitarra flamenca, Cante flamenco", JA + "flamenco")
R(c, "guitar vocal-opera", "BA", "Interpretación: Guitarra, Canto", JA + "planes-de-estudios")
R(c, "arts-management", "BA", "Producción y Gestión de Música y Artes Escénicas", JA + "planes-de-estudios")

c = "E  LA-CORU05"; CO = "https://csmcoruna.com/en/especialidades/"
R(c, "accordion harp vocal-opera woodwind strings guitar percussion piano brass", "BA", "Interpretación: acordeón, arpa, canto, viento madera, cuerda, guitarra, percusión, piano, viento metal", CO)
R(c, "jazz composition music-education conducting", "BA", "Interpretación – Jazz; Composición; Pedagogía; Dirección", CO)
c = "E  LAS-PAL18"; CN = "http://www.consmucan.es/erasmus/erasmus-estudiantes-incoming/bachelor-of-music-in-musicology"
R(c, CL + " composition musicology music-education", "BA", "Composición, Interpretación, Musicología, Pedagogía", CN, CLN)
c = "E  SALAMAN03"; CY = "https://coscyl.com/en/"
R(c, CL + " composition musicology folk", "BA", "Título Superior: Interpretación, Composición, Musicología y Etnomusicología", CY + "planes-de-estudios/superior-infogeneral/", CLN)
R(c, CL + " chamber-music", "MA", "Máster en Enseñanzas Artísticas de Interpretación Musical (Solista, Música de Cámara, Orquesta)", CY + "master/", CLN)
c = "E  ALBACET19"; AL = "https://csmclm.com/jornada-de-puertas-abiertas/"
R(c, "woodwind brass strings guitar percussion piano composition conducting", "BA", "Interpretación (clarinete … violonchelo); Dirección de banda; Composición", AL)
c = "E  PAMPLON17"; PA = "https://csmn.educacion.navarra.es/web1/informacion/prueba-de-acceso/"
R(c, CL + " jazz composition music-education musicology", "BA", "Interpretación (clásica y jazz), Composición, Pedagogía (clásico y jazz), Musicología", PA, CLN)
c = "E  VIGO03"; VI = "https://www.conservatoriosuperiorvigo.com/estudios/"
R(c, "vocal-opera composition strings guitar folk musicology music-education percussion piano", "BA", "Canto, Composición, Corda frotada, Guitarra, Instrumentos da música tradicional e popular, Musicoloxía, Pedagoxía, Percusión, Piano", VI)

c = "E  MADRID222"; MC = "https://musicacreativa.com/centro-superior/"
R(c, "jazz popular-music", "BA", "Grado en Interpretación de Músicas Actuales y Jazz", MC)
R(c, "composition", "BA", "Grado en Composición para Medios Audiovisuales", MC)
R(c, "global-music folk", "MA", "Máster en Interpretación de Flamenco; Máster en Folklore de la Península Ibérica", MC)
c = "E  SANTAND38"; RS = "https://www.escuelasuperiordemusicareinasofia.es/"
R(c, "vocal-opera woodwind brass strings piano", "BA MA", "Grado en Enseñanzas Artísticas Superiores de Música; Máster en Interpretación Musical (cátedras: canto, clarinete, contrabajo, fagot, flauta, oboe, piano, trompa, trompeta, viola, violín, violonchelo)", RS + "catedras-y-profesorado/")
R(c, "composition conducting", None, "Diploma en Composición; Diploma de Postgrado en Dirección de Orquesta (títulos propios)", RS + "plan-estudio/", "School's own diplomas, not official degrees")
c = "E  BARCELO137"; TM = "https://tallerdemusics.com/ca/superior/"
R(c, "jazz popular-music", "BA", "Grau: Interpretació de jazz i música moderna (incl. veu-songwriting)", TM)
R(c, "global-music", "BA", "Grau: Interpretació de flamenc (cante, guitarra)", TM)
R(c, "composition", "BA", "Grau: Composició", TM)
R(c, "music-education", "MA", "Màster oficial en Pedagogia musical", TM)
c = "E  BARCELO30"; LI = "https://www.conservatoriliceu.es/superior/"
R(c, CL + " guitar", "BA MA", "Grau / Màster: Interpretació en música clàssica i contemporània", LI + "titol-superior-musica/", CLN)
R(c, "jazz popular-music", "BA MA", "Grau / Màster: Interpretació en jazz i música moderna", LI + "masters/jazz-musica-moderna/")
R(c, "global-music", "BA", "Grau: Interpretació en guitarra flamenca", LI + "titol-superior-musica/")
R(c, "composition music-education", "BA", "Grau: Composició; Pedagogia", LI + "titol-superior-musica/")
R(c, "chamber-music composition vocal-opera", "MA", "Màsters: Música de cambra; Composició aplicada als mitjans audiovisuals i escènics; Òpera", LI + "masters/")
c = "E  PALMA27"; PB = "https://conservatorisuperior.com/"
R(c, CL, "BA", "Interpretació clàssica", PB + "interpretacio-classica/", CLN)
R(c, "jazz", "BA", "Interpretació jazz", PB + "interpretacio-jazz/")
R(c, "composition music-education musicology", "BA", "Composició; Pedagogia; Musicologia", PB + "pedagogia/")
c = "E  SAN-SEB01"; MK = "https://musikene.eus/"
R(c, "accordion harp vocal-opera woodwind strings guitar organ percussion piano brass folk", "BA", "Interpretación (acordeón … txistu …)", MK + "musikene-abre-el-plazo-de-inscripcion-a-grado-para-el-curso-2026-2027/?lang=en")
R(c, "jazz", "BA MA", "Interpretación Jazz; Máster de Interpretación-Jazz", MK + "masters/?lang=en")
R(c, "composition music-education conducting", "BA", "Composición; Pedagogía; Dirección (coro, orquesta)", MK + "musikene-abre-el-plazo-de-inscripcion-a-grado-para-el-curso-2026-2027/?lang=en")
R(c, CL, "MA", "Máster de Interpretación Musical; Máster de Estudios Orquestales", MK + "masters/masters-in-music-performance/?lang=en", CLN)
R(c, "arts-management composition", "MA", "Máster en Mediación, Gestión y Difusión Musical; Máster de Creación de la Música Contemporánea", MK + "masters/?lang=en")

c = "E  MADRID27"; RC = "https://rcsmm.eu/"
R(c, "strings woodwind brass percussion harp", "BA", "Interpretación – A. Instrumentos de orquesta y percusión", RC + "interpretacion")
R(c, "accordion guitar piano", "BA", "Interpretación – B. Instrumentos polifónicos no orquestales", RC + "interpretacion")
R(c, "early-music", "BA", "Interpretación – C. Música antigua", RC + "interpretacion")
R(c, "composition", "BA", "Composición", RC + "composicion")
R(c, "conducting", "BA", "Dirección", RC + "direccion")
R(c, "musicology", "BA", "Musicología", RC + "musicologia")
R(c, "music-education", "BA", "Pedagogía", RC + "pedagogia")
R(c, "arts-management", "BA", "Producción y Gestión", RC + "produccion-gestion")
R(c, "music-technology", "BA", "Sonología", RC + "sonologia")
R(c, "piano", "MA", "Máster en Pianista Acompañante y Repertorista", RC + "master/masterrepertorista/?m=34&s=155")
R(c, CL, "MA", "Máster en Interpretación e Investigación Performativa de Música Española", RC + "master-ensenanzas-artisticas-interpretacion-e-investigacion-performativa-musica-espanola", CLN)
c = "E  GRANADA04"; GR = "https://conservatoriosuperiorgranada.com/plan-de-estudios-2/"
R(c, "strings woodwind brass percussion vocal-opera piano guitar", "BA", "Interpretación: Sinfónicos, Canto, Piano, Guitarra", GR)
R(c, "composition music-education conducting", "BA", "Composición; Pedagogía; Dirección de orquesta", GR)
R(c, "global-music", "BA", "Flamenco – Guitarra flamenca", GR)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {
    "E  PALMA25": "ESADIB is the Balearic school of dramatic art; it teaches voice and singing within acting, but offers no degree programmes in music.",
}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "14.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
