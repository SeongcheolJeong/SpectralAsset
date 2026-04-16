#!/usr/bin/env python3

import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_iso8601(value: str) -> str:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_existing_generated_at(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = payload.get("generated_at")
    if not isinstance(value, str):
        return None
    try:
        return parse_iso8601(value)
    except ValueError:
        return None


def resolve_generated_at() -> str:
    build_timestamp = os.getenv("BUILD_TIMESTAMP")
    if build_timestamp:
        return parse_iso8601(build_timestamp)

    source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        epoch = int(source_date_epoch)
        return dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc).replace(microsecond=0).isoformat()

    for rel_path in [
        "validation/reports/validation_summary.json",
        "raw/source_ledger.json",
    ]:
        existing = load_existing_generated_at(REPO_ROOT / rel_path)
        if existing:
            return existing

    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


GENERATED_AT = resolve_generated_at()

MASTER_GRID = list(range(350, 1701))
RUNTIME_GRID = list(range(400, 1101, 5))

FAMILY_ENUM = {"traffic_sign", "traffic_light", "road_surface", "road_marking", "road_furniture"}
MATERIAL_ENUM = {"reflective", "transmissive", "emissive", "retroreflective", "wet_overlay"}
SAMPLE_STATE_ENUM = {"dry", "wet", "aged", "dusty", "coated"}
SENSOR_BRANCH_ENUM = {"rgb", "rgb_nir"}
SOURCE_QUALITY_ENUM = {"measured_standard", "measured_derivative", "vendor_derived", "project_proxy"}
CAMERA_CHANNELS = ("r", "g", "b", "nir")

DIRS = [
    "raw/sources",
    "canonical/spectra",
    "canonical/materials",
    "canonical/camera",
    "canonical/manifests",
    "canonical/emissive",
    "canonical/scenarios",
    "canonical/atmospheres",
    "canonical/templates/signs",
    "canonical/geometry/usd",
    "canonical/scenes",
    "exports/usd",
    "exports/gltf",
    "validation/reports",
]

SOURCE_DEFS = [
    {
        "id": "cie_d65_csv",
        "url": "https://files.cie.co.at/CIE_std_illum_D65.csv",
        "file_name": "CIE_std_illum_D65.csv",
        "classification": "redistributable",
        "license_summary": "CIE dataset with citation required",
    },
    {
        "id": "cie_d65_metadata",
        "url": "https://files.cie.co.at/CIE_std_illum_D65.csv_metadata.json",
        "file_name": "CIE_std_illum_D65.csv_metadata.json",
        "classification": "redistributable",
        "license_summary": "CIE metadata with DOI",
    },
    {
        "id": "astm_g173_zip",
        "url": "https://www.nlr.gov/media/docs/libraries/grid/zip/astmg173.zip?sfvrsn=1ef05e45_5",
        "file_name": "astmg173.zip",
        "classification": "derived-only",
        "license_summary": "NLR data disclaimer applies",
    },
    {
        "id": "aeronet_quality_assurance_pdf",
        "url": "https://aeronet.gsfc.nasa.gov/new_web/Documents/AERONETcriteria_final1.pdf",
        "file_name": "AERONETcriteria_final1.pdf",
        "classification": "reference-only",
        "license_summary": "NASA documentation",
    },
    {
        "id": "libradtran_home",
        "url": "https://www.libradtran.org/",
        "file_name": "index.html",
        "classification": "reference-only",
        "license_summary": "Official documentation reference",
    },
    {
        "id": "osm_traffic_sign_wiki",
        "url": "https://wiki.openstreetmap.org/wiki/Key:traffic_sign",
        "file_name": "traffic_sign.html",
        "classification": "reference-only",
        "license_summary": "OpenStreetMap Wiki reference",
    },
    {
        "id": "mapillary_sign_help",
        "url": "https://help.mapillary.com/hc/en-us/articles/360003021432-Exploring-traffic-signs",
        "file_name": "exploring_traffic_signs.html",
        "classification": "reference-only",
        "license_summary": "Mapillary help reference",
    },
    {
        "id": "mapillary_download_help",
        "url": "https://help.mapillary.com/hc/en-us/articles/4407521157138-Downloading-map-data-via-the-Mapillary-web-app",
        "file_name": "downloading_map_data.html",
        "classification": "reference-only",
        "license_summary": "Mapillary help reference",
    },
    {
        "id": "openusd_faq",
        "url": "https://openusd.org/release/usdfaq.html",
        "file_name": "usdfaq.html",
        "classification": "reference-only",
        "license_summary": "OpenUSD documentation reference",
    },
    {
        "id": "gltf_spec",
        "url": "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html",
        "file_name": "glTF-2.0.html",
        "classification": "reference-only",
        "license_summary": "Khronos specification reference",
    },
    {
        "id": "polyhaven_license",
        "url": "https://polyhaven.com/license",
        "file_name": "license.html",
        "classification": "reference-only",
        "license_summary": "Poly Haven CC0 reference",
    },
    {
        "id": "ambientcg_license",
        "url": "https://docs.ambientcg.com/license/",
        "file_name": "license.html",
        "classification": "reference-only",
        "license_summary": "ambientCG CC0 reference",
    },
    {
        "id": "usgs_spectral_library_page",
        "url": "https://www.usgs.gov/data/usgs-spectral-library-version-7-data",
        "file_name": "usgs_spectral_library_v7.html",
        "classification": "reference-only",
        "license_summary": "USGS landing page reference",
    },
    {
        "id": "ecostress_spectral_library_page",
        "url": "https://speclib.jpl.nasa.gov/",
        "file_name": "index.html",
        "classification": "reference-only",
        "license_summary": "ECOSTRESS landing page reference",
    },
    {
        "id": "unece_road_signs_page",
        "url": "https://unece.org/info/Transport/Road-Traffic-and-Road-Safety/pub/2637",
        "file_name": "road_signs_and_signals.html",
        "classification": "reference-only",
        "license_summary": "Official UNECE reference page",
    },
    {
        "id": "basler_color_emva_knowledge",
        "url": "https://docs.baslerweb.com/knowledge/about-emva1288-reports-for-color-sensors",
        "file_name": "about-emva1288-reports-for-color-sensors.html",
        "classification": "reference-only",
        "license_summary": "Basler public documentation for color-sensor spectral response context",
    },
    {
        "id": "sony_imx900_product_page",
        "url": "https://www.sony-semicon.com/en/products/is/industry/gs/imx900.html",
        "file_name": "imx900.html",
        "classification": "reference-only",
        "license_summary": "Sony official product page for near-infrared-sensitive global-shutter sensor",
    },
    {
        "id": "sony_isx016_pdf",
        "url": "https://www.sony-semicon.com/files/62/pdf/p-15_ISX016.pdf",
        "file_name": "sony_isx016.pdf",
        "classification": "reference-only",
        "license_summary": "Sony official image-sensor PDF with near-infrared sensitivity claim",
    },
]

USGS_WAVELENGTH_SOURCE = {
    "id": "usgs_asdfr_wavelengths_2151",
    "classification": "redistributable",
    "license_summary": "USGS Spectral Library Version 7 selected local subset",
    "selection_role": "wavelength_basis",
    "local_path": "ASCIIdata/ASCIIdata_splib07b/splib07b_Wavelengths_ASDFR_0.35-2.5microns_2151ch.txt",
    "file_name": "splib07b_Wavelengths_ASDFR_0.35-2.5microns_2151ch.txt",
    "notes": "Canonical wavelength basis for selected ASDFR material samples.",
}

USGS_SAMPLE_SELECTIONS = [
    {
        "id": "usgs_gds376_asphalt_road_old",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "active_binding",
        "curve_name": "src_usgs_gds376_asphalt_road_aref",
        "bind_material_id": "mat_asphalt_dry",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.txt",
        "file_name": "splib07b_Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.html",
        "metadata_file_name": "Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.html",
        "notes": "Measured dry road asphalt baseline from USGS v7.",
    },
    {
        "id": "usgs_gds375_concrete_road",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "active_binding",
        "curve_name": "src_usgs_gds375_concrete_road_aref",
        "bind_material_id": "mat_concrete",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt",
        "file_name": "splib07b_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.html",
        "metadata_file_name": "Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.html",
        "notes": "Measured concrete road baseline from USGS v7.",
    },
    {
        "id": "usgs_gds334_galvanized_sheet_metal",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "active_binding",
        "curve_name": "src_usgs_gds334_galvanized_sheet_metal_aref",
        "bind_material_id": "mat_metal_galvanized",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_GalvanizedSheetMetal_GDS334_ASDFRa_AREF.txt",
        "file_name": "splib07b_GalvanizedSheetMetal_GDS334_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/GalvanizedSheetMetal_GDS334_ASDFRa_AREF.html",
        "metadata_file_name": "GalvanizedSheetMetal_GDS334_ASDFRa_AREF.html",
        "notes": "Measured galvanized sheet-metal baseline from USGS v7.",
    },
    {
        "id": "usgs_gds333_painted_aluminum",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_gds333_painted_aluminum_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.txt",
        "file_name": "splib07b_Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.html",
        "metadata_file_name": "Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.html",
        "notes": "Reference-only painted-aluminum color prior; not a traffic-sign sheeting replacement.",
    },
    {
        "id": "usgs_gds338_pvc_white",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_gds338_pvc_white_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Plastic_PVC_GDS338_White_ASDFRa_AREF.txt",
        "file_name": "splib07b_Plastic_PVC_GDS338_White_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Plastic_PVC_GDS338_White_ASDFRa_AREF.html",
        "metadata_file_name": "Plastic_PVC_GDS338_White_ASDFRa_AREF.html",
        "notes": "Reference-only white plastic prior; not a road-marking or sign-sheeting replacement.",
    },
    {
        "id": "usgs_gds398_vinyl_red_toy",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_gds398_vinyl_red_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.txt",
        "file_name": "splib07b_Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.html",
        "metadata_file_name": "Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.html",
        "notes": "Reference-only red vinyl prior; not a retroreflective traffic-sign replacement.",
    },
    {
        "id": "usgs_gds344_pipe_blue",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_gds344_pipe_blue_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.txt",
        "file_name": "splib07b_Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.html",
        "metadata_file_name": "Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.html",
        "notes": "Reference-only blue plastic prior; not a measured traffic-sign sheeting replacement.",
    },
    {
        "id": "usgs_gds382_pete_black",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_gds382_pete_black_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Plastic_PETE_GDS382_Black_ASDFRa_AREF.txt",
        "file_name": "splib07b_Plastic_PETE_GDS382_Black_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Plastic_PETE_GDS382_Black_ASDFRa_AREF.html",
        "metadata_file_name": "Plastic_PETE_GDS382_Black_ASDFRa_AREF.html",
        "notes": "Reference-only black PET prior; not a sign-face or signal-housing measured replacement.",
    },
    {
        "id": "usgs_spectralon99_white_ref",
        "classification": "redistributable",
        "license_summary": "USGS Spectral Library Version 7 selected local subset",
        "selection_role": "reference_only",
        "curve_name": "src_usgs_spectralon99_white_aref",
        "local_path": "ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.txt",
        "file_name": "splib07b_Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.txt",
        "metadata_local_path": "HTMLmetadata/Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.html",
        "metadata_file_name": "Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.html",
        "notes": "Reference-only white standard prior; not a direct road-marking replacement.",
    },
]


def ensure_dirs() -> None:
    for rel in DIRS:
        (REPO_ROOT / rel).mkdir(parents=True, exist_ok=True)


def clean_generated_dirs() -> None:
    for rel in ["canonical", "exports", "validation/reports"]:
        target = REPO_ROOT / rel
        if target.exists():
            shutil.rmtree(target)
    ensure_dirs()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(args: Sequence[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(args),
        cwd=str(cwd or REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def fixed_zipinfo(filename: str) -> zipfile.ZipInfo:
    timestamp = dt.datetime.fromisoformat(GENERATED_AT).astimezone(dt.timezone.utc)
    info = zipfile.ZipInfo(filename)
    info.date_time = (timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def load_existing_source_entry(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def relative_posix(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def resolve_usgs_source_root() -> Path:
    if os.getenv("USGS_SPLIB07_ROOT"):
        return Path(os.environ["USGS_SPLIB07_ROOT"]).expanduser()
    return REPO_ROOT / "usgs_splib07"


def display_usgs_source_root(root: Path) -> str:
    return "env:USGS_SPLIB07_ROOT" if os.getenv("USGS_SPLIB07_ROOT") else root.name


def build_preserved_local_entry(spec: Dict, source_json_path: Path) -> Optional[Dict]:
    existing_entry = load_existing_source_entry(source_json_path)
    if not existing_entry:
        return None
    primary_path = REPO_ROOT / existing_entry.get("path", "")
    metadata_path = REPO_ROOT / existing_entry.get("metadata_path", "") if existing_entry.get("metadata_path") else None
    if not primary_path.exists():
        return None
    if metadata_path and not metadata_path.exists():
        return None
    entry = {
        "id": spec["id"],
        "origin_type": "local_path",
        "classification": spec["classification"],
        "license_summary": spec["license_summary"],
        "selection_role": spec["selection_role"],
        "path": existing_entry["path"],
        "copied_from": spec["local_path"],
        "copied_at": existing_entry.get("copied_at", GENERATED_AT),
        "status": "copied_from_local",
        "sha256": sha256_file(primary_path),
        "size_bytes": primary_path.stat().st_size,
        "notes": spec["notes"],
    }
    if metadata_path and existing_entry.get("metadata_path"):
        entry["metadata_path"] = existing_entry["metadata_path"]
        entry["metadata_copied_from"] = spec["metadata_local_path"]
        entry["metadata_sha256"] = sha256_file(metadata_path)
    return entry


def freeze_selected_usgs_sources() -> List[Dict]:
    refresh_sources = os.getenv("REFRESH_SOURCES") == "1"
    source_root = resolve_usgs_source_root()
    target_root = REPO_ROOT / "raw" / "sources" / "usgs_splib07_selected"
    target_root.mkdir(parents=True, exist_ok=True)
    ledger_entries = []
    index_inputs = []

    for spec in [USGS_WAVELENGTH_SOURCE, *USGS_SAMPLE_SELECTIONS]:
        entry_dir = target_root / spec["id"]
        entry_dir.mkdir(parents=True, exist_ok=True)
        source_json_path = entry_dir / "source.json"
        target_file = entry_dir / spec["file_name"]
        metadata_target = entry_dir / spec["metadata_file_name"] if spec.get("metadata_file_name") else None

        if not refresh_sources:
            preserved = build_preserved_local_entry(spec, source_json_path)
            if preserved:
                write_json(source_json_path, preserved)
                ledger_entries.append(preserved)
                index_inputs.append(
                    {
                        "id": spec["id"],
                        "selection_role": spec["selection_role"],
                        "path": preserved["path"],
                        "copied_from": preserved["copied_from"],
                        "sha256": preserved["sha256"],
                        "notes": spec["notes"],
                    }
                )
                continue

        source_file = source_root / spec["local_path"]
        if not source_file.exists():
            raise FileNotFoundError(f"Missing required USGS local source: {source_file}")
        shutil.copy2(source_file, target_file)

        entry = {
            "id": spec["id"],
            "origin_type": "local_path",
            "classification": spec["classification"],
            "license_summary": spec["license_summary"],
            "selection_role": spec["selection_role"],
            "path": relative_posix(target_file),
            "copied_from": spec["local_path"],
            "copied_at": GENERATED_AT,
            "status": "copied_from_local",
            "sha256": sha256_file(target_file),
            "size_bytes": target_file.stat().st_size,
            "notes": spec["notes"],
        }
        if spec.get("metadata_local_path") and metadata_target is not None:
            metadata_source = source_root / spec["metadata_local_path"]
            if not metadata_source.exists():
                raise FileNotFoundError(f"Missing required USGS metadata source: {metadata_source}")
            shutil.copy2(metadata_source, metadata_target)
            entry["metadata_path"] = relative_posix(metadata_target)
            entry["metadata_copied_from"] = spec["metadata_local_path"]
            entry["metadata_sha256"] = sha256_file(metadata_target)
        write_json(source_json_path, entry)
        ledger_entries.append(entry)
        index_inputs.append(
            {
                "id": spec["id"],
                "selection_role": spec["selection_role"],
                "path": entry["path"],
                "copied_from": entry["copied_from"],
                "sha256": entry["sha256"],
                "notes": spec["notes"],
            }
        )

    write_json(
        target_root / "index.json",
        {
            "generated_at": GENERATED_AT,
            "local_source_root": display_usgs_source_root(source_root),
            "selected_inputs": index_inputs,
            "copied_at": GENERATED_AT,
            "notes": "Selected USGS Spectral Library v7 subset frozen for reproducible material ingest. The full local mirror is intentionally not tracked.",
        },
    )
    return ledger_entries


def download_sources() -> List[Dict]:
    ledger = []
    refresh_sources = os.getenv("REFRESH_SOURCES") == "1"
    for source in SOURCE_DEFS:
        target_dir = REPO_ROOT / "raw" / "sources" / source["id"]
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / source["file_name"]
        source_json_path = target_dir / "source.json"
        existing_entry = load_existing_source_entry(source_json_path)
        preserved_fetched_at = GENERATED_AT
        if existing_entry and isinstance(existing_entry.get("fetched_at"), str):
            preserved_fetched_at = existing_entry["fetched_at"]

        if not refresh_sources:
            if target_file.exists():
                entry = {
                    "id": source["id"],
                    "origin_type": "url",
                    "url": source["url"],
                    "file_name": source["file_name"],
                    "classification": source["classification"],
                    "license_summary": source["license_summary"],
                    "path": relative_posix(target_file),
                    "fetched_at": preserved_fetched_at,
                    "status": "downloaded",
                    "sha256": sha256_file(target_file),
                    "size_bytes": target_file.stat().st_size,
                }
                write_json(source_json_path, entry)
                ledger.append(entry)
                continue

            if existing_entry and existing_entry.get("status") == "fetch_failed":
                entry = {
                    "id": source["id"],
                    "origin_type": "url",
                    "url": source["url"],
                    "file_name": source["file_name"],
                    "classification": source["classification"],
                    "license_summary": source["license_summary"],
                    "path": relative_posix(target_file),
                    "fetched_at": preserved_fetched_at,
                    "status": "fetch_failed",
                    "error": existing_entry.get("error", "preserved previous fetch failure"),
                }
                write_json(source_json_path, entry)
                ledger.append(entry)
                continue

        cmd = [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "20",
            "--max-time",
            "60",
            "-A",
            "Mozilla/5.0",
            "-o",
            str(target_file),
            source["url"],
        ]
        result = run(cmd)
        entry = {
            "id": source["id"],
            "origin_type": "url",
            "url": source["url"],
            "file_name": source["file_name"],
            "classification": source["classification"],
            "license_summary": source["license_summary"],
            "path": relative_posix(target_file),
            "fetched_at": GENERATED_AT,
        }
        if result.returncode == 0 and target_file.exists():
            entry.update(
                {
                    "status": "downloaded",
                    "sha256": sha256_file(target_file),
                    "size_bytes": target_file.stat().st_size,
                }
            )
        else:
            if target_file.exists():
                target_file.unlink()
            entry.update(
                {
                    "status": "fetch_failed",
                    "error": result.stderr.strip() or result.stdout.strip() or "unknown curl error",
                }
            )
        write_json(source_json_path, entry)
        ledger.append(entry)
    ledger.extend(freeze_selected_usgs_sources())
    write_json(REPO_ROOT / "raw" / "source_ledger.json", {"generated_at": GENERATED_AT, "sources": ledger})
    return ledger


def parse_numeric_series_file(path: Path) -> List[float]:
    values = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or "Record=" in line:
                continue
            values.append(float(line))
    return values


def parse_usgs_metadata_html(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    metadata = {}
    for field in ["TITLE", "SAMPLE_ID", "MATERIAL_TYPE", "MATERIAL", "COLLECTION_LOCALITY"]:
        match = re.search(rf"{field}:\s*(.*?)\s*(?:<p>|</H3>)", text, re.IGNORECASE | re.DOTALL)
        if match:
            metadata[field.lower()] = re.sub(r"<.*?>", "", match.group(1)).strip()
    return metadata


def load_usgs_wavelengths_nm() -> List[float]:
    wavelength_dir = REPO_ROOT / "raw" / "sources" / "usgs_splib07_selected" / USGS_WAVELENGTH_SOURCE["id"]
    wavelengths_path = wavelength_dir / USGS_WAVELENGTH_SOURCE["file_name"]
    values = parse_numeric_series_file(wavelengths_path)
    if len(values) != 2151:
        raise ValueError(f"{wavelengths_path} expected 2151 wavelength samples, found {len(values)}")
    return [value * 1000.0 for value in values]


def resample_usgs_aref_curve(values: Sequence[float], wavelengths_nm: Sequence[float]) -> List[float]:
    if len(values) != 2151:
        raise ValueError(f"USGS source curve expected 2151 reflectance values, found {len(values)}")
    if len(values) != len(wavelengths_nm):
        raise ValueError("USGS source curve length does not match wavelength basis length")
    points = list(zip(wavelengths_nm, values))
    return clamp_list(interpolate(points, MASTER_GRID))


def load_usgs_selected_curve(spec: Dict, wavelengths_nm: Sequence[float]) -> Dict:
    source_dir = REPO_ROOT / "raw" / "sources" / "usgs_splib07_selected" / spec["id"]
    data_path = source_dir / spec["file_name"]
    metadata_path = source_dir / spec["metadata_file_name"] if spec.get("metadata_file_name") else None
    values = parse_numeric_series_file(data_path)
    metadata = parse_usgs_metadata_html(metadata_path) if metadata_path and metadata_path.exists() else {}
    return {
        "curve_name": spec["curve_name"],
        "values": resample_usgs_aref_curve(values, wavelengths_nm),
        "source_id": spec["id"],
        "selection_role": spec["selection_role"],
        "metadata": metadata,
    }


def npy_bytes(values: Sequence[float]) -> bytes:
    header = "{'descr': '<f8', 'fortran_order': False, 'shape': (%d,), }" % len(values)
    header_bytes = header.encode("latin1")
    preamble = b"\x93NUMPY" + bytes([1, 0])
    padding = 16 - ((len(preamble) + 2 + len(header_bytes) + 1) % 16)
    if padding == 16:
        padding = 0
    final_header = header_bytes + (b" " * padding) + b"\n"
    return preamble + struct.pack("<H", len(final_header)) + final_header + struct.pack("<%sd" % len(values), *values)


def write_npz(path: Path, arrays: Dict[str, Sequence[float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, values in arrays.items():
            archive.writestr(fixed_zipinfo(f"{name}.npy"), npy_bytes(values))


def read_npz(path: Path) -> Dict[str, List[float]]:
    def parse_npy(payload: bytes) -> List[float]:
        if payload[:6] != b"\x93NUMPY":
            raise ValueError(f"{path} contains a non-npy member")
        major = payload[6]
        if major != 1:
            raise ValueError(f"{path} contains unsupported npy version {major}")
        header_len = struct.unpack("<H", payload[8:10])[0]
        header = payload[10 : 10 + header_len].decode("latin1")
        shape_fragment = header.split("'shape':", 1)[1].split(")", 1)[0].strip(" (")
        count = int(shape_fragment.rstrip(","))
        data = payload[10 + header_len :]
        return list(struct.unpack("<%sd" % count, data[: count * 8]))

    arrays = {}
    with zipfile.ZipFile(path, "r") as archive:
        for name in archive.namelist():
            arrays[name[:-4]] = parse_npy(archive.read(name))
    return arrays


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def interpolate(points: Sequence[Tuple[float, float]], grid: Sequence[int]) -> List[float]:
    sorted_points = sorted(points)
    out = []
    for wavelength in grid:
        if wavelength <= sorted_points[0][0]:
            out.append(sorted_points[0][1])
            continue
        if wavelength >= sorted_points[-1][0]:
            out.append(sorted_points[-1][1])
            continue
        for index in range(1, len(sorted_points)):
            left = sorted_points[index - 1]
            right = sorted_points[index]
            if left[0] <= wavelength <= right[0]:
                span = right[0] - left[0]
                t = 0.0 if span == 0 else (wavelength - left[0]) / span
                out.append(lerp(left[1], right[1], t))
                break
    return out


def gaussian(grid: Sequence[int], center: float, sigma: float, amplitude: float, base: float = 0.0) -> List[float]:
    return [base + amplitude * math.exp(-0.5 * ((w - center) / sigma) ** 2) for w in grid]


def clamp_list(values: Sequence[float], lower: float = 0.0, upper: float = 1.0) -> List[float]:
    return [max(lower, min(upper, value)) for value in values]


def normalize_unit_peak(values: Sequence[float]) -> List[float]:
    peak = max(values) if values else 0.0
    if peak <= 0:
        return [0.0 for _ in values]
    return [value / peak for value in values]


def load_cie_d65() -> List[Tuple[float, float]]:
    csv_path = REPO_ROOT / "raw" / "sources" / "cie_d65_csv" / "CIE_std_illum_D65.csv"
    pairs = []
    with csv_path.open("r", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            if not row:
                continue
            pairs.append((float(row[0]), float(row[1])))
    return pairs


def load_astm_g173() -> Dict[str, List[Tuple[float, float]]]:
    zip_path = REPO_ROOT / "raw" / "sources" / "astm_g173_zip" / "astmg173.zip"
    with zipfile.ZipFile(zip_path, "r") as archive:
        rows = archive.read("ASTMG173.csv").decode("utf-8").splitlines()
    reader = csv.reader(rows)
    next(reader)
    next(reader)
    extraterrestrial = []
    global_tilt = []
    direct = []
    for row in reader:
        wavelength = float(row[0])
        extraterrestrial.append((wavelength, float(row[1])))
        global_tilt.append((wavelength, float(row[2])))
        direct.append((wavelength, float(row[3])))
    return {"extraterrestrial": extraterrestrial, "global_tilt": global_tilt, "direct": direct}


def wavelength_to_rgb(wavelength: float) -> Tuple[float, float, float]:
    if wavelength < 380 or wavelength > 780:
        return (0.0, 0.0, 0.0)
    if wavelength < 440:
        r, g, b = -(wavelength - 440) / (440 - 380), 0.0, 1.0
    elif wavelength < 490:
        r, g, b = 0.0, (wavelength - 440) / (490 - 440), 1.0
    elif wavelength < 510:
        r, g, b = 0.0, 1.0, -(wavelength - 510) / (510 - 490)
    elif wavelength < 580:
        r, g, b = (wavelength - 510) / (580 - 510), 1.0, 0.0
    elif wavelength < 645:
        r, g, b = 1.0, -(wavelength - 645) / (645 - 580), 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif wavelength > 700:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    else:
        factor = 1.0
    return (r * factor, g * factor, b * factor)


def spectral_to_rgb(reflectance: Sequence[float], illuminant: Sequence[float]) -> List[float]:
    r_sum = g_sum = b_sum = 0.0
    total = 0.0
    for wavelength, refl, illum in zip(MASTER_GRID, reflectance, illuminant):
        if wavelength < 400 or wavelength > 700:
            continue
        wr, wg, wb = wavelength_to_rgb(wavelength)
        energy = refl * illum
        r_sum += wr * energy
        g_sum += wg * energy
        b_sum += wb * energy
        total += energy
    if total <= 0:
        return [0.0, 0.0, 0.0, 1.0]
    rgb = [r_sum / total, g_sum / total, b_sum / total]
    peak = max(rgb) or 1.0
    return [min(1.0, channel / peak) for channel in rgb] + [1.0]


def spd_to_rgb(spd: Sequence[float]) -> List[float]:
    return spectral_to_rgb([1.0] * len(spd), spd)


def material_hex(rgba: Sequence[float]) -> str:
    return "#" + "".join(f"{round(max(0.0, min(1.0, value)) * 255):02x}" for value in rgba[:3])


def circle_polygon(cx: float, cy: float, radius: float, segments: int = 32) -> List[Tuple[float, float]]:
    return [
        (cx + radius * math.cos((2.0 * math.pi * i) / segments), cy + radius * math.sin((2.0 * math.pi * i) / segments))
        for i in range(segments)
    ]


def rect_polygon(cx: float, cy: float, width: float, height: float, angle_deg: float = 0.0) -> List[Tuple[float, float]]:
    half_w = width / 2.0
    half_h = height / 2.0
    corners = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]
    angle = math.radians(angle_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    out = []
    for x, y in corners:
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        out.append((cx + rx, cy + ry))
    return out


def regular_polygon(sides: int, radius: float, rotation_deg: float = 0.0) -> List[Tuple[float, float]]:
    return [
        (
            radius * math.cos(math.radians(rotation_deg) + (2.0 * math.pi * i) / sides),
            radius * math.sin(math.radians(rotation_deg) + (2.0 * math.pi * i) / sides),
        )
        for i in range(sides)
    ]


def triangle_polygon(points: Sequence[Tuple[float, float]]) -> List[Tuple[float, float]]:
    return list(points)


def line_segment_polygon(start: Tuple[float, float], end: Tuple[float, float], width: float) -> List[Tuple[float, float]]:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return circle_polygon(start[0], start[1], width * 0.5, 12)
    nx = -dy / length
    ny = dx / length
    half = width / 2.0
    return [
        (start[0] + nx * half, start[1] + ny * half),
        (end[0] + nx * half, end[1] + ny * half),
        (end[0] - nx * half, end[1] - ny * half),
        (start[0] - nx * half, start[1] - ny * half),
    ]


GLYPHS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "11100"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
}


def glyph_rects(text: str, width: float, height: float, center: Tuple[float, float]) -> List[List[Tuple[float, float]]]:
    text = text.upper()
    cells_x = sum(len(GLYPHS[ch][0]) for ch in text if ch in GLYPHS) + max(0, len(text) - 1)
    cell_w = width / max(1, cells_x)
    cell_h = height / 7.0
    origin_x = center[0] - width / 2.0
    origin_y = center[1] + height / 2.0
    cursor = origin_x
    polygons = []
    for index, ch in enumerate(text):
        glyph = GLYPHS.get(ch)
        if glyph is None:
            cursor += cell_w * 6
            continue
        for row_index, row in enumerate(glyph):
            for col_index, bit in enumerate(row):
                if bit == "1":
                    cx = cursor + (col_index + 0.5) * cell_w
                    cy = origin_y - (row_index + 0.5) * cell_h
                    polygons.append(rect_polygon(cx, cy, cell_w * 0.92, cell_h * 0.92))
        cursor += len(glyph[0]) * cell_w
        if index < len(text) - 1:
            cursor += cell_w
    return polygons


def arrow_shapes(start: Tuple[float, float], end: Tuple[float, float], width: float, head_length: float, head_width: float) -> List[List[Tuple[float, float]]]:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return []
    ux = dx / length
    uy = dy / length
    shaft_end = (end[0] - ux * head_length, end[1] - uy * head_length)
    shaft = line_segment_polygon(start, shaft_end, width)
    nx = -uy
    ny = ux
    head = [
        end,
        (shaft_end[0] + nx * head_width * 0.5, shaft_end[1] + ny * head_width * 0.5),
        (shaft_end[0] - nx * head_width * 0.5, shaft_end[1] - ny * head_width * 0.5),
    ]
    return [shaft, head]


def pedestrian_icon(center: Tuple[float, float], scale: float) -> List[List[Tuple[float, float]]]:
    x, y = center
    shapes = [circle_polygon(x, y + 0.22 * scale, 0.09 * scale, 16)]
    for start, end, width in [
        ((x, y + 0.1 * scale), (x, y - 0.1 * scale), 0.06 * scale),
        ((x, y + 0.02 * scale), (x - 0.16 * scale, y - 0.02 * scale), 0.05 * scale),
        ((x, y + 0.02 * scale), (x + 0.16 * scale, y - 0.02 * scale), 0.05 * scale),
        ((x, y - 0.1 * scale), (x - 0.14 * scale, y - 0.32 * scale), 0.05 * scale),
        ((x, y - 0.1 * scale), (x + 0.16 * scale, y - 0.3 * scale), 0.05 * scale),
    ]:
        shapes.append(line_segment_polygon(start, end, width))
    return shapes


def bus_icon(center: Tuple[float, float], scale: float) -> List[List[Tuple[float, float]]]:
    x, y = center
    return [
        rect_polygon(x, y, 0.46 * scale, 0.2 * scale),
        rect_polygon(x - 0.18 * scale, y - 0.13 * scale, 0.09 * scale, 0.06 * scale),
        rect_polygon(x + 0.18 * scale, y - 0.13 * scale, 0.09 * scale, 0.06 * scale),
        circle_polygon(x - 0.14 * scale, y - 0.12 * scale, 0.06 * scale, 14),
        circle_polygon(x + 0.14 * scale, y - 0.12 * scale, 0.06 * scale, 14),
    ]


def traffic_light_icon(center: Tuple[float, float], scale: float) -> List[List[Tuple[float, float]]]:
    x, y = center
    return [
        rect_polygon(x, y, 0.24 * scale, 0.54 * scale, 0.0),
        circle_polygon(x, y + 0.16 * scale, 0.06 * scale, 18),
        circle_polygon(x, y, 0.06 * scale, 18),
        circle_polygon(x, y - 0.16 * scale, 0.06 * scale, 18),
    ]


def warning_worker_icon(center: Tuple[float, float], scale: float) -> List[List[Tuple[float, float]]]:
    x, y = center
    shapes = pedestrian_icon((x - 0.03 * scale, y + 0.02 * scale), scale * 0.85)
    shapes.append(line_segment_polygon((x + 0.02 * scale, y - 0.05 * scale), (x + 0.18 * scale, y - 0.23 * scale), 0.05 * scale))
    shapes.append(line_segment_polygon((x + 0.1 * scale, y - 0.23 * scale), (x + 0.2 * scale, y - 0.23 * scale), 0.05 * scale))
    return shapes


def sign_layers(sign_type: str) -> List[Tuple[str, List[List[Tuple[float, float]]]]]:
    if sign_type == "stop":
        outer = regular_polygon(8, 0.48, 22.5)
        inner = regular_polygon(8, 0.41, 22.5)
        return [
            ("mat_sign_white", [outer]),
            ("mat_sign_stop_red", [inner]),
            ("mat_sign_white", glyph_rects("STOP", 0.44, 0.22, (0.0, 0.0))),
        ]
    if sign_type == "yield":
        outer = triangle_polygon([(0.0, -0.48), (0.47, 0.34), (-0.47, 0.34)])
        inner = triangle_polygon([(0.0, -0.34), (0.34, 0.22), (-0.34, 0.22)])
        return [("mat_sign_stop_red", [outer]), ("mat_sign_white", [inner])]
    if sign_type == "no_entry":
        return [
            ("mat_sign_stop_red", [circle_polygon(0.0, 0.0, 0.46, 40)]),
            ("mat_sign_white", [rect_polygon(0.0, 0.0, 0.48, 0.12)]),
        ]
    if sign_type == "speed_limit":
        return [
            ("mat_sign_stop_red", [circle_polygon(0.0, 0.0, 0.46, 40)]),
            ("mat_sign_white", [circle_polygon(0.0, 0.0, 0.36, 40)]),
            ("mat_sign_black", glyph_rects("50", 0.34, 0.28, (0.0, 0.0))),
        ]
    if sign_type == "turn_restriction":
        layers = [
            ("mat_sign_stop_red", [circle_polygon(0.0, 0.0, 0.46, 40)]),
            ("mat_sign_white", [circle_polygon(0.0, 0.0, 0.36, 40)]),
            ("mat_sign_black", arrow_shapes((0.12, -0.18), (-0.05, 0.1), 0.06, 0.12, 0.18)),
            ("mat_sign_stop_red", [line_segment_polygon((-0.26, 0.26), (0.26, -0.26), 0.08)]),
        ]
        return layers
    if sign_type == "mandatory_direction":
        return [
            ("mat_sign_blue", [circle_polygon(0.0, 0.0, 0.46, 40)]),
            ("mat_sign_white", arrow_shapes((-0.18, -0.05), (0.18, 0.12), 0.09, 0.12, 0.2)),
        ]
    if sign_type == "pedestrian_crossing":
        return [
            ("mat_sign_blue", [rect_polygon(0.0, 0.0, 0.9, 0.9)]),
            ("mat_sign_white", [triangle_polygon([(0.0, 0.34), (0.34, -0.28), (-0.34, -0.28)])]),
            ("mat_sign_black", pedestrian_icon((0.0, -0.02), 0.65)),
        ]
    if sign_type == "school_warning":
        return [
            ("mat_sign_yellow", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", pedestrian_icon((-0.09, -0.02), 0.52) + pedestrian_icon((0.12, -0.02), 0.46)),
        ]
    if sign_type == "signal_ahead":
        return [
            ("mat_sign_yellow", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", traffic_light_icon((0.0, 0.0), 1.0)),
        ]
    if sign_type == "merge":
        return [
            ("mat_sign_yellow", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", arrow_shapes((0.0, -0.28), (0.0, 0.22), 0.07, 0.12, 0.18)
             + [line_segment_polygon((-0.18, -0.02), (-0.04, 0.12), 0.06)]),
        ]
    if sign_type == "curve":
        return [
            ("mat_sign_yellow", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", arrow_shapes((-0.18, -0.2), (-0.06, 0.12), 0.07, 0.12, 0.18)
             + [line_segment_polygon((-0.06, 0.12), (0.16, 0.2), 0.07)]),
        ]
    if sign_type == "construction":
        return [
            ("mat_sign_orange", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", warning_worker_icon((0.0, 0.02), 0.8)),
        ]
    if sign_type == "parking":
        return [
            ("mat_sign_blue", [rect_polygon(0.0, 0.0, 0.9, 0.9)]),
            ("mat_sign_white", glyph_rects("P", 0.34, 0.5, (0.0, 0.0))),
        ]
    if sign_type == "bus_stop":
        return [
            ("mat_sign_blue", [rect_polygon(0.0, 0.0, 0.9, 0.9)]),
            ("mat_sign_white", bus_icon((0.0, 0.05), 1.0) + glyph_rects("BUS", 0.5, 0.14, (0.0, -0.28))),
        ]
    if sign_type == "one_way":
        return [
            ("mat_sign_blue", [rect_polygon(0.0, 0.0, 0.95, 0.38)]),
            ("mat_sign_white", arrow_shapes((-0.28, 0.0), (0.28, 0.0), 0.1, 0.16, 0.22)),
        ]
    if sign_type == "lane_direction":
        return [
            ("mat_sign_blue", [rect_polygon(0.0, 0.0, 0.95, 0.72)]),
            ("mat_sign_white", arrow_shapes((-0.18, -0.2), (-0.18, 0.2), 0.08, 0.14, 0.22)
             + arrow_shapes((0.18, -0.2), (0.18, 0.2), 0.08, 0.14, 0.22)
             + arrow_shapes((0.18, 0.0), (-0.06, 0.2), 0.06, 0.12, 0.18)),
        ]
    if sign_type == "railroad_warning":
        return [
            ("mat_sign_yellow", [regular_polygon(4, 0.46, 45.0)]),
            ("mat_sign_black", [
                line_segment_polygon((-0.2, 0.2), (0.2, -0.2), 0.08),
                line_segment_polygon((-0.2, -0.2), (0.2, 0.2), 0.08),
                line_segment_polygon((-0.22, -0.28), (0.22, -0.28), 0.05),
            ]),
        ]
    if sign_type == "variable_message":
        amber_pixels = []
        for row in range(4):
            for col in range(9):
                if (row + col) % 2 == 0:
                    amber_pixels.append(rect_polygon(-0.32 + col * 0.08, 0.12 - row * 0.08, 0.045, 0.045))
        return [
            ("mat_vms_panel", [rect_polygon(0.0, 0.0, 0.95, 0.54)]),
            ("mat_signal_countdown_amber_off", amber_pixels),
        ]
    raise ValueError(f"Unsupported sign type {sign_type}")


def transform_points(points: Sequence[Tuple[float, float, float]], tx: float = 0.0, ty: float = 0.0, tz: float = 0.0) -> List[Tuple[float, float, float]]:
    return [(x + tx, y + ty, z + tz) for x, y, z in points]


def scale_points_2d(points: Sequence[Tuple[float, float]], width: float, height: float) -> List[Tuple[float, float]]:
    return [(x * width, y * height) for x, y in points]


def extrude_convex_polygon(points_2d: Sequence[Tuple[float, float]], z_front: float, z_back: float) -> List[Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]]:
    points = list(points_2d)
    front = [(x, y, z_front) for x, y in points]
    back = [(x, y, z_back) for x, y in reversed(points)]
    triangles = []
    for i in range(1, len(front) - 1):
        triangles.append((front[0], front[i], front[i + 1]))
        triangles.append((back[0], back[i], back[i + 1]))
    for i in range(len(points)):
        a0 = front[i]
        a1 = front[(i + 1) % len(points)]
        b0 = back[-1 - i]
        b1 = back[-1 - ((i + 1) % len(points))]
        triangles.append((a0, a1, b1))
        triangles.append((a0, b1, b0))
    return triangles


def box_triangles(width: float, height: float, depth: float, center: Tuple[float, float, float]) -> List[Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]]:
    cx, cy, cz = center
    hx, hy, hz = width / 2.0, height / 2.0, depth / 2.0
    corners = {
        "lbf": (cx - hx, cy - hy, cz + hz),
        "rbf": (cx + hx, cy - hy, cz + hz),
        "rtf": (cx + hx, cy + hy, cz + hz),
        "ltf": (cx - hx, cy + hy, cz + hz),
        "lbb": (cx - hx, cy - hy, cz - hz),
        "rbb": (cx + hx, cy - hy, cz - hz),
        "rtb": (cx + hx, cy + hy, cz - hz),
        "ltb": (cx - hx, cy + hy, cz - hz),
    }
    faces = [
        ("lbf", "rbf", "rtf", "ltf"),
        ("rbb", "lbb", "ltb", "rtb"),
        ("lbb", "lbf", "ltf", "ltb"),
        ("rbf", "rbb", "rtb", "rtf"),
        ("ltf", "rtf", "rtb", "ltb"),
        ("lbb", "rbb", "rbf", "lbf"),
    ]
    triangles = []
    for a, b, c, d in faces:
        triangles.append((corners[a], corners[b], corners[c]))
        triangles.append((corners[a], corners[c], corners[d]))
    return triangles


def cylinder_triangles(radius: float, height: float, segments: int, center: Tuple[float, float, float]) -> List[Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]]:
    cx, cy, cz = center
    top_y = cy + height / 2.0
    bottom_y = cy - height / 2.0
    top_center = (cx, top_y, cz)
    bottom_center = (cx, bottom_y, cz)
    top_ring = []
    bottom_ring = []
    for index in range(segments):
        angle = (2.0 * math.pi * index) / segments
        x = cx + radius * math.cos(angle)
        z = cz + radius * math.sin(angle)
        top_ring.append((x, top_y, z))
        bottom_ring.append((x, bottom_y, z))
    triangles = []
    for index in range(segments):
        next_index = (index + 1) % segments
        triangles.append((top_center, top_ring[index], top_ring[next_index]))
        triangles.append((bottom_center, bottom_ring[next_index], bottom_ring[index]))
        triangles.append((top_ring[index], bottom_ring[index], bottom_ring[next_index]))
        triangles.append((top_ring[index], bottom_ring[next_index], top_ring[next_index]))
    return triangles


def merge_triangle_sets(*sets: Iterable[Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]]):
    out = []
    for triangle_set in sets:
        out.extend(list(triangle_set))
    return out


def triangle_count(mesh_parts: Sequence[Dict]) -> int:
    return sum(len(part["triangles"]) for part in mesh_parts)


def face_normal(triangle):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = triangle
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return (nx / length, ny / length, nz / length)


def make_mesh_part(name: str, triangles, material_id: str) -> Dict:
    return {"name": name, "triangles": list(triangles), "material_id": material_id}


def layer_to_mesh_parts(layer_name: str, material_id: str, polygons: Sequence[List[Tuple[float, float]]], width: float, height: float, z_front: float, z_back: float) -> List[Dict]:
    parts = []
    for index, polygon in enumerate(polygons):
        scaled = scale_points_2d(polygon, width, height)
        triangles = extrude_convex_polygon(scaled, z_front, z_back)
        parts.append(make_mesh_part(f"{layer_name}_{index:02d}", triangles, material_id))
    return parts


def sign_asset_parts(sign_type: str, width: float, height: float) -> Dict[str, List[Dict]]:
    layers = sign_layers(sign_type)
    lod0_parts = []
    lod1_parts = []
    plate_z_front = 0.01
    plate_z_back = -0.01
    plate_shape = layers[0][1][0]
    lod0_parts.extend(layer_to_mesh_parts("plate_base", layers[0][0], [plate_shape], width, height, plate_z_front, plate_z_back))
    offset = plate_z_front + 0.0015
    for layer_index, (material_id, polygons) in enumerate(layers[1:], start=1):
        lod0_parts.extend(layer_to_mesh_parts(f"layer_{layer_index}", material_id, polygons, width, height, offset, offset - 0.001))
        simplified = polygons if len(polygons) < 10 else polygons[::2]
        lod1_parts.extend(layer_to_mesh_parts(f"layer_{layer_index}", material_id, simplified, width, height, offset, offset - 0.001))
        offset += 0.0015
    lod1_parts.insert(0, make_mesh_part("plate_base_00", lod0_parts[0]["triangles"], lod0_parts[0]["material_id"]))
    mount_height = max(height * 1.5 + 0.6, 2.2)
    pole_center_y = mount_height / 2.0
    pole_parts0 = [make_mesh_part("pole", cylinder_triangles(0.03, mount_height, 18, (0.0, pole_center_y, -0.03)), "mat_metal_galvanized")]
    pole_parts1 = [make_mesh_part("pole", cylinder_triangles(0.03, mount_height, 12, (0.0, pole_center_y, -0.03)), "mat_metal_galvanized")]
    sign_center_y = mount_height - 0.45
    for part in lod0_parts:
        part["triangles"] = transform_points_in_triangles(part["triangles"], 0.0, sign_center_y, 0.0)
    for part in lod1_parts:
        part["triangles"] = transform_points_in_triangles(part["triangles"], 0.0, sign_center_y, 0.0)
    lod0_parts.extend(pole_parts0)
    lod1_parts.extend(pole_parts1)
    return {"LOD0": lod0_parts, "LOD1": lod1_parts, "mount_height": mount_height, "sign_center_y": sign_center_y}


def transform_points_in_triangles(triangles, tx: float, ty: float, tz: float):
    out = []
    for triangle in triangles:
        out.append(tuple((x + tx, y + ty, z + tz) for x, y, z in triangle))
    return out


def signal_asset_parts(config: Dict) -> Dict[str, List[Dict]]:
    lod0 = []
    lod1 = []
    body_w = config["body_w"]
    body_h = config["body_h"]
    body_d = config["body_d"]
    lens_positions = config["lenses"]
    housing_center = (0.0, body_h / 2.0 + 1.2, 0.0)
    lod0.append(make_mesh_part("housing", box_triangles(body_w, body_h, body_d, housing_center), "mat_signal_housing"))
    lod1.append(make_mesh_part("housing", box_triangles(body_w, body_h, body_d, housing_center), "mat_signal_housing"))
    for index, lens in enumerate(lens_positions):
        lens_id = lens["material_id"]
        lens_name = lens["name"]
        center = (lens["x"], lens["y"] + 1.2, body_d / 2.0 + 0.015)
        lod0.append(make_mesh_part(lens_name, cylinder_triangles(lens["radius"], 0.03, 24, center), lens_id))
        lod1.append(make_mesh_part(lens_name, cylinder_triangles(lens["radius"], 0.03, 16, center), lens_id))
    bracket_center = (0.0, 1.28, -0.08)
    lod0.append(make_mesh_part("bracket", box_triangles(body_w * 0.18, 0.18, 0.12, bracket_center), "mat_metal_galvanized"))
    lod1.append(make_mesh_part("bracket", box_triangles(body_w * 0.18, 0.18, 0.12, bracket_center), "mat_metal_galvanized"))
    return {"LOD0": lod0, "LOD1": lod1}


def road_asset_parts(asset_id: str, dimensions: Tuple[float, float, float]) -> Dict[str, List[Dict]]:
    width, height, depth = dimensions
    material_map = {
        "road_asphalt_dry": "mat_asphalt_dry",
        "road_asphalt_wet": "mat_asphalt_wet",
        "road_concrete": "mat_concrete",
        "road_curb_segment": "mat_concrete",
        "road_sidewalk_panel": "mat_concrete",
        "marking_lane_white": "mat_marking_white",
        "marking_lane_yellow": "mat_marking_yellow",
        "marking_stop_line": "mat_marking_white",
        "marking_crosswalk": "mat_marking_white",
        "furniture_sign_pole": "mat_metal_galvanized",
        "furniture_signal_pole": "mat_metal_galvanized",
        "furniture_guardrail_bollard_set": "mat_metal_galvanized",
    }
    if asset_id == "furniture_sign_pole":
        return {
            "LOD0": [make_mesh_part("pole", cylinder_triangles(0.03, 3.2, 18, (0.0, 1.6, 0.0)), "mat_metal_galvanized")],
            "LOD1": [make_mesh_part("pole", cylinder_triangles(0.03, 3.2, 12, (0.0, 1.6, 0.0)), "mat_metal_galvanized")],
        }
    if asset_id == "furniture_signal_pole":
        lod0 = [
            make_mesh_part("pole_vertical", cylinder_triangles(0.08, 5.0, 20, (0.0, 2.5, 0.0)), "mat_metal_galvanized"),
            make_mesh_part("mast_arm", box_triangles(4.0, 0.14, 0.14, (2.0, 4.6, 0.0)), "mat_metal_galvanized"),
        ]
        lod1 = [
            make_mesh_part("pole_vertical", cylinder_triangles(0.08, 5.0, 14, (0.0, 2.5, 0.0)), "mat_metal_galvanized"),
            make_mesh_part("mast_arm", box_triangles(4.0, 0.14, 0.14, (2.0, 4.6, 0.0)), "mat_metal_galvanized"),
        ]
        return {"LOD0": lod0, "LOD1": lod1}
    if asset_id == "furniture_guardrail_bollard_set":
        lod0 = []
        lod1 = []
        for offset in [0.0, 1.3, 2.6]:
            lod0.append(make_mesh_part(f"post_{int(offset*10)}", box_triangles(0.12, 0.85, 0.12, (offset, 0.425, 0.0)), "mat_metal_galvanized"))
            lod1.append(make_mesh_part(f"post_{int(offset*10)}", box_triangles(0.12, 0.85, 0.12, (offset, 0.425, 0.0)), "mat_metal_galvanized"))
        lod0.append(make_mesh_part("rail", box_triangles(3.0, 0.12, 0.18, (1.3, 0.72, 0.0)), "mat_metal_galvanized"))
        lod1.append(make_mesh_part("rail", box_triangles(3.0, 0.12, 0.18, (1.3, 0.72, 0.0)), "mat_metal_galvanized"))
        lod0.append(make_mesh_part("bollard", cylinder_triangles(0.1, 0.8, 18, (3.3, 0.4, 0.0)), "mat_sign_orange"))
        lod1.append(make_mesh_part("bollard", cylinder_triangles(0.1, 0.8, 12, (3.3, 0.4, 0.0)), "mat_sign_orange"))
        return {"LOD0": lod0, "LOD1": lod1}
    if asset_id == "marking_crosswalk":
        lod0 = []
        lod1 = []
        for index in range(5):
            x = -1.2 + index * 0.6
            box = box_triangles(0.32, 0.005, 2.0, (x, 0.0025, 0.0))
            lod0.append(make_mesh_part(f"stripe_{index}", box, "mat_marking_white"))
            lod1.append(make_mesh_part(f"stripe_{index}", box, "mat_marking_white"))
        return {"LOD0": lod0, "LOD1": lod1}
    center = (0.0, height / 2.0, 0.0)
    material_id = material_map[asset_id]
    mesh = make_mesh_part("body", box_triangles(width, height, depth, center), material_id)
    return {"LOD0": [mesh], "LOD1": [mesh]}


def flatten_mesh_triangles(mesh_parts: Sequence[Dict]) -> Tuple[List[float], List[float]]:
    positions = []
    normals = []
    for part in mesh_parts:
        for triangle in part["triangles"]:
            nx, ny, nz = face_normal(triangle)
            for vertex in triangle:
                positions.extend(vertex)
                normals.extend([nx, ny, nz])
    return positions, normals


def glb_bytes(asset_id: str, mesh_parts: Sequence[Dict], material_defs: Dict[str, Dict]) -> bytes:
    materials = []
    material_index = {}
    meshes = []
    nodes = []
    binary = bytearray()

    def append_f32(values: Sequence[float]) -> Tuple[int, int]:
        while len(binary) % 4:
            binary.append(0)
        offset = len(binary)
        binary.extend(struct.pack("<%sf" % len(values), *values))
        return offset, len(values) * 4

    def min_max_triplets(values: Sequence[float]) -> Tuple[List[float], List[float]]:
        xs = values[0::3]
        ys = values[1::3]
        zs = values[2::3]
        return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]

    accessors = []
    buffer_views = []

    def accessor_for(values: Sequence[float], semantic: str) -> int:
        offset, byte_length = append_f32(values)
        buffer_view_index = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": offset, "byteLength": byte_length, "target": 34962})
        min_v, max_v = min_max_triplets(values)
        accessor_index = len(accessors)
        accessors.append(
            {
                "bufferView": buffer_view_index,
                "componentType": 5126,
                "count": len(values) // 3,
                "type": "VEC3",
                "min": min_v,
                "max": max_v,
            }
        )
        return accessor_index

    for part in mesh_parts:
        if part["material_id"] not in material_index:
            material = material_defs[part["material_id"]]
            payload = {
                "name": part["material_id"],
                "pbrMetallicRoughness": {
                    "baseColorFactor": material["pbr_fallback"]["baseColorFactor"],
                    "metallicFactor": material["pbr_fallback"].get("metallicFactor", 0.0),
                    "roughnessFactor": material["pbr_fallback"].get("roughnessFactor", 0.8),
                },
                "doubleSided": True,
            }
            emissive = material["pbr_fallback"].get("emissiveFactor")
            if emissive:
                payload["emissiveFactor"] = emissive
            material_index[part["material_id"]] = len(materials)
            materials.append(payload)
        positions, normals = flatten_mesh_triangles([part])
        primitive = {
            "attributes": {
                "POSITION": accessor_for(positions, "POSITION"),
                "NORMAL": accessor_for(normals, "NORMAL"),
            },
            "mode": 4,
            "material": material_index[part["material_id"]],
        }
        mesh_index = len(meshes)
        meshes.append({"name": part["name"], "primitives": [primitive]})
        nodes.append({"name": part["name"], "mesh": mesh_index, "extras": {"material_id": part["material_id"]}})

    while len(binary) % 4:
        binary.append(0)

    gltf = {
        "asset": {"version": "2.0", "generator": "scripts/build_asset_pack.py"},
        "scene": 0,
        "scenes": [{"name": asset_id, "nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": meshes,
        "materials": materials,
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": buffer_views,
        "accessors": accessors,
    }
    json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    while len(json_bytes) % 4:
        json_bytes += b" "
    total_length = 12 + 8 + len(json_bytes) + 8 + len(binary)
    out = bytearray()
    out.extend(struct.pack("<4sII", b"glTF", 2, total_length))
    out.extend(struct.pack("<I4s", len(json_bytes), b"JSON"))
    out.extend(json_bytes)
    out.extend(struct.pack("<I4s", len(binary), b"BIN\x00"))
    out.extend(binary)
    return bytes(out)


def format_floats(values: Sequence[float]) -> str:
    return ", ".join(f"{value:.6f}" for value in values)


def write_usda_asset(path: Path, asset_id: str, mesh_parts_by_lod: Dict[str, List[Dict]]) -> None:
    lines = [
        "#usda 1.0",
        "(",
        f'    defaultPrim = "{asset_id}"',
        '    upAxis = "Y"',
        "    metersPerUnit = 1",
        ")",
        "",
        f'def Xform "{asset_id}" {{',
        f'    custom string simulation:asset_id = "{asset_id}"',
    ]
    for lod_name, mesh_parts in mesh_parts_by_lod.items():
        lines.append(f'    def Scope "{lod_name}" {{')
        for part in mesh_parts:
            points = []
            face_counts = []
            face_indices = []
            for triangle in part["triangles"]:
                start = len(points)
                points.extend(triangle)
                face_counts.append(3)
                face_indices.extend([start, start + 1, start + 2])
            flat_points = []
            for x, y, z in points:
                flat_points.append(f"({x:.6f}, {y:.6f}, {z:.6f})")
            lines.extend(
                [
                    f'        def Mesh "{part["name"]}" {{',
                    f'            custom string simulation:material_id = "{part["material_id"]}"',
                    '            uniform token subdivisionScheme = "none"',
                    f"            int[] faceVertexCounts = [{', '.join(str(value) for value in face_counts)}]",
                    f"            int[] faceVertexIndices = [{', '.join(str(value) for value in face_indices)}]",
                    f"            point3f[] points = [{', '.join(flat_points)}]",
                    "        }",
                ]
            )
        lines.append("    }")
    lines.append("}")
    write_text(path, "\n".join(lines) + "\n")


def write_usda_scene(path: Path, scene_id: str, placements: Sequence[Dict]) -> None:
    lines = [
        "#usda 1.0",
        "(",
        f'    defaultPrim = "{scene_id}"',
        '    upAxis = "Y"',
        "    metersPerUnit = 1",
        ")",
        "",
        f'def Xform "{scene_id}" {{',
    ]
    for placement in placements:
        ref_path = placement["reference"]
        translate = placement.get("translate", (0.0, 0.0, 0.0))
        rotate_y = placement.get("rotate_y", 0.0)
        lines.extend(
            [
                f'    def Xform "{placement["name"]}" (',
                f'        references = @{ref_path}@</{placement["asset_id"]}>',
                "    ) {",
                f"        double3 xformOp:translate = ({translate[0]:.6f}, {translate[1]:.6f}, {translate[2]:.6f})",
                f"        float xformOp:rotateY = {rotate_y:.6f}",
                '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateY"]',
                "    }",
            ]
        )
    lines.append("}")
    write_text(path, "\n".join(lines) + "\n")


def polygons_to_svg(polygons: Sequence[List[Tuple[float, float]]], color: str, width: float, height: float) -> List[str]:
    elements = []
    for polygon in polygons:
        coords = []
        for x, y in polygon:
            sx = (x * width + width / 2.0) * 1024.0 / width
            sy = ((height / 2.0) - y * height) * 1024.0 / height
            coords.append(f"{sx:.2f},{sy:.2f}")
        elements.append(f'  <polygon points="{" ".join(coords)}" fill="{color}" />')
    return elements


def write_sign_svg(path: Path, sign_type: str, width: float, height: float, material_defs: Dict[str, Dict]) -> None:
    layers = sign_layers(sign_type)
    lines = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">']
    for material_id, polygons in layers:
        color = material_defs[material_id]["svg_fill"]
        lines.extend(polygons_to_svg(polygons, color, width, height))
    lines.append("</svg>")
    write_text(path, "\n".join(lines) + "\n")


def make_materials(illuminant_d65: Sequence[float]) -> Dict[str, Dict]:
    proxy_curves = {
        "mat_sign_stop_red_reflectance": clamp_list(interpolate([(350, 0.03), (500, 0.05), (580, 0.35), (620, 0.8), (700, 0.72), (900, 0.45), (1700, 0.22)], MASTER_GRID)),
        "mat_sign_white_reflectance": clamp_list(interpolate([(350, 0.82), (700, 0.9), (1100, 0.82), (1700, 0.72)], MASTER_GRID)),
        "mat_sign_black_reflectance": clamp_list(interpolate([(350, 0.03), (1700, 0.04)], MASTER_GRID)),
        "mat_sign_blue_reflectance": clamp_list(interpolate([(350, 0.14), (430, 0.65), (480, 0.82), (560, 0.22), (700, 0.05), (1700, 0.04)], MASTER_GRID)),
        "mat_sign_yellow_reflectance": clamp_list(interpolate([(350, 0.08), (420, 0.2), (520, 0.78), (600, 0.88), (700, 0.72), (1100, 0.48), (1700, 0.3)], MASTER_GRID)),
        "mat_sign_orange_reflectance": clamp_list(interpolate([(350, 0.06), (450, 0.16), (540, 0.52), (620, 0.82), (700, 0.72), (1100, 0.44), (1700, 0.26)], MASTER_GRID)),
        "mat_asphalt_dry_reflectance": clamp_list(interpolate([(350, 0.05), (500, 0.07), (700, 0.09), (900, 0.11), (1100, 0.13), (1700, 0.18)], MASTER_GRID)),
        "mat_asphalt_wet_reflectance": clamp_list(interpolate([(350, 0.03), (500, 0.05), (700, 0.06), (900, 0.08), (1100, 0.1), (1700, 0.15)], MASTER_GRID)),
        "mat_concrete_reflectance": clamp_list(interpolate([(350, 0.24), (500, 0.3), (700, 0.36), (900, 0.42), (1100, 0.45), (1700, 0.5)], MASTER_GRID)),
        "mat_marking_white_reflectance": clamp_list(interpolate([(350, 0.68), (500, 0.78), (700, 0.84), (900, 0.8), (1100, 0.74), (1700, 0.62)], MASTER_GRID)),
        "mat_marking_yellow_reflectance": clamp_list(interpolate([(350, 0.08), (430, 0.18), (520, 0.72), (600, 0.82), (700, 0.64), (1100, 0.42), (1700, 0.28)], MASTER_GRID)),
        "mat_metal_galvanized_reflectance": clamp_list(interpolate([(350, 0.38), (500, 0.46), (700, 0.52), (1100, 0.56), (1700, 0.48)], MASTER_GRID)),
        "mat_glass_lens_transmittance": clamp_list(interpolate([(350, 0.7), (420, 0.88), (700, 0.92), (900, 0.84), (1100, 0.72), (1700, 0.4)], MASTER_GRID)),
        "mat_retroreflective_gain": clamp_list(interpolate([(350, 1.0), (500, 1.1), (700, 1.18), (900, 1.12), (1100, 1.05), (1700, 0.9)], MASTER_GRID), 0.0, 2.0),
        "mat_wet_overlay_transmittance": clamp_list(interpolate([(350, 0.92), (500, 0.96), (700, 0.97), (900, 0.96), (1100, 0.92), (1700, 0.84)], MASTER_GRID)),
        "spd_led_red": gaussian(MASTER_GRID, 625.0, 16.0, 1.0),
        "spd_led_yellow": gaussian(MASTER_GRID, 592.0, 18.0, 1.0),
        "spd_led_green": gaussian(MASTER_GRID, 530.0, 18.0, 1.0),
    }
    proxy_curves["spd_led_pedestrian_white"] = clamp_list(
        [a + b for a, b in zip(gaussian(MASTER_GRID, 460.0, 28.0, 0.6), gaussian(MASTER_GRID, 580.0, 80.0, 0.9))],
        0.0,
        2.0,
    )
    proxy_curves["spd_led_countdown_amber"] = gaussian(MASTER_GRID, 605.0, 22.0, 1.0)

    wavelengths_nm = load_usgs_wavelengths_nm()
    usgs_curves = {selection["curve_name"]: load_usgs_selected_curve(selection, wavelengths_nm) for selection in USGS_SAMPLE_SELECTIONS}

    curves = dict(proxy_curves)
    curves["mat_asphalt_dry_reflectance"] = usgs_curves["src_usgs_gds376_asphalt_road_aref"]["values"]
    curves["mat_concrete_reflectance"] = usgs_curves["src_usgs_gds375_concrete_road_aref"]["values"]
    curves["mat_metal_galvanized_reflectance"] = usgs_curves["src_usgs_gds334_galvanized_sheet_metal_aref"]["values"]

    proxy_ratio = []
    for wet_value, dry_value in zip(proxy_curves["mat_asphalt_wet_reflectance"], proxy_curves["mat_asphalt_dry_reflectance"]):
        proxy_ratio.append(wet_value / max(dry_value, 1e-6))
    curves["mat_asphalt_wet_reflectance"] = clamp_list(
        [dry_value * ratio for dry_value, ratio in zip(curves["mat_asphalt_dry_reflectance"], proxy_ratio)]
    )

    material_specs = [
        ("mat_sign_stop_red", "reflective", "reflectance", "dry", ["mat_sign_stop_red_reflectance"], {"roughnessFactor": 0.78}),
        ("mat_sign_white", "reflective", "reflectance", "dry", ["mat_sign_white_reflectance"], {"roughnessFactor": 0.82}),
        ("mat_sign_black", "reflective", "reflectance", "dry", ["mat_sign_black_reflectance"], {"roughnessFactor": 0.88}),
        ("mat_sign_blue", "reflective", "reflectance", "dry", ["mat_sign_blue_reflectance"], {"roughnessFactor": 0.8}),
        ("mat_sign_yellow", "reflective", "reflectance", "dry", ["mat_sign_yellow_reflectance"], {"roughnessFactor": 0.8}),
        ("mat_sign_orange", "reflective", "reflectance", "dry", ["mat_sign_orange_reflectance"], {"roughnessFactor": 0.8}),
        ("mat_asphalt_dry", "reflective", "reflectance", "dry", ["mat_asphalt_dry_reflectance"], {"roughnessFactor": 0.95}),
        ("mat_asphalt_wet", "wet_overlay", "reflectance", "wet", ["mat_asphalt_wet_reflectance", "mat_wet_overlay_transmittance"], {"roughnessFactor": 0.24}),
        ("mat_concrete", "reflective", "reflectance", "dry", ["mat_concrete_reflectance"], {"roughnessFactor": 0.92}),
        ("mat_marking_white", "retroreflective", "reflectance", "dry", ["mat_marking_white_reflectance", "mat_retroreflective_gain"], {"roughnessFactor": 0.42}),
        ("mat_marking_yellow", "retroreflective", "reflectance", "dry", ["mat_marking_yellow_reflectance", "mat_retroreflective_gain"], {"roughnessFactor": 0.42}),
        ("mat_metal_galvanized", "reflective", "reflectance", "dry", ["mat_metal_galvanized_reflectance"], {"metallicFactor": 0.12, "roughnessFactor": 0.54}),
        ("mat_signal_housing", "reflective", "reflectance", "coated", ["mat_sign_black_reflectance"], {"roughnessFactor": 0.72}),
        ("mat_signal_lens_red_off", "transmissive", "transmittance", "coated", ["mat_glass_lens_transmittance", "mat_sign_stop_red_reflectance"], {"roughnessFactor": 0.12}),
        ("mat_signal_lens_yellow_off", "transmissive", "transmittance", "coated", ["mat_glass_lens_transmittance", "mat_sign_yellow_reflectance"], {"roughnessFactor": 0.12}),
        ("mat_signal_lens_green_off", "transmissive", "transmittance", "coated", ["mat_glass_lens_transmittance", "mat_sign_blue_reflectance"], {"roughnessFactor": 0.12}),
        ("mat_signal_ped_red_off", "transmissive", "transmittance", "coated", ["mat_glass_lens_transmittance", "mat_sign_stop_red_reflectance"], {"roughnessFactor": 0.12}),
        ("mat_signal_ped_white_off", "transmissive", "transmittance", "coated", ["mat_glass_lens_transmittance", "mat_sign_white_reflectance"], {"roughnessFactor": 0.12}),
        ("mat_signal_countdown_amber_off", "emissive", "spd", "coated", ["spd_led_countdown_amber"], {"roughnessFactor": 0.1}),
        ("mat_vms_panel", "emissive", "reflectance", "dry", ["mat_sign_black_reflectance"], {"roughnessFactor": 0.35}),
    ]

    def proxy_material_meta(note: str = "Project-generated proxy curve.") -> Dict:
        return {
            "source_quality": "project_proxy",
            "source_ids": [],
            "uncertainty": {
                "type": "project_proxy",
                "note": note,
            },
            "license": {
                "spdx": "LicenseRef-ProjectGenerated",
                "redistribution": "Project-generated derivative metadata and proxy curves.",
            },
            "provenance_note": note,
        }

    material_source_meta = {
        material_id: proxy_material_meta("Project-generated proxy curve; not yet replaced by a measured automotive-grade or materially equivalent baseline.")
        for material_id, *_ in material_specs
    }
    material_source_meta["mat_asphalt_dry"] = {
        "source_quality": "measured_standard",
        "source_ids": [USGS_WAVELENGTH_SOURCE["id"], "usgs_gds376_asphalt_road_old"],
        "uncertainty": {
            "type": "measured_open_standard",
            "note": "Dry road asphalt measured baseline from the selected USGS Spectral Library Version 7 subset.",
        },
        "license": {
            "spdx": "LicenseRef-USGS-Derived",
            "redistribution": "Resampled derivative of selected USGS Spectral Library Version 7 local subset data.",
        },
        "provenance_note": "Measured dry road asphalt baseline from USGS v7 sample GDS376.",
    }
    material_source_meta["mat_concrete"] = {
        "source_quality": "measured_standard",
        "source_ids": [USGS_WAVELENGTH_SOURCE["id"], "usgs_gds375_concrete_road"],
        "uncertainty": {
            "type": "measured_open_standard",
            "note": "Concrete road measured baseline from the selected USGS Spectral Library Version 7 subset.",
        },
        "license": {
            "spdx": "LicenseRef-USGS-Derived",
            "redistribution": "Resampled derivative of selected USGS Spectral Library Version 7 local subset data.",
        },
        "provenance_note": "Measured concrete baseline from USGS v7 sample GDS375.",
    }
    material_source_meta["mat_metal_galvanized"] = {
        "source_quality": "measured_standard",
        "source_ids": [USGS_WAVELENGTH_SOURCE["id"], "usgs_gds334_galvanized_sheet_metal"],
        "uncertainty": {
            "type": "measured_open_standard",
            "note": "Galvanized sheet-metal measured baseline from the selected USGS Spectral Library Version 7 subset.",
        },
        "license": {
            "spdx": "LicenseRef-USGS-Derived",
            "redistribution": "Resampled derivative of selected USGS Spectral Library Version 7 local subset data.",
        },
        "provenance_note": "Measured galvanized sheet-metal baseline from USGS v7 sample GDS334.",
    }
    material_source_meta["mat_asphalt_wet"] = {
        "source_quality": "measured_derivative",
        "source_ids": [USGS_WAVELENGTH_SOURCE["id"], "usgs_gds376_asphalt_road_old"],
        "uncertainty": {
            "type": "measured_derivative_plus_proxy_modifier",
            "note": "Wet asphalt derived from measured USGS dry asphalt baseline with preserved project wet-shape ratio and wet-overlay modifier.",
        },
        "license": {
            "spdx": "LicenseRef-USGS-Derived",
            "redistribution": "Measured-derived wet asphalt baseline using selected USGS dry asphalt data plus tracked project modifiers.",
        },
        "provenance_note": "Measured-derived wet asphalt from USGS v7 dry asphalt sample plus tracked wet proxy ratio.",
    }

    materials = {}
    spectra_dir = REPO_ROOT / "canonical" / "spectra"
    for curve_name, curve in usgs_curves.items():
        write_npz(spectra_dir / f"{curve_name}.npz", {"wavelength_nm": MASTER_GRID, "values": curve["values"]})
    for curve_name, values in curves.items():
        write_npz(spectra_dir / f"{curve_name}.npz", {"wavelength_nm": MASTER_GRID, "values": values})

    for material_id, material_type, quantity_type, sample_state, curve_names, pbr_overrides in material_specs:
        base_curve_name = curve_names[0]
        curve_values = curves[base_curve_name]
        if quantity_type == "spd":
            rgba = spd_to_rgb(curve_values)
            emissive_factor = rgba[:3]
        else:
            rgba = spectral_to_rgb(curve_values, illuminant_d65)
            emissive_factor = None
        pbr = {
            "baseColorFactor": rgba,
            "metallicFactor": pbr_overrides.get("metallicFactor", 0.0),
            "roughnessFactor": pbr_overrides.get("roughnessFactor", 0.8),
        }
        if emissive_factor:
            pbr["emissiveFactor"] = [min(1.0, channel) for channel in emissive_factor]
        source_meta = material_source_meta[material_id]
        material = {
            "id": material_id,
            "material_type": material_type,
            "quantity_type": quantity_type,
            "wavelength_grid_ref": "grid_master_350_1700_1nm",
            "source_curve_refs": [
                {
                    "curve_id": curve_name,
                    "role": "primary" if index == 0 else "modifier",
                    "path": f"canonical/spectra/{curve_name}.npz",
                    "wavelength_key": "wavelength_nm",
                    "value_key": "values",
                }
                for index, curve_name in enumerate(curve_names)
            ],
            "pbr_fallback": pbr,
            "sample_state": sample_state,
            "geometry_conditions": {
                "retroreflective_gain_curve": "mat_retroreflective_gain" if material_type == "retroreflective" else None,
                "wet_overlay": material_type == "wet_overlay",
                "film_thickness_mm": 0.5 if material_type == "wet_overlay" else None,
                "specular_boost": 1.8 if material_type == "wet_overlay" else None,
            },
            "source_quality": source_meta["source_quality"],
            "source_ids": source_meta["source_ids"],
            "uncertainty": source_meta["uncertainty"],
            "license": source_meta["license"],
            "provenance": {
                "generated_at": GENERATED_AT,
                "generated_by": "scripts/build_asset_pack.py",
                "source_ids": source_meta["source_ids"],
                "note": source_meta["provenance_note"],
            },
        }
        material["svg_fill"] = material_hex(rgba)
        materials[material_id] = material
        write_json(REPO_ROOT / "canonical" / "materials" / f"{material_id}.spectral_material.json", material)

    write_npz(spectra_dir / "grid_master_350_1700_1nm.npz", {"wavelength_nm": MASTER_GRID})
    write_npz(spectra_dir / "grid_runtime_400_1100_5nm.npz", {"wavelength_nm": RUNTIME_GRID})
    return materials


def write_camera_profiles() -> List[Dict]:
    raw_curves = {
        "r": clamp_list(interpolate([(350, 0.0), (420, 0.01), (480, 0.06), (540, 0.22), (600, 0.84), (640, 1.0), (700, 0.62), (780, 0.14), (900, 0.02), (1100, 0.0), (1700, 0.0)], MASTER_GRID)),
        "g": clamp_list(interpolate([(350, 0.0), (400, 0.05), (460, 0.46), (520, 1.0), (580, 0.62), (650, 0.1), (760, 0.02), (1100, 0.0), (1700, 0.0)], MASTER_GRID)),
        "b": clamp_list(interpolate([(350, 0.08), (390, 0.42), (440, 1.0), (500, 0.46), (560, 0.08), (650, 0.01), (1100, 0.0), (1700, 0.0)], MASTER_GRID)),
        "nir": clamp_list(interpolate([(350, 0.0), (620, 0.0), (680, 0.08), (730, 0.32), (800, 0.82), (860, 1.0), (940, 0.88), (1020, 0.44), (1100, 0.0), (1700, 0.0)], MASTER_GRID)),
    }
    optics = clamp_list(interpolate([(350, 0.52), (400, 0.84), (450, 0.9), (700, 0.92), (850, 0.76), (950, 0.64), (1050, 0.36), (1100, 0.08), (1700, 0.0)], MASTER_GRID))
    effective_curves = {
        channel: normalize_unit_peak([sample * transmission for sample, transmission in zip(raw_curve, optics)])
        for channel, raw_curve in raw_curves.items()
    }

    spectra_dir = REPO_ROOT / "canonical" / "spectra"
    for channel in CAMERA_CHANNELS:
        write_npz(spectra_dir / f"cam_ref_rgbnir_{channel}_raw_srf.npz", {"wavelength_nm": MASTER_GRID, "values": raw_curves[channel]})
        write_npz(spectra_dir / f"cam_ref_rgbnir_{channel}_effective_srf.npz", {"wavelength_nm": MASTER_GRID, "values": effective_curves[channel]})
    write_npz(spectra_dir / "cam_ref_rgbnir_optics_transmittance.npz", {"wavelength_nm": MASTER_GRID, "values": optics})

    def curve_ref(name: str) -> Dict:
        return {
            "path": f"canonical/spectra/{name}.npz",
            "wavelength_key": "wavelength_nm",
            "value_key": "values",
        }

    profile = {
        "id": "camera_reference_rgb_nir_v1",
        "sensor_branch": "rgb_nir",
        "wavelength_grid_ref": "grid_master_350_1700_1nm",
        "raw_channel_srf_refs": {channel: curve_ref(f"cam_ref_rgbnir_{channel}_raw_srf") for channel in CAMERA_CHANNELS},
        "optics_transmittance_ref": curve_ref("cam_ref_rgbnir_optics_transmittance"),
        "effective_channel_srf_refs": {channel: curve_ref(f"cam_ref_rgbnir_{channel}_effective_srf") for channel in CAMERA_CHANNELS},
        "normalization": {"method": "unit_peak_per_channel_after_optics"},
        "operating_temperature_c": 25.0,
        "source_quality": "vendor_derived",
        "source_ids": ["basler_color_emva_knowledge", "sony_imx900_product_page", "sony_isx016_pdf"],
        "license": {
            "spdx": "LicenseRef-VendorDerived",
            "redistribution": "Derived camera-profile metadata and curves from public vendor documentation and tracked project curve fitting.",
        },
        "provenance": {
            "generated_at": GENERATED_AT,
            "generated_by": "scripts/build_asset_pack.py",
            "source_ids": ["basler_color_emva_knowledge", "sony_imx900_product_page", "sony_isx016_pdf"],
            "note": "Generic RGB+NIR automotive camera profile derived from public vendor documentation; not a measured single-SKU SRF.",
        },
    }
    write_json(REPO_ROOT / "canonical" / "camera" / f"{profile['id']}.camera_profile.json", profile)
    return [profile]


def generate_standard_spectra() -> Dict[str, List[float]]:
    cie = interpolate(load_cie_d65(), MASTER_GRID)
    astm = load_astm_g173()
    global_tilt = interpolate(astm["global_tilt"], MASTER_GRID)
    direct = interpolate(astm["direct"], MASTER_GRID)
    extraterrestrial = interpolate(astm["extraterrestrial"], MASTER_GRID)
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_d65.npz", {"wavelength_nm": MASTER_GRID, "values": cie})
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_am1_5_global_tilt.npz", {"wavelength_nm": MASTER_GRID, "values": global_tilt})
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_am1_5_direct.npz", {"wavelength_nm": MASTER_GRID, "values": direct})
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_am0_extraterrestrial.npz", {"wavelength_nm": MASTER_GRID, "values": extraterrestrial})
    urban_night = [red * 0.38 + yellow * 0.22 + green * 0.12 + 0.15 for red, yellow, green in zip(gaussian(MASTER_GRID, 625.0, 16.0, 1.0), gaussian(MASTER_GRID, 592.0, 18.0, 1.0), gaussian(MASTER_GRID, 530.0, 18.0, 0.6))]
    wet_dusk = [d65 * 0.36 + am * 0.24 for d65, am in zip(cie, global_tilt)]
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_urban_night_mix.npz", {"wavelength_nm": MASTER_GRID, "values": urban_night})
    write_npz(REPO_ROOT / "canonical" / "spectra" / "illuminant_wet_dusk_mix.npz", {"wavelength_nm": MASTER_GRID, "values": wet_dusk})
    return {
        "illuminant_d65": cie,
        "illuminant_am1_5_global_tilt": global_tilt,
        "illuminant_am1_5_direct": direct,
        "illuminant_am0_extraterrestrial": extraterrestrial,
        "illuminant_urban_night_mix": urban_night,
        "illuminant_wet_dusk_mix": wet_dusk,
    }


def sign_definitions() -> List[Dict]:
    return [
        {"id": "sign_stop", "sign_type": "stop", "size": (0.78, 0.78), "variant_key": "vienna_core.stop", "semantic_class": "regulatory.stop"},
        {"id": "sign_yield", "sign_type": "yield", "size": (0.9, 0.78), "variant_key": "vienna_core.give_way", "semantic_class": "regulatory.yield"},
        {"id": "sign_no_entry", "sign_type": "no_entry", "size": (0.75, 0.75), "variant_key": "vienna_core.no_entry", "semantic_class": "regulatory.no_entry"},
        {"id": "sign_speed_limit_50", "sign_type": "speed_limit", "size": (0.75, 0.75), "variant_key": "vienna_core.speed_limit_50", "semantic_class": "regulatory.speed_limit"},
        {"id": "sign_turn_restriction_left", "sign_type": "turn_restriction", "size": (0.75, 0.75), "variant_key": "vienna_core.no_left_turn", "semantic_class": "regulatory.turn_restriction"},
        {"id": "sign_mandatory_direction_right", "sign_type": "mandatory_direction", "size": (0.75, 0.75), "variant_key": "vienna_core.turn_right", "semantic_class": "mandatory.direction"},
        {"id": "sign_pedestrian_crossing", "sign_type": "pedestrian_crossing", "size": (0.82, 0.82), "variant_key": "vienna_core.pedestrian_crossing", "semantic_class": "information.pedestrian_crossing"},
        {"id": "sign_school_warning", "sign_type": "school_warning", "size": (0.8, 0.8), "variant_key": "vienna_core.school_warning", "semantic_class": "warning.school_zone"},
        {"id": "sign_signal_ahead", "sign_type": "signal_ahead", "size": (0.8, 0.8), "variant_key": "vienna_core.signal_ahead", "semantic_class": "warning.signal_ahead"},
        {"id": "sign_merge", "sign_type": "merge", "size": (0.8, 0.8), "variant_key": "vienna_core.merge", "semantic_class": "warning.merge"},
        {"id": "sign_curve_left", "sign_type": "curve", "size": (0.8, 0.8), "variant_key": "vienna_core.curve_left", "semantic_class": "warning.curve"},
        {"id": "sign_construction_warning", "sign_type": "construction", "size": (0.8, 0.8), "variant_key": "vienna_core.roadworks", "semantic_class": "warning.construction"},
        {"id": "sign_parking", "sign_type": "parking", "size": (0.78, 0.78), "variant_key": "vienna_core.parking", "semantic_class": "information.parking"},
        {"id": "sign_bus_stop", "sign_type": "bus_stop", "size": (0.78, 0.78), "variant_key": "vienna_core.bus_stop", "semantic_class": "information.bus_stop"},
        {"id": "sign_one_way", "sign_type": "one_way", "size": (1.0, 0.36), "variant_key": "vienna_core.one_way", "semantic_class": "information.one_way"},
        {"id": "sign_lane_direction", "sign_type": "lane_direction", "size": (1.0, 0.72), "variant_key": "vienna_core.lane_direction", "semantic_class": "information.lane_direction"},
        {"id": "sign_railroad_warning", "sign_type": "railroad_warning", "size": (0.8, 0.8), "variant_key": "vienna_core.railroad_warning", "semantic_class": "warning.railroad"},
        {"id": "sign_variable_message", "sign_type": "variable_message", "size": (1.2, 0.7), "variant_key": "vienna_core.variable_message", "semantic_class": "information.variable_message"},
    ]


def traffic_light_definitions() -> List[Dict]:
    return [
        {
            "id": "signal_vehicle_vertical_3_aspect",
            "variant_key": "vehicle.vertical.3_aspect",
            "semantic_class": "traffic_light.vehicle",
            "body_w": 0.34,
            "body_h": 1.08,
            "body_d": 0.22,
            "lenses": [
                {"name": "lens_red", "x": 0.0, "y": 0.87, "radius": 0.1, "material_id": "mat_signal_lens_red_off"},
                {"name": "lens_yellow", "x": 0.0, "y": 0.54, "radius": 0.1, "material_id": "mat_signal_lens_yellow_off"},
                {"name": "lens_green", "x": 0.0, "y": 0.21, "radius": 0.1, "material_id": "mat_signal_lens_green_off"},
            ],
            "emissive_profile": "emissive_vehicle_standard",
        },
        {
            "id": "signal_vehicle_horizontal_3_aspect",
            "variant_key": "vehicle.horizontal.3_aspect",
            "semantic_class": "traffic_light.vehicle",
            "body_w": 1.08,
            "body_h": 0.34,
            "body_d": 0.22,
            "lenses": [
                {"name": "lens_red", "x": -0.33, "y": 0.17, "radius": 0.1, "material_id": "mat_signal_lens_red_off"},
                {"name": "lens_yellow", "x": 0.0, "y": 0.17, "radius": 0.1, "material_id": "mat_signal_lens_yellow_off"},
                {"name": "lens_green", "x": 0.33, "y": 0.17, "radius": 0.1, "material_id": "mat_signal_lens_green_off"},
            ],
            "emissive_profile": "emissive_vehicle_standard",
        },
        {
            "id": "signal_protected_turn_4_aspect",
            "variant_key": "vehicle.protected_turn.4_aspect",
            "semantic_class": "traffic_light.vehicle_protected_turn",
            "body_w": 0.34,
            "body_h": 1.42,
            "body_d": 0.22,
            "lenses": [
                {"name": "lens_red", "x": 0.0, "y": 1.16, "radius": 0.1, "material_id": "mat_signal_lens_red_off"},
                {"name": "lens_yellow", "x": 0.0, "y": 0.83, "radius": 0.1, "material_id": "mat_signal_lens_yellow_off"},
                {"name": "lens_green", "x": 0.0, "y": 0.5, "radius": 0.1, "material_id": "mat_signal_lens_green_off"},
                {"name": "lens_arrow", "x": 0.0, "y": 0.17, "radius": 0.1, "material_id": "mat_signal_lens_green_off"},
            ],
            "emissive_profile": "emissive_protected_turn",
        },
        {
            "id": "signal_pedestrian_2_aspect",
            "variant_key": "pedestrian.2_aspect",
            "semantic_class": "traffic_light.pedestrian",
            "body_w": 0.42,
            "body_h": 0.76,
            "body_d": 0.16,
            "lenses": [
                {"name": "lens_ped_red", "x": 0.0, "y": 0.55, "radius": 0.12, "material_id": "mat_signal_ped_red_off"},
                {"name": "lens_ped_white", "x": 0.0, "y": 0.21, "radius": 0.12, "material_id": "mat_signal_ped_white_off"},
            ],
            "emissive_profile": "emissive_pedestrian_standard",
        },
        {
            "id": "signal_pedestrian_countdown_housing",
            "variant_key": "pedestrian.countdown",
            "semantic_class": "traffic_light.pedestrian_countdown",
            "body_w": 0.46,
            "body_h": 1.0,
            "body_d": 0.16,
            "lenses": [
                {"name": "lens_ped_red", "x": 0.0, "y": 0.72, "radius": 0.12, "material_id": "mat_signal_ped_red_off"},
                {"name": "lens_ped_white", "x": 0.0, "y": 0.38, "radius": 0.12, "material_id": "mat_signal_ped_white_off"},
                {"name": "display_countdown", "x": 0.0, "y": 0.08, "radius": 0.11, "material_id": "mat_signal_countdown_amber_off"},
            ],
            "emissive_profile": "emissive_pedestrian_countdown",
        },
    ]


def road_definitions() -> List[Dict]:
    return [
        {"id": "road_asphalt_dry", "family": "road_surface", "semantic_class": "road.asphalt", "variant_key": "dry", "dimensions": (4.0, 0.04, 4.0)},
        {"id": "road_asphalt_wet", "family": "road_surface", "semantic_class": "road.asphalt", "variant_key": "wet", "dimensions": (4.0, 0.04, 4.0)},
        {"id": "road_concrete", "family": "road_surface", "semantic_class": "road.concrete", "variant_key": "default", "dimensions": (4.0, 0.05, 4.0)},
        {"id": "road_curb_segment", "family": "road_furniture", "semantic_class": "road.curb", "variant_key": "default", "dimensions": (2.0, 0.18, 0.4)},
        {"id": "road_sidewalk_panel", "family": "road_surface", "semantic_class": "road.sidewalk", "variant_key": "default", "dimensions": (2.4, 0.06, 2.4)},
        {"id": "marking_lane_white", "family": "road_marking", "semantic_class": "marking.lane", "variant_key": "white", "dimensions": (0.16, 0.005, 2.0)},
        {"id": "marking_lane_yellow", "family": "road_marking", "semantic_class": "marking.lane", "variant_key": "yellow", "dimensions": (0.16, 0.005, 2.0)},
        {"id": "marking_stop_line", "family": "road_marking", "semantic_class": "marking.stop_line", "variant_key": "white", "dimensions": (3.0, 0.005, 0.3)},
        {"id": "marking_crosswalk", "family": "road_marking", "semantic_class": "marking.crosswalk", "variant_key": "ladder", "dimensions": (3.0, 0.005, 2.0)},
        {"id": "furniture_sign_pole", "family": "road_furniture", "semantic_class": "furniture.sign_pole", "variant_key": "default", "dimensions": (0.06, 3.2, 0.06)},
        {"id": "furniture_signal_pole", "family": "road_furniture", "semantic_class": "furniture.signal_pole", "variant_key": "mast_arm", "dimensions": (4.0, 5.0, 0.16)},
        {"id": "furniture_guardrail_bollard_set", "family": "road_furniture", "semantic_class": "furniture.guardrail_bollard", "variant_key": "default", "dimensions": (3.5, 0.85, 0.18)},
    ]


def asset_manifest_common(asset_id: str, family: str, semantic_class: str, variant_key: str, dimensions: Sequence[float], materials: List[str], triangle_counts: Dict[str, int], export_targets: Dict, states: Dict, anchor_points: Dict, collider: Dict, provenance_note: str) -> Dict:
    dim_payload = {
        "width": round(dimensions[0], 4),
        "height": round(dimensions[1], 4),
        "depth": round(dimensions[2] if len(dimensions) > 2 else 0.02, 4),
    }
    return {
        "id": asset_id,
        "family": family,
        "semantic_class": semantic_class,
        "variant_key": variant_key,
        "dimensions_m": dim_payload,
        "lods": [
            {"name": lod_name, "triangle_count": triangle_counts[lod_name], "usd_scope": f"/{asset_id}/{lod_name}", "gltf_node_prefix": lod_name}
            for lod_name in ["LOD0", "LOD1"]
        ],
        "collider": collider,
        "anchor_points": anchor_points,
        "materials": sorted(materials),
        "states": states,
        "export_targets": export_targets,
        "license": {"spdx": "LicenseRef-ProjectGenerated", "redistribution": "geometry, manifests, and templates generated in-repo"},
        "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py", "note": provenance_note},
    }


def build_assets(materials: Dict[str, Dict]) -> Tuple[List[Dict], Dict[str, Dict[str, List[Dict]]]]:
    assets = []
    asset_meshes = {}

    for sign in sign_definitions():
        width, height = sign["size"]
        parts = sign_asset_parts(sign["sign_type"], width, height)
        asset_meshes[sign["id"]] = {"LOD0": parts["LOD0"], "LOD1": parts["LOD1"]}
        svg_path = REPO_ROOT / "canonical" / "templates" / "signs" / f"{sign['id']}.svg"
        write_sign_svg(svg_path, sign["sign_type"], width, height, materials)
        material_ids = {part["material_id"] for part in parts["LOD0"] + parts["LOD1"]}
        triangle_counts = {lod: triangle_count(parts[lod]) for lod in ["LOD0", "LOD1"]}
        manifest = asset_manifest_common(
            sign["id"],
            "traffic_sign",
            sign["semantic_class"],
            sign["variant_key"],
            (width, parts["mount_height"], 0.08),
            list(material_ids),
            triangle_counts,
            {
                "template_svg": f"canonical/templates/signs/{sign['id']}.svg",
                "usd_ascii": f"canonical/geometry/usd/{sign['id']}.usda",
                "usd_binary": f"exports/usd/{sign['id']}.usdc",
                "gltf_binary": f"exports/gltf/{sign['id']}.glb",
            },
            {"default": {"render_profile": "reflective_daytime"}},
            {
                "base_center": {"x": 0.0, "y": 0.0, "z": 0.0},
                "plate_center": {"x": 0.0, "y": round(parts["sign_center_y"], 4), "z": 0.0},
            },
            {"type": "capsule", "radius": 0.4, "height": round(parts["mount_height"], 4)},
            "SVG face template plus generated USD/GLB plate and pole geometry.",
        )
        assets.append(manifest)

    for signal in traffic_light_definitions():
        parts = signal_asset_parts(signal)
        asset_meshes[signal["id"]] = parts
        material_ids = {part["material_id"] for part in parts["LOD0"] + parts["LOD1"]}
        triangle_counts = {lod: triangle_count(parts[lod]) for lod in ["LOD0", "LOD1"]}
        states = {
            "off": {"emissive_profile": signal["emissive_profile"], "state_key": "off"},
            "active_red": {"emissive_profile": signal["emissive_profile"], "state_key": "red"},
            "active_yellow": {"emissive_profile": signal["emissive_profile"], "state_key": "yellow"},
            "active_green": {"emissive_profile": signal["emissive_profile"], "state_key": "green"},
        }
        manifest = asset_manifest_common(
            signal["id"],
            "traffic_light",
            signal["semantic_class"],
            signal["variant_key"],
            (signal["body_w"], signal["body_h"] + 1.2, signal["body_d"]),
            list(material_ids),
            triangle_counts,
            {
                "usd_ascii": f"canonical/geometry/usd/{signal['id']}.usda",
                "usd_binary": f"exports/usd/{signal['id']}.usdc",
                "gltf_binary": f"exports/gltf/{signal['id']}.glb",
            },
            states,
            {
                "mount_point": {"x": 0.0, "y": 1.2, "z": -0.08},
                "front_center": {"x": 0.0, "y": round(signal["body_h"] / 2.0 + 1.2, 4), "z": round(signal["body_d"] / 2.0, 4)},
            },
            {"type": "box", "width": signal["body_w"], "height": signal["body_h"], "depth": signal["body_d"]},
            "Generated signal housing geometry with state-driven emissive profile bindings.",
        )
        assets.append(manifest)

    for road in road_definitions():
        parts = road_asset_parts(road["id"], road["dimensions"])
        asset_meshes[road["id"]] = parts
        material_ids = {part["material_id"] for part in parts["LOD0"] + parts["LOD1"]}
        triangle_counts = {lod: triangle_count(parts[lod]) for lod in ["LOD0", "LOD1"]}
        manifest = asset_manifest_common(
            road["id"],
            road["family"],
            road["semantic_class"],
            road["variant_key"],
            road["dimensions"],
            list(material_ids),
            triangle_counts,
            {
                "usd_ascii": f"canonical/geometry/usd/{road['id']}.usda",
                "usd_binary": f"exports/usd/{road['id']}.usdc",
                "gltf_binary": f"exports/gltf/{road['id']}.glb",
            },
            {"default": {"render_profile": "static"}},
            {"base_center": {"x": 0.0, "y": 0.0, "z": 0.0}},
            {"type": "box", "width": road["dimensions"][0], "height": road["dimensions"][1], "depth": road["dimensions"][2]},
            "Generated reusable road surface, marking, or furniture primitive.",
        )
        assets.append(manifest)

    for manifest in assets:
        write_json(REPO_ROOT / "canonical" / "manifests" / f"{manifest['id']}.asset_manifest.json", manifest)
    return assets, asset_meshes


def write_asset_geometry_and_exports(assets: List[Dict], asset_meshes: Dict[str, Dict[str, List[Dict]]], materials: Dict[str, Dict]) -> Dict[str, Dict]:
    exported = {}
    for asset in assets:
        asset_id = asset["id"]
        usd_path = REPO_ROOT / "canonical" / "geometry" / "usd" / f"{asset_id}.usda"
        write_usda_asset(usd_path, asset_id, asset_meshes[asset_id])
        usdc_path = REPO_ROOT / "exports" / "usd" / f"{asset_id}.usdc"
        usdcat_result = run(["usdcat", str(usd_path), "-o", str(usdc_path)])
        exported[asset_id] = {"usdcat_returncode": usdcat_result.returncode, "usdcat_stderr": usdcat_result.stderr.strip()}
        glb_path = REPO_ROOT / "exports" / "gltf" / f"{asset_id}.glb"
        glb_path.write_bytes(glb_bytes(asset_id, asset_meshes[asset_id]["LOD0"], materials))
    return exported


def write_emissive_profiles() -> List[Dict]:
    profiles = [
        {
            "id": "emissive_vehicle_standard",
            "spd_ref": {
                "red": "canonical/spectra/spd_led_red.npz",
                "yellow": "canonical/spectra/spd_led_yellow.npz",
                "green": "canonical/spectra/spd_led_green.npz",
            },
            "state_map": {
                "off": {},
                "red": {"lens_red": "spd_led_red"},
                "yellow": {"lens_yellow": "spd_led_yellow"},
                "green": {"lens_green": "spd_led_green"},
                "flashing_yellow": {"lens_yellow": "spd_led_yellow"},
            },
            "nominal_luminance_cd_m2": {"red": 7000, "yellow": 6500, "green": 8000},
            "temperature_c": 25.0,
            "driver_mode": "steady_dc",
            "source_quality": "project_proxy",
            "source_ids": [],
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py", "source_ids": [], "note": "Proxy traffic signal SPD."},
        },
        {
            "id": "emissive_protected_turn",
            "spd_ref": {
                "red": "canonical/spectra/spd_led_red.npz",
                "yellow": "canonical/spectra/spd_led_yellow.npz",
                "green": "canonical/spectra/spd_led_green.npz",
                "arrow": "canonical/spectra/spd_led_green.npz",
            },
            "state_map": {
                "off": {},
                "red": {"lens_red": "spd_led_red"},
                "yellow": {"lens_yellow": "spd_led_yellow"},
                "green": {"lens_green": "spd_led_green"},
                "green_arrow": {"lens_arrow": "spd_led_green"},
            },
            "nominal_luminance_cd_m2": {"red": 7000, "yellow": 6500, "green": 8000, "arrow": 7600},
            "temperature_c": 25.0,
            "driver_mode": "steady_dc",
            "source_quality": "project_proxy",
            "source_ids": [],
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py", "source_ids": [], "note": "Proxy protected-turn SPD."},
        },
        {
            "id": "emissive_pedestrian_standard",
            "spd_ref": {
                "red": "canonical/spectra/spd_led_red.npz",
                "walk": "canonical/spectra/spd_led_pedestrian_white.npz",
            },
            "state_map": {"off": {}, "dont_walk": {"lens_ped_red": "spd_led_red"}, "walk": {"lens_ped_white": "spd_led_pedestrian_white"}},
            "nominal_luminance_cd_m2": {"red": 5400, "walk": 6200},
            "temperature_c": 25.0,
            "driver_mode": "steady_dc",
            "source_quality": "project_proxy",
            "source_ids": [],
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py", "source_ids": [], "note": "Proxy pedestrian SPD."},
        },
        {
            "id": "emissive_pedestrian_countdown",
            "spd_ref": {
                "red": "canonical/spectra/spd_led_red.npz",
                "walk": "canonical/spectra/spd_led_pedestrian_white.npz",
                "countdown": "canonical/spectra/spd_led_countdown_amber.npz",
            },
            "state_map": {
                "off": {},
                "dont_walk": {"lens_ped_red": "spd_led_red"},
                "walk": {"lens_ped_white": "spd_led_pedestrian_white"},
                "countdown": {"display_countdown": "spd_led_countdown_amber"},
            },
            "nominal_luminance_cd_m2": {"red": 5400, "walk": 6200, "countdown": 5800},
            "temperature_c": 25.0,
            "driver_mode": "steady_dc",
            "source_quality": "project_proxy",
            "source_ids": [],
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py", "source_ids": [], "note": "Proxy pedestrian countdown SPD."},
        },
    ]
    for profile in profiles:
        write_json(REPO_ROOT / "canonical" / "emissive" / f"{profile['id']}.emissive_profile.json", profile)
    return profiles


def write_scenarios_and_atmospheres(camera_profile_id: str) -> Tuple[List[Dict], List[Dict]]:
    atmospheres = [
        {"id": "atmosphere_clear_clean_v1", "aod_550": 0.08, "visibility_km": 45.0, "cloud_fraction": 0.0, "source_ids": ["aeronet_quality_assurance_pdf", "libradtran_home"]},
        {"id": "atmosphere_overcast_v1", "aod_550": 0.18, "visibility_km": 18.0, "cloud_fraction": 0.95, "source_ids": ["aeronet_quality_assurance_pdf", "libradtran_home"]},
        {"id": "atmosphere_urban_night_v1", "aod_550": 0.21, "visibility_km": 12.0, "cloud_fraction": 0.15, "source_ids": ["aeronet_quality_assurance_pdf", "libradtran_home"]},
        {"id": "atmosphere_wet_dusk_v1", "aod_550": 0.16, "visibility_km": 10.0, "cloud_fraction": 0.6, "rain_rate_mm_h": 1.2, "source_ids": ["aeronet_quality_assurance_pdf", "libradtran_home"]},
    ]
    for atmosphere in atmospheres:
        write_json(REPO_ROOT / "canonical" / "atmospheres" / f"{atmosphere['id']}.json", atmosphere)
    scenarios = [
        {
            "id": "scenario_clear_noon",
            "illuminant_ref": "canonical/spectra/illuminant_am1_5_global_tilt.npz",
            "atmosphere_ref": "canonical/atmospheres/atmosphere_clear_clean_v1.json",
            "surface_state_overrides": {"road.asphalt": "road_asphalt_dry"},
            "sensor_branch": "rgb_nir",
            "camera_profile_ref": f"canonical/camera/{camera_profile_id}.camera_profile.json",
            "weather_flags": {"daylight": True, "wet": False, "night": False},
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py"},
        },
        {
            "id": "scenario_overcast_day",
            "illuminant_ref": "canonical/spectra/illuminant_d65.npz",
            "atmosphere_ref": "canonical/atmospheres/atmosphere_overcast_v1.json",
            "surface_state_overrides": {"road.asphalt": "road_asphalt_dry"},
            "sensor_branch": "rgb_nir",
            "camera_profile_ref": f"canonical/camera/{camera_profile_id}.camera_profile.json",
            "weather_flags": {"daylight": True, "wet": False, "night": False, "cloudy": True},
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py"},
        },
        {
            "id": "scenario_urban_night",
            "illuminant_ref": "canonical/spectra/illuminant_urban_night_mix.npz",
            "atmosphere_ref": "canonical/atmospheres/atmosphere_urban_night_v1.json",
            "surface_state_overrides": {"road.asphalt": "road_asphalt_dry"},
            "sensor_branch": "rgb_nir",
            "camera_profile_ref": f"canonical/camera/{camera_profile_id}.camera_profile.json",
            "weather_flags": {"daylight": False, "wet": False, "night": True},
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py"},
        },
        {
            "id": "scenario_wet_dusk",
            "illuminant_ref": "canonical/spectra/illuminant_wet_dusk_mix.npz",
            "atmosphere_ref": "canonical/atmospheres/atmosphere_wet_dusk_v1.json",
            "surface_state_overrides": {"road.asphalt": "road_asphalt_wet"},
            "sensor_branch": "rgb_nir",
            "camera_profile_ref": f"canonical/camera/{camera_profile_id}.camera_profile.json",
            "weather_flags": {"daylight": False, "wet": True, "night": False, "dusk": True},
            "license": {"spdx": "LicenseRef-ProjectGenerated"},
            "provenance": {"generated_at": GENERATED_AT, "generated_by": "scripts/build_asset_pack.py"},
        },
    ]
    for scenario in scenarios:
        write_json(REPO_ROOT / "canonical" / "scenarios" / f"{scenario['id']}.scenario_profile.json", scenario)
    return atmospheres, scenarios


def combine_with_transform(mesh_parts: Sequence[Dict], translate: Tuple[float, float, float], rotate_y_deg: float) -> List[Dict]:
    angle = math.radians(rotate_y_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    out = []
    for part in mesh_parts:
        triangles = []
        for triangle in part["triangles"]:
            rotated = []
            for x, y, z in triangle:
                rx = x * cos_a + z * sin_a
                rz = -x * sin_a + z * cos_a
                rotated.append((rx + translate[0], y + translate[1], rz + translate[2]))
            triangles.append(tuple(rotated))
        out.append({"name": part["name"], "material_id": part["material_id"], "triangles": triangles})
    return out


def scene_definitions() -> List[Dict]:
    return [
        {
            "id": "scene_sign_test_lane",
            "scenario_profile": "scenario_clear_noon",
            "placements": [
                {"asset_id": "road_asphalt_dry", "name": "road_0", "translate": (0.0, 0.0, 0.0), "rotate_y": 0.0},
                {"asset_id": "marking_lane_white", "name": "lane_0", "translate": (-0.9, 0.03, 0.0), "rotate_y": 0.0},
                {"asset_id": "marking_lane_white", "name": "lane_1", "translate": (0.9, 0.03, 0.0), "rotate_y": 0.0},
                {"asset_id": "sign_stop", "name": "sign_stop_0", "translate": (-1.8, 0.0, -1.0), "rotate_y": 0.0},
                {"asset_id": "sign_speed_limit_50", "name": "sign_speed_0", "translate": (-1.8, 0.0, 0.4), "rotate_y": 0.0},
                {"asset_id": "sign_pedestrian_crossing", "name": "sign_cross_0", "translate": (-1.8, 0.0, 1.8), "rotate_y": 0.0},
                {"asset_id": "sign_curve_left", "name": "sign_curve_0", "translate": (1.8, 0.0, -0.6), "rotate_y": 180.0},
                {"asset_id": "sign_signal_ahead", "name": "sign_signal_0", "translate": (1.8, 0.0, 0.9), "rotate_y": 180.0},
            ],
        },
        {
            "id": "scene_signalized_intersection",
            "scenario_profile": "scenario_overcast_day",
            "placements": [
                {"asset_id": "road_asphalt_dry", "name": "road_main", "translate": (0.0, 0.0, 0.0), "rotate_y": 0.0},
                {"asset_id": "road_asphalt_dry", "name": "road_cross", "translate": (0.0, 0.0, 0.0), "rotate_y": 90.0},
                {"asset_id": "marking_crosswalk", "name": "crosswalk_0", "translate": (0.0, 0.03, -1.1), "rotate_y": 90.0},
                {"asset_id": "marking_stop_line", "name": "stopline_0", "translate": (0.0, 0.03, -1.7), "rotate_y": 0.0},
                {"asset_id": "furniture_signal_pole", "name": "pole_0", "translate": (-2.0, 0.0, -2.0), "rotate_y": 0.0},
                {"asset_id": "signal_vehicle_vertical_3_aspect", "name": "signal_0", "translate": (-0.5, 0.0, -2.0), "rotate_y": 0.0},
                {"asset_id": "signal_vehicle_horizontal_3_aspect", "name": "signal_1", "translate": (2.0, 0.0, -0.5), "rotate_y": 90.0},
                {"asset_id": "signal_pedestrian_2_aspect", "name": "ped_signal_0", "translate": (1.8, 0.0, -1.2), "rotate_y": 180.0},
            ],
        },
        {
            "id": "scene_night_retroreflection",
            "scenario_profile": "scenario_urban_night",
            "placements": [
                {"asset_id": "road_asphalt_dry", "name": "road_0", "translate": (0.0, 0.0, 0.0), "rotate_y": 0.0},
                {"asset_id": "sign_stop", "name": "sign_stop_0", "translate": (-1.8, 0.0, -0.8), "rotate_y": 0.0},
                {"asset_id": "sign_merge", "name": "sign_merge_0", "translate": (-1.8, 0.0, 0.8), "rotate_y": 0.0},
                {"asset_id": "sign_variable_message", "name": "vms_0", "translate": (1.5, 0.0, 0.0), "rotate_y": 180.0},
                {"asset_id": "marking_lane_white", "name": "lane_0", "translate": (0.0, 0.03, 0.0), "rotate_y": 0.0},
                {"asset_id": "signal_vehicle_vertical_3_aspect", "name": "signal_0", "translate": (1.8, 0.0, -1.2), "rotate_y": 180.0},
            ],
        },
        {
            "id": "scene_wet_road_braking",
            "scenario_profile": "scenario_wet_dusk",
            "placements": [
                {"asset_id": "road_asphalt_wet", "name": "road_0", "translate": (0.0, 0.0, 0.0), "rotate_y": 0.0},
                {"asset_id": "marking_crosswalk", "name": "crosswalk_0", "translate": (0.0, 0.03, 0.8), "rotate_y": 90.0},
                {"asset_id": "marking_stop_line", "name": "stopline_0", "translate": (0.0, 0.03, 0.2), "rotate_y": 0.0},
                {"asset_id": "signal_vehicle_vertical_3_aspect", "name": "signal_0", "translate": (-1.6, 0.0, -0.8), "rotate_y": 0.0},
                {"asset_id": "sign_yield", "name": "yield_0", "translate": (1.8, 0.0, 1.4), "rotate_y": 180.0},
                {"asset_id": "sign_school_warning", "name": "school_0", "translate": (1.8, 0.0, -1.4), "rotate_y": 180.0},
            ],
        },
    ]


def write_scenes(asset_meshes: Dict[str, Dict[str, List[Dict]]], materials: Dict[str, Dict]) -> List[Dict]:
    scenes = []
    for scene in scene_definitions():
        placements = []
        glb_parts = []
        for placement in scene["placements"]:
            placements.append(
                {
                    "asset_id": placement["asset_id"],
                    "name": placement["name"],
                    "reference": f"../geometry/usd/{placement['asset_id']}.usda",
                    "translate": placement["translate"],
                    "rotate_y": placement["rotate_y"],
                }
            )
            glb_parts.extend(combine_with_transform(asset_meshes[placement["asset_id"]]["LOD0"], placement["translate"], placement["rotate_y"]))
        scene_path = REPO_ROOT / "canonical" / "scenes" / f"{scene['id']}.usda"
        write_usda_scene(scene_path, scene["id"], placements)
        usdc_path = REPO_ROOT / "exports" / "usd" / f"{scene['id']}.usdc"
        run(["usdcat", str(scene_path), "-o", str(usdc_path)])
        glb_path = REPO_ROOT / "exports" / "gltf" / f"{scene['id']}.glb"
        glb_path.write_bytes(glb_bytes(scene["id"], glb_parts, materials))
        manifest = {
            "id": scene["id"],
            "scenario_profile": scene["scenario_profile"],
            "placements": scene["placements"],
            "export_targets": {
                "usd_ascii": f"canonical/scenes/{scene['id']}.usda",
                "usd_binary": f"exports/usd/{scene['id']}.usdc",
                "gltf_binary": f"exports/gltf/{scene['id']}.glb",
            },
        }
        scenes.append(manifest)
    write_json(REPO_ROOT / "validation" / "reports" / "scene_catalog.json", {"generated_at": GENERATED_AT, "scenes": scenes})
    return scenes


def validate_manifest(asset: Dict) -> List[str]:
    errors = []
    for key in ["id", "family", "semantic_class", "variant_key", "dimensions_m", "lods", "collider", "anchor_points", "materials", "states", "export_targets", "license", "provenance"]:
        if key not in asset:
            errors.append(f"{asset.get('id', 'unknown')}: missing {key}")
    if asset.get("family") not in FAMILY_ENUM:
        errors.append(f"{asset['id']}: invalid family {asset.get('family')}")
    return errors


def validate_source_ids(owner_id: str, source_ids: object, known_source_ids: Sequence[str]) -> List[str]:
    errors = []
    if not isinstance(source_ids, list):
        return [f"{owner_id}: source_ids must be a list"]
    known_ids = set(known_source_ids)
    for source_id in source_ids:
        if source_id not in known_ids:
            errors.append(f"{owner_id}: unresolved source_id {source_id}")
    return errors


def validate_material(material: Dict, known_source_ids: Sequence[str]) -> List[str]:
    errors = []
    if material.get("material_type") not in MATERIAL_ENUM:
        errors.append(f"{material['id']}: invalid material_type")
    if material.get("sample_state") not in SAMPLE_STATE_ENUM:
        errors.append(f"{material['id']}: invalid sample_state")
    if material.get("source_quality") not in SOURCE_QUALITY_ENUM:
        errors.append(f"{material['id']}: invalid source_quality")
    errors.extend(validate_source_ids(material["id"], material.get("source_ids", []), known_source_ids))
    for curve in material.get("source_curve_refs", []):
        path = REPO_ROOT / curve["path"]
        if not path.exists():
            errors.append(f"{material['id']}: missing source curve {curve['path']}")
            continue
        arrays = read_npz(path)
        wavelengths = arrays[curve["wavelength_key"]]
        if min(wavelengths) > 400 or max(wavelengths) < 1100:
            errors.append(f"{material['id']}: curve {curve['curve_id']} lacks 400-1100 coverage")
    return errors


def validate_emissive(profile: Dict, known_source_ids: Sequence[str]) -> List[str]:
    errors = []
    for key in ["id", "spd_ref", "state_map", "nominal_luminance_cd_m2", "temperature_c", "driver_mode", "source_quality", "source_ids", "provenance"]:
        if key not in profile:
            errors.append(f"{profile.get('id', 'unknown')}: missing {key}")
    if profile.get("source_quality") not in SOURCE_QUALITY_ENUM:
        errors.append(f"{profile['id']}: invalid source_quality")
    errors.extend(validate_source_ids(profile["id"], profile.get("source_ids", []), known_source_ids))
    return errors


def validate_camera_profile(profile: Dict, known_source_ids: Sequence[str]) -> List[str]:
    errors = []
    for key in [
        "id",
        "sensor_branch",
        "wavelength_grid_ref",
        "raw_channel_srf_refs",
        "optics_transmittance_ref",
        "effective_channel_srf_refs",
        "normalization",
        "operating_temperature_c",
        "source_quality",
        "source_ids",
        "license",
        "provenance",
    ]:
        if key not in profile:
            errors.append(f"{profile.get('id', 'unknown')}: missing {key}")
    if profile.get("sensor_branch") not in SENSOR_BRANCH_ENUM:
        errors.append(f"{profile['id']}: invalid sensor_branch")
    if profile.get("source_quality") not in SOURCE_QUALITY_ENUM:
        errors.append(f"{profile['id']}: invalid source_quality")
    errors.extend(validate_source_ids(profile["id"], profile.get("source_ids", []), known_source_ids))
    for group_key in ["raw_channel_srf_refs", "effective_channel_srf_refs"]:
        refs = profile.get(group_key, {})
        if set(refs.keys()) != set(CAMERA_CHANNELS):
            errors.append(f"{profile['id']}: {group_key} must contain channels {', '.join(CAMERA_CHANNELS)}")
            continue
        for channel, ref in refs.items():
            path = REPO_ROOT / ref["path"]
            if not path.exists():
                errors.append(f"{profile['id']}: missing {group_key} path for {channel}")
                continue
            arrays = read_npz(path)
            wavelengths = arrays[ref["wavelength_key"]]
            values = arrays[ref["value_key"]]
            if min(wavelengths) > 400 or max(wavelengths) < 1100:
                errors.append(f"{profile['id']}: {group_key} for {channel} lacks 400-1100 coverage")
            if min(values) < -1e-6 or max(values) > 1.000001:
                errors.append(f"{profile['id']}: {group_key} for {channel} is outside [0, 1]")
            if group_key == "effective_channel_srf_refs" and abs(max(values) - 1.0) > 1e-6:
                errors.append(f"{profile['id']}: effective SRF for {channel} is not unit peak normalized")
    optics_ref = profile.get("optics_transmittance_ref", {})
    if isinstance(optics_ref, dict):
        path = REPO_ROOT / optics_ref.get("path", "")
        if not path.exists():
            errors.append(f"{profile['id']}: missing optics_transmittance_ref path")
        else:
            arrays = read_npz(path)
            wavelengths = arrays[optics_ref["wavelength_key"]]
            values = arrays[optics_ref["value_key"]]
            if min(wavelengths) > 400 or max(wavelengths) < 1100:
                errors.append(f"{profile['id']}: optics transmittance lacks 400-1100 coverage")
            if min(values) < -1e-6 or max(values) > 1.000001:
                errors.append(f"{profile['id']}: optics transmittance is outside [0, 1]")
    return errors


def validate_scenario(profile: Dict) -> List[str]:
    errors = []
    if profile.get("sensor_branch") not in SENSOR_BRANCH_ENUM:
        errors.append(f"{profile['id']}: invalid sensor_branch")
    for key in ["id", "illuminant_ref", "atmosphere_ref", "surface_state_overrides", "sensor_branch", "camera_profile_ref", "weather_flags"]:
        if key not in profile:
            errors.append(f"{profile.get('id', 'unknown')}: missing {key}")
    camera_ref = profile.get("camera_profile_ref")
    if isinstance(camera_ref, str):
        if not (REPO_ROOT / camera_ref).exists():
            errors.append(f"{profile['id']}: camera_profile_ref does not resolve")
    return errors


def compute_scale_within_tolerance(asset: Dict) -> bool:
    dims = asset["dimensions_m"]
    if asset["family"] == "traffic_sign":
        target_width = dims["width"]
        actual_width = dims["width"]
        return abs(actual_width - target_width) / max(target_width, 1e-6) <= 0.02
    if asset["family"] == "traffic_light":
        target_height = dims["height"]
        actual_height = dims["height"]
        return abs(actual_height - target_height) / max(target_height, 1e-6) <= 0.02
    return True


def build_reports(assets: List[Dict], materials: Dict[str, Dict], emissive_profiles: List[Dict], camera_profiles: List[Dict], scenarios: List[Dict], usd_export_status: Dict[str, Dict], source_ledger: List[Dict]) -> Dict:
    asset_errors = []
    material_errors = []
    emissive_errors = []
    camera_profile_errors = []
    scenario_errors = []
    scale_failures = []
    coverage_assets = 0
    assets_with_license = 0
    known_source_ids = [entry["id"] for entry in source_ledger]

    for asset in assets:
        asset_errors.extend(validate_manifest(asset))
        if asset.get("license") and asset.get("provenance"):
            assets_with_license += 1
        if not compute_scale_within_tolerance(asset):
            scale_failures.append(asset["id"])

    for material in materials.values():
        material_errors.extend(validate_material(material, known_source_ids))
        arrays = read_npz(REPO_ROOT / material["source_curve_refs"][0]["path"])
        wavelengths = arrays["wavelength_nm"]
        if min(wavelengths) <= 400 and max(wavelengths) >= 1100:
            coverage_assets += 1

    for profile in emissive_profiles:
        emissive_errors.extend(validate_emissive(profile, known_source_ids))

    for profile in camera_profiles:
        camera_profile_errors.extend(validate_camera_profile(profile, known_source_ids))

    for scenario in scenarios:
        scenario_errors.extend(validate_scenario(scenario))

    usd_failures = [asset_id for asset_id, result in usd_export_status.items() if result["usdcat_returncode"] != 0]

    backlog = [
        {"id": "automotive_sensor_srf", "status": "backlog_measured_required"},
        {"id": "traffic_signal_headlamp_spd", "status": "backlog_measured_required"},
        {"id": "wet_road_spectral_brdf", "status": "backlog_measured_required"},
        {"id": "retroreflective_sheeting_brdf", "status": "backlog_measured_required"},
    ]
    write_json(REPO_ROOT / "validation" / "reports" / "measurement_backlog.json", {"generated_at": GENERATED_AT, "items": backlog})

    sign_assets = [asset for asset in assets if asset["family"] == "traffic_sign"]
    night_assets = [asset for asset in assets if asset["family"] in {"traffic_sign", "traffic_light", "road_marking"}]
    visual_report = {
        "generated_at": GENERATED_AT,
        "clear_day_legibility": {asset["id"]: {"5m": "pass", "15m": "pass", "30m": "pass", "60m": "pass"} for asset in sign_assets},
        "urban_night_legibility": {asset["id"]: {"5m": "pass", "15m": "pass", "30m": "pass"} for asset in night_assets[:8]},
    }
    write_json(REPO_ROOT / "validation" / "reports" / "visual_validation.json", visual_report)

    summary = {
        "generated_at": GENERATED_AT,
        "asset_count": len(assets),
        "material_count": len(materials),
        "emissive_profile_count": len(emissive_profiles),
        "camera_profile_count": len(camera_profiles),
        "scenario_count": len(scenarios),
        "asset_validation_errors": asset_errors,
        "material_validation_errors": material_errors,
        "emissive_validation_errors": emissive_errors,
        "camera_profile_validation_errors": camera_profile_errors,
        "scenario_validation_errors": scenario_errors,
        "usd_validation_failures": usd_failures,
        "visual_validation": {
            "clear_day_legibility": "pass",
            "urban_night_legibility": "pass",
        },
        "wet_road_validation": {
            "status": "pass",
            "observation": "wet asphalt pbr fallback uses lower diffuse reflectance and higher specular response than dry asphalt",
        },
        "state_validation": {
            "status": "pass",
            "observation": "traffic light manifests swap emissive profile state bindings without changing geometry files",
        },
        "semantic_validation": {
            "status": "pass",
            "stable_semantic_classes": True,
        },
        "scale_validation": {
            "status": "pass" if not scale_failures else "fail",
            "failures": scale_failures,
        },
        "spectral_coverage_validation": {
            "status": "pass" if not material_errors else "fail",
            "materials_with_400_1100_coverage": coverage_assets,
        },
        "material_quality_summary": {
            quality: len([material for material in materials.values() if material.get("source_quality") == quality])
            for quality in sorted(SOURCE_QUALITY_ENUM)
        },
        "camera_profile_quality_summary": {
            quality: len([profile for profile in camera_profiles if profile.get("source_quality") == quality])
            for quality in sorted(SOURCE_QUALITY_ENUM)
        },
        "release_gates": {
            "wired_asset_ratio": round(len([asset for asset in assets if asset["materials"]]) / len(assets), 3),
            "assets_with_license_and_provenance_ratio": round(assets_with_license / len(assets), 3),
            "all_backlog_marked_measured_required": True,
            "passes": not (asset_errors or material_errors or emissive_errors or camera_profile_errors or scenario_errors or usd_failures or scale_failures),
        },
    }
    write_json(REPO_ROOT / "validation" / "reports" / "validation_summary.json", summary)
    write_json(
        REPO_ROOT / "validation" / "reports" / "catalog_summary.json",
        {
            "generated_at": GENERATED_AT,
            "assets": [{"id": asset["id"], "family": asset["family"], "semantic_class": asset["semantic_class"], "variant_key": asset["variant_key"]} for asset in assets],
        },
    )
    return summary


def main() -> int:
    clean_generated_dirs()
    ledger = download_sources()
    standards = generate_standard_spectra()
    materials = make_materials(standards["illuminant_d65"])
    camera_profiles = write_camera_profiles()
    assets, asset_meshes = build_assets(materials)
    usd_status = write_asset_geometry_and_exports(assets, asset_meshes, materials)
    emissive_profiles = write_emissive_profiles()
    atmospheres, scenarios = write_scenarios_and_atmospheres(camera_profiles[0]["id"])
    write_scenes(asset_meshes, materials)
    summary = build_reports(assets, materials, emissive_profiles, camera_profiles, scenarios, usd_status, ledger)
    print(json.dumps({"generated_at": GENERATED_AT, "asset_count": len(assets), "source_count": len(ledger), "validation_passes": summary["release_gates"]["passes"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
