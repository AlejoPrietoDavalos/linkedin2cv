"""Textos visibles y formato hardcodeado del PDF."""

from typing import Optional


SUMMARY_TECH_STACK_LABEL = "● Stack tecnológico:"

REPLACE_BULLET_ARROW = (" ➣", "<br/>➣")
REPLACE_BULLET_DOT = (" ●", "<br/><br/>●")
REPLACE_BULLET_SQUARE = (" ■", "<br/>■")

LABEL_AGE = "Edad:"
LABEL_LOCATION = "Ubicación:"
LABEL_MAIL = "Mail:"
LABEL_WEBSITE_HEADER = "➤➤ Mi página web ➤➤"
LABEL_WEBSITE_ES = " Español"
LABEL_WEBSITE_EN = " Inglés"
LABEL_GITHUB = "➤➤ GitHub"
LABEL_LINKEDIN = "➤➤ LinkedIn"

SECTION_ABOUT_ME_TITLE = "Sobre mi"
SECTION_ABOUT_ME_TEXT = (
    "Programo soluciones end-to-end en <b>Python</b>, soy resolutivo y me motivan mucho los desafíos.<br/>"
    "Con gran interés en colaborar en proyectos de software/datos junto a otros profesionales."
)
SECTION_GOAL_TITLE = "Objetivo profesional"
SECTION_GOAL_TEXT = (
    "Poder aplicar <b>Python</b> en todo, siempre dispuesto a aprender nuevas tecnologías, "
    "especialmente en <b>Ciencia de Datos</b>."
)
SECTION_TECH_SUMMARY_TITLE = "Resumen técnico"
SECTION_PROJECTS_TITLE = "Proyectos personales"
SECTION_PROJECTS_TEXT = (
    "● Tool para músicos usando Machine Learning.<br/>"
    "➣ Descomposición de instrumentos en pistas.<br/>"
    "➣ Cálculo de tempo, análisis de espectrograma.<br/><br/>"
    "● Teledetección de barcos para pesca ilegal.<br/>"
    "➣ Análisis de imágenes satelitales SAR.<br/>"
    "➣ Deep Learning para detección de objetos.<br/><br/>"
    "● Chatbot de Whatsapp con IA para restaurant.<br/>"
    "➣ El producto final tomará el pedido del usuario.<br/><br/>"
    "● Automatizaciones para streaming.<br/>"
    "➣ Desarrollé un juego en Python con interacción.<br/>"
    "➣ Scripting para resolver tareas repetitivas.<br/>"
)
SECTION_STACK_TITLE = "Stack tecnológico"

JOB_SUBTITLE_PREFIX = "➤➤"
LABEL_CURRENTLY = "Actualidad"
JOB_DESCRIPTION_FALLBACK = "Sin descripción"

FINAL_CREDIT_URL = "https://alejoprietodavalos.github.io/portfolio-es/posts/linkedin-to-cv/"
FINAL_CREDIT_TEXT = "Curriculum programado/generado por mí a partir de los datos extraídos de LinkedIn."


def format_sidebar_info_line(label: str, value: str) -> str:
    return f"<b>{label}</b> {value}"


def format_website_line(*, url_es: str, url_en: str) -> str:
    return (
        f"<b>{LABEL_WEBSITE_HEADER}</b>"
        f"<a href='{url_es}'>{LABEL_WEBSITE_ES}</a> - "
        f"<a href='{url_en}'>{LABEL_WEBSITE_EN}</a>"
    )


def format_link_line(*, label: str, url: str) -> str:
    return f"<b><a href='{url}'>{label}</a></b>"


def format_position_subtitle(*, company_name: str, started_on: str) -> str:
    return f"{company_name} ({started_on})"


def apply_visible_text_replacements(value: Optional[str]) -> Optional[str]:
    if not isinstance(value, str):
        return value
    value = value.replace(*REPLACE_BULLET_ARROW)
    value = value.replace(*REPLACE_BULLET_DOT)
    value = value.replace(*REPLACE_BULLET_SQUARE)
    return value
