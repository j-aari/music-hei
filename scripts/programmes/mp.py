"""Ohjelman nimi -> alat (disciplines.json) avainsanoilla, monikielinen. Ensin erityiset (jazz, pop, alte musik...)."""
import re
RULES = [
    ("jazz", r"jazz"),
    ("popular-music", r"\bpop|popular|rock\b|songwrit|e-gitarre|e-bass|electric (guitar|bass)|pop/rock|musique actuelle|musiques actuelles|lichte muziek|popul[aä]r|afro|urban|contemporary (popular|music performance)"),
    ("early-music", r"alte musik|historisch|historical|early music|baroque|barock|cembalo|harpsichord|clavecin|clavic[eé]mbalo|fortepiano|hammerklavier|blockfl|recorder|fl[uû]te [aà] bec|flauto dolce|viola da gamba|viole de gambe|gamba|laute|lute|luth|liuto|traversfl|oude muziek|musique ancienne|m[uú]sica antigua|musica antica|theorbo|violone"),
    ("folk", r"volksmusik|folk|traditional music|musique traditionnelle|m[uú]sica tradicional|kansanmusiik|folkemusik|folkmusik|hackbrett|zither|steirische|diatonische harmonika|ethno(?!musikolog)"),
    ("global-music", r"world music|global music|wereldmuziek|musiques du monde|maailmanmusiik|flamenco|latin"),
    ("church-music", r"kirkemusik|kyrkomusik|duchovní hudba|kirchenmusik|church music|musique sacr|musica sacra|kerkmuziek|kyrkomusik|kirkkomusiik|m[uú]sica sacra"),
    ("organ", r"varhan|orgel|organ\b|orgue|organo|[oó]rgano|urut"),
    ("piano", r"klaver|klavír|klavir|fortepian|klavier(?!kammer)|piano|pianoforte|fortepiano"),
    ("accordion", r"akkordeon|accordion|accord[eé]on|fisarmonica|acorde[oó]n|harmonika|bayan"),
    ("guitar", r"kytar|gitarre|guitar|guitare|chitarra|guitarra|gitaar|kitara"),
    ("harp", r"harpe|harfa|harfe|harp|harpe|arpa\b|harp"),
    ("strings", r"stryger|bratsch|fiol|housl|violu\b|kontrabas|stråk|jousi|viulu|sello|violin|viola(?! da)|violoncell|cello|kontrabass|double bass|contrabass|contrebasse|contrabbasso|contrabajo|streich|string|cordes|archi\b|cuerda|strijk|alto\b|violon\b|viool|altviool"),
    ("chamber-music", r"kammermusik|chamber music|musique de chambre|musica da camera|m[uú]sica de c[aá]mara|kamermuziek"),
    ("woodwind", r"fløjt|flöjt|fløyte|flétn|hoboj|obo\b|klarinet|fagot|træblæs|treblås|träblås|puupuhal|huilu|floete|fl[oö]te|flute|flûte|flauto|flauta|fluit|oboe|hautbois|klarinette|clarinet|clarinette|clarinetto|clarinete|klarinet|fagott|bassoon|basson|fagotto|fagot|saxo|holzbl|woodwind|bois\b|legni"),
    ("brass", r"messing|trompet|trubk|basun|lesní roh|trombon|vaskipuhal|käyrätorvi|trompete|trumpet|trompette|tromba|trompeta|trompet|posaune|trombone|tromb[oó]n|horn\b|cor\b|corno|trompa|hoorn|tuba|euphonium|blechbl|brass|cuivres|ottoni|metal"),
    ("percussion", r"slagtøj|slagverk|slagverk|bicí|lyömä|rummut|schlag|percussion|percusi[oó]n|percussioni|slagwerk|drum|batterie|batería|mallet|vibraphon|timpani|pauke"),
    ("vocal-opera", r"sang\b|sång|zpěv|laulu|operaakad|gesang|singing|voice|vocal|chant\b|canto|zang|opera|oper\b|op[eé]ra|lied\b|oratorium|sologesang"),
    ("conducting", r"direktion|dirigování|direksjon|kapellimest|kuoronjoh|dirig|conduct|direction d'orchestre|direction de ch|direzione|direcci[oó]n|directie|chorleit|choral conducting|kapellmeister"),
    ("composition", r"komposition|skladb|sävellys|kompos|composi|compositie|tonsatz|arrang|film scor|filmmusik|media music|medienkomp"),
    ("music-theory", r"musikteori|hørelære|musiikinteor|musiktheorie|music theory|th[eé]orie|teoria|teor[ií]a|muziektheorie|solfeg|analys|écriture|harmony|tonsatz"),
    ("music-education", r"musiklærer|musikpædagog|musikformidl|musikkpedagog|musiklärar|musiikkipedagog|musiikinopettaj|p[aä]dagog|pedagog|p[eé]dagog|didakt|educa|lehramt|teacher|enseign|insegn|docent|igp\b|emp\b|elementar|musikerzieh|schoolmusic|schulmusik|didattica|formation musicale|vermittlung"),
    ("music-technology", r"tonemester|lydtekn|lyddesign|ljudtekn|ljuddesign|elektronisk musik|musiikkiteknolog|äänitekn|computermusik|computer music|sound art|klangkunst|tonmeister|toningenieur|sound engineer|audio|recording|\bson\b|ingénieur du son|sonolog|elektronische musik|electronic music|electroacoust|elektroakust|music technology|musiktechnolog|sonic arts|acoustic|sound design"),
    ("music-production", r"produktion|production|produzione|producci[oó]n|producer|music business"),
    ("musicology", r"musikwissenschaft|musicolog|musikologie|muziekwetenschap|ethnomusikolog|ethnomusicolog|musikologia|musicologia|cultural study"),
    ("arts-management", r"management|kulturmanag|arts admin|entrepreneur|business|médiation culturelle"),
    ("music-therapy", r"therap"),
]
RX = [(d, re.compile(p, re.I)) for d, p in RULES]
def classify(name):
    out = [d for d, rx in RX if rx.search(name)]
    # jazz/pop/early-music -instrumentit: soitinala lisätään vain jos ei tyylisuuntaa (tyyli riittää suodattimeen)
    styled = {"jazz", "popular-music", "early-music"} & set(out)
    if styled:
        out = [d for d in out if d in styled or d in ("vocal-opera", "composition", "music-education", "conducting") and "jazz" not in out]
    return out
