#!/usr/bin/env python3
"""
Descarga el CSV de origen y genera dos archivos en la raiz del repo:
  - data.json   : datos comprimidos que consume el dashboard (liviano).
  - export.csv  : una fila por pedido con muchas columnas, para el boton "Exportar Excel".
Se ejecuta desde el GitHub Action (.github/workflows/update-data.yml).
Solo usa la libreria estandar: no requiere pip install ni archivos auxiliares.
"""
import csv, json, io, os, sys, datetime, urllib.request

CSV_URL = "https://vtex.brandlive.net/upload/queries/ops-om-ar.csv"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CP de 4 digitos -> Partido (solo Provincia de Bs. As.). Embebido para no depender de archivos.
PART = json.loads(r'''{"1602":"Vicente Lopez","1603":"Vicente Lopez","1604":"Vicente Lopez","1605":"Vicente Lopez","1606":"Vicente Lopez","1607":"San Isidro","1608":"Tigre","1609":"San Isidro","1610":"Escobar","1611":"Tigre","1612":"Exaltacion De La Cruz","1613":"Malvinas Argentinas","1614":"Malvinas Argentinas","1615":"Malvinas Argentinas","1616":"Pilar","1617":"Tigre","1618":"Tigre","1619":"Escobar","1620":"Escobar","1621":"Tigre","1622":"Pilar","1623":"Escobar","1624":"Tigre","1625":"Escobar","1626":"Escobar","1627":"Escobar","1629":"Pilar","1630":"Pilar","1631":"Pilar","1632":"Pilar","1633":"Pilar","1634":"Pilar","1635":"Pilar","1636":"Vicente Lopez","1637":"Vicente Lopez","1638":"Vicente Lopez","1639":"Pilar","1640":"San Isidro","1641":"San Isidro","1642":"San Isidro","1643":"San Isidro","1644":"San Fernando","1645":"San Fernando","1646":"San Isidro","1647":"San Fernando","1648":"Tigre","1650":"General San Martin","1651":"San Miguel","1653":"Moron","1655":"Hurlingham","1657":"Tres De Febrero","1661":"San Miguel","1663":"San Miguel","1664":"Pilar","1667":"Exaltacion De La Cruz","1669":"Pilar","1685":"Moron","1686":"Hurlingham","1688":"Hurlingham","1690":"Tres De Febrero","1702":"Tres De Febrero","1704":"La Matanza","1706":"Moron","1707":"Moron","1708":"Moron","1712":"Moron","1713":"Ituzaingo","1714":"Ituzaingo","1715":"Ituzaingo","1716":"Merlo","1718":"Moreno","1721":"Moreno","1722":"Moreno","1723":"Merlo","1724":"Merlo","1727":"Marcos Paz","1736":"Moreno","1738":"Moreno","1740":"Moreno","1741":"General Las Heras","1742":"Moreno","1743":"Moreno","1744":"Moreno","1745":"Moreno","1746":"Moreno","1747":"General Rodriguez","1748":"General Rodriguez","1749":"General Rodriguez","1750":"General Rodriguez","1752":"La Matanza","1753":"La Matanza","1754":"La Matanza","1755":"La Matanza","1757":"La Matanza","1758":"La Matanza","1759":"La Matanza","1761":"Merlo","1763":"La Matanza","1764":"La Matanza","1765":"La Matanza","1766":"La Matanza","1768":"La Matanza","1770":"La Matanza","1778":"La Matanza","1781":"Marcos Paz","1783":"Marcos Paz","1784":"Marcos Paz","1785":"La Matanza","1786":"La Matanza","1789":"Marcos Paz","1791":"Marcos Paz","1792":"Marcos Paz","1793":"Marcos Paz","1801":"Ezeiza","1802":"Ezeiza","1803":"Ezeiza","1804":"Ezeiza","1805":"Esteban Echeverria","1806":"Ezeiza","1807":"Esteban Echeverria","1812":"Ezeiza","1821":"Lomas De Zamora","1822":"Lanus","1823":"Lanus","1824":"Lanus","1825":"Lanus","1826":"Lanus","1827":"Lomas De Zamora","1828":"Lomas De Zamora","1832":"Lomas De Zamora","1833":"Lomas De Zamora","1834":"Lomas De Zamora","1835":"Presidente Peron","1836":"La Matanza","1837":"Berazategui","1838":"Esteban Echeverria","1839":"Esteban Echeverria","1840":"Quilmes","1841":"Esteban Echeverria","1842":"Esteban Echeverria","1843":"Almirante Brown","1844":"Almirante Brown","1845":"Almirante Brown","1847":"Almirante Brown","1848":"Almirante Brown","1849":"Almirante Brown","1851":"Almirante Brown","1852":"Almirante Brown","1853":"Florencio Varela","1854":"Almirante Brown","1855":"Quilmes","1856":"Almirante Brown","1857":"Quilmes","1858":"Presidente Peron","1859":"La Costa","1861":"Berazategui","1862":"Presidente Peron","1863":"Florencio Varela","1864":"San Vicente","1865":"San Vicente","1867":"Hurlingham","1869":"Avellaneda","1870":"Avellaneda","1871":"Avellaneda","1872":"Avellaneda","1873":"Avellaneda","1874":"Avellaneda","1875":"Avellaneda","1876":"Quilmes","1877":"Quilmes","1878":"Quilmes","1879":"Quilmes","1880":"Berazategui","1881":"Quilmes","1882":"Quilmes","1883":"Quilmes","1884":"Berazategui","1885":"Berazategui","1886":"Berazategui","1889":"Florencio Varela","1890":"Berazategui","1893":"Berazategui","1894":"La Plata","1895":"La Plata","1896":"La Plata","1897":"La Plata","1898":"La Plata","1900":"La Plata","1901":"La Plata","1902":"La Plata","1903":"La Plata","1904":"La Plata","1906":"La Plata","1907":"La Plata","1908":"La Plata","1909":"La Plata","1910":"La Plata","1911":"Magdalena","1912":"La Plata","1913":"Magdalena","1914":"La Plata","1916":"La Plata","1918":"La Plata","1923":"Berisso","1924":"Berisso","1925":"Ensenada","1926":"Ensenada","1931":"Ensenada","1933":"La Plata","1947":"Magdalena","1980":"Brandsen","1983":"Brandsen","1984":"San Vicente","1986":"Brandsen","1987":"General Paz","2223":"Pergamino","2700":"Pergamino","2702":"Pergamino","2704":"Pergamino","2705":"Rojas","2706":"Pergamino","2713":"Pergamino","2715":"Pergamino","2718":"Pergamino","2724":"Pergamino","2740":"Arrecifes","2741":"Salto","2751":"Pergamino","2752":"Capitan Sarmiento","2760":"San Antonio De Areco","2800":"Zarate","2802":"Campana","2803":"Campana","2804":"Campana","2807":"Campana","2814":"Exaltacion De La Cruz","2900":"San Nicolas","2901":"San Nicolas","2902":"San Nicolas","2907":"Tordillo","2914":"Ramallo","2915":"Ramallo","2930":"San Pedro","2933":"Ramallo","2938":"Baradero","2942":"Baradero","2943":"Baradero","6000":"Junin","6002":"Junin","6003":"General Arenales","6005":"General Arenales","6013":"General Viamonte","6015":"General Viamonte","6026":"General Pinto","6027":"General Arenales","6032":"Leandro N Alem","6047":"Bragado","6049":"Junin","6050":"General Pinto","6053":"General Pinto","6062":"General Pinto","6065":"Florentino Ameghino","6070":"Lincoln","6073":"Lincoln","6075":"Lincoln","6077":"Lincoln","6078":"Lincoln","6079":"Lincoln","6102":"General Villegas","6107":"General Villegas","6223":"General Villegas","6224":"General Villegas","6230":"General Villegas","6231":"Carlos Tejedor","6235":"General Villegas","6237":"Rivadavia","6239":"Moreno","6241":"General Villegas","6249":"General Villegas","6339":"Salliquelo","6346":"Pellegrini","6347":"Pellegrini","6348":"Pellegrini","6400":"Trenque Lauquen","6403":"Olavarria","6411":"Guamini","6417":"Guamini","6430":"Adolfo Alsina","6435":"Guamini","6439":"Guamini","6441":"Adolfo Alsina","6455":"Carlos Tejedor","6471":"Daireaux","6500":"9 De Julio","6502":"9 De Julio","6503":"9 De Julio","6505":"9 De Julio","6509":"Carlos Tejedor","6511":"Bolivar","6515":"9 De Julio","6516":"9 De Julio","6530":"Carlos Casares","6531":"Carlos Casares","6533":"Lincoln","6536":"Carlos Casares","6537":"Carlos Casares","6550":"Bolivar","6551":"Bolivar","6553":"Bolivar","6555":"Daireaux","6560":"9 De Julio","6593":"Daireaux","6600":"Mercedes","6602":"Mercedes","6605":"Navarro","6608":"Lujan","6616":"Chacabuco","6620":"Chivilcoy","6621":"25 De Mayo","6622":"Chivilcoy","6625":"Chivilcoy","6627":"Navarro","6628":"Suipacha","6634":"Alberti","6637":"Bragado","6640":"Bragado","6641":"Bragado","6646":"Bragado","6648":"Bragado","6660":"25 De Mayo","6663":"25 De Mayo","6665":"25 De Mayo","6691":"Alberti","6700":"Lujan","6701":"Lujan","6702":"Lujan","6703":"Lujan","6706":"Lujan","6708":"Lujan","6712":"Lujan","6717":"25 De Mayo","6720":"San Andres De Giles","6725":"Carmen De Areco","6734":"Chacabuco","6740":"Chacabuco","6748":"Chacabuco","6753":"Lujan","7000":"Tandil","7001":"Tandil","7005":"Benito Juarez","7007":"Loberia","7011":"Necochea","7020":"Benito Juarez","7033":"Roque Perez","7100":"Dolores","7101":"Tordillo","7109":"La Costa","7111":"La Costa","7113":"La Costa","7114":"Moron","7115":"Dolores","7116":"Chascomus","7120":"Pilar","7130":"Chascomus","7150":"Ayacucho","7160":"General Guido","7164":"Pinamar","7165":"Villa Gesell","7166":"Pinamar","7167":"Pinamar","7169":"Pinamar","7171":"Pinamar","7172":"Mar Chiquita","7174":"Mar Chiquita","7200":"Las Flores","7214":"Azul","7220":"Monte","7223":"General Belgrano","7228":"General Belgrano","7240":"Lobos","7245":"Roque Perez","7249":"Lobos","7260":"Saladillo","7263":"General Alvear","7300":"Azul","7303":"Tapalque","7311":"Azul","7342":"Tapalque","7400":"Olavarria","7403":"Olavarria","7404":"Laprida","7406":"General La Madrid","7414":"Laprida","7421":"Olavarria","7429":"San Miguel","7436":"Olavarria","7500":"Tres Arroyos","7501":"Coronel Pringles","7509":"Coronel Dorrego","7513":"Adolfo Gonzales Chaves","7515":"Adolfo Gonzales Chaves","7530":"Coronel Pringles","7540":"Coronel Suarez","7541":"Coronel Suarez","7545":"Coronel Suarez","7569":"Coronel Suarez","7570":"Coronel Suarez","7600":"General Pueyrredon","7601":"Tres De Febrero","7602":"Mar Chiquita","7603":"General Pueyrredon","7604":"General Pueyrredon","7605":"Mar Chiquita","7606":"General Pueyrredon","7607":"Rauch","7608":"General Pueyrredon","7610":"Maipu","7611":"Mar Chiquita","7613":"Balcarce","7614":"General Pueyrredon","7620":"Balcarce","7630":"Necochea","7631":"Necochea","7632":"Necochea","7635":"Loberia","7774":"General Alvarado","7792":"Mar Chiquita","7794":"Mar Chiquita","7803":"Mar Chiquita","7807":"General Pueyrredon","8000":"Bahia Blanca","8001":"Bahia Blanca","8002":"Bahia Blanca","8003":"Bahia Blanca","8049":"Bahia Blanca","8071":"Coronel De Marina Leonardo Rosales","8103":"Bahia Blanca","8105":"Bahia Blanca","8107":"Bahia Blanca","8109":"Coronel De Marina Leonardo Rosales","8118":"Bahia Blanca","8124":"Puan","8126":"Puan","8129":"Puan","8132":"Villarino","8142":"Villarino","8146":"Villarino","8150":"Coronel Dorrego","8153":"Monte Hermoso","8170":"Saavedra","8180":"Puan","8183":"Puan","8187":"Puan","8225":"Puan","8504":"Patagones","8508":"Patagones","8512":"Patagones","5351":"Vicente Lopez","5531":"Pellegrini","5571":"Chivilcoy","3625":"La Matanza","8352":"Zarate","4130":"Mercedes","5143":"General Alvarado"}''')

C2MAP = {"moova": "Moova", "cabify": "Cabify", "andreani": "Andreani", "fasttrack": "Fasttrack",
         "innerlogistics": "Inner", "ocasa": "Ocasa", "pickit": "Pickit"}
PMAP = {"andreani": "Andreani", "cabify": "Cabify", "fasttrack": "Fasttrack", "hop": "HOP",
        "inner": "Inner", "moova": "Moova", "ocasa": "Ocasa", "pickit": "Pickit",
        "elogisticaregular": "Elogistica", "elogistica": "Elogistica"}
COURIER_ORDER = ["Moova", "Andreani", "Ocasa", "Fasttrack", "Inner", "Pickit",
                 "Cabify", "Elogistica", "HOP", "Sin asignar"]
TIPO_ORDER = ["Regular", "Same Day", "Nextday", "SPU", "SPU-HOP", "HTH", "Meliflex", "Reverse", "Otro"]
SVC_NICE = {"regular": "Regular", "pickpoint": "Pick-up point", "spu": "SPU / retiro",
            "all": "Estandar (all)", "sameday": "Same day", "sameday_pm": "Same day PM",
            "nextday": "Next day", "nextday_pm": "Next day PM",
            "topper_misiones": "Topper Misiones", "(sin dato)": "Sin dato", "ampm": "AM/PM"}

# Columnas del export.csv (encabezado -> columna del CSV origen). Las derivadas se calculan.
EXPORT_COLS = [
    ("ID Pedido", "order_id"),
    ("ID Externo", "order_ext-id"),
    ("Marca", "@brand"),
    ("Canal", "chb_name"),
    ("Courier", "@courier"),
    ("Tipo de envío", "@tipo"),
    ("Servicio", "ship_shipping-method"),
    ("Tipo servicio", "ship_shipping-type"),
    ("Estado", "order_status"),
    ("Fecha", "@fecha"),
    ("Creado", "order_channel-created-at"),
    ("Promesa entrega", "order_delivery-promise"),
    ("Provincia", "@prov"),
    ("Partido", "@partido"),
    ("CP", "order_zipcode"),
    ("Cant. solicitada", "order_req-qty"),
    ("Cant. confirmada", "order_conf-qty"),
    ("Estado envío", "ship_status"),
    ("Carrier", "ship_carrier1"),
    ("Tracking", "ship_tracking-number"),
    ("Envío creado", "ship_created-at"),
    ("Despachado", "ship_shipped"),
    ("Entregado", "ship_delivered"),
    ("1ra visita", "ship_1st_visit"),
    ("Batch", "ship-batch_name"),
]


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
    if not state: return "-"
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
        sys.exit(1)

    seen, recs, exrows = set(), [], []
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
        brand = r.get("brand_name") or "-"
        if brand == "Bocashop cabj":
            brand = "Bocashop"
        cour = courier_of(method, r.get("ship_carier2"))
        tp = tipo_of(method)
        dt = (r.get("order_channel-created-at") or "")[:10]
        prov = prov_of(r.get("order_state"))
        plabel = prov_label(r.get("order_state"))
        zc = (str(r.get("order_zipcode") or "")).strip()
        recs.append({"brand": brand, "cour": cour, "tp": tp, "dt": dt,
                     "del": 1 if status == "delivered" else 0,
                     "svc": r.get("ship_shipping-type") or "(sin dato)",
                     "prov": prov, "plabel": plabel, "zip": zc})
        # fila de export (mismo orden que recs)
        derived = {"@brand": brand, "@courier": cour, "@tipo": tp, "@fecha": dt,
                   "@prov": plabel, "@partido": (PART.get(zc, "") if prov == "BA" else "")}
        exrows.append([derived.get(src, r.get(src, "")) if src.startswith("@") else (r.get(src, "") or "")
                       for _, src in EXPORT_COLS])

    if not recs:
        print("ERROR: el CSV no contiene pedidos validos despues de filtrar.", file=sys.stderr)
        sys.exit(1)

    # ----- data.json (dashboard) -----
    bc = {}
    for r in recs: bc[r["brand"]] = bc.get(r["brand"], 0) + 1
    brands = sorted(bc, key=lambda b: -bc[b])
    couriers = [c for c in COURIER_ORDER if c in {r["cour"] for r in recs}]
    tipos = [t for t in TIPO_ORDER if t in {r["tp"] for r in recs}]
    scount = {}
    for r in recs: scount[r["svc"]] = scount.get(r["svc"], 0) + 1
    services = sorted(scount, key=lambda s: -scount[s])
    dates = sorted({r["dt"] for r in recs if is_date(r["dt"])})
    bi = {b: i for i, b in enumerate(brands)}; ci = {c: i for i, c in enumerate(couriers)}
    ti = {t: i for i, t in enumerate(tipos)}; si = {s: i for i, s in enumerate(services)}
    di = {d: i for i, d in enumerate(dates)}

    zi, zips, zvotes = {}, [], {}
    for r in recs:
        z = r["zip"]
        if not z: continue
        if z not in zi:
            zi[z] = len(zips); zips.append(z)
        key = (r["plabel"], 1 if r["prov"] == "BA" else 0)
        zvotes.setdefault(z, {})
        zvotes[z][key] = zvotes[z].get(key, 0) + 1
    zip_prov, zip_ba = [], []
    for z in zips:
        best = max(zvotes[z].items(), key=lambda kv: kv[1])[0]
        zip_prov.append(best[0]); zip_ba.append(best[1])

    orders = []
    for r in recs:
        z = zi.get(r["zip"], -1) if r["zip"] else -1
        orders.append([bi[r["brand"]], ci[r["cour"]], si[r["svc"]],
                       di.get(r["dt"], 0), z, r["del"], ti[r["tp"]]])

    payload = {
        "brands": brands, "couriers": couriers, "tipos": tipos,
        "services": services, "svc_nice": [SVC_NICE.get(s, s) for s in services],
        "dates": dates, "zips": zips, "zip_prov": zip_prov, "zip_ba": zip_ba,
        "orders": orders,
        "date_min": dates[0] if dates else None, "date_max": dates[-1] if dates else None,
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    with open(os.path.join(ROOT, "data.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    # ----- export.csv (boton Exportar) -----
    with open(os.path.join(ROOT, "export.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([h for h, _ in EXPORT_COLS])
        w.writerows(exrows)

    print("OK: %d pedidos | data.json + export.csv (%d columnas)" % (len(orders), len(EXPORT_COLS)), flush=True)


if __name__ == "__main__":
    main()
