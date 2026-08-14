#!/usr/bin/env python3
"""
Descarga el CSV de origen, lo transforma y escribe data.json en la raiz del repo.
Se ejecuta desde el GitHub Action (.github/workflows/update-data.yml).

No requiere pip install ni archivos auxiliares: solo la libreria estandar.
"""
import csv, json, io, os, sys, datetime, urllib.request

CSV_URL = "https://vtex.brandlive.net/upload/queries/ops-om-ar.csv"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

C2MAP = {"moova": "Moova", "cabify": "Cabify", "andreani": "Andreani", "fasttrack": "Fasttrack",
         "innerlogistics": "Inner", "ocasa": "Ocasa", "pickit": "Pickit"}
PMAP = {"andreani": "Andreani", "cabify": "Cabify", "fasttrack": "Fasttrack", "hop": "HOP",
        "inner": "Inner", "moova": "Moova", "ocasa": "Ocasa", "pickit": "Pickit",
        "elogisticaregular": "Elogistica", "elogistica": "Elogistica"}
COURIER_ORDER = ["Moova", "Andreani", "Ocasa", "Fasttrack", "Inner", "Pickit",
                 "Cabify", "Elogistica", "HOP", "Sin asignar"]
TIPO_ORDER = ["Regular", "Same Day", "Nextday", "SPU", "SPU-HOP", "HTH", "Meliflex", "Reverse", "Otro"]
SVC_NICE = {"regular": "Regular", "pickpoint": "Pick-up point", "spu": "SPU / retiro",
            "all": "Estándar (all)", "sameday": "Same day", "sameday_pm": "Same day PM",
            "nextday": "Next day", "nextday_pm": "Next day PM",
            "topper_misiones": "Topper Misiones", "(sin dato)": "Sin dato", "ampm": "AM/PM"}


def courier_of(method, c2):
    ml = (method or "").lower()
    if ml in ("me2_flex_bsas", "me2_flex_caba"):
        return C2MAP.get((c2 or "").strip().lower(), "Sin asignar")
    if ml.startswith("spu_estandar"):
        return "Elogistica"
    if ml.startswith("spu_ocasa"):
        return "Ocasa"
    pre = ml.split("_")[0].split(":")[0]
    if pre in PMAP:
        return PMAP[pre]
    return C2MAP.get((c2 or "").strip().lower(), "Sin asignar")


def tipo_of(method):
    ml = (method or "").lower()
    if ml in ("me2_flex_bsas", "me2_flex_caba"): return "Meliflex"
    if "reverse" in ml: return "Reverse"
    if ml == "hop_pickuppoints": return "SPU-HOP"
    if "hth" in ml: return "HTH"
    if "sameday" in ml: return "Same Day"
    if "nextday" in ml: return "Nextday"
    if "_spu_" in ml or ml.startswith("spu_") or ml == "pickit" or "pickuppoints" in ml: return "SPU"
    if "regular" in ml: return "Regular"
    return "Otro"


def prov_of(state):
    if not state: return "OTRA"
    s = str(state).strip().lower()
    if "autonoma" in s or s == "capital federal" or "ciudad" in s: return "CABA"
    if "buenos aires" in s: return "BA"
    return "OTRA"


def prov_label(state):
    """Etiqueta legible de la provincia (para el mapa de calor a nivel pais)."""
    if not state: return "—"
    s = str(state).strip()
    low = s.lower()
    if "autonoma" in low or low == "capital federal" or "ciudad" in low:
        return "CABA"
    return s.title()


def is_date(s):
    return len(s) == 10 and s[4] == "-" and s[7] == "-" and s[:4].isdigit()


def download(url):
    print("Descargando CSV: %s" % url, flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; gh-actions-dashboard/1.0)"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()
    print("Descargado: %.1f MB" % (len(raw) / 1048576.0), flush=True)
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def main():
    try:
        text = download(CSV_URL)
    except Exception as e:
        print("ERROR al descargar el CSV: %s" % e, file=sys.stderr)
        sys.exit(1)

    reader = csv.DictReader(io.StringIO(text))
    cols = reader.fieldnames or []
    needed = ["order_id", "order_status", "ship_shipping-method", "brand_name"]
    missing = [c for c in needed if c not in cols]
    if missing:
        print("ERROR: al CSV le faltan columnas: %s" % missing, file=sys.stderr)
        print("Columnas encontradas: %s" % cols[:20], file=sys.stderr)
        sys.exit(1)

    seen, recs = set(), []
    for r in reader:
        oid = r.get("order_id")
        if not oid or oid in seen:
            continue
        seen.add(oid)
        status = r.get("order_status") or ""
        if status == "cancelled":
            continue
        method = r.get("ship_shipping-method") or ""
        if method == "me2":
            continue
        brand = r.get("brand_name") or "—"
        if brand == "Bocashop cabj":
            brand = "Bocashop"
        recs.append({
            "brand": brand,
            "cour": courier_of(method, r.get("ship_carier2")),
            "tp": tipo_of(method),
            "dt": (r.get("order_channel-created-at") or "")[:10],
            "del": 1 if status == "delivered" else 0,
            "svc": r.get("ship_shipping-type") or "(sin dato)",
            "prov": prov_of(r.get("order_state")),
            "plabel": prov_label(r.get("order_state")),
            "zip": (str(r.get("order_zipcode") or "")).strip(),
        })

    if not recs:
        print("ERROR: el CSV no contiene pedidos validos despues de filtrar.", file=sys.stderr)
        sys.exit(1)

    bc = {}
    for r in recs: bc[r["brand"]] = bc.get(r["brand"], 0) + 1
    brands = sorted(bc, key=lambda b: -bc[b])

    cset = {r["cour"] for r in recs}
    couriers = [c for c in COURIER_ORDER if c in cset]

    tset = {r["tp"] for r in recs}
    tipos = [t for t in TIPO_ORDER if t in tset]

    sc = {}
    for r in recs: sc[r["svc"]] = sc.get(r["svc"], 0) + 1
    services = sorted(sc, key=lambda s: -sc[s])

    dates = sorted({r["dt"] for r in recs if is_date(r["dt"])})

    bi = {b: i for i, b in enumerate(brands)}
    ci = {c: i for i, c in enumerate(couriers)}
    ti = {t: i for i, t in enumerate(tipos)}
    si = {s: i for i, s in enumerate(services)}
    di = {d: i for i, d in enumerate(dates)}

    # Tabla de codigos postales de TODO el pais (el navegador resuelve coords/partido).
    # Para cada CP guardamos su provincia (label mas frecuente) y si es Prov. Bs. As.
    zi, zips = {}, []
    zvotes = {}   # zip -> {(label, esBA): conteo}
    for r in recs:
        z = r["zip"]
        if not z:
            continue
        if z not in zi:
            zi[z] = len(zips)
            zips.append(z)
        key = (r["plabel"], 1 if r["prov"] == "BA" else 0)
        zvotes.setdefault(z, {})
        zvotes[z][key] = zvotes[z].get(key, 0) + 1

    zip_prov, zip_ba = [], []
    for z in zips:
        best = max(zvotes[z].items(), key=lambda kv: kv[1])[0]
        zip_prov.append(best[0])
        zip_ba.append(best[1])

    orders = []
    for r in recs:
        z = zi.get(r["zip"], -1) if r["zip"] else -1
        orders.append([bi[r["brand"]], ci[r["cour"]], si[r["svc"]],
                       di.get(r["dt"], 0), z, r["del"], ti[r["tp"]]])

    payload = {
        "brands": brands, "couriers": couriers, "tipos": tipos,
        "services": services, "svc_nice": [SVC_NICE.get(s, s) for s in services],
        "dates": dates,
        "zips": zips, "zip_prov": zip_prov, "zip_ba": zip_ba,
        "orders": orders,
        "date_min": dates[0] if dates else None,
        "date_max": dates[-1] if dates else None,
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    out = os.path.join(ROOT, "data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    print("OK: %d pedidos | %d marcas | %d couriers | %s a %s | data.json %d KB" % (
        len(orders), len(brands), len(couriers),
        payload["date_min"], payload["date_max"], os.path.getsize(out) // 1024), flush=True)


if __name__ == "__main__":
    main()
