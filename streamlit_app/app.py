"""
🦜 ريش بلا حدود: قصة تجارة الببغاوات حول العالم
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
                        HOME_DIET, PET_PROFILE, SOURCE_AR, country_ar, display_name, has_photo,
                        name_ar, photo_credit, photo_url)
from parrot_art import parrot_svg

st.set_page_config(page_title="ريش بلا حدود 🦜", page_icon="🦜", layout="wide",
                   initial_sidebar_state="collapsed")

# ═══════════════════════════ الألوان (داكن وهادئ) ═══════════════════════════
BG, CARD, LINE = "#111816", "#18221F", "#263430"
TEXT, SOFT, MUTED = "#E9EEEA", "#C4D0C9", "#9AABA2"
SAGE, WILD, CAPT, GREY, GOLD, BLUE = "#8CC5A0", "#E07A5F", "#6FAF86", "#3A4842", "#E9B872", "#7FB3D5"
SOURCE_COLORS = {"مصطاد من البرية": WILD, "مُربّى في الأسر": CAPT, "مُربّى من بيض بري": GOLD,
                 "مُصادَر": "#A493C4", "قبل الاتفاقية": "#5A6B63", "غير معروف": GREY}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, p, li, label, h1, h2, h3, h4, input, textarea, button,
[data-testid="stMarkdownContainer"], [data-baseweb="tab"], [data-baseweb="select"] {{
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
}}
.main .block-container, [data-testid="stMarkdownContainer"], .stTabs, label, .stRadio,
.stSelectbox, .stMultiSelect, [data-testid="stPopoverBody"] {{ direction: rtl; text-align: right; }}
[data-testid="stSlider"] [data-baseweb="slider"] {{ direction: ltr; }}
.block-container {{ max-width: 1180px; padding-top: 3.6rem; }}
.stApp {{ background: {BG}; }}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{ display: none; }}

/* التبويبات: أزرار هادئة */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; flex-wrap: wrap; background: {CARD}; border: 1px solid {LINE};
    border-radius: 16px; padding: 6px; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 12px; padding: 10px 18px; font-size: 16px; font-weight: 500;
    color: {SOFT}; background: transparent; }}
.stTabs [aria-selected="true"] {{ background: {SAGE} !important; color: #0F1A15 !important; font-weight: 700; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* الكروت */
.card {{ background: {CARD}; border: 1px solid {LINE}; border-radius: 22px; padding: 22px 26px; }}
.kicker {{ color: {SAGE}; font-size: 14px; font-weight: 600; margin: 0; }}
.kicker.red {{ color: #EE9478; }}
.h1 {{ font-size: 48px; font-weight: 700; line-height: 1.2; color: {TEXT}; margin: 8px 0 14px; }}
.h2 {{ font-size: 32px; font-weight: 700; line-height: 1.3; color: {TEXT}; margin: 6px 0 10px; }}
.lead {{ font-size: 18px; line-height: 1.9; color: {SOFT}; }}
.lead b {{ color: {TEXT}; }}
.big {{ font-size: 96px; font-weight: 700; line-height: 1; color: {TEXT}; text-align: center; }}
.center {{ text-align: center; }}
.mini {{ background: {CARD}; border: 1px solid {LINE}; border-radius: 18px; padding: 16px 18px; text-align: center; }}
.mini .v {{ font-size: 28px; font-weight: 700; color: {TEXT}; }}
.mini .l {{ font-size: 14px; color: {MUTED}; margin-top: 2px; }}
.note {{ background: #1F2D28; border-radius: 14px; padding: 14px 18px; color: #D3DED7; font-size: 16px; line-height: 1.8; margin: 10px 0 6px; }}
.note b {{ color: {TEXT}; }}
.reveal {{ font-size: 19px; line-height: 1.8; color: #D3DED7; text-align: center; padding: 10px 0; }}
.reveal b.ok {{ color: {SAGE}; }}
.reveal b.no {{ color: #EE9478; }}
.chapters {{ display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin: 4px 0 26px; }}
.chapters a {{ text-decoration: none; padding: 6px 14px; border-radius: 999px; color: {SOFT};
    border: 1px solid {LINE}; font-size: 14px; }}
.chapters a:hover {{ border-color: {SAGE}; color: {TEXT}; }}
.dots {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 7px; max-width: 420px; }}
.dots span {{ display: block; aspect-ratio: 1; border-radius: 50%; }}
.danger-row {{ display: flex; justify-content: space-between; gap: 10px; padding: 14px 18px; border-radius: 14px;
    background: {CARD}; border: 1px solid #3A2A25; margin-bottom: 10px; color: {TEXT}; }}
.danger-row b {{ color: #EE9478; }}
.tool {{ background: {CARD}; border: 1px solid {LINE}; border-radius: 20px; padding: 20px; height: 100%; }}
.tool .t {{ font-size: 19px; font-weight: 700; color: {TEXT}; margin: 6px 0 4px; }}
.tool .d {{ font-size: 15px; color: {MUTED}; }}
.spacer {{ height: 64px; }}

/* الصور */
.photo {{ border-radius: 22px; overflow: hidden; border: 1px solid {LINE}; background: {CARD}; }}
.photo img {{ width: 100%; display: block; object-fit: cover; object-position: center 30%; }}
.photo .cap {{ font-size: 12px; color: {MUTED}; padding: 6px 12px; direction: ltr; text-align: left; }}
.album {{ background: {CARD}; border: 1px solid {LINE}; border-radius: 20px; padding: 10px 10px 14px;
    text-align: center; margin-bottom: 16px; }}
.album .ph {{ width: 100%; height: 190px; object-fit: cover; object-position: center 30%; border-radius: 14px; margin-bottom: 8px; }}
.album .n {{ font-size: 17px; font-weight: 700; color: {TEXT}; }}
.album .s {{ font-size: 13px; color: {MUTED}; font-style: italic; }}
.album .t {{ font-size: 15px; color: {SAGE}; font-weight: 600; margin-top: 4px; }}

/* بطاقة الببغاء */
.pcard .name {{ font-size: 30px; font-weight: 700; color: {TEXT}; line-height: 1.2; }}
.pcard .sci {{ font-style: italic; color: {MUTED}; font-size: 16px; direction: ltr; text-align: right; }}
.chip {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 14px; margin: 8px 0 0 6px;
    background: #22302B; color: {SOFT}; }}
.chip.red {{ background: #3A2A25; color: #EE9478; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; }}
.stats .v {{ font-size: 24px; font-weight: 700; color: {TEXT}; }}
.stats .l {{ font-size: 13px; color: {MUTED}; }}

/* اللعبة والمقارنة */
.match {{ background: {CARD}; border: 1px solid {LINE}; border-radius: 22px; padding: 14px; text-align: center; }}
.match.win {{ border: 2px solid {SAGE}; }}
.match .pct {{ font-size: 40px; font-weight: 700; color: {SAGE}; line-height: 1; margin-top: 6px; }}
.match .why {{ text-align: right; font-size: 15px; line-height: 1.9; color: {SOFT}; margin-top: 8px; }}
.vs {{ font-size: 40px; font-weight: 700; color: {SAGE}; text-align: center; padding-top: 120px; }}
.cmp {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
.cmp td {{ padding: 10px 12px; border-bottom: 1px solid {LINE}; text-align: center; color: {TEXT}; }}
.cmp td.k {{ color: {MUTED}; font-size: 15px; }}
.cmp td.w {{ color: {SAGE}; font-weight: 700; }}
.foot {{ color: {MUTED}; font-size: 13px; margin-top: 40px; text-align: center; }}
</style>
""", unsafe_allow_html=True)


def style(fig, title=None, h=430):
    """نفس الشكل الهادئ لكل الرسومات."""
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans Arabic, sans-serif", color=SOFT, size=14),
        margin=dict(l=10, r=10, t=50 if title else 16, b=10), height=h,
        title=dict(text=title, x=0.99, xanchor="right", font=dict(size=19, color=TEXT)),
        hoverlabel=dict(font_family="IBM Plex Sans Arabic", bgcolor=CARD),
    )
    fig.update_xaxes(gridcolor="#22302B", zeroline=False)
    fig.update_yaxes(gridcolor="#22302B", zeroline=False)
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


def space():
    html('<div class="spacer"></div>')


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
    fig.update_geos(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False, landcolor="#1F2D28",
                    showland=True, projection_type="natural earth", lataxis_range=[-58, 85])
    return fig


MAP_SCALE = ["#1F2D28", "#2E5444", CAPT, GOLD, WILD]


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

# ═══════════════════════════ الهيدر + الفلاتر ═══════════════════════════
h1, h2 = st.columns([3, 1])
h1.markdown(f'<p style="margin:0;font-size:24px;font-weight:700;color:{TEXT}">ريش بلا حدود</p>'
            f'<p style="margin:0;font-size:15px;color:{MUTED}">تجارة الببغاوات الحية حول العالم · 1975 إلى 2024 · إعداد نوره السويلم</p>',
            unsafe_allow_html=True)

# الفلاتر في زر واحد (تشتغل على تبويبات التحليل والخليج والبيانات، والقصة تبقى على كل البيانات)
with h2.popover("الفلاتر", icon=":material/tune:", width="stretch"):
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
    ":material/auto_stories: القصة", ":material/flutter_dash: الببغاوات", ":material/target: أي ببغاء يناسبك؟",
    ":material/insights: التحليل", ":material/mosque: السعودية والخليج", ":material/table_view: البيانات"])


def need_data():
    """لو الفلاتر فضّت البيانات، نطلع رسالة ونوقف هالتبويب."""
    if filters_empty:
        st.warning("ما فيه بيانات تنطبق على هالفلاتر. جرّبي توسّعينها من زر «الفلاتر» فوق 🙏")
        return False
    return True


# ═══════════════════════════ 📖 القصة ═══════════════════════════
with tab_story:
    # ── البداية ──
    c1, c2 = st.columns([1.35, 1], gap="large")
    with c1:
        html(f"""<div style="padding-top:40px">
        <p class="kicker">قصة تبدأ من بيتي</p>
        <div class="h1">عندي كنيور صغير،<br>وخلّاني أسأل: من وين تجي الببغاوات؟</div>
        <p class="lead">جمعت بيانات كل ببغاء حي انتقل بشكل قانوني بين الدول من 1975 إلى 2024،
        ودمجتها مع صفات كل الأنواع الـ 404. هذي القصة اللي طلعت لي 👇</p></div>""")
    with c2:
        html(photo_html("Pyrrhura molinae", 430))
        st.caption("كنيور الخدود الخضراء · Pyrrhura molinae")

    html("""<div class="chapters">
      <a href="#ch1">١ كم ببغاء؟</a><a href="#ch2">٢ من البرية للأسر</a><a href="#ch3">٣ خمّني</a>
      <a href="#ch4">٤ الحجم يفرق؟</a><a href="#ch5">٥ منطقة الخطر</a><a href="#ch6">٦ وإحنا؟</a>
      <a href="#ch7">استكشفي</a></div>""")
    space()

    # ── الفصل ١: كم ببغاء؟ ──
    total = trade["quantity"].sum()
    html(f"""<div id="ch1" class="center">
      <p class="kicker">الفصل ١ · كم ببغاء؟</p>
      <div class="big">{total / 1e6:.1f} مليون</div>
      <p class="lead" style="max-width:720px;margin:14px auto 0">ببغاء حي انتقل بين الدول في 50 سنة. يعني تقريباً
      <b>{total / 50 / 1e3:.0f} ألف طير كل سنة</b>، من {trade['exporter_code'].nunique()} دولة إلى {trade['importer_code'].nunique()} دولة.</p>
    </div>""")
    st.write("")
    m = st.columns(3)
    for col, (v, l) in zip(m, [(f"{parrots['in_trade'].sum()}", "نوع دخل التجارة من 404"),
                               (f"{len(trade):,}", "سجل تجارة بعد التنظيف"),
                               (fmt(trade.loc[trade["exporter_code"] == "ZA", "quantity"].sum()), "صدّرتها جنوب أفريقيا لحالها")]):
        col.markdown(f'<div class="mini"><div class="v">{v}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)

    st.write("")
    with st.expander("شوفي الخريطة تتحرك عبر 50 سنة (اضغطي ▶️)", icon=":material/public:"):
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
                            range_color=(0, anim["log_q"].max()), color_continuous_scale=MAP_SCALE,
                            labels={"quantity": "طير", "period": "الفترة"})
        fig.update_traces(marker_line_color=BG, marker_line_width=.4)
        geo_style(fig)
        fig.update_coloraxes(colorbar=dict(title="طير", tickvals=[1, 2, 3, 4, 5, 6],
                                           ticktext=["10", "100", "1k", "10k", "100k", "1M"], len=.6))
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 900
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300
        fig.layout.sliders[0].currentvalue.prefix = "الفترة: "
        st.plotly_chart(style(fig, None, 520), width="stretch")
    space()

    # ── الفصل ٢: من البرية للأسر ──
    with st.container(border=True):
        html("""<div id="ch2"><p class="kicker">الفصل ٢ · من البرية إلى الأسر</p>
        <div class="h2">القوانين غيّرت كل شي</div>
        <p class="lead">اضغطي على كل فترة، وشوفي كم ببغاء من كل 100 كان مصطاد من البرية:</p></div>""")
        known = trade[trade["source"].isin(["Wild-caught", "Captive-bred", "Ranched"])].copy()
        known["decade"] = known["year"] // 10 * 10
        dec = known.pivot_table(index="decade", columns="source", values="quantity", aggfunc="sum", fill_value=0)
        wild_share = (dec["Wild-caught"] / dec.sum(axis=1) * 100)
        labels = {1990: "التسعينات", 2000: "الألفين", 2010: "2010 وما بعد", 2020: "2020 وما بعد"}
        notes = {1990: "في التسعينات: تقريباً نص الطيور من البرية",
                 2000: "في الألفين: بعد حظر أمريكا (1992) نزلت",
                 2010: "بعد حظر أوروبا (2005) نزلت أكثر",
                 2020: "اليوم: أقل من 5 من كل 100"}
        pick = st.segmented_control("الفترة", list(labels.values()), default="التسعينات",
                                    key="decade", label_visibility="collapsed") or "التسعينات"
        d = [k for k, v in labels.items() if v == pick][0]
        pct = round(wild_share[d])
        dots = "".join(f'<span style="background:{WILD if i < pct else "#2E4A3D"}"></span>' for i in range(100))
        a, b = st.columns([1, 1.4])
        a.markdown(f'<div style="font-size:88px;font-weight:700;color:#EE9478;line-height:1;margin-top:20px">{pct}%</div>'
                   f'<p class="lead">{notes[d]}</p>', unsafe_allow_html=True)
        b.markdown(f'<div class="dots" role="img" aria-label="{pct} من كل 100 مصطاد من البرية">{dots}</div>',
                   unsafe_allow_html=True)

        yearly = trade.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
        fig = px.area(yearly, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                      category_orders={"source_ar": list(SOURCE_COLORS)},
                      labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
        for y, txt in [(1992, "حظر أمريكا"), (2005, "حظر أوروبا")]:
            fig.add_vline(x=y, line_dash="dash", line_color=SOFT, opacity=.5)
            fig.add_annotation(x=y, y=1, yref="paper", text=txt, showarrow=False, xanchor="left", xshift=6,
                               font=dict(size=13, color=SOFT))
        fig.update_traces(line_width=0)
        fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
        st.plotly_chart(style(fig, "عدد الببغاوات كل سنة حسب المصدر", 400), width="stretch")
        note("أكبر نزلتين صارت بعد <b>حظر أمريكا للطيور البرية (1992)</b> و<b>حظر أوروبا (2005)</b>. "
             "يعني القوانين فعلاً نفعت. (اللون الرمادي في الثمانينات معناه إن المصدر ما كان ينكتب.)")
    space()

    # ── الفصل ٣: خمّني ──
    html("""<div id="ch3" class="center"><p class="kicker">الفصل ٣ · خمّني</p>
    <div class="h2">أي واحد فيهم انباع أكثر شي في العالم؟</div></div>""")
    options = [("Psittacus erithacus", "الكاسكو"), ("Agapornis fischeri", "طائر الحب فيشر"),
               ("Pyrrhura molinae", "كنيور الخدود الخضراء")]
    top_sp = parrots.sort_values("total_traded", ascending=False)
    guess = st.session_state.get("guess")
    gcols = st.columns(3)
    for col, (sp, nm) in zip(gcols, options):
        with col:
            r = parrots[parrots["species"] == sp].iloc[0]
            border = LINE
            if guess:
                border = SAGE if sp == top_sp.iloc[0]["species"] else (WILD if sp == guess else LINE)
            html(f'<div style="border:2px solid {border};border-radius:24px;overflow:hidden">{photo_html(sp, 250)}</div>')
            if guess:
                html(f'<p class="center" style="color:{SOFT};margin:8px 0">{fmt(r["total_traded"])} طير · الترتيب #{r["rank"]}</p>')
            if st.button(nm, key=f"g_{sp}", width="stretch"):
                st.session_state["guess"] = sp
                st.rerun()
    if guess:
        right = guess == top_sp.iloc[0]["species"]
        top10 = top_sp.head(10)["total_traded"].sum() / top_sp["total_traded"].sum()
        html(f'<div class="reveal"><b class="{"ok" if right else "no"}">{"صح عليك! 🎉" if right else "قريب، بس لا 😅"}</b> '
             f'{name_ar(top_sp.iloc[0]["species"])} هو الأول بـ {fmt(top_sp.iloc[0]["total_traded"])} طير. '
             f'وأكثر 10 أنواع لحالها تشكّل <b>{top10:.0%}</b> من كل الطيور.</div>')
        t10 = top_sp.head(10).iloc[::-1]
        fig = go.Figure(go.Bar(x=t10["total_traded"], y=[name_ar(s) for s in t10["species"]], orientation="h",
                               marker_color=[GOLD if s == "Pyrrhura molinae" else CAPT for s in t10["species"]],
                               text=[fmt(v) for v in t10["total_traded"]], textposition="outside", cliponaxis=False))
        fig.update_xaxes(visible=False, range=[0, t10["total_traded"].max() * 1.25])
        st.plotly_chart(style(fig, "أكثر 10 ببغاوات انباعت", 420), width="stretch")
    space()

    # ── الفصل ٤: الحجم يفرق؟ ──
    with st.container(border=True):
        html("""<div id="ch4"><p class="kicker">الفصل ٤ · سؤال</p>
        <div class="h2">تتوقعين الببغاوات الكبيرة تنباع أكثر؟</div></div>""")
        size_ans = st.session_state.get("size_ans")
        b1, b2, _ = st.columns([1, 1, 2])
        if b1.button("إيه، الكبير أحلى", width="stretch", type="primary" if size_ans == "yes" else "secondary"):
            st.session_state["size_ans"] = "yes"
            st.rerun()
        if b2.button("لا، ما أتوقع", width="stretch", type="primary" if size_ans == "no" else "secondary"):
            st.session_state["size_ans"] = "no"
            st.rerun()
        if size_ans:
            tr = parrots[parrots["in_trade"]]
            rho_m = np.log10(parrots["total_traded"] + 1).corr(np.log10(parrots["mass_g"]), method="spearman")
            rho_r = np.log10(parrots["total_traded"] + 1).corr(np.log10(parrots["range_km2"]), method="spearman")
            html(f'<div class="reveal" style="text-align:right"><b class="{"ok" if size_ans == "no" else "no"}">'
                 f'{"صح! 👏" if size_ans == "no" else "مفاجأة:"}</b> الحجم تقريباً ما يفرق (الارتباط {rho_m:.2f} بس). '
                 f'اللي يفرق فعلاً هو <b>كم النوع منتشر في الطبيعة</b> ({rho_r:.2f}): الأنواع المنتشرة أسهل وأرخص، '
                 f'فتصير هي اللي في المحلات.</div>')
            fig = px.scatter(tr, x="mass_g", y="total_traded", log_x=True, log_y=True, hover_name="name",
                             labels={"mass_g": "الوزن (جم)", "total_traded": "عدد الطيور"})
            fig.update_traces(marker=dict(color=CAPT, size=9, opacity=.6, line=dict(width=0)))
            me = tr[tr["species"] == "Pyrrhura molinae"]
            fig.add_trace(go.Scatter(x=me["mass_g"], y=me["total_traded"], mode="markers+text",
                                     text=["كنيوري 💚"], textposition="top center", hoverinfo="skip",
                                     marker=dict(color=GOLD, size=16), textfont=dict(color=GOLD, size=14)))
            fig.update_layout(showlegend=False)
            st.plotly_chart(style(fig, "كل نقطة = نوع ببغاء: الوزن مقابل التجارة", 420), width="stretch")
    space()

    # ── الفصل ٥: منطقة الخطر ──
    html('<div id="ch5"></div>')
    W = parrots[parrots["wild_traded"] > 0].copy()
    W["danger"] = (W["range_km2"] < 50_000) & (W["wild_traded"] > 1_000)
    D = W[W["danger"]].sort_values("wild_traded", ascending=False)
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        html(f"""<p class="kicker red">الفصل ٥ · منطقة الخطر</p>
        <div class="h2">{len(D)} نوع بيتها صغير، وانصاد منها آلاف</div>
        <p class="lead">أغلبها لوري وكوكاتو من جزر إندونيسيا. موطن كل واحد منها أصغر من 50 ألف كم²
        (تقريباً بحجم القصيم)، ومع ذلك انصاد من كل نوع أكثر من 1,000 طير من البرية.</p>""")
    with c2:
        for _, r in D.head(3).iterrows():
            html(f'<div class="danger-row"><span>{name_ar(r["species"])}</span>'
                 f'<b>{r["wild_traded"]:,} طير بري</b></div>')
        st.caption("غيّري الحدود بنفسك من تبويب «التحليل» ← منطقة الخطر")
    fig = px.scatter(W, x="range_km2", y="wild_traded", log_x=True, log_y=True, hover_name="name",
                     color=W["danger"].map({True: "في خطر", False: "باقي الأنواع"}),
                     color_discrete_map={"في خطر": WILD, "باقي الأنواع": "#4A5C54"},
                     labels={"range_km2": "مساحة الموطن (كم²)", "wild_traded": "طيور مصطادة من البرية", "color": ""})
    fig.add_vrect(x0=W["range_km2"].min() * .8, x1=50_000, fillcolor=WILD, opacity=.07, line_width=0)
    fig.add_hline(y=1_000, line_dash="dot", line_color=WILD)
    fig.update_traces(marker=dict(size=10, line=dict(width=0)))
    fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
    st.plotly_chart(style(fig, None, 380), width="stretch")
    space()

    # ── الفصل ٦: وإحنا؟ ──
    with st.container(border=True):
        html('<div id="ch6"></div>')
        sa = trade[trade["importer_code"] == "SA"]
        after = sa.loc[sa["year"] >= 2016, "quantity"].sum() / sa["quantity"].sum()
        sa_top = sa.groupby("species")["quantity"].sum().idxmax()
        c1, c2 = st.columns([1.3, 1], gap="large")
        with c1:
            html(f"""<p class="kicker">الفصل ٦ · وإحنا؟ 🇸🇦</p>
            <div class="h2">السعودية استوردت {sa['quantity'].sum():,} ببغاء</div>
            <p class="lead">الاستيراد شبه وقف بين 2005 و2014، وبعدها رجع بقوة: <b>{after:.0%} من كل الببغاوات</b>
            اللي دخلت المملكة وصلت بعد 2016، وأكثرها طيور الحب.</p>""")
            s = sa.groupby("year")["quantity"].sum().reindex(range(1975, 2025), fill_value=0)
            fig = go.Figure(go.Scatter(x=s.index, y=s.values, fill="tozeroy", mode="lines",
                                       line=dict(color=SAGE, width=2), fillcolor="rgba(140,197,160,.25)",
                                       hovertemplate="%{x}: %{y:,} طير<extra></extra>"))
            st.plotly_chart(style(fig, "واردات السعودية كل سنة", 280), width="stretch")
        with c2:
            html(pic_or_svg(sa_top, "True parrots", 330))
            st.caption(f"{name_ar(sa_top)}: أكثر ببغاء استوردته المملكة")
    space()

    # ── استكشفي ──
    html("""<div id="ch7" class="center"><p class="kicker">دورك الحين</p>
    <div class="h2">استكشفي بنفسك</div><p class="lead">كل أداة لها تبويب فوق 👆</p></div>""")
    tools = [(":material/target:", "أي ببغاء يناسبك؟", "6 أسئلة وتطلع لك أنسب 3 أنواع"),
             (":material/flutter_dash:", "الببغاوات", "تعرّفي على أي نوع، قارني بين اثنين، أو تصفّحي الألبوم"),
             (":material/insights:", "التحليل", "الخريطة، طرق التجارة، الصفات، ومنطقة الخطر بحدودك"),
             (":material/table_view:", "البيانات", "الجداول والإحصائيات وتحميل CSV")]
    for col, (ic, t, dsc) in zip(st.columns(4), tools):
        with col:
            with st.container(border=True):
                st.markdown(f"### {ic}")
                st.markdown(f"**{t}**")
                st.caption(dsc)


# ═══════════════════════════ 🦜 الببغاوات ═══════════════════════════
with tab_birds:
    view = st.segmented_control("القسم", ["تعرّف على ببغاء", "قارني بين ببغاوين", "الألبوم"],
                                default="تعرّف على ببغاء", key="birds_view",
                                label_visibility="collapsed") or "تعرّف على ببغاء"
    st.write("")
    opts = parrots.sort_values("total_traded", ascending=False)["species"].tolist()

    if view == "تعرّف على ببغاء":
        pick = st.selectbox("اختاري ببغاء (مرتبة من الأكثر تجارة)", opts, index=opts.index("Pyrrhura molinae"),
                            format_func=display_name)
        b = parrots[parrots["species"] == pick].iloc[0]
        info = FEATURED.get(pick, {})
        bt = trade[trade["species"] == pick]
        heavier = (parrots["mass_g"] < b["mass_g"]).mean()
        wild_s = f"{b['wild_share']:.0%}" if pd.notna(b["wild_share"]) else "–"
        rng = f"{b['range_km2']:,.0f} كم²" if pd.notna(b["range_km2"]) else "غير معروفة"

        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            html(pic_or_svg(pick, b["family"], 380))
            if info:
                note(f"✨ {info['fact']}")
        with c2:
            chips = (f'<span class="chip">{b["family_ar"]}</span><span class="chip">{b["habitat_ar"]}</span>'
                     f'<span class="chip">{b["diet_ar"]} (في الطبيعة)</span>')
            if (bt["cites_appendix"] == "I").any():
                chips += '<span class="chip red">محمي: الملحق الأول</span>'
            html(f"""<div class="card pcard">
              <div class="name">{name_ar(pick)}</div><div class="sci">{pick}</div><div>{chips}</div>
              <div class="stats">
                <div><div class="v">{b['mass_g']:,.0f} جم</div><div class="l">أثقل من {heavier:.0%} من الببغاوات</div></div>
                <div><div class="v">#{b['rank']}</div><div class="l">ترتيبه في التجارة من 404</div></div>
                <div><div class="v">{fmt(b['total_traded'])}</div><div class="l">طير انتقل بين الدول</div></div>
                <div><div class="v" style="color:#EE9478">{wild_s}</div><div class="l">مصطاد من البرية</div></div>
                <div><div class="v">{rng}</div><div class="l">مساحة انتشاره</div></div>
                <div><div class="v">{int(b['n_exporters'])}</div><div class="l">دولة صدّرته</div></div>
              </div></div>""")
            if info.get("pet"):
                html(f"""<div class="card" style="margin-top:14px;line-height:1.9;color:{SOFT}">
                  <p class="kicker" style="margin-bottom:6px">معلومات للمربّين</p>
                  <b style="color:{TEXT}">موطنه:</b> {info['origin']}<br>
                  <b style="color:{TEXT}">الطول:</b> {info['length']} · <b style="color:{TEXT}">العمر:</b> {info['life']}<br>
                  <b style="color:{TEXT}">الكلام:</b> {info['talk']} · <b style="color:{TEXT}">الإزعاج:</b> {info['noise']}<br>
                  <b style="color:{TEXT}">الأكل في البيت:</b> {HOME_DIET}
                  <div style="font-size:13px;color:{MUTED};margin-top:8px">معلومات عامة وتقريبية. لأي سؤال صحي راجعي طبيب طيور.</div>
                </div>""")
            elif info:
                html(f'<div class="card" style="margin-top:14px"><p class="kicker">موطنه</p>{info["origin"]}</div>')

        if bt.empty:
            st.success("🌿 هالنوع **ما انباع ولا طير منه** بين الدول. محظوظ!")
        else:
            y = bt.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
            fig = px.bar(y, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                         labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
            fig.update_layout(legend=dict(orientation="h", y=-.2, title=None), bargap=.15)
            st.plotly_chart(style(fig, "تاريخ تجارته", 340), width="stretch")
            cc1, cc2, cc3 = st.columns([1, 1, 1.1])
            for cc, side_, color, ttl in [(cc1, "exporter_ar", WILD, "مين يبيعه؟"),
                                          (cc2, "importer_ar", BLUE, "مين يشتريه؟")]:
                s = bt.groupby(side_)["quantity"].sum().nlargest(6).sort_values()
                f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=color,
                                     text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
                f.update_xaxes(visible=False, range=[0, s.max() * 1.45])
                cc.plotly_chart(style(f, ttl, 300), width="stretch")
            if pd.notna(b["lat"]):
                f = go.Figure(go.Scattergeo(lat=[b["lat"]], lon=[b["lon"]], mode="markers",
                                            marker=dict(size=max(12, min(60, np.sqrt(b["range_km2"] or 1) / 25)),
                                                        color=GOLD, opacity=.8, line=dict(color="white", width=1))))
                geo_style(f)
                cc3.plotly_chart(style(f, "وين يعيش في الطبيعة؟", 300), width="stretch")

    elif view == "قارني بين ببغاوين":
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
        rows = [("الوزن (جم)", "mass_g", "{:,.0f}", None),
                ("طول الجناح (مم)", "wing_length_mm", "{:,.0f}", None),
                ("مساحة الانتشار (كم²)", "range_km2", "{:,.0f}", "max"),
                ("طيور انتقلت بين الدول", "total_traded", "{:,.0f}", None),
                ("ترتيبه في التجارة", "rank", "#{:.0f}", None),
                ("نسبة المصطاد من البرية", "wild_share", "{:.1%}", "min"),
                ("دول صدّرته", "n_exporters", "{:,.0f}", None)]
        t = (f'<table class="cmp"><tr><td class="w" style="color:{TEXT}">{name_ar(a)}</td><td></td>'
             f'<td class="w" style="color:{TEXT}">{name_ar(bb)}</td></tr>')
        for label, col, f, win in rows:
            va, vb = A[col], B[col]
            ca = cb = ""
            if win and pd.notna(va) and pd.notna(vb) and va != vb:
                better_a = (va > vb) if win == "max" else (va < vb)
                ca, cb = ("w", "") if better_a else ("", "w")
            t += f'<tr><td class="{ca}">{val(va, f)}</td><td class="k">{label}</td><td class="{cb}">{val(vb, f)}</td></tr>'
        t += (f'<tr><td>{A["diet_ar"]}</td><td class="k">الأكل (في الطبيعة)</td><td>{B["diet_ar"]}</td></tr>'
              f'<tr><td>{A["habitat_ar"]}</td><td class="k">البيئة</td><td>{B["habitat_ar"]}</td></tr></table>')
        st.write("")
        html(t)
        st.caption("الأخضر = الأحسن للطير نفسه: انتشار أكبر في الطبيعة، ونسبة أقل مصطادة من البرية.")
        both = (trade[trade["species"].isin([a, bb])].groupby(["year", "species"])["quantity"].sum()
                .reset_index().assign(name=lambda d: d["species"].map(name_ar)))
        if not both.empty:
            fig = px.line(both, x="year", y="quantity", color="name", markers=True,
                          color_discrete_sequence=[GOLD, BLUE],
                          labels={"year": "السنة", "quantity": "عدد الطيور", "name": ""})
            fig.update_layout(legend=dict(orientation="h", y=-.2))
            st.plotly_chart(style(fig, "تجارتهم عبر السنين", 360), width="stretch")
        # الحجم الحقيقي: نرسم الطيرين بنسبة طول الجناح
        if pd.notna(A["wing_length_mm"]) and pd.notna(B["wing_length_mm"]):
            big = max(A["wing_length_mm"], B["wing_length_mm"])
            sa_, sb_ = int(60 + 180 * A["wing_length_mm"] / big), int(60 + 180 * B["wing_length_mm"] / big)
            html(f"""<div class="card" style="text-align:center">
              <div style="font-weight:700;font-size:19px;margin-bottom:8px;color:{TEXT}">الحجم الحقيقي جنب بعض</div>
              <div style="display:flex;justify-content:center;align-items:flex-end;gap:50px;color:{SOFT}">
                <div>{parrot_svg(a, A['family'], sa_)}<div>{name_ar(a)}</div></div>
                <div>{parrot_svg(bb, B['family'], sb_)}<div>{name_ar(bb)}</div></div>
              </div></div>""")

    else:
        a1, a2 = st.columns([1, 2])
        album_view = a1.segmented_control("العرض", ["صور", "رسومات"], default="صور", key="album_view",
                                          label_visibility="collapsed") or "صور"
        a2.caption("الصور اخترتها أنا أو من Wikimedia Commons، والرسومات مرسومة بالكود بألوان كل نوع.")
        album = parrots[parrots["species"].isin(FEATURED)].sort_values("total_traded", ascending=False)
        cols = st.columns(4)
        for i, (_, r) in enumerate(album.iterrows()):
            f = FEATURED[r["species"]]
            traded = fmt(r["total_traded"]) + " طير" if r["total_traded"] else "ما انباع أبداً 🌿"
            if album_view == "صور" and has_photo(r["species"]):
                pic = (f'<img class="ph" src="{photo_url(r["species"], 400)}" loading="lazy" '
                       f'alt="{f["ar"]}" title="{photo_credit(r["species"])}">')
            else:
                pic = parrot_svg(r["species"], r["family"], 170)
            with cols[i % 4]:
                html(f"""<div class="album">{pic}<div class="n">{f['ar']}</div>
                  <div class="s">{r['species']}</div><div class="t">{traded}</div></div>""")


# ═══════════════════════════ 🎯 أي ببغاء يناسبك؟ ═══════════════════════════
with tab_quiz:
    html('<div class="h2">أي ببغاء يناسبك؟</div>')
    st.caption(f"جاوبي على 6 أسئلة، وأطلع لك أنسب 3 ببغاوات من {len(PET_PROFILE)} نوع مشهور. (تقريبي وللمتعة 😄)")
    with st.container(border=True):
        q1, q2 = st.columns(2)
        space_ = q1.radio("وين بيعيش الطير؟", ["شقة صغيرة", "شقة كبيرة أو بيت", "بيت كبير وفيه غرفة للطير"], index=1)
        noise = q2.radio("كم تتحملين الإزعاج؟", ["لازم يكون هادئ", "شوي عادي", "ما يهمني أبداً"], index=1)
        talk = q1.radio("تبينه يتكلم؟", ["إيه، هذا أهم شي", "حلو لو يتكلم بس مو شرط", "ما يهمني"], index=1)
        time = q2.radio("كم ساعة تقدرين تجلسين معه كل يوم؟", ["ساعة أو أقل", "ساعتين إلى ثلاث", "أغلب اليوم"], index=1)
        years = q1.radio("كم سنة تقدرين تلتزمين فيه؟", ["10 إلى 20 سنة", "20 إلى 40 سنة", "أكثر من 40 سنة"], index=1)
        exp = q2.radio("خبرتك مع الطيور؟", ["هذا أول ببغاء لي", "عندي خبرة"], index=0)

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
            why.append("✅ حجمه مناسب لمكانك")
        if p["noise"] > max_noise:
            score -= 25 * (p["noise"] - max_noise); why.append("⚠️ صوته أعلى من اللي تتحملينه")
        else:
            why.append("✅ صوته مقبول لك")
        if talk.startswith("إيه"):
            score -= 20 * max(0, 2 - p["talk"])
            why.append("✅ يتكلم كويس" if p["talk"] >= 2 else "⚠️ كلامه قليل")
        elif talk.startswith("حلو"):
            score -= 5 * max(0, 2 - p["talk"])
        if p["care"] > max_care:
            score -= 25 * (p["care"] - max_care); why.append("⚠️ يحتاج وقت واهتمام أكثر")
        else:
            why.append("✅ يناسب وقتك")
        if p["life"] > max_life:
            score -= 20 if p["life"] - max_life <= 20 else 35; why.append(f"⚠️ ممكن يعيش {p['life']} سنة")
        if exp.startswith("هذا") and not p["easy"]:
            score -= 30; why.append("⚠️ يحتاج خبرة")
        # فروق صغيرة عشان ما يتعادلون كلهم على 100%
        if not noise.startswith("ما يهمني"):
            score -= 3 * (p["noise"] - 1)
        if not time.startswith("أغلب"):
            score -= 3 * (p["care"] - 1)
        if not talk.startswith("ما يهمني"):
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
          <div style="font-size:28px">{medals[i]}</div>{pic_or_svg(s, r['family'], 220)}
          <div style="font-size:21px;font-weight:700;margin-top:8px;color:{TEXT}">{name_ar(s)}</div>
          <div class="pct">{score}%</div><div style="color:{MUTED}">نسبة التوافق</div>
          <div class="why">{'<br>'.join(why[:5])}<br>🌿 من البرية: {wild} من تجارته</div>
        </div>""", unsafe_allow_html=True)
    note("مهما اخترتي، <b>اشتري طير مُربّى في الأسر</b> من مربّي موثوق. الطيور المصطادة من البرية "
         "تتأذى في النقل، وصيدها يضر الأنواع اللي موطنها صغير.")


# ═══════════════════════════ 📊 التحليل ═══════════════════════════
with tab_analysis:
    view = st.segmented_control("القسم", ["التجارة العالمية", "صفات الببغاوات", "منطقة الخطر"],
                                default="التجارة العالمية", key="ana_view",
                                label_visibility="collapsed") or "التجارة العالمية"
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

        if view == "التجارة العالمية":
            c1, c2 = st.columns([1.35, 1])
            with c1:
                side = st.segmented_control("الخريطة", ["الدول المصدّرة", "الدول المستوردة"], default="الدول المصدّرة",
                                            key="map_side", label_visibility="collapsed") or "الدول المصدّرة"
                key = "exporter" if side == "الدول المصدّرة" else "importer"
                geo = T.groupby([f"{key}_iso3", f"{key}_ar"])["quantity"].sum().reset_index().dropna()
                fig = px.choropleth(geo, locations=f"{key}_iso3", color=np.log10(geo["quantity"]),
                                    hover_name=f"{key}_ar", custom_data=["quantity"], color_continuous_scale=MAP_SCALE)
                fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>%{customdata[0]:,} طير<extra></extra>",
                                  marker_line_color=BG, marker_line_width=.4)
                geo_style(fig)
                fig.update_coloraxes(colorbar=dict(title="طير", tickvals=[1, 2, 3, 4, 5, 6],
                                                   ticktext=["10", "100", "1k", "10k", "100k", "1M"], len=.6))
                st.plotly_chart(style(fig, None, 430), width="stretch")
            with c2:
                top = T.groupby(f"{key}_ar")["quantity"].sum().nlargest(12).sort_values()
                fig = go.Figure(go.Bar(x=top.values, y=top.index, orientation="h",
                                       marker_color=WILD if key == "exporter" else BLUE,
                                       text=[fmt(v) for v in top.values], textposition="outside", cliponaxis=False))
                fig.update_xaxes(range=[0, top.max() * 1.3], visible=False)
                st.plotly_chart(style(fig, "أكبر 12 دولة " + ("مصدّرة" if key == "exporter" else "مستوردة"), 470),
                                width="stretch")
            st.markdown("#### أكبر طرق التجارة")
            n = st.slider("عدد الطرق", 5, 30, 15)
            r = T.groupby(["exporter_ar", "importer_ar"])["quantity"].sum().nlargest(n).reset_index()
            ex = list(dict.fromkeys(r["exporter_ar"]))
            im = list(dict.fromkeys(r["importer_ar"]))
            fig = go.Figure(go.Sankey(
                node=dict(label=[f"{e} " for e in ex] + [f" {i}" for i in im], pad=12, thickness=14,
                          color=[WILD] * len(ex) + [BLUE] * len(im), line=dict(width=0)),
                link=dict(source=[ex.index(e) for e in r["exporter_ar"]],
                          target=[len(ex) + im.index(i) for i in r["importer_ar"]],
                          value=r["quantity"], color="rgba(140,197,160,.22)",
                          hovertemplate="%{source.label} ← %{target.label}<br>%{value:,} طير<extra></extra>")))
            st.plotly_chart(style(fig, None, 520), width="stretch")
            note("<b>جنوب أفريقيا</b> هي «مزرعة الببغاوات» في العالم: صدّرت <b>5.6 مليون</b> طير، "
                 "أغلبها مُربّى في الأسر، ورايحة لجنوب آسيا والشرق الأوسط.")

        elif view == "صفات الببغاوات":
            sp = TS.groupby("species")["quantity"].sum().rename("traded")
            PP = P.drop(columns="total_traded").merge(sp, on="species", how="left").fillna({"traded": 0})
            PP["traded_plot"] = PP["traded"].clip(lower=1)
            fig = px.scatter(PP, x="mass_g", y="traded_plot", color="diet_ar",
                             size=np.sqrt(PP["range_km2"].fillna(1e4)), size_max=32, hover_name="name",
                             log_x=True, log_y=True,
                             hover_data={"mass_g": ":.0f", "traded": ":,", "habitat_ar": True, "traded_plot": False},
                             color_discrete_sequence=[GOLD, CAPT, WILD, BLUE, "#A493C4"],
                             labels={"mass_g": "الوزن (جم)", "traded_plot": "عدد الطيور", "traded": "عدد الطيور",
                                     "diet_ar": "الأكل", "habitat_ar": "البيئة"})
            fig.update_traces(marker=dict(line=dict(width=0), opacity=.75))
            st.plotly_chart(style(fig, "كل نوع: الوزن مقابل التجارة (حجم الدائرة = مساحة الانتشار)", 520),
                            width="stretch")
            note("الحجم <b>ما يفرق كثير</b> (ρ = 0.14). اللي يفرق هو <b>مدى انتشار النوع</b> في الطبيعة (ρ = 0.47).")
            c1, c2 = st.columns(2)
            with c1:
                d = PP.groupby("diet_ar").agg(median=("traded", "median"),
                                              share=("traded", lambda s: (s > 0).mean())).reset_index()
                d = d.sort_values("median")
                fig = go.Figure(go.Bar(x=d["median"], y=d["diet_ar"], orientation="h", marker_color=GOLD,
                                       text=[f"{m:,.0f} طير" for m in d["median"]], customdata=d["share"],
                                       hovertemplate="%{y}<br>الوسيط: %{x:,.0f} طير<br>انباع منها: %{customdata:.0%}<extra></extra>",
                                       textposition="outside", cliponaxis=False))
                fig.update_xaxes(range=[0, max(d["median"].max() * 1.9, 1)], visible=False)
                st.plotly_chart(style(fig, "وسيط التجارة لكل نوع حسب الأكل", 360), width="stretch")
            with c2:
                fig = px.box(P[P["habitat"] != "Unknown"], x="habitat_ar", y="mass_g", log_y=True, points="all",
                             hover_name="name", labels={"mass_g": "الوزن (جم)", "habitat_ar": ""})
                fig.update_traces(marker_color=CAPT, line_color=SAGE)
                st.plotly_chart(style(fig, "الوزن حسب البيئة", 360), width="stretch")
            note("آكلين <b>الحبوب</b> و<b>الرحيق</b> و<b>كل شيء</b> ينباعون أكثر بكثير من آكلين <b>الفواكه</b>. "
                 "بس التصنيف هذا حسب أكلهم <b>في الطبيعة</b>: كنيور الخدود الخضراء يُصنّف آكل فواكه، "
                 "بس في البيت يأكل حبوب وخضار، وترتيبه <b>#14</b> 💚")
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Histogram(x=np.log10(P["mass_g"]), nbinsx=35, marker_color=CAPT,
                                             marker_line=dict(color=BG, width=1)))
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
                fig = px.imshow(corr, text_auto=True, color_continuous_scale=[WILD, CARD, SAGE],
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
                             color_discrete_map={"في خطر": WILD, "باقي الأنواع": "#4A5C54"}, hover_name="name",
                             log_x=True, log_y=True, size=np.where(W2["danger"], 16, 7), size_max=16,
                             hover_data={"wild_share": ":.0%", "range_km2": ":,.0f", "حالة": False},
                             labels={"range_km2": "مساحة الانتشار (كم²)", "wild_traded": "طيور مصطادة من البرية",
                                     "wild_share": "نسبة البري"})
            fig.add_vrect(x0=W2["range_km2"].min() * .8, x1=max_range, fillcolor=WILD, opacity=.07, line_width=0)
            fig.add_hline(y=min_wild, line_dash="dot", line_color=WILD)
            fig.update_traces(marker=dict(line=dict(width=0)))
            fig.update_layout(legend_title=None)
            D2 = W2[W2["danger"]].sort_values("wild_traded", ascending=False)
            st.plotly_chart(style(fig, f"{len(D2)} نوع في منطقة الخطر", 460), width="stretch")
            if not D2.empty:
                cols = st.columns(min(4, len(D2)))
                for i, (_, r) in enumerate(D2.head(4).iterrows()):
                    with cols[i]:
                        html(f"""<div class="album">{pic_or_svg(r['species'], r['family'], 170)}
                        <div class="n">{name_ar(r['species'])}</div><div class="s">{r['species']}</div>
                        <div class="t" style="color:#EE9478">{r['wild_traded']:,} طير بري</div></div>""")
                table = D2[["name", "family_ar", "range_km2", "wild_traded", "wild_share"]].rename(columns={
                    "name": "النوع", "family_ar": "العائلة", "range_km2": "مساحة الانتشار (كم²)",
                    "wild_traded": "طيور برية", "wild_share": "نسبة البري"})
                st.dataframe(table, hide_index=True, width="stretch", column_config={
                    "مساحة الانتشار (كم²)": st.column_config.NumberColumn(format="%d"),
                    "طيور برية": st.column_config.ProgressColumn(format="%d", min_value=0,
                                                                 max_value=int(D2["wild_traded"].max())),
                    "نسبة البري": st.column_config.NumberColumn(format="percent")})
            note("أغلب هالأنواع <b>لوري وكوكاتو من جزر إندونيسيا وميلانيزيا</b>. و<b>كوكاتو غوفين</b> موطنه حوالي 4,000 كم² بس!")


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
                        f'<div class="l">ببغاء استوردته السعودية</div></div>', unsafe_allow_html=True)
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
                          color_discrete_sequence=[SAGE, WILD, BLUE, "#A493C4", GOLD, "#5A6B63"],
                          labels={"year": "السنة", "quantity": "عدد الطيور", "country": "الدولة"})
            fig.update_traces(line_width=0)
            fig.update_layout(legend=dict(orientation="h", y=-.2, title=None))
            st.plotly_chart(style(fig, "واردات الببغاوات لدول الخليج", 420), width="stretch")
            c1, c2 = st.columns(2)
            s = G[G["species"].notna()].groupby("species")["quantity"].sum().nlargest(10).sort_values()
            f = go.Figure(go.Bar(x=s.values, y=[name_ar(x) for x in s.index], orientation="h", marker_color=GOLD,
                                 text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
            f.update_xaxes(visible=False, range=[0, s.max() * 1.35])
            c1.plotly_chart(style(f, "وش يشتري الخليج؟", 420), width="stretch")
            s = G.groupby("exporter_ar")["quantity"].sum().nlargest(10).sort_values()
            f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=WILD,
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
        st.markdown("#### الإحصائيات")
        st.dataframe(df.describe().T.round(2), width="stretch")
        st.download_button("نزّلي البيانات المفلترة (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                           "parrots_filtered.csv", "text/csv", icon=":material/download:")

html('<div class="foot">ريش بلا حدود · نوره السويلم 💚 · البيانات: CITES Trade Database (UNEP-WCMC) '
     'و AVONET (Tobias et al. 2022) · التجارة القانونية المسجّلة فقط، وبيانات 2024 قد تكون ناقصة</div>')
