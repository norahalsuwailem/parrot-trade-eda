"""
🦜 جواز سفر الببغاء: قصة تجارة الببغاوات حول العالم، يحكيها تسوكي
نوره السويلم · مشروع الوحدة الثالثة · أكاديمية طويق

التشغيل:  streamlit run app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import streamlit as st

from content_ar import (CITES_FAMILY, DIET_AR, FAMILY_AR, FEATURED, GULF, HABITAT_AR,
                        HOME_DIET, PET_PROFILE, SOURCE_AR, _as_data_uri, country_ar,
                        display_name, has_photo, name_ar, photo_credit, photo_url)
from parrot_art import parrot_svg

st.set_page_config(page_title="جواز سفر الببغاء 🦜", page_icon="🦜", layout="wide",
                   initial_sidebar_state="collapsed")

IMAGES = Path(__file__).parent / "images"
TSUKI = _as_data_uri(str(IMAGES / "tsuki.jpg"))          # صورة تسوكي (كنيوري)
TSUKI_FACE = _as_data_uri(str(IMAGES / "tsuki_face.jpg"))

# ═══════════════════════════ الألوان: فاتح وداكن ═══════════════════════════
LIGHT = dict(BG="#EEF6EF", CARD="#FFFFFF", LINE="#E3EDE5", TEXT="#23312B", SOFT="#4A5A52", MUTED="#66756D",
             GREEN="#2E7D46", DEEP="#1F5C33", WILD="#E8553F", CAPT="#6FB07F", GREY="#C9D3CC", GOLD="#E0A800",
             BLUE="#4DA8DA", BUBBLE="#FFF6DD", MINT="#EEF6EF", CORAL_BG="#FFF1EE", CORAL="#C9402C",
             DOT_OFF="#CFE7D4", CHIP="#D5E3D8", GRID="#E6EEE8", F=["#FFD86B", "#FF9B85", "#8FD0A0", "#8CC6EA"],
             MAP=["#E3F1E6", "#A9D8B4", "#6FB07F", "#E0A800", "#E8553F"], PLOT="plotly_white")
DARK = dict(BG="#14201B", CARD="#1C2A24", LINE="#2C3D35", TEXT="#EEF3EF", SOFT="#C3D1C8", MUTED="#9BAEA2",
            GREEN="#8CD3A0", DEEP="#A8E2B8", WILD="#E8755F", CAPT="#6FAF86", GREY="#3A4842", GOLD="#FFD36B",
            BLUE="#7FB3D5", BUBBLE="#33301F", MINT="#22342C", CORAL_BG="#3A2724", CORAL="#F29A86",
            DOT_OFF="#2C4438", CHIP="#34473E", GRID="#26362F", F=["#B8932F", "#B86A5A", "#4E8A60", "#4F86A8"],
            MAP=["#22342C", "#2E5444", "#6FAF86", "#FFD36B", "#E8755F"], PLOT="plotly_dark")
YELLOW = "#FFC93C"

# ═══════════════════════════ الهيدر (نقرأ الوضع أول شي) ═══════════════════════════
h1, h2, h3 = st.columns([3, 1, 1], vertical_alignment="center")
with h2:
    dark = st.toggle("🌙 الوضع الداكن", key="dark")
C = DARK if dark else LIGHT
SOURCE_COLORS = {"مصطاد من البرية": C["WILD"], "مُربّى في الأسر": C["CAPT"], "مُربّى من بيض بري": C["GOLD"],
                 "مُصادَر": "#A493C4", "قبل الاتفاقية": "#7D8A83", "غير معروف": C["GREY"]}

# ═══════════════════════════ التصميم (CSS) ═══════════════════════════
dark_widgets = f"""
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {{
    background: {C['CARD']} !important; color: {C['TEXT']} !important; border-color: {C['CHIP']} !important; }}
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="popover"] ul, [data-baseweb="menu"] {{
    background: {C['CARD']} !important; color: {C['TEXT']} !important; }}
[data-baseweb="popover"] li {{ color: {C['TEXT']} !important; }}
[data-testid="stPopoverBody"], [data-testid="stExpander"] details {{ background: {C['CARD']} !important; }}
[data-testid="stExpander"] summary {{ color: {C['TEXT']} !important; }}
[data-testid="stButtonGroup"] button {{ background: {C['CARD']}; color: {C['SOFT']}; border-color: {C['CHIP']}; }}
[data-testid="stPopover"] button, [data-testid="stPopoverButton"] {{ background: {C['CARD']} !important;
    color: {C['TEXT']} !important; border-color: {C['CHIP']} !important; }}
[data-testid="stPopover"] button p {{ color: {C['TEXT']} !important; }}
""" if dark else ""

feathers = "".join(
    f'<svg class="feather f{i % 3}" aria-hidden="true" width="{w}" height="{w * 3}" viewBox="0 0 40 120" '
    f'style="{pos};--r:{r}deg"><path d="M20 5 C34 20 36 60 22 100 L20 112 L18 100 C4 60 6 20 20 5 Z" '
    f'fill="{C["F"][i % 4]}"/><path d="M20 8 L20 116" stroke="{C["MUTED"]}" stroke-opacity=".35" stroke-width="1.6"/></svg>'
    for i, (w, pos, r) in enumerate([(40, "top:90px;left:24px", -30), (30, "top:46%;left:10px", 20),
                                     (36, "bottom:40px;left:70px", 50), (34, "top:160px;right:18px", 35),
                                     (28, "bottom:120px;right:30px", -25), (24, "top:62%;right:8px", 70)]))

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+Bhaijaan+2:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, p, li, label, h1, h2, h3, h4, input, textarea, button,
[data-testid="stMarkdownContainer"], [data-baseweb="tab"], [data-baseweb="select"] {{
    font-family: 'Baloo Bhaijaan 2', sans-serif !important; }}
.main .block-container, [data-testid="stMarkdownContainer"], .stTabs, label, .stRadio,
.stSelectbox, .stMultiSelect, [data-testid="stPopoverBody"] {{ direction: rtl; text-align: right; }}
[data-testid="stSlider"] [data-baseweb="slider"] {{ direction: ltr; }}
.block-container {{ max-width: 1160px; padding-top: 3.4rem; position: relative; z-index: 1; }}
.stApp {{ background: {C['BG']}; color: {C['TEXT']}; transition: background .3s; }}
.stApp p, .stApp label, .stApp li, [data-testid="stCaptionContainer"] {{ color: {C['SOFT']}; }}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp strong {{ color: {C['TEXT']}; }}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* الريش اللي يطفو */
.feathers {{ position: fixed; inset: 0; pointer-events: none; z-index: 0; }}
.feather {{ position: absolute; animation: drift 6s ease-in-out infinite; }}
.feather.f1 {{ animation-duration: 8s; animation-delay: -2s; }}
.feather.f2 {{ animation-duration: 7s; animation-delay: -4s; }}
@keyframes drift {{ 0%,100% {{ transform: translateY(0) rotate(var(--r)); }}
                    50% {{ transform: translateY(-14px) rotate(calc(var(--r) + 8deg)); }} }}

/* التبويبات */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; flex-wrap: wrap; background: {C['CARD']}; border-radius: 999px;
    padding: 6px; box-shadow: 0 6px 18px rgba(0,0,0,.06); }}
.stTabs [data-baseweb="tab"] {{ border-radius: 999px; padding: 8px 18px; font-size: 17px; color: {C['SOFT']}; background: transparent; }}
.stTabs [aria-selected="true"] {{ background: {YELLOW} !important; color: #23312B !important; font-weight: 700; }}
.stTabs [aria-selected="true"] p {{ color: #23312B !important; font-weight: 700; }}
.stTabs [data-baseweb="tab"] p {{ font-size: 17px; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* الكروت (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {{
    background: {C['CARD']}; border-color: {C['LINE']} !important; border-radius: 28px; }}
.stage {{ min-height: 420px; }}
.kicker {{ color: {C['GREEN']} !important; font-size: 18px; font-weight: 700; margin: 0; }}
.kicker.red {{ color: {C['WILD']} !important; }}
.h1 {{ font-size: 60px; font-weight: 800; line-height: 1.1; color: {C['DEEP']}; margin: 6px 0 12px; }}
.h2 {{ font-size: 38px; font-weight: 800; line-height: 1.25; color: {C['TEXT']}; margin: 4px 0 10px; }}
.lead {{ font-size: 20px; line-height: 1.75; color: {C['SOFT']} !important; }}
.lead b {{ color: {C['TEXT']}; }}
.big {{ font-size: 104px; font-weight: 800; line-height: 1; color: {C['DEEP']}; text-align: center; }}
.center {{ text-align: center; }}
.bubble {{ background: {C['BUBBLE']}; border-radius: 22px; padding: 14px 20px; font-size: 19px; line-height: 1.65; color: {C['TEXT']}; }}
.bubble b {{ color: {C['TEXT']}; }}
.say {{ display: flex; align-items: center; gap: 12px; margin: 10px 0; }}
.say img {{ width: 54px; height: 54px; border-radius: 50%; object-fit: cover; border: 3px solid {YELLOW}; flex: none; }}
.tsuki {{ width: 100%; max-width: 330px; aspect-ratio: 1; object-fit: cover; object-position: center 20%;
    border-radius: 50% 50% 46% 46%; border: 6px solid {YELLOW}; display: block; margin: 0 auto; }}
.mini {{ background: {C['MINT']}; border-radius: 20px; padding: 14px 18px; text-align: center; }}
.mini .v {{ font-size: 32px; font-weight: 800; color: {C['DEEP']}; }}
.mini .l {{ font-size: 15px; color: {C['SOFT']}; }}
.reveal {{ background: {C['MINT']}; border-radius: 20px; padding: 12px 18px; font-size: 20px; line-height: 1.7;
    color: {C['TEXT']}; text-align: center; margin: 8px 0; }}
.reveal b.ok {{ color: {C['GREEN']}; }} .reveal b.no {{ color: {C['WILD']}; }}
.chip {{ display: inline-block; background: {C['CORAL_BG']}; border-radius: 16px; padding: 10px 16px; margin: 4px 0 4px 8px;
    font-size: 17px; color: {C['TEXT']}; }}
.chip b {{ color: {C['CORAL']}; }}
.dots {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 7px; max-width: 380px; margin: 0 auto; }}
.dots span {{ display: block; aspect-ratio: 1; border-radius: 50%; }}
.flock {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 2px; }}
.opt {{ border-radius: 26px; padding: 12px; text-align: center; border: 3px solid {C['LINE']}; background: {C['MINT']}; }}
.opt.ok {{ border-color: {C['GREEN']}; }} .opt.no {{ border-color: {C['WILD']}; background: {C['CORAL_BG']}; }}
.opt .n {{ font-size: 21px; font-weight: 700; color: {C['TEXT']}; }}
.opt .r {{ font-size: 16px; color: {C['SOFT']}; }}
.circle {{ width: 270px; height: 270px; border-radius: 50%; background: {C['CORAL_BG']}; margin: 0 auto;
    display: flex; align-items: center; justify-content: center; }}
.tool {{ border-radius: 24px; padding: 16px; text-align: center; }}
.tool .t {{ font-size: 21px; font-weight: 700; color: {C['TEXT']}; }}
.tool .d {{ font-size: 15px; color: {C['SOFT']}; }}
.steps {{ display: flex; gap: 6px; justify-content: center; align-items: center; margin: 2px 0 6px; }}
.steps span {{ height: 12px; border-radius: 999px; }}

/* الأزرار */
[data-testid="stBaseButton-primary"] {{ background: {YELLOW} !important; color: #23312B !important; border: none !important;
    border-radius: 999px !important; font-weight: 700 !important; }}
[data-testid="stBaseButton-primary"] p {{ color: #23312B !important; font-size: 18px; }}
[data-testid="stBaseButton-secondary"] {{ border-radius: 999px !important; }}
{dark_widgets}

/* الصور */
.photo {{ border-radius: 24px; overflow: hidden; border: 1px solid {C['LINE']}; background: {C['CARD']}; }}
.photo img {{ width: 100%; display: block; object-fit: cover; object-position: center 30%; }}
.photo .cap {{ font-size: 12px; color: {C['MUTED']}; padding: 6px 12px; direction: ltr; text-align: left; }}
.album {{ background: {C['CARD']}; border: 1px solid {C['LINE']}; border-radius: 22px; padding: 10px 10px 14px;
    text-align: center; margin-bottom: 16px; }}
.album .ph {{ width: 100%; height: 190px; object-fit: cover; object-position: center 30%; border-radius: 16px; margin-bottom: 8px; }}
.album .n {{ font-size: 18px; font-weight: 700; color: {C['TEXT']}; }}
.album .s {{ font-size: 13px; color: {C['MUTED']}; font-style: italic; }}
.album .t {{ font-size: 15px; color: {C['GREEN']}; font-weight: 700; margin-top: 4px; }}
.card {{ background: {C['CARD']}; border: 1px solid {C['LINE']}; border-radius: 24px; padding: 20px 24px; }}
.pcard .name {{ font-size: 32px; font-weight: 800; color: {C['TEXT']}; line-height: 1.2; }}
.pcard .sci {{ font-style: italic; color: {C['MUTED']}; font-size: 16px; direction: ltr; text-align: right; }}
.tag {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 14px; margin: 8px 0 0 6px;
    background: {C['MINT']}; color: {C['SOFT']}; }}
.tag.red {{ background: {C['CORAL_BG']}; color: {C['CORAL']}; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 14px; }}
.stats .v {{ font-size: 24px; font-weight: 800; color: {C['TEXT']}; }}
.stats .l {{ font-size: 13px; color: {C['MUTED']}; }}
.note {{ background: {C['BUBBLE']}; border-radius: 18px; padding: 12px 18px; color: {C['TEXT']}; font-size: 17px; line-height: 1.8; margin: 10px 0; }}
.note b {{ color: {C['TEXT']}; }}
.match {{ background: {C['CARD']}; border: 2px solid {C['LINE']}; border-radius: 24px; padding: 14px; text-align: center; }}
.match.win {{ border: 3px solid {YELLOW}; }}
.match .pct {{ font-size: 42px; font-weight: 800; color: {C['GREEN']}; line-height: 1; margin-top: 6px; }}
.match .why {{ text-align: right; font-size: 15px; line-height: 1.9; color: {C['SOFT']}; margin-top: 8px; }}
.vs {{ font-size: 42px; font-weight: 800; color: {YELLOW}; text-align: center; padding-top: 120px; }}
.cmp {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
.cmp td {{ padding: 10px 12px; border-bottom: 1px dashed {C['LINE']}; text-align: center; color: {C['TEXT']}; }}
.cmp td.k {{ color: {C['MUTED']}; font-size: 15px; }}
.cmp td.w {{ color: {C['GREEN']}; font-weight: 800; }}
.foot {{ color: {C['MUTED']}; font-size: 13px; margin-top: 40px; text-align: center; }}
</style>
<div class="feathers">{feathers}</div>
""", unsafe_allow_html=True)


def style(fig, title=None, h=430):
    """نفس الشكل لكل الرسومات (يتغير مع الوضع الفاتح والداكن)."""
    fig.update_layout(
        template=C["PLOT"], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Baloo Bhaijaan 2, sans-serif", color=C["SOFT"], size=15),
        margin=dict(l=10, r=10, t=50 if title else 16, b=10), height=h,
        title=dict(text=title, x=0.99, xanchor="right", font=dict(size=20, color=C["TEXT"])),
        hoverlabel=dict(font_family="Baloo Bhaijaan 2", bgcolor=C["CARD"], font_color=C["TEXT"]),
    )
    fig.update_xaxes(gridcolor=C["GRID"], zeroline=False)
    fig.update_yaxes(gridcolor=C["GRID"], zeroline=False)
    return fig


def fmt(n):
    """22520296 ← 22.5 مليون"""
    n = float(n)
    if n >= 1e6:
        return f"{n / 1e6:.1f} مليون"
    if n >= 1e3:
        return f"{n / 1e3:.0f} ألف"
    return f"{n:,.0f}"


def html(s):
    st.markdown(s, unsafe_allow_html=True)


def note(s):
    html(f'<div class="note">{s}</div>')


def tsuki_says(s):
    """فقاعة كلام من تسوكي."""
    html(f'<div class="say"><img src="{TSUKI_FACE}" alt="تسوكي"><div class="bubble">{s}</div></div>')


def draw(species, size=180, family="True parrots"):
    return parrot_svg(species, family, size)


def photo_html(species, h=320):
    """الصورة (من مجلد images أو ويكيميديا) مع اسم المصوّر لو موجود."""
    credit = photo_credit(species)
    cap = f'<div class="cap">{credit}</div>' if credit else ""
    return (f'<div class="photo"><img src="{photo_url(species, 600)}" style="height:{h}px" loading="lazy" '
            f'alt="{name_ar(species)}">{cap}</div>')


def pic_or_svg(species, family, h=260):
    """صورة لو موجودة، وإلا رسمة."""
    if has_photo(species):
        return photo_html(species, h)
    return f'<div style="text-align:center">{parrot_svg(species, family, h - 40)}</div>'


def geo_style(fig):
    fig.update_geos(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False, landcolor=C["MINT"],
                    showland=True, projection_type="natural earth", lataxis_range=[-58, 85])
    return fig


# ═══════════════════════════ قراءة البيانات ═══════════════════════════
@st.cache_data
def load_data():
    data_dir = Path(__file__).parent / "data"   # يشتغل محلياً وعلى Streamlit Cloud
    trade = pd.read_csv(data_dir / "trade_clean.csv", low_memory=False)
    parrots = pd.read_csv(data_dir / "parrots_clean.csv")

    # أسماء الدول بالعربي + كود ISO-3 للخرائط
    codes = pd.concat([trade["exporter_code"], trade["importer_code"]]).dropna().unique()
    ar_names = {c: country_ar(c) for c in codes}
    iso3 = {}
    for c in codes:
        k = pycountry.countries.get(alpha_2=c)
        iso3[c] = k.alpha_3 if k else None
    for side in ["exporter", "importer"]:
        trade[f"{side}_ar"] = trade[f"{side}_code"].map(ar_names)
        trade[f"{side}_iso3"] = trade[f"{side}_code"].map(iso3)

    trade["source_ar"] = trade["source"].map(SOURCE_AR)
    trade["family_en"] = trade["family"].map(CITES_FAMILY).fillna("Unknown")

    parrots["diet_ar"] = parrots["diet"].map(DIET_AR)
    parrots["habitat_ar"] = parrots["habitat"].map(HABITAT_AR)
    parrots["family_ar"] = parrots["family"].map(FAMILY_AR)
    parrots["name"] = parrots["species"].apply(display_name)
    parrots["rank"] = parrots["total_traded"].rank(ascending=False, method="min").astype(int)
    return trade, parrots


trade, parrots = load_data()

# ═══════════════════════════ باقي الهيدر + الفلاتر ═══════════════════════════
h1.markdown(f'<div style="display:flex;align-items:center;gap:12px"><img src="{TSUKI_FACE}" alt="تسوكي" '
            f'style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:3px solid {YELLOW}">'
            f'<div><p style="margin:0;font-size:28px;font-weight:800;color:{C["DEEP"]};line-height:1.1">جواز سفر الببغاء</p>'
            f'<p style="margin:0;font-size:15px;color:{C["MUTED"]}">رحلات الببغاوات بين الدول · 1975 إلى 2024 · نوره السويلم</p></div></div>',
            unsafe_allow_html=True)

# الفلاتر في زر واحد (تشتغل على التحليل والخليج والبيانات، والقصة تبقى على كل البيانات)
with h3.popover("الفلاتر", icon=":material/tune:", width="stretch"):
    st.caption("تتطبّق على: التحليل، السعودية والخليج، البيانات")
    yr = st.slider("السنوات", 1975, 2024, (1975, 2024))
    src_all = list(SOURCE_AR.values())
    sources = st.pills("مصدر الطيور", src_all, selection_mode="multi", default=src_all) or src_all
    fam_all = list(FAMILY_AR.values())
    fams_ar = st.pills("العائلة", fam_all, selection_mode="multi", default=fam_all) or fam_all
    fams = [k for k, v in FAMILY_AR.items() if v in fams_ar]
    diet_all = list(DIET_AR.values())
    diets_ar = st.pills("نوع الأكل (في الطبيعة)", diet_all, selection_mode="multi", default=diet_all) or diet_all
    diets = [k for k, v in DIET_AR.items() if v in diets_ar]
    mass = st.slider("الوزن (جرام)", 0, 1800, (0, 1800), step=10)

P = parrots[parrots["family"].isin(fams) & parrots["diet"].isin(diets) & parrots["mass_g"].between(*mass)]
T = trade[trade["year"].between(*yr) & trade["source_ar"].isin(sources)]
if set(fams) != set(FAMILY_AR):          # نفلتر العائلة بس لو المستخدم غيّرها
    T = T[T["family_en"].isin(fams)]
TS = T[T["species"].isin(P["species"])]   # سجلات الأنواع اللي تنطبق عليها فلاتر الصفات
filters_empty = T.empty or P.empty
st.write("")

tab_story, tab_birds, tab_quiz, tab_analysis, tab_gulf, tab_data = st.tabs([
    "📖 القصة", "🦜 الببغاوات", "🎯 أي ببغاء يناسبكم؟", "📊 التحليل", "🇸🇦 السعودية والخليج", "📋 البيانات"])


def need_data():
    """لو الفلاتر فضّت البيانات، نطلع رسالة ونوقف هالتبويب."""
    if filters_empty:
        st.warning("ما فيه بيانات تنطبق على هالفلاتر. جرّبوا توسّعونها من زر «الفلاتر» فوق 🙏")
        return False
    return True


# ═══════════════════════════ 📖 القصة (خطوة بخطوة) ═══════════════════════════
CHAPTERS = ["البداية", "كم ببغاء؟", "من البرية للقفص", "خمّنوا", "الحجم يفرق؟", "منطقة الخطر", "وإحنا؟", "استكشفوا"]
if "step" not in st.session_state:
    st.session_state["step"] = 0


def go_to(i):
    """نروح لفصل معيّن (نستخدمها في أزرار التالي والسابق)."""
    st.session_state["step"] = max(0, min(len(CHAPTERS) - 1, i))
    st.session_state["chapter_nav"] = CHAPTERS[st.session_state["step"]]


def jump():
    """لما المستخدم يختار فصل من الشريط فوق."""
    if st.session_state.get("chapter_nav"):
        st.session_state["step"] = CHAPTERS.index(st.session_state["chapter_nav"])


with tab_story:
    step = st.session_state["step"]
    st.session_state.setdefault("chapter_nav", CHAPTERS[step])
    st.segmented_control("الفصول", CHAPTERS, key="chapter_nav", on_change=jump, label_visibility="collapsed")
    dots = "".join(f'<span style="width:{30 if i == step else 12}px;background:'
                   f'{YELLOW if i == step else (C["CAPT"] if i < step else C["CHIP"])}"></span>'
                   for i in range(len(CHAPTERS)))
    html(f'<div class="steps">{dots}</div>')

    with st.container(border=True):
        # ── ٠. البداية ──
        if step == 0:
            c1, c2 = st.columns([1, 1.3], gap="large", vertical_alignment="center")
            with c1:
                html(f'<div class="bubble" style="max-width:360px;margin:0 auto 14px">أهلًا! أنا الكنيور <b>تسوكي</b> 💚<br>'
                     f'كنيور قرين تشيك. تعالوا أوريكم وش يصير للببغاوات حول العالم!</div>'
                     f'<img class="tsuki" src="{TSUKI}" alt="تسوكي، كنيور قرين تشيك">')
            with c2:
                html("""<div class="stage" style="display:flex;flex-direction:column;justify-content:center">
                <p class="kicker">قصة 50 سنة من رحلات الببغاوات بين الدول</p>
                <div class="h1">جواز سفر الببغاء</div>
                <p class="lead">صاحبتي نوره جمعت بيانات كل ببغاء انتقل بين الدول من 1975 إلى 2024،
                ودمجتها مع صفات كل الأنواع الـ 404. وأنا بحكي لكم القصة خطوة بخطوة.</p></div>""")
                st.button("يلا نبدأ ←", type="primary", on_click=go_to, args=(1,))

        # ── ١. كم ببغاء؟ ──
        elif step == 1:
            total = trade["quantity"].sum()
            flock = "".join(draw(s, 62) for s in ["Pyrrhura molinae", "Agapornis fischeri", "Psittacus erithacus",
                                                  "Ara macao", "Agapornis roseicollis", "Aratinga solstitialis",
                                                  "Cacatua galerita", "Myiopsitta monachus", "Alexandrinus krameri",
                                                  "Amazona aestiva", "Agapornis personatus"])
            html(f"""<div class="center"><p class="kicker">١ · كم ببغاء؟</p>
              <div class="big">{total / 1e6:.1f} مليون</div>
              <p class="lead">ببغاء حي انتقل بين الدول في 50 سنة</p>
              <div class="flock" aria-label="كل رسمة = تقريباً 2 مليون ببغاء">{flock}</div>
              <p style="font-size:15px">كل رسمة = تقريباً 2 مليون ببغاء</p></div>""")
            tsuki_says(f"تخيّلوا! يعني تقريباً <b>{total / 50 / 1e3:.0f} ألف ببغاء كل سنة</b>، "
                       f"من {trade['exporter_code'].nunique()} دولة إلى {trade['importer_code'].nunique()} دولة.")
            with st.expander("🌍 شوفوا الخريطة تتحرك عبر 50 سنة (اضغطوا ▶️)"):
                side = st.segmented_control("الخريطة", ["مين يصدّر؟", "مين يستورد؟"], default="مين يصدّر؟",
                                            key="anim_side", label_visibility="collapsed") or "مين يصدّر؟"
                key = "exporter" if side == "مين يصدّر؟" else "importer"
                # كل إطار = 5 سنوات
                T5 = trade.assign(period=(trade["year"] // 5 * 5).astype(str) + "–" + (trade["year"] // 5 * 5 + 4).astype(str))
                anim = (T5.groupby(["period", f"{key}_iso3", f"{key}_ar"])["quantity"].sum()
                        .reset_index().dropna().sort_values("period"))
                anim["log_q"] = np.log10(anim["quantity"])
                fig = px.choropleth(anim, locations=f"{key}_iso3", color="log_q", animation_frame="period",
                                    hover_name=f"{key}_ar",
                                    hover_data={"quantity": ":,", "log_q": False, f"{key}_iso3": False, "period": False},
                                    range_color=(0, anim["log_q"].max()), color_continuous_scale=C["MAP"],
                                    labels={"quantity": "طير", "period": "الفترة"})
                fig.update_traces(marker_line_color=C["CARD"], marker_line_width=.4)
                geo_style(fig)
                fig.update_coloraxes(colorbar=dict(title="طير", tickvals=[1, 2, 3, 4, 5, 6],
                                                   ticktext=["10", "100", "1k", "10k", "100k", "1M"], len=.6))
                fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 900
                fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300
                fig.layout.sliders[0].currentvalue.prefix = "الفترة: "
                st.plotly_chart(style(fig, None, 500), width="stretch")

        # ── ٢. من البرية للقفص ──
        elif step == 2:
            known = trade[trade["source"].isin(["Wild-caught", "Captive-bred", "Ranched"])].copy()
            known["decade"] = known["year"] // 10 * 10
            dec = known.pivot_table(index="decade", columns="source", values="quantity", aggfunc="sum", fill_value=0)
            wild_share = dec["Wild-caught"] / dec.sum(axis=1) * 100
            labels = {1990: "التسعينات", 2000: "الألفين", 2010: "2010+", 2020: "2020+"}
            notes = {1990: "في التسعينات: تقريباً نص الطيور من البرية 😟",
                     2000: "بعد حظر أمريكا (1992) بدأت تنزل",
                     2010: "بعد حظر أوروبا (2005) نزلت أكثر",
                     2020: "اليوم: أقل من 5! القوانين نفعت 🎉"}
            c1, c2 = st.columns([1.3, 1], gap="large", vertical_alignment="center")
            with c1:
                html("""<p class="kicker">٢ · من البرية إلى القفص</p>
                <div class="h2">كم ببغاء من كل 100 كان مصطاد من البرية؟</div>
                <p class="lead">اضغطوا على كل فترة وشوفوا النقاط:</p>""")
                pick = st.segmented_control("الفترة", list(labels.values()), default="التسعينات",
                                            key="decade", label_visibility="collapsed") or "التسعينات"
                d = [k for k, v in labels.items() if v == pick][0]
                pct = round(wild_share[d])
                html(f'<div style="display:flex;align-items:center;gap:20px;margin-top:10px">'
                     f'<div style="font-size:92px;font-weight:800;color:{C["WILD"]};line-height:1">{pct}%</div>'
                     f'<div class="bubble">{notes[d]}</div></div>')
            with c2:
                dots100 = "".join(f'<span style="background:{C["WILD"] if i < pct else C["DOT_OFF"]}"></span>'
                                  for i in range(100))
                html(f'<div class="dots" role="img" aria-label="{pct} من كل 100 مصطاد من البرية">{dots100}</div>')
            with st.expander("📈 شوفوا الرسم كامل سنة بسنة"):
                yearly = trade.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
                fig = px.area(yearly, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                              category_orders={"source_ar": list(SOURCE_COLORS)},
                              labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
                for y, txt in [(1992, "حظر أمريكا"), (2005, "حظر أوروبا")]:
                    fig.add_vline(x=y, line_dash="dash", line_color=C["SOFT"], opacity=.5)
                    fig.add_annotation(x=y, y=1, yref="paper", text=txt, showarrow=False, xanchor="left", xshift=6)
                fig.update_traces(line_width=0)
                fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
                st.plotly_chart(style(fig, None, 380), width="stretch")
                st.caption("اللون الرمادي في الثمانينات معناه إن المصدر ما كان ينكتب.")

        # ── ٣. خمّنوا ──
        elif step == 3:
            html("""<div class="center"><p class="kicker">٣ · خمّنوا!</p>
            <div class="h2">أي واحد انباع أكثر شي في العالم؟</div></div>""")
            options = [("Psittacus erithacus", "الكاسكو"), ("Agapornis fischeri", "طائر الحب فيشر"),
                       ("Pyrrhura molinae", "كنيور قرين تشيك")]
            top_sp = parrots.sort_values("total_traded", ascending=False)
            winner = top_sp.iloc[0]["species"]
            guess = st.session_state.get("guess")
            for col, (sp, nm) in zip(st.columns(3), options):
                r = parrots[parrots["species"] == sp].iloc[0]
                cls = "" if not guess else ("ok" if sp == winner else ("no" if sp == guess else ""))
                res = (f"{fmt(r['total_traded'])} طير" + (" · الأول 🏆" if sp == winner else "")) if guess else "اضغطوا للاختيار"
                with col:
                    html(f'<div class="opt {cls}">{draw(sp, 170)}<div class="n">{nm}</div><div class="r">{res}</div></div>')
                    st.button(f"اخترت {nm}", key=f"g_{sp}", width="stretch",
                              on_click=lambda s=sp: st.session_state.update(guess=s))
            if guess:
                top10 = top_sp.head(10)["total_traded"].sum() / top_sp["total_traded"].sum()
                right = guess == winner
                html(f'<div class="reveal"><b class="{"ok" if right else "no"}">{"صح عليكم! 🎉" if right else "قريب، بس لا 😅"}</b> '
                     f'{name_ar(winner)} هو الأول بـ {fmt(top_sp.iloc[0]["total_traded"])} طير، '
                     f'وأكثر 10 أنواع لحالها = <b>{top10:.0%}</b> من كل الطيور.</div>')
                with st.expander("🏆 شوفوا أكثر 10 ببغاوات انباعت"):
                    t10 = top_sp.head(10).iloc[::-1]
                    fig = go.Figure(go.Bar(x=t10["total_traded"], y=[name_ar(s) for s in t10["species"]], orientation="h",
                                           marker_color=[YELLOW if s == "Pyrrhura molinae" else C["CAPT"] for s in t10["species"]],
                                           text=[fmt(v) for v in t10["total_traded"]], textposition="outside", cliponaxis=False))
                    fig.update_xaxes(visible=False, range=[0, t10["total_traded"].max() * 1.25])
                    st.plotly_chart(style(fig, None, 400), width="stretch")

        # ── ٤. الحجم يفرق؟ ──
        elif step == 4:
            size_ans = st.session_state.get("size_ans")
            c1, c2 = st.columns([1.3, 1], gap="large", vertical_alignment="center")
            with c1:
                html("""<p class="kicker">٤ · سؤال</p>
                <div class="h2">تتوقعون الببغاوات الكبيرة تنباع أكثر من الصغيرة؟</div>""")
                b1, b2 = st.columns(2)
                b1.button("إيه، الكبير أحلى", width="stretch", type="primary" if size_ans == "yes" else "secondary",
                          on_click=lambda: st.session_state.update(size_ans="yes"))
                b2.button("لا، ما نتوقع", width="stretch", type="primary" if size_ans == "no" else "secondary",
                          on_click=lambda: st.session_state.update(size_ans="no"))
                if size_ans:
                    # سبيرمان = ارتباط بيرسون بين الترتيب (rank)، كذا ما نحتاج مكتبة scipy
                    def spearman(x, y):
                        ok = x.notna() & y.notna()
                        return x[ok].rank().corr(y[ok].rank())
                    rho_m = spearman(parrots["total_traded"], parrots["mass_g"])
                    rho_r = spearman(parrots["total_traded"], parrots["range_km2"])
                    html(f'<div class="reveal" style="text-align:right"><b class="{"ok" if size_ans == "no" else "no"}">'
                         f'{"صح! 👏" if size_ans == "no" else "مفاجأة! 😮"}</b> الحجم تقريباً ما يفرق ({rho_m:.2f}). '
                         f'اللي يفرق هو <b>كم النوع منتشر في الطبيعة</b> ({rho_r:.2f}): المنتشر أسهل وأرخص، فيصير في المحلات.</div>')
            with c2:
                mac = parrots.loc[parrots["species"] == "Ara macao", "mass_g"].iloc[0]
                lov = parrots.loc[parrots["species"] == "Agapornis fischeri", "mass_g"].iloc[0]
                html(f'<div style="display:flex;align-items:flex-end;justify-content:center;gap:24px;text-align:center">'
                     f'<div>{draw("Ara macao", 210)}<p>المكاو: {mac / 1000:.1f} كيلو</p></div>'
                     f'<div>{draw("Agapornis fischeri", 90)}<p>طائر الحب: {lov:.0f} جم</p></div></div>')
            if size_ans:
                with st.expander("🔍 شوفوا كل الأنواع: الوزن مقابل التجارة"):
                    tr = parrots[parrots["in_trade"]]
                    fig = px.scatter(tr, x="mass_g", y="total_traded", log_x=True, log_y=True, hover_name="name",
                                     labels={"mass_g": "الوزن (جم)", "total_traded": "عدد الطيور"})
                    fig.update_traces(marker=dict(color=C["CAPT"], size=9, opacity=.6, line=dict(width=0)))
                    me = tr[tr["species"] == "Pyrrhura molinae"]
                    fig.add_trace(go.Scatter(x=me["mass_g"], y=me["total_traded"], mode="markers+text",
                                             text=["تسوكي 💚"], textposition="top center", hoverinfo="skip",
                                             marker=dict(color=YELLOW, size=16), textfont=dict(color=C["TEXT"], size=15)))
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(style(fig, None, 400), width="stretch")

        # ── ٥. منطقة الخطر ──
        elif step == 5:
            W = parrots[parrots["wild_traded"] > 0].copy()
            W["danger"] = (W["range_km2"] < 50_000) & (W["wild_traded"] > 1_000)
            D = W[W["danger"]].sort_values("wild_traded", ascending=False)
            gof = parrots.loc[parrots["species"] == "Cacatua goffiniana", "range_km2"].iloc[0]
            c1, c2 = st.columns([1, 1.4], gap="large", vertical_alignment="center")
            with c1:
                html(f'<div class="circle">{draw(D.iloc[0]["species"], 200, D.iloc[0]["family"])}</div>')
            with c2:
                html(f"""<p class="kicker red">٥ · منطقة الخطر</p>
                <div class="h2">{len(D)} نوع بيتها صغير، وانصاد منها آلاف</div>
                <p class="lead">أغلبها من جزر إندونيسيا. موطن كل واحد أصغر من القصيم، ومع ذلك انصاد منه
                أكثر من 1,000 طير من البرية.</p>
                <span class="chip">{name_ar(D.iloc[0]['species'])}: <b>{fmt(D.iloc[0]['wild_traded'])} طير بري</b></span>
                <span class="chip">كوكاتو غوفين: <b>موطنه {gof:,.0f} كم² بس</b></span>""")
            with st.expander("⚠️ شوفوا الأنواع على الرسم"):
                fig = px.scatter(W, x="range_km2", y="wild_traded", log_x=True, log_y=True, hover_name="name",
                                 color=W["danger"].map({True: "في خطر", False: "باقي الأنواع"}),
                                 color_discrete_map={"في خطر": C["WILD"], "باقي الأنواع": C["GREY"]},
                                 labels={"range_km2": "مساحة الموطن (كم²)", "wild_traded": "طيور مصطادة من البرية", "color": ""})
                fig.add_vrect(x0=W["range_km2"].min() * .8, x1=50_000, fillcolor=C["WILD"], opacity=.07, line_width=0)
                fig.add_hline(y=1_000, line_dash="dot", line_color=C["WILD"])
                fig.update_traces(marker=dict(size=10, line=dict(width=0)))
                fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
                st.plotly_chart(style(fig, None, 380), width="stretch")
                st.caption("تقدرون تغيّرون الحدود بنفسكم من تبويب «التحليل» ← منطقة الخطر")

        # ── ٦. وإحنا؟ ──
        elif step == 6:
            sa = trade[trade["importer_code"] == "SA"]
            after = sa.loc[sa["year"] >= 2016, "quantity"].sum() / sa["quantity"].sum()
            sa_top = sa.groupby("species")["quantity"].sum().idxmax()
            c1, c2 = st.columns([1.4, 1], gap="large", vertical_alignment="center")
            with c1:
                html(f"""<p class="kicker">٦ · وإحنا؟ 🇸🇦</p>
                <div class="h2">السعودية استوردت {sa['quantity'].sum():,} ببغاء</div>
                <p class="lead">الاستيراد شبه وقف بين 2005 و2014، وبعدها رجع بقوة.</p>
                <div style="display:flex;gap:12px;flex-wrap:wrap">
                  <div class="mini"><div class="v">{after:.0%}</div><div class="l">وصلت بعد 2016</div></div>
                  <div class="mini" style="background:{C['BUBBLE']}"><div class="v" style="color:{C['GOLD']}">طيور الحب</div>
                  <div class="l">أكثر شي نشتريه</div></div></div>""")
            with c2:
                html(f'<div class="center">{draw(sa_top, 240)}</div>')
            s = sa.groupby("year")["quantity"].sum().reindex(range(1975, 2025), fill_value=0)
            fig = go.Figure(go.Scatter(x=s.index, y=s.values, fill="tozeroy", mode="lines",
                                       line=dict(color=C["GREEN"], width=2), fillcolor="rgba(111,176,127,.28)",
                                       hovertemplate="%{x}: %{y:,} طير<extra></extra>"))
            st.plotly_chart(style(fig, "واردات السعودية كل سنة", 260), width="stretch")

        # ── ٧. استكشفوا ──
        else:
            html(f"""<div class="say" style="justify-content:center"><img src="{TSUKI_FACE}" alt="تسوكي">
              <div><p class="kicker">خلصت القصة! شكراً إنكم سمعتوني 🎉</p>
              <div class="h2" style="margin:0">دوركم الحين: استكشفوا بنفسكم</div></div></div>
              <p class="center">كل أداة لها تبويب فوق 👆</p>""")
            tools = [("Aratinga solstitialis", "أي ببغاء يناسبكم؟", "6 أسئلة وتعرفون", C["BUBBLE"]),
                     ("Cacatua galerita", "الببغاوات", "تعرّفوا، قارنوا، والألبوم", C["MINT"]),
                     ("Psittacus erithacus", "التحليل", "الخريطة والصفات والخطر", C["CORAL_BG"]),
                     ("Ara macao", "البيانات", "الجداول وتحميل CSV", C["MINT"])]
            for col, (sp, t, dsc, bg) in zip(st.columns(4), tools):
                col.markdown(f'<div class="tool" style="background:{bg}">{draw(sp, 110)}<div class="t">{t}</div>'
                             f'<div class="d">{dsc}</div></div>', unsafe_allow_html=True)
            st.write("")
            _, mid, _ = st.columns([1, 1, 1])
            mid.button("عيدوا القصة من البداية", width="stretch", on_click=go_to, args=(0,))

        # ── أزرار التنقل ──
        if 0 < step < len(CHAPTERS) - 1:
            st.divider()
            n1, n2, n3 = st.columns([1, 2, 1], vertical_alignment="center")
            n1.button("التالي ←", type="primary", width="stretch", on_click=go_to, args=(step + 1,))
            n2.markdown(f'<p class="center" style="margin:0">{step} من {len(CHAPTERS) - 2}</p>', unsafe_allow_html=True)
            n3.button("→ السابق", width="stretch", on_click=go_to, args=(step - 1,))


# ═══════════════════════════ 🦜 الببغاوات ═══════════════════════════
with tab_birds:
    view = st.segmented_control("القسم", ["تعرّفوا على ببغاء", "قارنوا بين ببغاوين", "الألبوم"],
                                default="تعرّفوا على ببغاء", key="birds_view",
                                label_visibility="collapsed") or "تعرّفوا على ببغاء"
    st.write("")
    opts = parrots.sort_values("total_traded", ascending=False)["species"].tolist()

    if view == "تعرّفوا على ببغاء":
        pick = st.selectbox("اختاروا ببغاء (مرتبة من الأكثر تجارة)", opts, index=opts.index("Pyrrhura molinae"),
                            format_func=display_name)
        b = parrots[parrots["species"] == pick].iloc[0]
        info = FEATURED.get(pick, {})
        bt = trade[trade["species"] == pick]
        heavier = (parrots["mass_g"] < b["mass_g"]).mean()
        wild_s = f"{b['wild_share']:.0%}" if pd.notna(b["wild_share"]) else "–"
        rng = f"{b['range_km2']:,.0f} كم²" if pd.notna(b["range_km2"]) else "غير معروفة"

        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            pv = "📷 صورة"
            if has_photo(pick):
                pv = st.segmented_control("العرض", ["📷 صورة", "🎨 رسمة"], default="📷 صورة", key="meet_view",
                                          label_visibility="collapsed") or "📷 صورة"
            html(photo_html(pick, 380) if pv == "📷 صورة" and has_photo(pick)
                 else f'<div class="center">{draw(pick, 300, b["family"])}</div>')
            if pick == "Pyrrhura molinae":
                tsuki_says("هذا أنا! 💚 أهدأ أنواع الكنيور ومناسب للشقق.")
            elif info:
                note(f"✨ {info['fact']}")
        with c2:
            tags = (f'<span class="tag">{b["family_ar"]}</span><span class="tag">{b["habitat_ar"]}</span>'
                    f'<span class="tag">{b["diet_ar"]} (في الطبيعة)</span>')
            if (bt["cites_appendix"] == "I").any():
                tags += '<span class="tag red">محمي: الملحق الأول</span>'
            html(f"""<div class="card pcard">
              <div class="name">{name_ar(pick)}</div><div class="sci">{pick}</div><div>{tags}</div>
              <div class="stats">
                <div><div class="v">{b['mass_g']:,.0f} جم</div><div class="l">أثقل من {heavier:.0%} من الببغاوات</div></div>
                <div><div class="v">#{b['rank']}</div><div class="l">ترتيبه في التجارة من 404</div></div>
                <div><div class="v">{fmt(b['total_traded'])}</div><div class="l">طير انتقل بين الدول</div></div>
                <div><div class="v" style="color:{C['WILD']}">{wild_s}</div><div class="l">مصطاد من البرية</div></div>
                <div><div class="v">{rng}</div><div class="l">مساحة انتشاره</div></div>
                <div><div class="v">{int(b['n_exporters'])}</div><div class="l">دولة صدّرته</div></div>
              </div></div>""")
            if info.get("pet"):
                html(f"""<div class="card" style="margin-top:14px;line-height:1.9;color:{C['SOFT']}">
                  <p class="kicker" style="margin-bottom:6px">🏠 معلومات للمربّين</p>
                  <b>موطنه:</b> {info['origin']}<br>
                  <b>الطول:</b> {info['length']} · <b>العمر:</b> {info['life']}<br>
                  <b>الكلام:</b> {info['talk']} · <b>الإزعاج:</b> {info['noise']}<br>
                  <b>الأكل في البيت:</b> {HOME_DIET}
                  <div style="font-size:13px;color:{C['MUTED']};margin-top:8px">معلومات عامة وتقريبية. لأي سؤال صحي راجعوا طبيب طيور 🩺</div>
                </div>""")
            elif info:
                html(f'<div class="card" style="margin-top:14px"><p class="kicker">🌍 موطنه</p>{info["origin"]}</div>')

        if bt.empty:
            st.success("🌿 هالنوع **ما انباع ولا طير منه** بين الدول. محظوظ!")
        else:
            y = bt.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
            fig = px.bar(y, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                         labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
            fig.update_layout(legend=dict(orientation="h", y=-.2, title=None), bargap=.15)
            st.plotly_chart(style(fig, "تاريخ تجارته", 340), width="stretch")
            cc1, cc2, cc3 = st.columns([1, 1, 1.1])
            for cc, side_, color, ttl in [(cc1, "exporter_ar", C["WILD"], "مين يبيعه؟"),
                                          (cc2, "importer_ar", C["BLUE"], "مين يشتريه؟")]:
                s = bt.groupby(side_)["quantity"].sum().nlargest(6).sort_values()
                f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=color,
                                     text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
                f.update_xaxes(visible=False, range=[0, s.max() * 1.45])
                cc.plotly_chart(style(f, ttl, 300), width="stretch")
            if pd.notna(b["lat"]):
                f = go.Figure(go.Scattergeo(lat=[b["lat"]], lon=[b["lon"]], mode="markers",
                                            marker=dict(size=max(12, min(60, np.sqrt(b["range_km2"] or 1) / 25)),
                                                        color=YELLOW, opacity=.85, line=dict(color="white", width=1))))
                geo_style(f)
                cc3.plotly_chart(style(f, "وين يعيش في الطبيعة؟", 300), width="stretch")

    elif view == "قارنوا بين ببغاوين":
        c1, cm, c2 = st.columns([1, .25, 1])
        a = c1.selectbox("الببغاء الأول", opts, index=opts.index("Pyrrhura molinae"), format_func=display_name, key="cmp_a")
        bb = c2.selectbox("الببغاء الثاني", opts, index=opts.index("Agapornis fischeri"), format_func=display_name, key="cmp_b")
        A = parrots[parrots["species"] == a].iloc[0]
        B = parrots[parrots["species"] == bb].iloc[0]
        c1.markdown(pic_or_svg(a, A["family"]), unsafe_allow_html=True)
        cm.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)
        c2.markdown(pic_or_svg(bb, B["family"]), unsafe_allow_html=True)

        def val(x, f="{:,.0f}"):
            return f.format(x) if pd.notna(x) else "–"

        # (العنوان، العمود، التنسيق، مين يفوز: الأكبر ولا الأصغر ولا ما فيه فايز)
        rows = [("⚖️ الوزن (جم)", "mass_g", "{:,.0f}", None),
                ("📏 طول الجناح (مم)", "wing_length_mm", "{:,.0f}", None),
                ("🌍 مساحة الانتشار (كم²)", "range_km2", "{:,.0f}", "max"),
                ("📦 طيور انتقلت بين الدول", "total_traded", "{:,.0f}", None),
                ("🏆 ترتيبه في التجارة", "rank", "#{:.0f}", None),
                ("🌿 نسبة المصطاد من البرية", "wild_share", "{:.1%}", "min"),
                ("🚢 دول صدّرته", "n_exporters", "{:,.0f}", None)]
        t = (f'<table class="cmp"><tr><td class="w" style="color:{C["TEXT"]}">{name_ar(a)}</td><td></td>'
             f'<td class="w" style="color:{C["TEXT"]}">{name_ar(bb)}</td></tr>')
        for label, col, f, win in rows:
            va, vb = A[col], B[col]
            ca = cb = ""
            if win and pd.notna(va) and pd.notna(vb) and va != vb:
                better_a = (va > vb) if win == "max" else (va < vb)
                ca, cb = ("w", "") if better_a else ("", "w")
            t += f'<tr><td class="{ca}">{val(va, f)}</td><td class="k">{label}</td><td class="{cb}">{val(vb, f)}</td></tr>'
        t += (f'<tr><td>{A["diet_ar"]}</td><td class="k">🍽️ الأكل (في الطبيعة)</td><td>{B["diet_ar"]}</td></tr>'
              f'<tr><td>{A["habitat_ar"]}</td><td class="k">🌳 البيئة</td><td>{B["habitat_ar"]}</td></tr></table>')
        st.write("")
        html(f'<div class="card">{t}</div>')
        st.caption("🟢 الأخضر = الأحسن للطير نفسه: انتشار أكبر في الطبيعة، ونسبة أقل مصطادة من البرية.")
        both = (trade[trade["species"].isin([a, bb])].groupby(["year", "species"])["quantity"].sum()
                .reset_index().assign(name=lambda d: d["species"].map(name_ar)))
        if not both.empty:
            fig = px.line(both, x="year", y="quantity", color="name", markers=True,
                          color_discrete_sequence=[C["GOLD"], C["BLUE"]],
                          labels={"year": "السنة", "quantity": "عدد الطيور", "name": ""})
            fig.update_layout(legend=dict(orientation="h", y=-.2))
            st.plotly_chart(style(fig, "تجارتهم عبر السنين", 360), width="stretch")
        # الحجم الحقيقي: نرسم الطيرين بنسبة طول الجناح
        if pd.notna(A["wing_length_mm"]) and pd.notna(B["wing_length_mm"]):
            big = max(A["wing_length_mm"], B["wing_length_mm"])
            sa_, sb_ = int(60 + 180 * A["wing_length_mm"] / big), int(60 + 180 * B["wing_length_mm"] / big)
            html(f"""<div class="card" style="text-align:center">
              <div style="font-weight:800;font-size:20px;margin-bottom:8px;color:{C['TEXT']}">📐 الحجم الحقيقي جنب بعض</div>
              <div style="display:flex;justify-content:center;align-items:flex-end;gap:50px;color:{C['SOFT']}">
                <div>{parrot_svg(a, A['family'], sa_)}<div>{name_ar(a)}</div></div>
                <div>{parrot_svg(bb, B['family'], sb_)}<div>{name_ar(bb)}</div></div>
              </div></div>""")

    else:
        a1, a2 = st.columns([1, 2])
        album_view = a1.segmented_control("العرض", ["📷 صور", "🎨 رسومات"], default="📷 صور", key="album_view",
                                          label_visibility="collapsed") or "📷 صور"
        a2.caption("الصور اخترتها أنا أو من Wikimedia Commons، والرسومات مرسومة بالكود بألوان كل نوع.")
        album = parrots[parrots["species"].isin(FEATURED)].sort_values("total_traded", ascending=False)
        cols = st.columns(4)
        for i, (_, r) in enumerate(album.iterrows()):
            f = FEATURED[r["species"]]
            traded = fmt(r["total_traded"]) + " طير" if r["total_traded"] else "ما انباع أبداً 🌿"
            if album_view == "📷 صور" and has_photo(r["species"]):
                pic = (f'<img class="ph" src="{photo_url(r["species"], 400)}" loading="lazy" '
                       f'alt="{f["ar"]}" title="{photo_credit(r["species"])}">')
            else:
                pic = parrot_svg(r["species"], r["family"], 170)
            with cols[i % 4]:
                html(f"""<div class="album">{pic}<div class="n">{f['emoji']} {f['ar']}</div>
                  <div class="s">{r['species']}</div><div class="t">{traded}</div></div>""")


# ═══════════════════════════ 🎯 أي ببغاء يناسبكم؟ ═══════════════════════════
with tab_quiz:
    html('<div class="h2">🎯 أي ببغاء يناسبكم؟</div>')
    tsuki_says(f"جاوبوا على 6 أسئلة، وأطلع لكم أنسب 3 ببغاوات من {len(PET_PROFILE)} نوع مشهور. (تقريبي وللمتعة 😄)")
    with st.container(border=True):
        q1, q2 = st.columns(2)
        space_ = q1.radio("🏠 وين بيعيش الطير؟", ["شقة صغيرة", "شقة كبيرة أو بيت", "بيت كبير وفيه غرفة للطير"], index=1)
        noise = q2.radio("🔊 كم تتحملون الإزعاج؟", ["لازم يكون هادئ", "شوي عادي", "ما يهمنا أبداً"], index=1)
        talk = q1.radio("🗣️ تبونه يتكلم؟", ["إيه، هذا أهم شي", "حلو لو يتكلم بس مو شرط", "ما يهمنا"], index=1)
        time = q2.radio("⏰ كم ساعة تقدرون تجلسون معه كل يوم؟", ["ساعة أو أقل", "ساعتين إلى ثلاث", "أغلب اليوم"], index=1)
        years = q1.radio("⏳ كم سنة تقدرون تلتزمون فيه؟", ["10 إلى 20 سنة", "20 إلى 40 سنة", "أكثر من 40 سنة"], index=1)
        exp = q2.radio("🎓 خبرتكم مع الطيور؟", ["هذا أول ببغاء لنا", "عندنا خبرة"], index=0)

    max_size = {"شقة صغيرة": 1, "شقة كبيرة أو بيت": 2}.get(space_, 3)
    max_noise = {"لازم يكون هادئ": 1, "شوي عادي": 3}.get(noise, 4)
    max_care = {"ساعة أو أقل": 1, "ساعتين إلى ثلاث": 2}.get(time, 3)
    max_life = {"10 إلى 20 سنة": 20, "20 إلى 40 سنة": 40}.get(years, 100)

    results = []
    for s, p in PET_PROFILE.items():
        score, why = 100, []
        if p["size"] > max_size:
            score -= 30 * (p["size"] - max_size); why.append("⚠️ يحتاج مساحة أكبر")
        else:
            why.append("✅ حجمه مناسب لمكانكم")
        if p["noise"] > max_noise:
            score -= 25 * (p["noise"] - max_noise); why.append("⚠️ صوته أعلى من اللي تتحملونه")
        else:
            why.append("✅ صوته مقبول لكم")
        if talk.startswith("إيه"):
            score -= 20 * max(0, 2 - p["talk"])
            why.append("✅ يتكلم كويس" if p["talk"] >= 2 else "⚠️ كلامه قليل")
        elif talk.startswith("حلو"):
            score -= 5 * max(0, 2 - p["talk"])
        if p["care"] > max_care:
            score -= 25 * (p["care"] - max_care); why.append("⚠️ يحتاج وقت واهتمام أكثر")
        else:
            why.append("✅ يناسب وقتكم")
        if p["life"] > max_life:
            score -= 20 if p["life"] - max_life <= 20 else 35; why.append(f"⚠️ ممكن يعيش {p['life']} سنة")
        if exp.startswith("هذا") and not p["easy"]:
            score -= 30; why.append("⚠️ يحتاج خبرة")
        # فروق صغيرة عشان ما يتعادلون كلهم على 100%
        if not noise.startswith("ما يهمنا"):
            score -= 3 * (p["noise"] - 1)
        if not time.startswith("أغلب"):
            score -= 3 * (p["care"] - 1)
        if not talk.startswith("ما يهمنا"):
            score -= 2 * (3 - p["talk"])
        # آخر شي: الأقل صيداً من البرية يتقدّم (أفضل للطيور)
        r_ = parrots.loc[parrots["species"] == s, "wild_share"]
        if len(r_) and pd.notna(r_.iloc[0]):
            score -= round(10 * r_.iloc[0])
        results.append((max(score, 0), s, why))
    results.sort(key=lambda x: -x[0])

    st.write("")
    medals = ["🥇", "🥈", "🥉"]
    for i, (col, (score, s, why)) in enumerate(zip(st.columns(3), results[:3])):
        r = parrots[parrots["species"] == s].iloc[0]
        wild = f"{r['wild_share']:.0%}" if pd.notna(r["wild_share"]) else "–"
        col.markdown(f"""<div class="match {'win' if i == 0 else ''}">
          <div style="font-size:30px">{medals[i]}</div>{pic_or_svg(s, r['family'], 220)}
          <div style="font-size:22px;font-weight:800;margin-top:8px;color:{C['TEXT']}">{FEATURED[s]['emoji']} {name_ar(s)}</div>
          <div class="pct">{score}%</div><div style="color:{C['MUTED']}">نسبة التوافق</div>
          <div class="why">{'<br>'.join(why[:5])}<br>🌿 من البرية: {wild} من تجارته</div>
        </div>""", unsafe_allow_html=True)
    note("💡 مهما اخترتوا، <b>اشتروا طير مُربّى في الأسر</b> من مربّي موثوق. الطيور المصطادة من البرية "
         "تتأذى في النقل، وصيدها يضر الأنواع اللي موطنها صغير.")


# ═══════════════════════════ 📊 التحليل ═══════════════════════════
with tab_analysis:
    view = st.segmented_control("القسم", ["🌍 التجارة العالمية", "🪶 صفات الببغاوات", "⚠️ منطقة الخطر"],
                                default="🌍 التجارة العالمية", key="ana_view",
                                label_visibility="collapsed") or "🌍 التجارة العالمية"
    if need_data():
        wild = T.loc[T["source"] == "Wild-caught", "quantity"].sum()
        known_q = T.loc[T["source"].isin(["Wild-caught", "Captive-bred", "Ranched"]), "quantity"].sum()
        kpis = [(fmt(T["quantity"].sum()), "ببغاء انتقل بين الدول"),
                (f"{TS['species'].nunique()}", f"نوع في التجارة (من {len(P)})"),
                (f"{wild / known_q:.0%}" if known_q else "–", "مصطاد من البرية (من المعروف)"),
                (f"{T['exporter_code'].nunique()} · {T['importer_code'].nunique()}", "دولة مصدّرة · مستوردة")]
        for col, (v, l) in zip(st.columns(4), kpis):
            col.markdown(f'<div class="mini"><div class="v">{v}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)
        st.caption(f"حسب الفلاتر: {yr[0]}–{yr[1]}")
        st.write("")

        if view == "🌍 التجارة العالمية":
            c1, c2 = st.columns([1.35, 1])
            with c1:
                side = st.segmented_control("الخريطة", ["الدول المصدّرة", "الدول المستوردة"], default="الدول المصدّرة",
                                            key="map_side", label_visibility="collapsed") or "الدول المصدّرة"
                key = "exporter" if side == "الدول المصدّرة" else "importer"
                geo = T.groupby([f"{key}_iso3", f"{key}_ar"])["quantity"].sum().reset_index().dropna()
                fig = px.choropleth(geo, locations=f"{key}_iso3", color=np.log10(geo["quantity"]),
                                    hover_name=f"{key}_ar", custom_data=["quantity"], color_continuous_scale=C["MAP"])
                fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>%{customdata[0]:,} طير<extra></extra>",
                                  marker_line_color=C["CARD"], marker_line_width=.4)
                geo_style(fig)
                fig.update_coloraxes(colorbar=dict(title="طير", tickvals=[1, 2, 3, 4, 5, 6],
                                                   ticktext=["10", "100", "1k", "10k", "100k", "1M"], len=.6))
                st.plotly_chart(style(fig, None, 430), width="stretch")
            with c2:
                top = T.groupby(f"{key}_ar")["quantity"].sum().nlargest(12).sort_values()
                fig = go.Figure(go.Bar(x=top.values, y=top.index, orientation="h",
                                       marker_color=C["WILD"] if key == "exporter" else C["BLUE"],
                                       text=[fmt(v) for v in top.values], textposition="outside", cliponaxis=False))
                fig.update_xaxes(range=[0, top.max() * 1.3], visible=False)
                st.plotly_chart(style(fig, "أكبر 12 دولة " + ("مصدّرة" if key == "exporter" else "مستوردة"), 470),
                                width="stretch")
            st.markdown("#### 🔀 أكبر طرق التجارة")
            n = st.slider("عدد الطرق", 5, 30, 15)
            r = T.groupby(["exporter_ar", "importer_ar"])["quantity"].sum().nlargest(n).reset_index()
            ex = list(dict.fromkeys(r["exporter_ar"]))
            im = list(dict.fromkeys(r["importer_ar"]))
            fig = go.Figure(go.Sankey(
                node=dict(label=[f"{e} " for e in ex] + [f" {i}" for i in im], pad=12, thickness=14,
                          color=[C["WILD"]] * len(ex) + [C["BLUE"]] * len(im), line=dict(width=0)),
                link=dict(source=[ex.index(e) for e in r["exporter_ar"]],
                          target=[len(ex) + im.index(i) for i in r["importer_ar"]],
                          value=r["quantity"], color="rgba(255,201,60,.30)",
                          hovertemplate="%{source.label} ← %{target.label}<br>%{value:,} طير<extra></extra>")))
            st.plotly_chart(style(fig, None, 520), width="stretch")
            note("💡 <b>جنوب أفريقيا</b> هي «مزرعة الببغاوات» في العالم: صدّرت <b>5.6 مليون</b> طير، "
                 "أغلبها مُربّى في الأسر، ورايحة لجنوب آسيا والشرق الأوسط.")

        elif view == "🪶 صفات الببغاوات":
            sp = TS.groupby("species")["quantity"].sum().rename("traded")
            PP = P.drop(columns="total_traded").merge(sp, on="species", how="left").fillna({"traded": 0})
            PP["traded_plot"] = PP["traded"].clip(lower=1)
            fig = px.scatter(PP, x="mass_g", y="traded_plot", color="diet_ar",
                             size=np.sqrt(PP["range_km2"].fillna(1e4)), size_max=32, hover_name="name",
                             log_x=True, log_y=True,
                             hover_data={"mass_g": ":.0f", "traded": ":,", "habitat_ar": True, "traded_plot": False},
                             color_discrete_sequence=[C["GOLD"], C["CAPT"], C["WILD"], C["BLUE"], "#A493C4"],
                             labels={"mass_g": "الوزن (جم)", "traded_plot": "عدد الطيور", "traded": "عدد الطيور",
                                     "diet_ar": "الأكل", "habitat_ar": "البيئة"})
            fig.update_traces(marker=dict(line=dict(width=0), opacity=.78))
            st.plotly_chart(style(fig, "كل نوع: الوزن مقابل التجارة (حجم الدائرة = مساحة الانتشار)", 520),
                            width="stretch")
            note("💡 الحجم <b>ما يفرق كثير</b> (ρ = 0.14). اللي يفرق هو <b>مدى انتشار النوع</b> في الطبيعة (ρ = 0.47).")
            c1, c2 = st.columns(2)
            with c1:
                d = PP.groupby("diet_ar").agg(median=("traded", "median"),
                                              share=("traded", lambda s: (s > 0).mean())).reset_index()
                d = d.sort_values("median")
                fig = go.Figure(go.Bar(x=d["median"], y=d["diet_ar"], orientation="h", marker_color=C["GOLD"],
                                       text=[f"{m:,.0f} طير" for m in d["median"]], customdata=d["share"],
                                       hovertemplate="%{y}<br>الوسيط: %{x:,.0f} طير<br>انباع منها: %{customdata:.0%}<extra></extra>",
                                       textposition="outside", cliponaxis=False))
                fig.update_xaxes(range=[0, max(d["median"].max() * 1.9, 1)], visible=False)
                st.plotly_chart(style(fig, "وسيط التجارة لكل نوع حسب الأكل", 360), width="stretch")
            with c2:
                fig = px.box(P[P["habitat"] != "Unknown"], x="habitat_ar", y="mass_g", log_y=True, points="all",
                             hover_name="name", labels={"mass_g": "الوزن (جم)", "habitat_ar": ""})
                fig.update_traces(marker_color=C["CAPT"], line_color=C["GREEN"])
                st.plotly_chart(style(fig, "الوزن حسب البيئة", 360), width="stretch")
            note("💡 آكلين <b>الحبوب</b> و<b>الرحيق</b> و<b>كل شيء</b> ينباعون أكثر بكثير من آكلين <b>الفواكه</b>. "
                 "بس التصنيف هذا حسب أكلهم <b>في الطبيعة</b>: تسوكي (كنيور قرين تشيك) يُصنّف آكل فواكه، "
                 "بس في البيت يأكل حبوب وخضار، وترتيبه <b>#14</b> 💚")
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Histogram(x=np.log10(P["mass_g"]), nbinsx=35, marker_color=C["CAPT"],
                                             marker_line=dict(color=C["CARD"], width=1)))
                fig.update_xaxes(title="الوزن (جم، مقياس لوغاريتمي)", tickvals=[1, 1.5, 2, 2.5, 3],
                                 ticktext=["10", "32", "100", "316", "1,000"])
                fig.update_yaxes(title="عدد الأنواع")
                st.plotly_chart(style(fig, "توزيع الأوزان", 340), width="stretch")
            with c2:
                num = PP.assign(**{"الوزن": np.log10(PP["mass_g"]), "المنقار": PP["beak_length_mm"],
                                   "الجناح": PP["wing_length_mm"], "الذيل": PP["tail_length_mm"],
                                   "الانتشار": np.log10(PP["range_km2"]), "التجارة": np.log10(PP["traded"] + 1)})
                cols_ar = ["الوزن", "المنقار", "الجناح", "الذيل", "الانتشار", "التجارة"]
                corr = num[cols_ar].corr(method="spearman").round(2)
                fig = px.imshow(corr, text_auto=True, color_continuous_scale=[C["WILD"], C["CARD"], C["GREEN"]],
                                zmin=-1, zmax=1, aspect="auto")
                st.plotly_chart(style(fig, "الارتباط بين الصفات والتجارة", 340), width="stretch")

        else:
            c1, c2 = st.columns(2)
            max_range = c1.select_slider("«موطن صغير» يعني أقل من…", options=[10_000, 25_000, 50_000, 100_000, 250_000],
                                         value=50_000, format_func=lambda v: f"{v:,} كم²")
            min_wild = c2.select_slider("…وانصاد منه على الأقل", options=[100, 500, 1_000, 5_000, 10_000],
                                        value=1_000, format_func=lambda v: f"{v:,} طير")
            W2 = P[P["wild_traded"] > 0].copy()
            W2["danger"] = (W2["range_km2"] < max_range) & (W2["wild_traded"] >= min_wild)
            W2["حالة"] = W2["danger"].map({True: "في خطر", False: "باقي الأنواع"})
            fig = px.scatter(W2, x="range_km2", y="wild_traded", color="حالة",
                             color_discrete_map={"في خطر": C["WILD"], "باقي الأنواع": C["GREY"]}, hover_name="name",
                             log_x=True, log_y=True, size=np.where(W2["danger"], 16, 7), size_max=16,
                             hover_data={"wild_share": ":.0%", "range_km2": ":,.0f", "حالة": False},
                             labels={"range_km2": "مساحة الانتشار (كم²)", "wild_traded": "طيور مصطادة من البرية",
                                     "wild_share": "نسبة البري"})
            fig.add_vrect(x0=W2["range_km2"].min() * .8, x1=max_range, fillcolor=C["WILD"], opacity=.07, line_width=0)
            fig.add_hline(y=min_wild, line_dash="dot", line_color=C["WILD"])
            fig.update_traces(marker=dict(line=dict(width=0)))
            fig.update_layout(legend_title=None)
            D2 = W2[W2["danger"]].sort_values("wild_traded", ascending=False)
            st.plotly_chart(style(fig, f"{len(D2)} نوع في منطقة الخطر", 460), width="stretch")
            if not D2.empty:
                cols = st.columns(min(4, len(D2)))
                for i, (_, r) in enumerate(D2.head(4).iterrows()):
                    with cols[i]:
                        html(f"""<div class="album">{parrot_svg(r['species'], r['family'], 150)}
                        <div class="n">{name_ar(r['species'])}</div><div class="s">{r['species']}</div>
                        <div class="t" style="color:{C['WILD']}">{r['wild_traded']:,} طير بري</div></div>""")
                table = D2[["name", "family_ar", "range_km2", "wild_traded", "wild_share"]].rename(columns={
                    "name": "النوع", "family_ar": "العائلة", "range_km2": "مساحة الانتشار (كم²)",
                    "wild_traded": "طيور برية", "wild_share": "نسبة البري"})
                st.dataframe(table, hide_index=True, width="stretch", column_config={
                    "مساحة الانتشار (كم²)": st.column_config.NumberColumn(format="%d"),
                    "طيور برية": st.column_config.ProgressColumn(format="%d", min_value=0,
                                                                 max_value=int(D2["wild_traded"].max())),
                    "نسبة البري": st.column_config.NumberColumn(format="percent")})
            note("💡 أغلب هالأنواع <b>لوري وكوكاتو من جزر إندونيسيا وميلانيزيا</b>. و<b>كوكاتو غوفين</b> موطنه حوالي 4,000 كم² بس!")


# ═══════════════════════════ 🇸🇦 السعودية والخليج ═══════════════════════════
with tab_gulf:
    if need_data():
        G = T[T["importer_code"].isin(GULF)].assign(country=lambda d: d["importer_code"].map(GULF))
        if G.empty:
            st.info("ما فيه واردات خليجية بهالفلاتر.")
        else:
            sa = G[G["importer_code"] == "SA"]
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="mini"><div class="v">{fmt(sa["quantity"].sum())}</div>'
                        f'<div class="l">ببغاء استوردته السعودية 🇸🇦</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="mini"><div class="v">{fmt(G["quantity"].sum())}</div>'
                        f'<div class="l">استوردته دول الخليج الست</div></div>', unsafe_allow_html=True)
            if not sa.empty:
                after = sa.loc[sa["year"] >= 2016, "quantity"].sum() / max(sa["quantity"].sum(), 1)
                c3.markdown(f'<div class="mini"><div class="v">{after:.0%}</div>'
                            f'<div class="l">من واردات المملكة وصلت بعد 2016</div></div>', unsafe_allow_html=True)
            st.write("")
            g = G.groupby(["year", "country"])["quantity"].sum().reset_index()
            fig = px.area(g, x="year", y="quantity", color="country",
                          category_orders={"country": list(GULF.values())},
                          color_discrete_sequence=[C["GREEN"], C["WILD"], C["BLUE"], "#A493C4", C["GOLD"], "#7D8A83"],
                          labels={"year": "السنة", "quantity": "عدد الطيور", "country": "الدولة"})
            fig.update_traces(line_width=0)
            fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
            st.plotly_chart(style(fig, "واردات الببغاوات لدول الخليج", 420), width="stretch")
            c1, c2 = st.columns(2)
            s = G[G["species"].notna()].groupby("species")["quantity"].sum().nlargest(10).sort_values()
            f = go.Figure(go.Bar(x=s.values, y=[name_ar(x) for x in s.index], orientation="h", marker_color=C["GOLD"],
                                 text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
            f.update_xaxes(visible=False, range=[0, s.max() * 1.35])
            c1.plotly_chart(style(f, "وش يشتري الخليج؟", 420), width="stretch")
            s = G.groupby("exporter_ar")["quantity"].sum().nlargest(10).sort_values()
            f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=C["WILD"],
                                 text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
            f.update_xaxes(visible=False, range=[0, s.max() * 1.35])
            c2.plotly_chart(style(f, "من وين تجي؟", 420), width="stretch")


# ═══════════════════════════ 📋 البيانات ═══════════════════════════
with tab_data:
    if need_data():
        which = st.segmented_control("الجدول", ["جدول الأنواع (المدموج)", "سجلات التجارة (النظيفة)"],
                                     default="جدول الأنواع (المدموج)", key="data_view") or "جدول الأنواع (المدموج)"
        if which.startswith("جدول الأنواع"):
            df = P.drop(columns=["diet_ar", "habitat_ar", "family_ar", "name", "rank"])
        else:
            df = T.drop(columns=["exporter_ar", "importer_ar", "exporter_iso3", "importer_iso3",
                                 "source_ar", "family_en"])
        st.markdown(f"**{len(df):,} صف × {df.shape[1]} عمود** (بعد الفلاتر)")
        st.dataframe(df.head(500), width="stretch", hide_index=True)
        st.markdown("#### 📊 الإحصائيات")
        st.dataframe(df.describe().T.round(2), width="stretch")
        st.download_button("⬇️ نزّلوا البيانات المفلترة (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                           "parrots_filtered.csv", "text/csv")

html('<div class="foot">جواز سفر الببغاء · نوره السويلم وتسوكي 💚 · البيانات: CITES Trade Database (UNEP-WCMC) '
     'و AVONET (Tobias et al. 2022) · التجارة القانونية المسجّلة فقط، وبيانات 2024 قد تكون ناقصة</div>')
