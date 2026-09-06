#!/usr/bin/env python3
"""probe_caterpillar_wf — falsify-008 caterpillar URDF 赤の反証 (falsify-009).

H11: falsify-008 の ParseError (line 9 コメント内 --) は唯一の well-formedness
障害で、コメントを除いた本体 XML は well-formed かつ EDN boom chain と
数値整合する — 反証対象は falsify-008 の「fixture 修正しない限り parity
oracle 成立不能」の記録。コメント除去後も parse 不成立 / 数値不一致が
残れば H11 は破れる。

決定的 (入力ファイルのみに依存)。fixture は一切修正しない。
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
URDF = REPO / "fixtures" / "giemon_caterpillar_facade" / "giemon_caterpillar_facade.urdf"
EDN = REPO / "fixtures" / "giemon_caterpillar_facade" / "giemon_caterpillar_facade.edn"
COMPONENTS = ["ixx", "iyy", "izz", "ixy", "ixz", "iyz"]
BS = chr(92)
Q = chr(34)

# pr-str blob 内は `:name \"linkX\"` (リテラル backslash+quote)。
# regex は backslash を \\. で受ける — 構築式は tmp 検証済み (v5 形)。
NAME_PAT = re.compile(":name" + r"\s*" + r"\\" + Q + "([A-Za-z0-9_]+)" + r"\\" + Q)
INERTIA_PAT = re.compile(r":inertia\s*\{([^}]*)\}")
KV_PAT = re.compile(r":(\w[\w-]*)\s+([0-9.eE+\-]+)")


def strip_xml_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def build_edn_map(edn_text):
    out = {}
    matches = list(NAME_PAT.finditer(edn_text))
    for i, nm in enumerate(matches):
        name = nm.group(1)
        if name in out:
            continue
        seg_start = nm.end()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(edn_text)
        seg = edn_text[seg_start:seg_end]
        m = INERTIA_PAT.search(seg)
        if m:
            out[name] = {k: float(v) for k, v in KV_PAT.findall(m.group(1))}
    return out


def main():
    raw = URDF.read_text(encoding="utf-8")
    edn_text = EDN.read_text(encoding="utf-8")

    step1 = "ok"
    try:
        ET.fromstring(raw)
    except ET.ParseError as e:
        step1 = f"ParseError: {e}"

    stripped = strip_xml_comments(raw)
    step2 = "ok"
    try:
        root = ET.fromstring(stripped)
    except ET.ParseError as e:
        step2 = f"ParseError: {e}"
        print(f"STEP1 raw_parse={step1}")
        print(f"STEP2 comment_stripped_parse=FAILED {step2} <-- RED")
        return 0
    n_links = len(root.findall("link"))
    n_joints = len(root.findall("joint"))

    urdf_in = {}
    missing_attr = []
    for link in root.findall("link"):
        ine = link.find("inertial")
        if ine is None:
            continue
        ie = ine.find("inertia")
        vals = {}
        for c in COMPONENTS:
            if ie.get(c) is None:
                missing_attr.append(f"{link.get('name')}:{c}")
            else:
                vals[c] = float(ie.get(c))
        urdf_in[link.get("name")] = vals

    edn_in = build_edn_map(edn_text)

    mismatches = []
    for name, uv in sorted(urdf_in.items()):
        ev = edn_in.get(name)
        if ev is None:
            mismatches.append(f"{name}: EDN :inertia block なし")
            continue
        for c in COMPONENTS:
            e = ev.get(c, 0.0)  # 0-default 読み
            if e != uv.get(c):
                mismatches.append(f"{name}.{c}: edn={e} urdf={uv.get(c)}")

    blocks_total = len(INERTIA_PAT.findall(edn_text))
    print(f"STEP1 raw_parse={step1}")
    print(f"STEP2 comment_stripped_parse=ok links={n_links} joints={n_joints}")
    print(f"STEP3 urdf_inertia_links={len(urdf_in)} missing_attr={missing_attr or 'none'}")
    print(f"STEP4 edn_named_links={sorted(edn_in)} blocks_total={blocks_total}")
    print(f"STEP5 mismatch={len(mismatches)} {mismatches or '(0-default 読みで全一致)'}")
    print("SUMMARY "
          + f"raw={'wf_fail' if step1 != 'ok' else 'wf_ok'}"
          + f" stripped={'wf_fail' if step2 != 'ok' else 'wf_ok'}"
          + f" links={n_links} joints={n_joints}"
          + f" urdf_in={len(urdf_in)} edn_in={len(edn_in)}"
          + f" mismatch={len(mismatches)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
