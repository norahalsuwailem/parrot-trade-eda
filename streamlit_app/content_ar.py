"""
المحتوى العربي للداشبورد: الترجمات، وأسماء الدول، ومعلومات الأنواع المشهورة.
البيانات نفسها تبقى بالإنجليزي، ونترجمها وقت العرض فقط.
"""
import re
import gettext
import pycountry

# ─────────────── ترجمة القيم ───────────────
SOURCE_AR = {
    "Wild-caught": "مصطاد من البرية",
    "Captive-bred": "مُربّى في الأسر",
    "Ranched": "مُربّى من بيض بري",
    "Confiscated": "مُصادَر",
    "Pre-Convention": "قبل الاتفاقية",
    "Unknown": "غير معروف",
}

DIET_AR = {
    "Frugivore": "آكل فواكه",
    "Granivore": "آكل حبوب",
    "Omnivore": "يأكل كل شيء",
    "Nectarivore": "آكل رحيق",
    "Herbivore": "آكل نباتات",
}

HABITAT_AR = {
    "Forest": "غابات",
    "Woodland": "أحراج",
    "Shrubland": "أراضي شجيرات",
    "Grassland": "مراعٍ",
    "Human Modified": "مناطق مأهولة",
    "Desert": "صحراء",
    "Unknown": "غير معروف",
}

FAMILY_AR = {
    "True parrots": "الببغاوات الحقيقية",
    "Cockatoos": "الكوكاتو",
    "NZ parrots (Kakapo, Kea)": "ببغاوات نيوزيلندا",
}

# عائلة CITES (اسم علمي) ← اسم العائلة في بياناتنا
CITES_FAMILY = {
    "Psittacidae": "True parrots",
    "Cacatuidae": "Cockatoos",
    "Strigopidae": "NZ parrots (Kakapo, Kea)",
}

GULF = {"SA": "السعودية", "AE": "الإمارات", "KW": "الكويت",
        "QA": "قطر", "BH": "البحرين", "OM": "عُمان"}

# ─────────────── أسماء الدول بالعربي ───────────────
_COUNTRY_OVERRIDES = {
    "XX": "غير معروف", "SA": "السعودية", "AE": "الإمارات", "US": "الولايات المتحدة",
    "GB": "المملكة المتحدة", "TW": "تايوان", "CD": "الكونغو الديمقراطية", "CG": "الكونغو",
    "KR": "كوريا الجنوبية", "KP": "كوريا الشمالية", "RU": "روسيا", "IR": "إيران",
    "SY": "سوريا", "VE": "فنزويلا", "BO": "بوليفيا", "TZ": "تنزانيا", "VN": "فيتنام",
    "LA": "لاوس", "MD": "مولدوفا", "CZ": "التشيك", "MK": "مقدونيا الشمالية",
    "PS": "فلسطين", "NL": "هولندا", "ZA": "جنوب أفريقيا", "CN": "الصين",
    "HK": "هونغ كونغ", "MO": "ماكاو", "BN": "بروناي", "FM": "ميكرونيسيا",
    "YU": "يوغوسلافيا", "CS": "تشيكوسلوفاكيا", "SU": "الاتحاد السوفيتي",
    "DD": "ألمانيا الشرقية", "AN": "جزر الأنتيل الهولندية",
}

try:
    _ar = gettext.translation("iso3166-1", pycountry.LOCALES_DIR, languages=["ar"])
except Exception:  # لو ما لقى الترجمة، نستخدم الإنجليزي
    _ar = None

_TASHKEEL = re.compile(r"[ً-ْ]")


def country_ar(code, fallback="غير معروف"):
    """كود الدولة (SA) ← اسمها بالعربي (السعودية)."""
    if not isinstance(code, str):
        return fallback
    if code in _COUNTRY_OVERRIDES:
        return _COUNTRY_OVERRIDES[code]
    c = pycountry.countries.get(alpha_2=code)
    if c is None:
        return code
    if _ar is None:
        return getattr(c, "common_name", c.name)
    name = _TASHKEEL.sub("", _ar.gettext(c.name))
    return name.split("،")[0].strip()


# ─────────────── الأنواع المشهورة ───────────────
# المصادر:
#  - الأعمار: askavet.com (Parrot Lifespan 2025, Dr Duncan Houston BVSc)
#  - صفات الكنيور: Wikipedia (Green-cheeked parakeet)
#  - الأكل في البيت: happybirds.hu (Parrot feeding and care)
# الأرقام تقريبية وتختلف من طير لطير.

HOME_DIET = ("خلطة حبوب أو حبيبات (pellets) كأساس، مع خضار طازجة يومياً، "
             "وفواكه بكميات قليلة. تجنّب الأفوكادو والبصل والأكل المملّح أو المسكّر.")

FEATURED = {
    "Pyrrhura molinae": dict(
        ar="كنيور الخدود الخضراء", emoji="💚", pet=True,
        origin="الأرجنتين، بوليفيا، البرازيل، باراغواي",
        length="26 سم", life="25–30 سنة مع رعاية جيدة", talk="قليل (صوت مبحوح)", noise="هادئ نسبياً",
        fact="أهدأ أنواع الكنيور، ومناسب للشقق. حنون وذكي."),
    "Aratinga solstitialis": dict(
        ar="الصن كنيور (الكنيور الشمسي)", emoji="🌞", pet=True,
        origin="شمال شرق أمريكا الجنوبية",
        length="30 سم", life="15–30 سنة", talk="قليل", noise="عالي جداً",
        fact="من أجمل الببغاوات ألواناً، بس صوته من أعلى الأصوات."),
    "Aratinga nenday": dict(
        ar="كنيور الناندي", emoji="🖤", pet=True,
        origin="باراغواي، الأرجنتين، البرازيل، بوليفيا",
        length="30 سم", life="15–30 سنة", talk="متوسط", noise="عالي",
        fact="كان اسمه في CITES «Nandayus nenday»، وصححناه في الدمج!"),
    "Agapornis fischeri": dict(
        ar="طائر الحب فيشر", emoji="🧡", pet=True,
        origin="تنزانيا",
        length="14 سم", life="10–25 سنة", talk="نادراً", noise="ثرثار",
        fact="أكثر ببغاء انباع في العالم: أكثر من 3 ملايين طير!"),
    "Agapornis personatus": dict(
        ar="طائر الحب المقنّع", emoji="🎭", pet=True,
        origin="تنزانيا",
        length="14 سم", life="10–25 سنة", talk="نادراً", noise="ثرثار",
        fact="اسمه من «القناع» الأسود على وجهه."),
    "Agapornis roseicollis": dict(
        ar="طائر الحب وردي الوجه", emoji="🌸", pet=True,
        origin="ناميبيا، أنغولا، جنوب أفريقيا",
        length="17 سم", life="10–25 سنة", talk="نادراً", noise="ثرثار",
        fact="أكثر ببغاء استوردته السعودية. وانشال من قوائم CITES، فتجارته الحقيقية أكبر."),
    "Psittacus erithacus": dict(
        ar="الكاسكو (الرمادي الأفريقي)", emoji="🩶", pet=True,
        origin="وسط أفريقيا",
        length="33 سم", life="40–60 سنة، وأحياناً أكثر", talk="ممتاز (من أذكى الطيور)", noise="متوسط",
        fact="صار في الملحق الأول (الأشد حماية) سنة 2016، وتجارته وقفت تقريباً بعدها."),
    "Psittacus timneh": dict(
        ar="التيمني", emoji="🩶", pet=True,
        origin="غرب أفريقيا",
        length="29 سم", life="40–60 سنة", talk="ممتاز", noise="متوسط",
        fact="كان يُعتبر نوعاً فرعياً من الكاسكو، وفُصل لنوع مستقل."),
    "Myiopsitta monachus": dict(
        ar="ببغاء الراهب (الكويكر)", emoji="🏠", pet=True,
        origin="الأرجنتين، الأوروغواي",
        length="29 سم", life="15–20 سنة", talk="جيد", noise="عالي",
        fact="الوحيد اللي يبني أعشاش جماعية من الأغصان. وأكبر شحنة في البيانات كانت منه: 124 ألف طير!"),
    "Alexandrinus krameri": dict(
        ar="الدرة", emoji="💚", pet=True,
        origin="أفريقيا وجنوب آسيا",
        length="40 سم مع الذيل", life="25–30 سنة", talk="جيد", noise="عالي",
        fact="الببغاء الأخضر المنتشر في مدن الخليج. اسمه القديم Psittacula krameri."),
    "Poicephalus senegalus": dict(
        ar="ببغاء السنغال", emoji="🧡", pet=True,
        origin="غرب أفريقيا",
        length="23 سم", life="25–50 سنة", talk="متوسط", noise="هادئ نسبياً",
        fact="صغير بس شخصيته قوية، وبطنه البرتقالي يميّزه."),
    "Amazona aestiva": dict(
        ar="الأمازون أزرق الجبهة", emoji="💙", pet=True,
        origin="البرازيل، باراغواي، بوليفيا، الأرجنتين",
        length="37 سم", life="40–70 سنة", talk="ممتاز", noise="عالي",
        fact="من أشهر الببغاوات المتكلمة في أمريكا الجنوبية."),
    "Ara ararauna": dict(
        ar="المكاو الأزرق والأصفر", emoji="💙", pet=True,
        origin="أمريكا الجنوبية",
        length="85 سم", life="35–80 سنة", talk="جيد", noise="عالي جداً",
        fact="يحتاج مساحة كبيرة جداً، ومنقاره يكسر جوز الهند!"),
    "Ara macao": dict(
        ar="المكاو القرمزي", emoji="❤️", pet=True,
        origin="أمريكا الوسطى والجنوبية",
        length="85 سم", life="35–80 سنة", talk="متوسط", noise="عالي جداً",
        fact="من أكبر الببغاوات وأكثرها ألواناً."),
    "Cacatua galerita": dict(
        ar="الكوكاتو ذو العرف الأصفر", emoji="👑", pet=True,
        origin="أستراليا وغينيا الجديدة",
        length="50 سم", life="40–70 سنة، وأحياناً أكثر", talk="جيد", noise="عالي جداً",
        fact="يرفع عرفه الأصفر لما يتحمّس أو يخاف."),
    "Cacatua goffiniana": dict(
        ar="كوكاتو غوفين", emoji="⚠️", pet=False,
        origin="جزر تانيمبار (إندونيسيا)",
        length="31 سم", life="40–70 سنة", talk="متوسط", noise="عالي",
        fact="من منطقة الخطر: موطنه حوالي 4,000 كم² بس، وانصاد منه آلاف."),
    "Cacatua ducorpsii": dict(
        ar="كوكاتو جزر سليمان", emoji="⚠️", pet=False,
        origin="جزر سليمان",
        length="31 سم", life="40–70 سنة", talk="متوسط", noise="عالي",
        fact="أول نوع في منطقة الخطر: أكثر من 23 ألف طير مصطاد من البرية."),
    "Cacatua alba": dict(
        ar="الكوكاتو الأبيض (المظلّة)", emoji="🤍", pet=True,
        origin="جزر الملوك الشمالية (إندونيسيا)",
        length="46 سم", life="40–70 سنة", talk="متوسط", noise="عالي جداً",
        fact="عرفه يفتح مثل المظلّة. ومن أنواع منطقة الخطر."),
    "Eos bornea": dict(
        ar="اللوري الأحمر", emoji="❤️", pet=False,
        origin="جزر الملوك (إندونيسيا)",
        length="31 سم", life="غير متوفر", talk="قليل", noise="عالي",
        fact="يأكل الرحيق بلسان يشبه الفرشاة. ومن أنواع منطقة الخطر."),
    "Strigops habroptila": dict(
        ar="الكاكابو", emoji="🦉", pet=False,
        origin="نيوزيلندا",
        length="60 سم", life="قد يتجاوز 60 سنة", talk="—", noise="—",
        fact="أثقل ببغاء في العالم، والوحيد اللي ما يطير. وما انباع ولا طير منه أبداً."),
}


# أسماء عربية لأنواع إضافية تطلع كثير في الرسومات (بدون بطاقة رعاية)
EXTRA_NAMES = {
    "Psephotus haematonotus": "الببغاء أحمر الردف",
    "Platycercus eximius": "الروزيلا الشرقي",
    "Lorius chlorocercus": "لوري جزر سليمان",
    "Lorius garrulus": "اللوري الثرثار",
    "Chalcopsitta cardinalis": "اللوري الكاردينال",
    "Psittacara acuticaudatus": "الكنيور أزرق التاج",
    "Psittacara mitratus": "الكنيور المقنّع",
    "Cyanoliseus patagonus": "الببغاء النقّار",
    "Agapornis lilianae": "طائر الحب ليليان",
    "Agapornis nigrigenis": "طائر الحب أسود الخد",
    "Eclectus roratus": "الإكلكتوس",
    "Nymphicus hollandicus": "الكوكتيل",
}


def name_ar(species):
    """الاسم العربي لو موجود، وإلا الاسم العلمي."""
    if species in FEATURED:
        return FEATURED[species]["ar"]
    return EXTRA_NAMES.get(species, species)


def display_name(species):
    """الاسم اللي يطلع في القوائم: عربي · علمي لو له اسم عربي، وإلا العلمي بس."""
    ar = name_ar(species)
    return f"{ar} · {species}" if ar != species else species


# ─────────────── صور حقيقية (Wikimedia Commons) ───────────────
# (اسم الملف في ويكيميديا، المصوّر، الرخصة)
PHOTOS = {
    "Pyrrhura molinae": ("Green-cheeked_Parakeet_(Pyrrhura_molinae_molinae),_Samaipata,_Bolivia_1.jpg", "jeanpaulboerekamps", "CC0"),
    "Aratinga solstitialis": ("Aratinga_solstitialis_-captive-two-8a.jpg", "Wayne Deeker", "CC BY 3.0"),
    "Aratinga nenday": ("2011-4_parrot_in_Strasbourg.jpg", "J. Patrick Fischer", "CC BY 3.0"),
    "Agapornis fischeri": ("Agapornis_fischeri_-Ueno_Zoo,_Japan_-three-8a-4c.jpg", "Takashi H", "CC BY-SA 2.0"),
    "Agapornis personatus": ("Agapornis_personatus_-Serengeti,_Tanzania-8.jpg", "Demetrius John Kessy", "CC BY 2.0"),
    "Agapornis roseicollis": ("Rosy-faced_lovebird_(Agapornis_roseicollis_roseicollis)_2.jpg", "Charles J. Sharp", "CC BY-SA 4.0"),
    "Psittacus erithacus": ("Perroquet_à_Yampopo_Beach_-_Douala.jpg", "Florettesokeng", "CC BY-SA 4.0"),
    "Psittacus timneh": ("Psittacus_erithacus_timneh-parrot_on_cage.jpg", "Peter Fuchs", "CC BY-SA 2.0"),
    "Myiopsitta monachus": ("Monk_parakeet_(Myiopsitta_monachus)_Santiago.jpg", "Charles J. Sharp", "CC BY-SA 4.0"),
    "Alexandrinus krameri": ("African_Rose-ringed_Parakeet,_Tendaba,_Gambia_1.jpg", "danielskatz", "CC BY 4.0"),
    "Poicephalus senegalus": ("Senegal-parrot-montage-2.jpg", "ThomHasi", "CC BY 2.5"),
    "Amazona aestiva": ("Turquoise-fronted_amazon_(Amazona_aestiva)_older_adult.JPG", "Charles J. Sharp", "CC BY-SA 4.0"),
    "Ara ararauna": ("Ara_ararauna_Luc_Viatour.jpg", "Luc Viatour", "CC BY 2.0"),
    "Ara macao": ("Scarlet_macaw_(Ara_macao_cyanopterus)_Copan.jpg", "Charles J. Sharp", "CC BY-SA 4.0"),
    "Cacatua galerita": ("Cacatua_galerita_Tas_2.jpg", "JJ Harrison", "CC BY-SA 3.0"),
    "Cacatua goffiniana": ("Cacatua_goffiniana,_Yamdena,_Tanimbar,_Indonesia_1.jpg", "james_birdtourasia", "CC0"),
    "Cacatua ducorpsii": ("Salomonenkakadu.jpg", "Sebastian Weingarten", "CC BY-SA 4.0"),
    "Cacatua alba": ("Cacatua_alba_-Bali_Bird_Park_-crest-8.jpg", "www.viajar24h.com", "CC BY 2.0"),
    "Eos bornea": ("Eos_bornea_-Taronga_Zoo,_Sydney,_Australia-8a_(1).jpg", "Robert Howie", "CC BY-SA 2.0"),
    "Strigops habroptila": ("Sirocco_full_length_portrait.jpg", "Department of Conservation (NZ)", "CC BY 2.0"),
}


def photo_url(species, width=500):
    """رابط الصورة من ويكيميديا (يحوّل تلقائياً للحجم المطلوب)."""
    from urllib.parse import quote
    if species not in PHOTOS:
        return None
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(PHOTOS[species][0])}?width={width}"


# ─────────────── لعبة: أي ببغاء يناسبك؟ ───────────────
# تقييم تقريبي مبني على بطاقات الأنواع فوق:
# size: 1 صغير · 2 متوسط · 3 كبير      noise: 1 هادئ ... 4 عالي جداً
# talk: 0 نادراً ... 3 ممتاز            life: أقصى عمر تقريبي (سنة)
# care: كم يحتاج وقت واهتمام كل يوم (1 قليل ... 3 كثير)   easy: مناسب لأول مرة؟
PET_PROFILE = {
    "Pyrrhura molinae":      dict(size=1, noise=1, talk=1, life=30, care=2, easy=True),
    "Aratinga solstitialis": dict(size=2, noise=4, talk=1, life=30, care=2, easy=True),
    "Aratinga nenday":       dict(size=2, noise=3, talk=2, life=30, care=2, easy=True),
    "Agapornis fischeri":    dict(size=1, noise=2, talk=0, life=20, care=1, easy=True),
    "Agapornis personatus":  dict(size=1, noise=2, talk=0, life=20, care=1, easy=True),
    "Agapornis roseicollis": dict(size=1, noise=2, talk=0, life=20, care=1, easy=True),
    "Psittacus erithacus":   dict(size=2, noise=2, talk=3, life=60, care=3, easy=False),
    "Psittacus timneh":      dict(size=2, noise=2, talk=3, life=60, care=3, easy=False),
    "Myiopsitta monachus":   dict(size=2, noise=3, talk=2, life=20, care=2, easy=True),
    "Alexandrinus krameri":  dict(size=2, noise=3, talk=2, life=30, care=2, easy=True),
    "Poicephalus senegalus": dict(size=1, noise=1, talk=2, life=50, care=2, easy=True),
    "Amazona aestiva":       dict(size=2, noise=3, talk=3, life=70, care=3, easy=False),
    "Ara ararauna":          dict(size=3, noise=4, talk=2, life=80, care=3, easy=False),
    "Ara macao":             dict(size=3, noise=4, talk=1, life=80, care=3, easy=False),
    "Cacatua galerita":      dict(size=3, noise=4, talk=2, life=70, care=3, easy=False),
    "Cacatua alba":          dict(size=3, noise=4, talk=1, life=70, care=3, easy=False),
}
