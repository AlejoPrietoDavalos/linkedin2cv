from pathlib import Path
import os
import shutil

# Base paths
PATH_DATA_DIR = Path("data")
PATH_ASSETS_DIR = Path("assets")

# Assets paths
PATH_IMAGES_DIR = PATH_ASSETS_DIR / "images"
PATH_FONTS = PATH_ASSETS_DIR / "fonts"
PATH_DEFAULT_CONFIG_DIR = PATH_ASSETS_DIR / "default_config"
PATH_SECTIONS_DIR = PATH_ASSETS_DIR / "sections"

# Data paths
PATH_RUNTIME_CONFIG_DIR = PATH_DATA_DIR / "config"
PATH_LINKEDIN_SNAPSHOTS = PATH_DATA_DIR / "linkedin_snapshots"

# Runtime config files
PATH_KEYWORDS = PATH_RUNTIME_CONFIG_DIR / "keywords.json"
PATH_JOB_IDS = PATH_RUNTIME_CONFIG_DIR / "job_ids.json"

# Environment variables
ENV_FOLDER_DATA = "FOLDER_DATA"
ENV_PHOTO_NAME = "PHOTO_NAME"

FOLDER_DATA = os.getenv(ENV_FOLDER_DATA)
PHOTO_NAME = os.getenv(ENV_PHOTO_NAME)

if not FOLDER_DATA:
    raise RuntimeError(f"La variable de entorno '{ENV_FOLDER_DATA}' es requerida.")
if not PHOTO_NAME:
    raise RuntimeError(f"La variable de entorno '{ENV_PHOTO_NAME}' es requerida.")

# Derived paths
PATH_FOLDER_DATA = PATH_LINKEDIN_SNAPSHOTS / FOLDER_DATA
if not PATH_FOLDER_DATA.exists():
    raise RuntimeError(
        f"No hay datos en: '{PATH_FOLDER_DATA}'. "
        "Revisar variable de entorno o agregar datos a la carpeta."
    )

PATH_LINKEDIN_PROFILE = PATH_FOLDER_DATA / "Profile.csv"
PATH_LINKEDIN_POSITIONS = PATH_FOLDER_DATA / "Positions.csv"
PATH_LINKEDIN_EDUCATION = PATH_FOLDER_DATA / "Education.csv"

PATH_PHOTO = PATH_IMAGES_DIR / PHOTO_NAME
PATH_PYTHON_ICON = PATH_IMAGES_DIR / "python_icon.png"
PATH_PDF_BASENAME = PATH_FOLDER_DATA.stem


def ensure_runtime_config_file(filename: str) -> Path:
    path_runtime = PATH_RUNTIME_CONFIG_DIR / filename
    if path_runtime.exists():
        return path_runtime

    path_default = PATH_DEFAULT_CONFIG_DIR / filename
    if not path_default.exists():
        raise RuntimeError(f"No existe archivo default requerido: {path_default}")

    PATH_RUNTIME_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path_default, path_runtime)
    return path_runtime


def ensure_data_structure() -> None:
    PATH_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PATH_LINKEDIN_SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    PATH_RUNTIME_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_path_pdf_output(full_name: str) -> Path:
    return PATH_DATA_DIR / f"Curriculum - {full_name}.pdf"
