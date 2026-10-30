"""
Lookups derived from the device registry (material/lut.xlsx, the partner's look-up table), used by the
ingestion (0a_offline_readings.py, 0b_online_ingest.py) and by the snapshot update
(snapshot_add_lorawan.py).

    python scripts/build_lookups.py

Writes, in material/:
  ARGUS_nodes.csv       site,nodeid,latitude,longitude,altitude — node coordinates from the LUT
                        (one row per node with coordinates; the first row of a node that has them)
  site_lookup.csv       device,site — the pilot site of devices whose readings arrive under a partner
                        channel instead of a site ("lorawan", "eurecat"): every LoRaWAN DevEUI and the
                        Eurecat devices in the LUT, plus the two multispectral imagers, which the LUT does
                        not list and which are at Ranverso (confirmed by the project)
  lorawan_channels.csv  key,unit — the unit of each LoRaWAN payload key, from the LUT's converted
                        examples ("measurements": [{"n", "v", "u"}])
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

MATERIAL = Path(__file__).resolve().parent.parent / "material"
SITE = {"Baltanas": "baltanas", "Delos": "delos", "Monti Lucretili": "lucretili", "Lucretili": "lucretili",
        "Ranverso": "ranverso", "Schenkenberg": "schenkenberg"}
# Devices the LUT does not list, with the site the project gave for them.
EXTRA_SITES = {"Multimodal_Imager_1": "ranverso", "Multimodal_Imager_2": "ranverso",
               "f3a12c45-8b2e-5f1d-9e34-ab67cd890ef1": "ranverso",   # sensor of Multimodal_Imager_1
               "a4968f18-92d6-568e-96d2-de8cf9fa2df1": "ranverso"}   # sensor of Multimodal_Imager_2
PARTNER_CHANNEL_DEVICES = ("lorawan", "eurecat", "ath")   # LUT topic ids of partner channels (ath: Eurecat)
# Units of LoRaWAN keys that no converted example shows, from the LUT's "Physical Quantity" column
# (2CF7F1C072600345: "Electrical Conductivity (dS/m), Temperature (ºC), Soil Moisture (%)"; the soil sensor
# A8610A333526680F reports a second temperature/humidity pair).
EXTRA_UNITS = {"temp2": "C", "hum2": "%", "moisture": "%", "ec": "dS/m"}


def _num(v):
    try:
        f = float(v)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


def main() -> None:
    lut = pd.read_excel(MATERIAL / "lut.xlsx", header=None).iloc[2:]
    nodes, lookup, units = {}, dict(EXTRA_SITES), dict(EXTRA_UNITS)
    for _, r in lut.iterrows():
        site = SITE.get(str(r[10]).strip())
        node = None if pd.isna(r[3]) else str(r[3]).strip()
        sensor = None if pd.isna(r[2]) else str(r[2]).strip()
        code = None if pd.isna(r[0]) else str(r[0]).strip()
        lat, lon, alt = _num(r[7]), _num(r[8]), _num(r[9])
        if site and node and lat is not None and lon is not None and node not in nodes:
            nodes[node] = (site, lat, lon, alt)
        topic = "" if pd.isna(r[5]) else str(r[5]).strip().lower()
        example = "" if pd.isna(r[20]) else str(r[20])
        partner = topic in PARTNER_CHANNEL_DEVICES or '"site": "lorawan"' in example or '"site": "eurecat"' in example
        if site and partner:
            for dev in (node, sensor, code):
                if dev and dev != "nan":
                    lookup.setdefault(dev, site)
        if '"site": "lorawan"' in example:
            try:
                for m in json.loads(example).get("measurements", []):
                    if m.get("n") and m.get("u") is not None:
                        units.setdefault(m["n"], m["u"])
            except json.JSONDecodeError:
                pass
    with open(MATERIAL / "ARGUS_nodes.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["site", "nodeid", "latitude", "longitude", "altitude"])
        for node, (site, lat, lon, alt) in sorted(nodes.items(), key=lambda kv: (kv[1][0], kv[0])):
            w.writerow([site.capitalize(), node, lat, lon, "" if alt is None else alt])
    with open(MATERIAL / "site_lookup.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["device", "site"])
        w.writerows(sorted(lookup.items()))
    with open(MATERIAL / "lorawan_channels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "unit"])
        w.writerows(sorted(units.items()))
    print(f"{len(nodes)} nodes with coordinates, {len(lookup)} partner-channel devices, {len(units)} LoRaWAN keys with units")


if __name__ == "__main__":
    main()
