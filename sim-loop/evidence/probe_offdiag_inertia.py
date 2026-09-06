#!/usr/bin/env python3
"""probe_offdiag_inertia — off-diagonal inertia 0-default 暗黙契約の機械測定 (falsify-008).

測定内容 (測定専用・既存コードに触れない):
  1. 両 fixture (giemon_arm6, giemon_caterpillar_facade) の EDN と URDF から
     全 link の inertia テンソル 6 成分を抽出し、textual convention を数える:
     - URDF: 全 link が ixy/ixz/iyz を明示しているか (6/6 keys)
     - EDN:  各 link が 6 key 明示 / off-diagonal 3 key 省略 のどちらか
  2. 0-default 読み (省略=0) と strict 読み (6 key 必須, 省略=nil) を
     シミュレートし、URDF との数値不一致件数を数える。
  3. URDF の XML well-formedness を検査 (parse_urdf 前提の成立性)。
  4. parity oracle (`from_edn(edn) == parse_urdf(urdf)`) の実装個所を
     giemon の .clj/.cljc から数える (0 なら oracle は未実装)。

決定的 (入力ファイルのみに依存、乱数・時刻なし)。
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # .../orgs/kotoba-lang/giemon
FIX = REPO / "fixtures"
COMPONENTS = ["ixx", "iyy", "izz", "ixy", "ixz", "iyz"]
OFFDIAG = ["ixy", "ixz", "iyz"]


def parse_urdf(path):
    """link name -> {component: float} (URDF は 6 成分を明示)。

    well-formed でない XML (例: XML コメント内の `--`) は ParseError —
    呼び出し側で捕捉して構造的赤として数える。
    """
    root = ET.parse(path).getroot()
    out = {}
    for link in root.findall("link"):
        inertial = link.find("inertial")
        if inertial is None:
            continue
        ine = inertial.find("inertia")
        out[link.get("name")] = {c: float(ine.get(c)) for c in COMPONENTS}
    return out


def parse_edn_inertias(path):
    """EDN 生テキストから (link name, present inertia keys) を抽出。

    pr-str blob 内の `#:link{:name "X" ... :inertia {...}}` を走査する。
    戻り値: list of (name, {present_keys: value})
    """
    text = path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r":inertia\s*\{([^}]*)\}", text):
        body = m.group(1)
        head = text[: m.start()]
        names = re.findall(r':name\s*\\"([^"\\]+)\\"', head)
        name = names[-1] if names else "?anonymous?"
        kv = dict(re.findall(r":(\w[\w-]*)\s+([0-9.eE+-]+)", body))
        out.append((name, {k: float(v) for k, v in kv.items()}))
    return out


def count_impl_hits():
    """giemon src/test の .clj/.cljc に parity oracle 実装があるか数える。"""
    pats = ["parse_urdf", "parse-urdf", "from_edn", "from-edn"]
    hits = []
    for sub in ("src", "test"):
        for p in (REPO / sub).rglob("*.clj*"):
            t = p.read_text(encoding="utf-8", errors="replace")
            for pat in pats:
                if pat in t:
                    hits.append(f"{p.name}:{pat}")
    return hits


def check_fixture(fixture):
    print(f"== {fixture} ==")
    try:
        urdf = parse_urdf(FIX / fixture / f"{fixture}.urdf")
    except ET.ParseError as e:
        print(f"  URDF well-formedness: FAILED -- ParseError: {e} <-- RED (parse_urdf 不能)")
        raw = (FIX / fixture / f"{fixture}.urdf").read_text(encoding="utf-8")
        n_iner = len(re.findall(r"<inertia\s", raw))
        edn = parse_edn_inertias(FIX / fixture / f"{fixture}.edn")
        print(f"  (参考) URDF 内 <inertia タグ数: {n_iner}; EDN :inertia blocks: {len(edn)}")
        return ("wf_fail", str(e))

    edn = parse_edn_inertias(FIX / fixture / f"{fixture}.edn")
    edn_by_name, dupes = {}, []
    for name, kv in edn:
        if name in edn_by_name:
            dupes.append(name)
        else:
            edn_by_name[name] = kv
    print(f"  urdf links with inertial : {len(urdf)}")
    print(f"  edn :inertia blocks      : {len(edn)} (names: {sorted(edn_by_name)})")
    if dupes:
        print(f"  EDN duplicate names      : {sorted(set(dupes))}  <-- RED")
    n_missing, n_explicit0, n_value_mismatch, n_strict_fail = 0, 0, 0, 0
    for name, uvals in sorted(urdf.items()):
        ekv = edn_by_name.get(name)
        if ekv is None:
            print(f"  {name}: EDN に :inertia block なし <-- oracle 不成立 (EDN 側欠落)")
            n_strict_fail += 1
            continue
        missing = [c for c in COMPONENTS if c not in ekv]
        if missing:
            n_missing += 1
            n_strict_fail += 1  # strict 読み (6 key 必須) はここで nil/エラー
        explicit0 = [c for c in OFFDIAG if ekv.get(c) == 0.0]
        n_explicit0 += len(explicit0)
        diffs = []
        for c in COMPONENTS:
            ev = ekv.get(c, 0.0)  # 0-default 読み
            if ev != uvals[c]:
                diffs.append(f"{c}: edn={ekv.get(c, 'MISSING->0')} urdf={uvals[c]}")
        if diffs:
            n_value_mismatch += 1
            print(f"  {name}: 0-default でも不一致 {diffs} <-- RED (数値不一致)")
        else:
            tag = "offdiag省略" if missing else ("明示0" if explicit0 else "6key明示")
            print(f"  {name}: 一致 (0-default) [{tag}] missing={missing or '-'}")
    print(f"  EDN offdiag 省略 link    : {n_missing}/{len(urdf)}")
    print(f"  EDN 明示 0 offdiag key   : {n_explicit0}")
    print(f"  strict 読みで落ちる link : {n_strict_fail}/{len(urdf)}")
    print(f"  0-default でも数値不一致 : {n_value_mismatch} link")
    return ("ok", (n_missing, n_explicit0, n_strict_fail, n_value_mismatch))


def main():
    results = [check_fixture(f) for f in ("giemon_arm6", "giemon_caterpillar_facade")]
    hits = count_impl_hits()
    print("== parity oracle 実装個数 (giemon src/test の .clj/.cljc) ==")
    print(f"  parse_urdf/from_edn 系文字列ヒット: {len(hits)} {hits if hits else '(0 — oracle 未実装)'}")
    print("SUMMARY " + " ".join(
        f"{f}:{'wf_fail' if s == 'wf_fail' else f'missing={v[0]},explicit0={v[1]},strict_fail={v[2]},mismatch={v[3]}'}"
        for f, (s, v) in zip(("giemon_arm6", "giemon_caterpillar_facade"), results))
        + f" oracle_impl={len(hits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
