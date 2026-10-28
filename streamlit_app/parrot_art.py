"""
رسومات الببغاوات 🦜
كل ببغاء يُرسم بالكود (SVG) بألوانه الحقيقية تقريباً.
الفكرة: نفس الشكل الأساسي، ونغيّر الألوان وطول الذيل والعُرف لكل نوع.
"""

# ألوان كل نوع: الجسم، الرأس، الجناح، أطراف الجناح، الذيل، البطن، الوجه، المنقار...
SPECIES_LOOK = {
    "Pyrrhura molinae": dict(body="#3E9B3A", head="#4B4541", wing="#2F7F33", tips="#2C5FA8",
                             tail="#8B1E2B", belly="#5E8F55", face="#4E9B48", beak="#2E2E2E",
                             ring="#F1F1EC", scale=True, patch="#9E2A2B", tail_len=48),
    "Aratinga solstitialis": dict(body="#F9B81B", head="#FF8A1E", wing="#F9B81B", tips="#2F9E4F",
                                  tail="#3E8E5A", belly="#FF9F2B", face="#FF6F1A", beak="#2E2E2E",
                                  ring="#F1F1EC", tail_len=50),
    "Aratinga nenday": dict(body="#56B04A", head="#1F1F1F", wing="#4DA243", tips="#2C5FA8",
                            tail="#3C8F4A", belly="#79C26B", face="#1F1F1F", beak="#2E2E2E",
                            ring="#EDEDE6", tail_len=50),
    "Agapornis fischeri": dict(body="#62BE48", head="#F59A2E", wing="#4FA83C", tips="#3D8B33",
                               tail="#3C7FC4", belly="#9AD26B", face="#E9792A", beak="#E2362C",
                               ring="#FFFFFF", ring_big=True, tail_len=24),
    "Agapornis personatus": dict(body="#62BE48", head="#1E1E1E", wing="#4FA83C", tips="#3D8B33",
                                 tail="#3C7FC4", belly="#F3D23A", face="#1E1E1E", beak="#E2362C",
                                 ring="#FFFFFF", ring_big=True, collar="#F3D23A", tail_len=24),
    "Agapornis roseicollis": dict(body="#69BF4D", head="#7CC55A", wing="#55A940", tips="#3D8B33",
                                  tail="#3C7FC4", belly="#93D06D", face="#F28BA0", beak="#E9DDB0",
                                  ring="#5A6B4E", tail_len=24),
    "Psittacus erithacus": dict(body="#8C9095", head="#A3A7AB", wing="#7A7E83", tips="#5E6166",
                                tail="#C8102E", belly="#9EA2A6", face="#E8E8E8", beak="#1F1F1F",
                                ring="#F4F4F0", tail_len=26, face_bare=True),
    "Psittacus timneh": dict(body="#6E7176", head="#85898D", wing="#5F6267", tips="#4A4D51",
                             tail="#7A2430", belly="#7D8186", face="#DADADA", beak="#C9A27A",
                             ring="#F4F4F0", tail_len=26, face_bare=True),
    "Myiopsitta monachus": dict(body="#6DBE45", head="#9FD06F", wing="#5AAE3A", tips="#2C66B5",
                                tail="#5AAE3A", belly="#C3C9C0", face="#C3C9C0", beak="#E6C98F",
                                ring="#6A7065", tail_len=46),
    "Alexandrinus krameri": dict(body="#86C94B", head="#8FD25A", wing="#76BA40", tips="#5A9A30",
                                 tail="#5FAE3E", belly="#A8DB78", face="#8FD25A", beak="#D62B2B",
                                 ring="#E3B23C", collar="#1A1A1A", collar2="#F09AB0", tail_len=86),
    "Poicephalus senegalus": dict(body="#4E9F3D", head="#5E6366", wing="#45903A", tips="#3B7D32",
                                  tail="#3E8735", belly="#F2A71B", face="#5E6366", beak="#2B2B2B",
                                  ring="#F6D23A", tail_len=26),
    "Amazona aestiva": dict(body="#4CA64C", head="#4CA64C", wing="#3F9442", tips="#2F6DB5",
                            tail="#5BB25A", belly="#7AC36E", face="#F5D33A", forehead="#3F7FD6",
                            beak="#2B2B2B", ring="#E9E3D2", shoulder="#D6312B", tail_len=32),
    "Ara ararauna": dict(body="#1F6FC5", head="#2D8C4E", wing="#1A60B0", tips="#123F7A",
                         tail="#1A60B0", belly="#F7B500", face="#F7F5EE", beak="#1E1E1E",
                         ring="#F7F5EE", face_bare=True, tail_len=92),
    "Ara macao": dict(body="#D52B1E", head="#D52B1E", wing="#F2C318", tips="#1F5FBF",
                      tail="#C42418", belly="#D52B1E", face="#F7F1EA", beak="#E9DCC6",
                      ring="#F7F1EA", face_bare=True, tail_len=92),
    "Cacatua galerita": dict(body="#F6F6F2", head="#F9F9F5", wing="#EDEDE7", tips="#E2E2D8",
                             tail="#EDEDE7", belly="#FAFAF6", face="#F9F9F5", beak="#2A2A2A",
                             ring="#FFFFFF", crest="#F6D21C", tail_len=34),
    "Cacatua goffiniana": dict(body="#F6F6F2", head="#F9F9F5", wing="#EDEDE7", tips="#E2E2D8",
                               tail="#EDEDE7", belly="#FAFAF6", face="#F7C6C6", beak="#D9D2C2",
                               ring="#C9D3E0", crest="#F4F4EE", tail_len=30),
    "Cacatua ducorpsii": dict(body="#F6F6F2", head="#F9F9F5", wing="#EDEDE7", tips="#E2E2D8",
                              tail="#EDEDE7", belly="#FAFAF6", face="#F9F9F5", beak="#D9D2C2",
                              ring="#8FB3D9", crest="#F4F4EE", tail_len=30),
    "Cacatua alba": dict(body="#FBFBF8", head="#FDFDFA", wing="#F1F1EC", tips="#E6E6DE",
                         tail="#F1F1EC", belly="#FDFDFA", face="#FDFDFA", beak="#2A2A2A",
                         ring="#E3EEF6", crest="#FDFDFA", tail_len=34),
    "Eos bornea": dict(body="#E0262B", head="#E0262B", wing="#C41E25", tips="#1F3FA8",
                       tail="#B51F27", belly="#E0262B", face="#E0262B", beak="#F2833A",
                       ring="#2D2D2D", tail_len=36),
    "Strigops habroptila": dict(body="#7FA03A", head="#9AB45A", wing="#6E8E2E", tips="#4E6820",
                                tail="#6E8E2E", belly="#B4C46A", face="#C9C98A", beak="#E2D6B5",
                                ring="#5D5A3A", tail_len=30, chunky=True),
}

# شكل افتراضي لأي ببغاء ما رسمناه: أخضر للببغاوات، وأبيض للكوكاتو
DEFAULT_LOOK = {
    "True parrots": dict(body="#58AD4A", head="#66B856", wing="#4C9A40", tips="#2F6DB5",
                         tail="#4C9A40", belly="#86C774", face="#66B856", beak="#2E2E2E",
                         ring="#EDEDE6", tail_len=38),
    "Cockatoos": SPECIES_LOOK["Cacatua alba"],
    "NZ parrots (Kakapo, Kea)": SPECIES_LOOK["Strigops habroptila"],
}


def parrot_svg(species, family="True parrots", size=220):
    """يرجّع رسمة SVG لببغاء جالس على غصن."""
    c = SPECIES_LOOK.get(species, DEFAULT_LOOK.get(family, DEFAULT_LOOK["True parrots"]))
    tl = c.get("tail_len", 38)
    body_rx = 40 if c.get("chunky") else 33

    parts = []

    # الذيل
    parts.append(f'<path d="M84 150 L100 156 L{70 - tl*0.35:.0f} {170 + tl} L{58 - tl*0.35:.0f} {162 + tl} Z" '
                 f'fill="{c["tail"]}"/>')

    # الجسم + البطن
    parts.append(f'<ellipse cx="104" cy="118" rx="{body_rx}" ry="50" transform="rotate(-18 104 118)" fill="{c["body"]}"/>')
    parts.append(f'<ellipse cx="116" cy="126" rx="20" ry="36" transform="rotate(-18 116 126)" fill="{c["belly"]}"/>')
    if c.get("patch"):   # بقعة البطن (مثل الجرين تشيك)
        parts.append(f'<ellipse cx="114" cy="146" rx="12" ry="9" fill="{c["patch"]}" opacity=".9"/>')
    if c.get("scale"):   # نقش الصدر المتموّج
        for y in (100, 110, 120):
            parts.append(f'<path d="M110 {y} q5 6 10 0 q5 6 10 0" stroke="#D9D4C8" stroke-width="2" fill="none" opacity=".75"/>')

    # الجناح + أطرافه
    parts.append(f'<path d="M92 84 C70 108 72 150 98 170 C108 142 110 110 104 86 Z" fill="{c["wing"]}"/>')
    parts.append(f'<path d="M80 140 C82 156 88 164 98 170 C100 156 98 146 96 138 Z" fill="{c["tips"]}"/>')
    if c.get("shoulder"):  # بقعة الكتف (مثل الأمازون)
        parts.append(f'<ellipse cx="98" cy="96" rx="6" ry="9" fill="{c["shoulder"]}"/>')

    # الطوق (مثل الدرة وطائر الحب المقنّع)
    if c.get("collar"):
        parts.append(f'<path d="M100 84 Q122 102 148 86" stroke="{c["collar"]}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    if c.get("collar2"):
        parts.append(f'<path d="M100 89 Q122 107 146 92" stroke="{c["collar2"]}" stroke-width="3" fill="none" stroke-linecap="round"/>')

    # العُرف (الكوكاتو)
    if c.get("crest"):
        for x1, y1, x2, y2 in [(112, 50, 92, 14), (118, 46, 104, 8), (124, 44, 120, 6), (106, 56, 82, 26)]:
            parts.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2 - 6:.0f} {(y1+y2)/2:.0f} {x2} {y2} Q{(x1+x2)/2 + 6:.0f} {(y1+y2)/2 + 6:.0f} {x1 + 8} {y1 + 4} Z" fill="{c["crest"]}"/>')

    # الرأس + الوجه
    parts.append(f'<circle cx="124" cy="68" r="28" fill="{c["head"]}"/>')
    if c.get("forehead"):
        parts.append(f'<path d="M110 48 Q126 36 146 52 Q132 50 118 56 Z" fill="{c["forehead"]}"/>')
    if c.get("face_bare"):
        parts.append(f'<ellipse cx="136" cy="70" rx="13" ry="12" fill="{c["face"]}"/>')
    else:
        parts.append(f'<ellipse cx="132" cy="74" rx="15" ry="12" fill="{c["face"]}"/>')

    # العين
    ring_r = 8 if c.get("ring_big") else 6.5
    parts.append(f'<circle cx="134" cy="63" r="{ring_r}" fill="{c["ring"]}"/>')
    parts.append('<circle cx="135" cy="63" r="3.6" fill="#141414"/>')
    parts.append('<circle cx="136.4" cy="61.6" r="1.2" fill="#FFFFFF"/>')

    # المنقار (المعقوف)
    parts.append(f'<path d="M146 60 C164 58 170 78 158 92 C157 82 152 76 144 76 Z" fill="{c["beak"]}"/>')
    parts.append(f'<path d="M145 77 C152 79 156 85 153 92 C147 90 143 84 143 79 Z" fill="{c["beak"]}" opacity=".78"/>')

    # الغصن + الأرجل
    parts.append('<rect x="18" y="176" width="176" height="11" rx="5.5" fill="#7A5230"/>')
    parts.append('<path d="M150 176 q14 -10 26 -6" stroke="#7A5230" stroke-width="5" fill="none" stroke-linecap="round"/>')
    parts.append('<ellipse cx="164" cy="168" rx="9" ry="5" fill="#5E9B3A"/>')
    for x in (100, 116):
        parts.append(f'<path d="M{x} 166 v8 m-5 3 q5 -6 10 0" stroke="#8A8F93" stroke-width="4" fill="none" stroke-linecap="round"/>')

    h = int(size * 1.15)
    return (f'<svg viewBox="0 0 200 230" width="{size}" height="{h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="رسمة ببغاء {species}">{"".join(parts)}</svg>')
