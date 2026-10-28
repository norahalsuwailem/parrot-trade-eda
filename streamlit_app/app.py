"""
🦜 ريش بلا حدود: داشبورد تجارة الببغاوات حول العالم
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
                        HOME_DIET, SOURCE_AR, country_ar, display_name, name_ar)
from parrot_art import parrot_svg

st.set_page_config(page_title="ريش بلا حدود 🦜", page_icon="🦜", layout="wide")

# ═══════════════════════════ الألوان والتصميم ═══════════════════════════
DEEP, JUNGLE, LEAF, GOLD, SCARLET, MACAW, CREAM = (
    "#0B1F17", "#2D6A4F", "#8AC926", "#F2B705", "#E63946", "#3A86C8", "#F4EFE3")
SOURCE_COLORS = {"مصطاد من البرية": SCARLET, "مُربّى في الأسر": LEAF, "مُربّى من بيض بري": GOLD,
                 "مُصادَر": "#9D7FBF", "قبل الاتفاقية": "#5E5C55", "غير معروف": "#8C8A80"}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');

/* الخط العربي في كل مكان */
html, body, [class*="css"], .stApp, p, li, label, h1, h2, h3, h4, input, textarea, button,
[data-testid="stMarkdownContainer"], [data-baseweb="tab"], [data-baseweb="select"] {
    font-family: 'Tajawal', sans-serif !important;
}
/* الاتجاه من اليمين لليسار */
.main .block-container, section[data-testid="stSidebar"] { direction: rtl; text-align: right; }
[data-testid="stMarkdownContainer"], .stTabs, label, .stRadio, .stSelectbox, .stMultiSelect { direction: rtl; text-align: right; }
/* السلايدرات تبقى من اليسار لليمين عشان تشتغل صح */
[data-testid="stSlider"] [data-baseweb="slider"] { direction: ltr; }

.stApp { background: radial-gradient(1200px 600px at 15% -10%, #1d4a36 0%, #0B1F17 55%) fixed; }
section[data-testid="stSidebar"] { background: #0F2A1F; border-left: 1px solid #1f4434; }

.hero { padding: 24px 32px; border-radius: 24px; margin-bottom: 18px; display: flex; align-items: center;
        gap: 24px; justify-content: space-between;
        background: linear-gradient(250deg, rgba(230,57,70,.20), rgba(242,183,5,.12) 45%, rgba(58,134,200,.20));
        border: 1px solid rgba(244,239,227,.14); }
.hero .kicker { color: #F2B705; letter-spacing: .1em; font-size: 15px; font-weight: 700; }
.hero .title { font-size: 54px; font-weight: 900; color: #F4EFE3; line-height: 1.1; margin: 4px 0; }
.hero .sub { color: #D4DED6; font-size: 19px; max-width: 760px; }
.hero .birds { display: flex; gap: 4px; }

.kpi { background: rgba(244,239,227,.05); border: 1px solid rgba(244,239,227,.10);
       border-radius: 18px; padding: 16px 20px; height: 100%; }
.kpi .v { font-size: 34px; font-weight: 900; color: #F4EFE3; line-height: 1.15; }
.kpi .l { color: #A9B8AE; font-size: 15px; margin-top: 2px; }
.kpi .bar { height: 5px; border-radius: 5px; margin-bottom: 10px; width: 46px; }

.insight { border-right: 5px solid #F2B705; background: rgba(242,183,5,.08); padding: 14px 18px;
           border-radius: 14px 0 0 14px; margin: 8px 0 20px; color: #EDE7D8; font-size: 17px; line-height: 1.7; }
.insight b { color: #F2B705; }

.card { background: rgba(244,239,227,.05); border: 1px solid rgba(244,239,227,.12);
        border-radius: 22px; padding: 20px 24px; }
.card .name { font-size: 32px; font-weight: 900; color: #F4EFE3; line-height: 1.2; }
.card .sci { font-style: italic; color: #A9B8AE; font-size: 17px; direction: ltr; text-align: right; }
.chip { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 14px; font-weight: 700;
        margin: 6px 0 0 6px; background: rgba(244,239,227,.10); color: #EDE7D8; }
.chip.red { background: #E63946; color: white; }
.stat .v { font-size: 26px; font-weight: 900; color: #F4EFE3; }
.stat .l { color: #A9B8AE; font-size: 14px; }
.care { background: rgba(138,201,38,.08); border: 1px solid rgba(138,201,38,.25); border-radius: 18px;
        padding: 16px 20px; margin-top: 14px; color: #E6EFE0; font-size: 16px; line-height: 1.8; }
.care h4 { margin: 0 0 6px 0; color: #8AC926; }
.fact { background: rgba(58,134,200,.12); border-radius: 14px; padding: 12px 16px; margin-top: 12px;
        color: #E2ECF5; font-size: 16px; }

.album { background: rgba(244,239,227,.05); border: 1px solid rgba(244,239,227,.12); border-radius: 20px;
         padding: 10px 12px 14px; text-align: center; margin-bottom: 16px; min-height: 330px; }
.album .n { font-size: 18px; font-weight: 800; color: #F4EFE3; }
.album .s { font-size: 13px; color: #A9B8AE; font-style: italic; }
.album .t { font-size: 15px; color: #F2B705; font-weight: 700; margin-top: 4px; }

.stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { background: rgba(244,239,227,.05); border-radius: 12px 12px 0 0;
                               padding: 10px 16px; font-size: 17px; }
.stTabs [aria-selected="true"] { background: rgba(242,183,5,.16) !important; }
.foot { color: #7F8F85; font-size: 13px; margin-top: 30px; text-align: center; }
</style>
""", unsafe_allow_html=True)


def style(fig, title=None, h=430):
    """تنسيق موحّد لكل الرسومات."""
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Tajawal, sans-serif", color="#E8E3D6", size=14),
        margin=dict(l=10, r=10, t=56 if title else 20, b=10), height=h,
        title=dict(text=title, x=0.99, xanchor="right", font=dict(size=20)),
        hoverlabel=dict(font_family="Tajawal"),
    )
    fig.update_xaxes(gridcolor="rgba(244,239,227,.07)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(244,239,227,.07)", zeroline=False)
    return fig


def fmt(n):
    """22520296 ← 22.5 مليون"""
    n = float(n)
    if n >= 1e6:
        return f"{n / 1e6:.1f} مليون"
    if n >= 1e3:
        return f"{n / 1e3:.0f} ألف"
    return f"{n:,.0f}"


def insight(html):
    st.markdown(f'<div class="insight">💡 {html}</div>', unsafe_allow_html=True)


def svg(species, family="True parrots", size=220):
    st.markdown(f'<div style="text-align:center">{parrot_svg(species, family, size)}</div>',
                unsafe_allow_html=True)


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

# ═══════════════════════════ الشريط الجانبي ═══════════════════════════
with st.sidebar:
    st.markdown("## 🦜 ريش بلا حدود")
    st.markdown(
        "كل **ببغاء حي** انتقل بين الدول بشكل قانوني من **1975 إلى 2024** "
        "(قاعدة بيانات **CITES**، 161 ألف سجل)، مدموجة مع صفات **كل أنواع الببغاوات الـ 404** "
        "(قاعدة بيانات **AVONET**): الوزن، والأكل، والبيئة، ومساحة الانتشار.")
    st.divider()
    st.header("🎛️ الفلاتر")

    yr = st.slider("السنوات", 1975, 2024, (1975, 2024))

    src_all = list(SOURCE_AR.values())
    sources = st.multiselect("مصدر الطيور", src_all, default=src_all)

    fam_all = list(FAMILY_AR.values())
    fams_ar = st.multiselect("العائلة", fam_all, default=fam_all)
    fams = [k for k, v in FAMILY_AR.items() if v in fams_ar]

    diet_all = list(DIET_AR.values())
    diets_ar = st.multiselect("نوع الأكل (في الطبيعة)", diet_all, default=diet_all)
    diets = [k for k, v in DIET_AR.items() if v in diets_ar]

    mass = st.slider("الوزن (جرام)", 0, 1800, (0, 1800), step=10)

    st.divider()
    st.caption("المصادر: CITES Trade Database (UNEP-WCMC) · AVONET (Tobias et al. 2022)\n\n"
               "إعداد: **نوره السويلم** 💚")

# تطبيق الفلاتر
P = parrots[parrots["family"].isin(fams) & parrots["diet"].isin(diets) & parrots["mass_g"].between(*mass)]
T = trade[trade["year"].between(*yr) & trade["source_ar"].isin(sources)]
if set(fams) != set(FAMILY_AR):          # نفلتر العائلة بس لو المستخدم غيّرها
    T = T[T["family_en"].isin(fams)]
TS = T[T["species"].isin(P["species"])]   # سجلات الأنواع اللي تنطبق عليها فلاتر الصفات

if T.empty or P.empty:
    st.warning("ما فيه بيانات تنطبق على هالفلاتر. جرّبي توسّعينها من الشريط الجانبي 🙏")
    st.stop()

# ═══════════════════════════ الواجهة الرئيسية ═══════════════════════════
hero_birds = "".join(parrot_svg(s, size=96) for s in
                     ["Ara macao", "Pyrrhura molinae", "Cacatua galerita", "Agapornis fischeri"])
st.markdown(f"""
<div class="hero">
  <div>
    <div class="kicker">٥٠ سنة · ٤٠٤ نوع · أكثر من ٢٠٠ دولة</div>
    <div class="title">ريش بلا حدود</div>
    <div class="sub">رحلة الببغاوات من الغابة إلى القفص: مين يبيع؟ مين يشتري؟ وأي الأنواع تدفع الثمن؟</div>
  </div>
  <div class="birds">{hero_birds}</div>
</div>""", unsafe_allow_html=True)

wild = T.loc[T["source"] == "Wild-caught", "quantity"].sum()
known = T.loc[T["source"].isin(["Wild-caught", "Captive-bred", "Ranched"]), "quantity"].sum()
kpis = [(fmt(T["quantity"].sum()), "ببغاء انتقل بين الدول", SCARLET),
        (f"{TS['species'].nunique()}", f"نوع في التجارة (من {len(P)})", GOLD),
        (f"{wild / known:.0%}" if known else "–", "مصطاد من البرية*", LEAF),
        (f"{T['exporter_code'].nunique()} ← {T['importer_code'].nunique()}", "دولة مصدّرة ← مستوردة", MACAW)]
for col, (v, l, c) in zip(st.columns(4), kpis):
    col.markdown(f'<div class="kpi"><div class="bar" style="background:{c}"></div>'
                 f'<div class="v">{v}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)
st.caption(f"*من الطيور اللي مصدرها معروف · {yr[0]}–{yr[1]}")
st.write("")

tabs = st.tabs(["🌍 التجارة العالمية", "🦜 تعرّف على ببغاء", "🖼️ ألبوم الببغاوات",
                "🪶 صفات الببغاوات", "⚠️ منطقة الخطر", "🇸🇦 السعودية والخليج", "📋 البيانات"])

# ───────────────────────── ١. التجارة العالمية ─────────────────────────
with tabs[0]:
    c1, c2 = st.columns([1.35, 1])
    with c1:
        side = st.radio("عرض الخريطة", ["الدول المصدّرة", "الدول المستوردة"], horizontal=True,
                        label_visibility="collapsed")
        key = "exporter" if side == "الدول المصدّرة" else "importer"
        geo = T.groupby([f"{key}_iso3", f"{key}_ar"])["quantity"].sum().reset_index().dropna()
        fig = px.choropleth(geo, locations=f"{key}_iso3", color=np.log10(geo["quantity"]),
                            hover_name=f"{key}_ar", custom_data=["quantity"],
                            color_continuous_scale=["#13372a", JUNGLE, LEAF, GOLD, SCARLET])
        fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>%{customdata[0]:,} طير<extra></extra>",
                          marker_line_color=DEEP, marker_line_width=.4)
        fig.update_geos(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False,
                        landcolor="#173a2b", showland=True, projection_type="natural earth",
                        lataxis_range=[-58, 85])
        fig.update_coloraxes(colorbar=dict(title="طير", tickvals=[1, 2, 3, 4, 5, 6],
                                           ticktext=["10", "100", "1k", "10k", "100k", "1M"], len=.6))
        st.plotly_chart(style(fig, "من وين تطلع الببغاوات؟" if key == "exporter" else "وين تروح الببغاوات؟", 450),
                        width="stretch")
    with c2:
        top = T.groupby(f"{key}_ar")["quantity"].sum().nlargest(12).sort_values()
        fig = go.Figure(go.Bar(x=top.values, y=top.index, orientation="h",
                               marker_color=SCARLET if key == "exporter" else MACAW,
                               text=[fmt(v) for v in top.values], textposition="outside", cliponaxis=False))
        fig.update_xaxes(range=[0, top.max() * 1.3], visible=False)
        st.plotly_chart(style(fig, "أكبر 12 دولة " + ("مصدّرة" if key == "exporter" else "مستوردة"), 450),
                        width="stretch")

    yearly = T.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
    fig = px.area(yearly, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                  category_orders={"source_ar": list(SOURCE_COLORS)},
                  labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
    for y, txt in [(1992, "حظر أمريكا<br>للطيور البرية"), (2005, "حظر أوروبا<br>للطيور البرية")]:
        if yr[0] <= y <= yr[1]:
            fig.add_vline(x=y, line_dash="dash", line_color="#E8E3D6", opacity=.6)
            fig.add_annotation(x=y, y=1, yref="paper", text=txt, showarrow=False, xanchor="left",
                               xshift=6, font=dict(size=13))
    fig.update_layout(legend=dict(orientation="h", y=-.18, title=None))
    st.plotly_chart(style(fig, "عدد الببغاوات كل سنة حسب المصدر", 460), width="stretch")
    insight("من الطيور اللي مصدرها معروف، كان <b>حوالي النص مصطاد من البرية في التسعينات</b>، "
            "واليوم <b>أقل من 5%</b>. النزول الكبير صار بعد <b>حظر أمريكا (1992)</b> و<b>حظر أوروبا (2005)</b>. "
            "يعني القوانين نجحت! واللون الرمادي في الثمانينات معناه إن المصدر ما كان ينكتب.")

    st.markdown("#### 🔀 أكبر طرق التجارة")
    n = st.slider("عدد الطرق", 5, 30, 15)
    r = T.groupby(["exporter_ar", "importer_ar"])["quantity"].sum().nlargest(n).reset_index()
    ex = list(dict.fromkeys(r["exporter_ar"]))
    im = list(dict.fromkeys(r["importer_ar"]))
    fig = go.Figure(go.Sankey(
        node=dict(label=[f"{e} " for e in ex] + [f" {i}" for i in im], pad=12, thickness=14,
                  color=[SCARLET] * len(ex) + [MACAW] * len(im), line=dict(width=0)),
        link=dict(source=[ex.index(e) for e in r["exporter_ar"]],
                  target=[len(ex) + im.index(i) for i in r["importer_ar"]],
                  value=r["quantity"], color="rgba(242,183,5,.28)",
                  hovertemplate="%{source.label} ← %{target.label}<br>%{value:,} طير<extra></extra>")))
    st.plotly_chart(style(fig, None, 540), width="stretch")
    insight("<b>جنوب أفريقيا</b> هي «مزرعة الببغاوات» في العالم: صدّرت <b>5.6 مليون</b> طير، "
            "أغلبها مُربّى في الأسر، ورايحة لجنوب آسيا والشرق الأوسط.")

# ───────────────────────── ٢. تعرّف على ببغاء ─────────────────────────
with tabs[1]:
    order = parrots.sort_values("total_traded", ascending=False)
    options = order["species"].tolist()
    default = options.index("Pyrrhura molinae") if "Pyrrhura molinae" in options else 0
    pick = st.selectbox("🔍 اختاري ببغاء (مرتبة من الأكثر تجارة)", options, index=default,
                        format_func=display_name)
    b = parrots[parrots["species"] == pick].iloc[0]
    info = FEATURED.get(pick, {})
    bt = trade[trade["species"] == pick]

    heavier = (parrots["mass_g"] < b["mass_g"]).mean()
    wild_s = f"{b['wild_share']:.0%}" if pd.notna(b["wild_share"]) else "–"
    rng = f"{b['range_km2']:,.0f} كم²" if pd.notna(b["range_km2"]) else "غير معروفة"
    appendix_i = (bt["cites_appendix"] == "I").any()

    c1, c2 = st.columns([1, 1.4])
    with c1:
        svg(pick, b["family"], 300)
        if info:
            st.markdown(f'<div class="fact">✨ {info["fact"]}</div>', unsafe_allow_html=True)
    with c2:
        title = name_ar(pick)
        chips = (f'<span class="chip">{b["family_ar"]}</span>'
                 f'<span class="chip">🌳 {b["habitat_ar"]}</span>'
                 f'<span class="chip">🍽️ {b["diet_ar"]} (في الطبيعة)</span>')
        if appendix_i:
            chips += '<span class="chip red">محمي: الملحق الأول</span>'
        st.markdown(f"""
        <div class="card">
          <div class="name">{info.get('emoji', '🦜')} {title}</div>
          <div class="sci">{pick}</div>
          <div>{chips}</div>
          <hr style="border-color:rgba(244,239,227,.1)">
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px" class="stat">
            <div><div class="v">{b['mass_g']:,.0f} جم</div><div class="l">أثقل من {heavier:.0%} من الببغاوات</div></div>
            <div><div class="v">#{b['rank']}</div><div class="l">ترتيبه في التجارة من 404</div></div>
            <div><div class="v">{fmt(b['total_traded'])}</div><div class="l">طير انتقل بين الدول</div></div>
            <div><div class="v" style="color:{SCARLET}">{wild_s}</div><div class="l">مصطاد من البرية</div></div>
            <div><div class="v">{rng}</div><div class="l">مساحة انتشاره</div></div>
            <div><div class="v">{int(b['n_exporters'])}</div><div class="l">دولة صدّرته</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if info.get("pet"):
            st.markdown(f"""
            <div class="care">
              <h4>🏠 معلومات للمربّين</h4>
              🌍 <b>موطنه:</b> {info['origin']}<br>
              📏 <b>الطول:</b> {info['length']} &nbsp;·&nbsp; ⏳ <b>العمر:</b> {info['life']}<br>
              🗣️ <b>الكلام:</b> {info['talk']} &nbsp;·&nbsp; 🔊 <b>الإزعاج:</b> {info['noise']}<br>
              🥗 <b>الأكل في البيت:</b> {HOME_DIET}
              <div style="font-size:13px;color:#A9B8AE;margin-top:8px">معلومات عامة وتقريبية. لأي سؤال صحي راجعي طبيب طيور 🩺</div>
            </div>""", unsafe_allow_html=True)
        elif info:
            st.markdown(f'<div class="care"><h4>🌍 موطنه</h4>{info["origin"]}</div>', unsafe_allow_html=True)

    if bt.empty:
        st.success("🌿 هالنوع **ما انباع ولا طير منه** بين الدول. محظوظ!")
    else:
        y = bt.groupby(["year", "source_ar"])["quantity"].sum().reset_index()
        fig = px.bar(y, x="year", y="quantity", color="source_ar", color_discrete_map=SOURCE_COLORS,
                     labels={"year": "السنة", "quantity": "عدد الطيور", "source_ar": "المصدر"})
        fig.update_layout(legend=dict(orientation="h", y=-.2, title=None), bargap=.1)
        st.plotly_chart(style(fig, "تاريخ تجارته", 360), width="stretch")

        cc1, cc2, cc3 = st.columns([1, 1, 1.1])
        for cc, side, color, ttl in [(cc1, "exporter_ar", SCARLET, "مين يبيعه؟"),
                                     (cc2, "importer_ar", MACAW, "مين يشتريه؟")]:
            s = bt.groupby(side)["quantity"].sum().nlargest(6).sort_values()
            f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=color,
                                 text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
            f.update_xaxes(visible=False, range=[0, s.max() * 1.45])
            cc.plotly_chart(style(f, ttl, 300), width="stretch")
        if pd.notna(b["lat"]):
            f = go.Figure(go.Scattergeo(lat=[b["lat"]], lon=[b["lon"]], mode="markers",
                                        marker=dict(size=max(12, min(60, np.sqrt(b["range_km2"] or 1) / 25)),
                                                    color=GOLD, opacity=.8, line=dict(color="white", width=1))))
            f.update_geos(bgcolor="rgba(0,0,0,0)", landcolor="#173a2b", showland=True, showcoastlines=False,
                          showframe=False, projection_type="natural earth", lataxis_range=[-58, 85])
            cc3.plotly_chart(style(f, "وين يعيش في الطبيعة؟", 300), width="stretch")

# ───────────────────────── ٣. ألبوم الببغاوات ─────────────────────────
with tabs[2]:
    st.markdown("### 🖼️ أشهر الببغاوات في التجارة")
    st.caption("رسومات تقريبية بألوان كل نوع. للتفاصيل اختاري النوع من تبويب «تعرّف على ببغاء».")
    album = parrots[parrots["species"].isin(FEATURED)].sort_values("total_traded", ascending=False)
    cols = st.columns(4)
    for i, (_, r) in enumerate(album.iterrows()):
        f = FEATURED[r["species"]]
        traded = fmt(r["total_traded"]) + " طير" if r["total_traded"] else "ما انباع أبداً 🌿"
        with cols[i % 4]:
            st.markdown(f"""
            <div class="album">
              {parrot_svg(r['species'], r['family'], 170)}
              <div class="n">{f['emoji']} {f['ar']}</div>
              <div class="s">{r['species']}</div>
              <div class="t">{traded}</div>
            </div>""", unsafe_allow_html=True)

# ───────────────────────── ٤. صفات الببغاوات ─────────────────────────
with tabs[3]:
    sp = TS.groupby("species")["quantity"].sum().rename("traded")
    PP = P.drop(columns="total_traded").merge(sp, on="species", how="left").fillna({"traded": 0})
    PP["traded_plot"] = PP["traded"].clip(lower=1)
    fig = px.scatter(PP, x="mass_g", y="traded_plot", color="diet_ar", size=np.sqrt(PP["range_km2"].fillna(1e4)),
                     size_max=34, hover_name="name", log_x=True, log_y=True,
                     hover_data={"mass_g": ":.0f", "traded": ":,", "habitat_ar": True, "traded_plot": False},
                     color_discrete_sequence=[GOLD, LEAF, SCARLET, MACAW, "#C77DFF"],
                     labels={"mass_g": "الوزن (جم)", "traded_plot": "عدد الطيور", "traded": "عدد الطيور",
                             "diet_ar": "الأكل", "habitat_ar": "البيئة"})
    fig.update_traces(marker=dict(line=dict(width=.5, color=DEEP), opacity=.8))
    st.plotly_chart(style(fig, "كل نوع ببغاء: الوزن مقابل التجارة (حجم الدائرة = مساحة الانتشار)", 540),
                    width="stretch")
    insight("الحجم <b>ما يفرق كثير</b> (ρ = 0.14). اللي يفرق هو <b>مدى انتشار النوع</b> في الطبيعة (ρ = 0.47): "
            "الأنواع المنتشرة سهل الحصول عليها ورخيصة، فتصير هي الموجودة في محلات الحيوانات.")

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
        st.plotly_chart(style(fig, "وسيط التجارة لكل نوع حسب الأكل", 380), width="stretch")
    with c2:
        fig = px.box(P[P["habitat"] != "Unknown"], x="habitat_ar", y="mass_g", color="habitat_ar",
                     log_y=True, points="all", hover_name="name",
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     labels={"mass_g": "الوزن (جم)", "habitat_ar": ""})
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, "الوزن حسب البيئة", 380), width="stretch")
    insight("آكلين <b>الحبوب</b> و<b>الرحيق</b> و<b>كل شيء</b> ينباعون أكثر بكثير من آكلين <b>الفواكه</b>. "
            "بس انتبهي: التصنيف هذا حسب أكلهم <b>في الطبيعة</b>. مثلاً كنيور الخدود الخضراء يُصنّف آكل فواكه، "
            "بس في البيت يأكل حبوب وخضار، وترتيبه <b>#14</b> في التجارة 💚")

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Histogram(x=np.log10(P["mass_g"]), nbinsx=35, marker_color=LEAF,
                                     marker_line=dict(color=DEEP, width=1)))
        fig.update_xaxes(title="الوزن (جم، مقياس لوغاريتمي)", tickvals=[1, 1.5, 2, 2.5, 3],
                         ticktext=["10", "32", "100", "316", "1,000"])
        fig.update_yaxes(title="عدد الأنواع")
        st.plotly_chart(style(fig, "توزيع الأوزان", 360), width="stretch")
    with c2:
        num = PP.assign(**{"الوزن": np.log10(PP["mass_g"]), "المنقار": PP["beak_length_mm"],
                           "الجناح": PP["wing_length_mm"], "الذيل": PP["tail_length_mm"],
                           "الانتشار": np.log10(PP["range_km2"]), "التجارة": np.log10(PP["traded"] + 1)})
        cols_ar = ["الوزن", "المنقار", "الجناح", "الذيل", "الانتشار", "التجارة"]
        corr = num[cols_ar].corr(method="spearman").round(2)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale=[SCARLET, DEEP, LEAF],
                        zmin=-1, zmax=1, aspect="auto")
        st.plotly_chart(style(fig, "الارتباط بين الصفات والتجارة", 360), width="stretch")

# ───────────────────────── ٥. منطقة الخطر ─────────────────────────
with tabs[4]:
    st.markdown("### ⚠️ أنواع موطنها صغير، وانصاد منها آلاف من البرية")
    c1, c2 = st.columns(2)
    max_range = c1.select_slider("«موطن صغير» يعني أقل من…", options=[10_000, 25_000, 50_000, 100_000, 250_000],
                                 value=50_000, format_func=lambda v: f"{v:,} كم²")
    min_wild = c2.select_slider("…وانصاد منه على الأقل", options=[100, 500, 1_000, 5_000, 10_000],
                                value=1_000, format_func=lambda v: f"{v:,} طير")
    W = P[P["wild_traded"] > 0].copy()
    W["danger"] = (W["range_km2"] < max_range) & (W["wild_traded"] >= min_wild)
    W["حالة"] = W["danger"].map({True: "في خطر", False: "باقي الأنواع"})
    fig = px.scatter(W, x="range_km2", y="wild_traded", color="حالة",
                     color_discrete_map={"في خطر": SCARLET, "باقي الأنواع": "#6F7D73"}, hover_name="name",
                     log_x=True, log_y=True, size=np.where(W["danger"], 16, 7), size_max=16,
                     hover_data={"wild_share": ":.0%", "range_km2": ":,.0f", "حالة": False},
                     labels={"range_km2": "مساحة الانتشار (كم²)", "wild_traded": "طيور مصطادة من البرية",
                             "wild_share": "نسبة البري"})
    fig.add_vrect(x0=W["range_km2"].min() * .8, x1=max_range, fillcolor=SCARLET, opacity=.07, line_width=0)
    fig.add_hline(y=min_wild, line_dash="dot", line_color=SCARLET)
    fig.update_layout(legend_title=None)
    D = W[W["danger"]].sort_values("wild_traded", ascending=False)
    st.plotly_chart(style(fig, f"{len(D)} نوع في منطقة الخطر", 480), width="stretch")

    if not D.empty:
        cols = st.columns(min(4, len(D)))
        for i, (_, r) in enumerate(D.head(4).iterrows()):
            nm = name_ar(r["species"])
            with cols[i]:
                st.markdown(f"""<div class="album">{parrot_svg(r['species'], r['family'], 150)}
                <div class="n">{nm}</div><div class="s">{r['species']}</div>
                <div class="t" style="color:{SCARLET}">{r['wild_traded']:,} طير بري</div></div>""",
                            unsafe_allow_html=True)
        table = D[["name", "family_ar", "range_km2", "wild_traded", "wild_share"]].rename(columns={
            "name": "النوع", "family_ar": "العائلة", "range_km2": "مساحة الانتشار (كم²)",
            "wild_traded": "طيور برية", "wild_share": "نسبة البري"})
        st.dataframe(table, hide_index=True, width="stretch", column_config={
            "مساحة الانتشار (كم²)": st.column_config.NumberColumn(format="%d"),
            "طيور برية": st.column_config.ProgressColumn(format="%d", min_value=0,
                                                         max_value=int(D["wild_traded"].max())),
            "نسبة البري": st.column_config.NumberColumn(format="percent")})
    insight("أغلب هالأنواع <b>لوري وكوكاتو من جزر إندونيسيا وميلانيزيا</b>. موطنها كامل أصغر من "
            "<b>منطقة القصيم</b>، ومع ذلك انصاد منها آلاف. و<b>كوكاتو غوفين</b> موطنه حوالي 4,000 كم² بس!")

# ───────────────────────── ٦. السعودية والخليج ─────────────────────────
with tabs[5]:
    G = T[T["importer_code"].isin(GULF)].assign(country=lambda d: d["importer_code"].map(GULF))
    if G.empty:
        st.info("ما فيه واردات خليجية بهالفلاتر.")
    else:
        sa = G[G["importer_code"] == "SA"]
        sa_top = sa.groupby("species")["quantity"].sum().idxmax() if not sa.empty else None
        c1, c2, c3 = st.columns([1, 1, 1.2])
        c1.markdown(f'<div class="kpi"><div class="bar" style="background:{LEAF}"></div><div class="v">{fmt(sa["quantity"].sum())}</div>'
                    f'<div class="l">ببغاء استوردته السعودية 🇸🇦</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi"><div class="bar" style="background:{GOLD}"></div><div class="v">{fmt(G["quantity"].sum())}</div>'
                    f'<div class="l">استوردته دول الخليج الست</div></div>', unsafe_allow_html=True)
        if sa_top:
            c3.markdown(f'<div class="kpi" style="display:flex;align-items:center;gap:10px">'
                        f'{parrot_svg(sa_top, size=70)}<div><div class="v" style="font-size:22px">'
                        f'{name_ar(sa_top)}</div>'
                        f'<div class="l">أكثر ببغاء استوردته المملكة</div></div></div>', unsafe_allow_html=True)
        st.write("")
        g = G.groupby(["year", "country"])["quantity"].sum().reset_index()
        fig = px.area(g, x="year", y="quantity", color="country",
                      category_orders={"country": list(GULF.values())},
                      color_discrete_sequence=[LEAF, SCARLET, MACAW, "#C77DFF", GOLD, "#F4A261"],
                      labels={"year": "السنة", "quantity": "عدد الطيور", "country": "الدولة"})
        fig.update_layout(legend=dict(orientation="h", y=-.18, title=None))
        st.plotly_chart(style(fig, "واردات الببغاوات لدول الخليج", 430), width="stretch")

        c1, c2 = st.columns(2)
        s = G[G["species"].notna()].groupby("species")["quantity"].sum().nlargest(10).sort_values()
        f = go.Figure(go.Bar(x=s.values, y=[name_ar(x) for x in s.index],
                             orientation="h", marker_color=GOLD,
                             text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
        f.update_xaxes(visible=False, range=[0, s.max() * 1.35])
        c1.plotly_chart(style(f, "وش يشتري الخليج؟", 420), width="stretch")
        s = G.groupby("exporter_ar")["quantity"].sum().nlargest(10).sort_values()
        f = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=SCARLET,
                             text=[fmt(v) for v in s.values], textposition="outside", cliponaxis=False))
        f.update_xaxes(visible=False, range=[0, s.max() * 1.35])
        c2.plotly_chart(style(f, "من وين تجي؟", 420), width="stretch")

        after = sa.loc[sa["year"] >= 2016, "quantity"].sum() / max(sa["quantity"].sum(), 1)
        insight(f"واردات السعودية <b>وقفت تقريباً بين 2005 و2014</b>، وبعدها رجعت بقوة: "
                f"<b>{after:.0%}</b> من كل الببغاوات اللي دخلت المملكة وصلت <b>بعد 2016</b>، وأكثرها <b>طيور الحب</b> 🧡")

# ───────────────────────── ٧. البيانات ─────────────────────────
with tabs[6]:
    which = st.radio("الجدول", ["جدول الأنواع (المدموج)", "سجلات التجارة (النظيفة)"], horizontal=True)
    if which.startswith("جدول الأنواع"):
        df = P.drop(columns=["diet_ar", "habitat_ar", "family_ar", "name", "rank"])
    else:
        df = T.drop(columns=["exporter_ar", "importer_ar", "exporter_iso3", "importer_iso3",
                             "source_ar", "family_en"])
    st.markdown(f"**{len(df):,} صف × {df.shape[1]} عمود** (بعد الفلاتر)")
    st.dataframe(df.head(500), width="stretch", hide_index=True)
    st.markdown("#### 📊 الإحصائيات")
    st.dataframe(df.describe().T.round(2), width="stretch")
    st.download_button("⬇️ نزّلي البيانات المفلترة (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                       "parrots_filtered.csv", "text/csv")

st.markdown('<div class="foot">ريش بلا حدود · نوره السويلم 💚 · البيانات: CITES Trade Database (UNEP-WCMC) '
            'و AVONET (Tobias et al. 2022) · التجارة القانونية المسجّلة فقط، وبيانات 2024 قد تكون ناقصة</div>',
            unsafe_allow_html=True)
