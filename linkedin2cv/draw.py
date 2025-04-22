from typing import Optional, List, Tuple
from pathlib import Path
import re

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer, Flowable
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.colors import Color

from linkedin2cv.models import LinkedinData, StyleCV, SizesCV

TECH_STACK_LABEL = "● Stack tecnológico:"
DIST_BETWEEN_TITLE_SIDEBAR_TO_TEXT = 5
DIST_PYTHON_ICON_TO_TITLE = 4
DIST_BETWEEN_LINKS = 1
DIST_FULL_NAME_TO_HEADLINE = 8
DIST_HEADLINE_TO_LINKS = 4
DIST_LINE_SPACING_LEFT = 3 * mm  # Espaciado desde la barra lateral (izquierda)
DIST_LINE_SPACING_RIGHT = 3 * mm  # Espaciado desde el borde derecho
LINE_THICKNESS = 0.5  # Grosor de la línea horizontal
DIST_BETWEEN_TITLE_TEXT_SIDEBAR = 15
LEN_PYTHON_ICON = 3
SIDEBAR_TO_BODY_GAP = 2 * mm
PHOTO_TOP_PADDING = 10 * mm
SPACER_HEIGHT = 15
FRAME_MARGIN_LEFT = 1 * mm
FRAME_MARGIN_RIGHT = 1 * mm


def clean_text(text: str) -> str:
    """
    Elimina los espacios en blanco y las etiquetas <br/> al principio y al final del texto.
    """
    # Eliminar espacios en blanco al principio y al final
    cleaned_text = text.strip()
    
    # Eliminar etiquetas <br/> al principio y al final
    cleaned_text = re.sub(r"^<br/>|<br/>$", "", cleaned_text)
    
    return cleaned_text

def remove_https(url: str) -> str:
    return url.replace('https://', '')


def draw_background(*, c: Canvas, color: Color, page_width: int, page_height: int) -> None:
    c.setFillColor(color)
    c.rect(0, 0, page_width, page_height, fill=True, stroke=0)


def draw_photo(
        *,
        c: Canvas,
        path_photo: Optional[Path],
        sizes_cv: SizesCV,
        page_height: int,
        is_photo_circle: bool = True
) -> None:
    if path_photo and path_photo.exists():
        x = sizes_cv.margin_left + (sizes_cv.column_left_wifth - sizes_cv.photo_size) / 2
        y = page_height - sizes_cv.photo_size - PHOTO_TOP_PADDING

        if is_photo_circle:
            radius = sizes_cv.photo_size / 2
            center_x = x + radius
            center_y = y + radius
            c.saveState()
            path = c.beginPath()
            path.circle(center_x, center_y, radius)
            c.clipPath(path, stroke=0)

        c.drawImage(str(path_photo), x, y,
                            width=sizes_cv.photo_size, height=sizes_cv.photo_size,
                            preserveAspectRatio=True, mask='auto')

        if is_photo_circle:
            c.restoreState()


def draw_title_text_sidebar(*, title: str, text: str, styles: StyleSheet1) -> List[Paragraph | Spacer]:
    return [
        Paragraph(f"<b>{title}</b>", styles["SidebarTitle"]),
        Spacer(1, DIST_BETWEEN_TITLE_SIDEBAR_TO_TEXT),
        Paragraph(clean_text(text), styles["SidebarText"])
    ]

def draw_sidebar(
        *,
        c: Canvas,
        data: LinkedinData,
        sizes_cv: SizesCV,
        style_cv: StyleCV,
        styles: StyleSheet1,
        age: int,
        location: str,
        page_height: int,
        url_website: Optional[str] = None,
        url_github: Optional[str] = None,
) -> None:
    c.setFillColor(style_cv.sidebar_panel)
    c.rect(sizes_cv.margin_left, 0, sizes_cv.column_left_wifth, page_height, fill=True, stroke=0)

    photo_bottom = page_height - sizes_cv.photo_size - PHOTO_TOP_PADDING
    sidebar_text_bottom = sizes_cv.margin + 5 * mm
    sidebar_height = photo_bottom - sidebar_text_bottom

    content = []
    content.append(Paragraph(data.profile.full_name, styles["SidebarName"]))
    content.append(Spacer(1, DIST_FULL_NAME_TO_HEADLINE))
    content.append(Paragraph(data.profile.headline, styles["SidebarHeadline"]))
    content.append(Spacer(1, DIST_HEADLINE_TO_LINKS))

    # Info personal (edad, links)
    info_lines = []
    if age:
        info_lines.append(f"<b>Edad:</b> {age}")
    if location:
        info_lines.append(f"<b>Ubicación:</b> {location}")
    if url_website:
        info_lines.append(f"<b>➤➤ Mi página web ➤➤</b> <a href='{url_website}'>{remove_https(url_website)}</a>")
    if url_github:
        info_lines.append(f"<b>➤➤ GitHub ➤➤</b> <a href='{url_github}'>{remove_https(url_github)}</a>")

    for line in info_lines:
        content.append(Paragraph(line, styles["SidebarLinks"]))
        content.append(Spacer(1, DIST_BETWEEN_LINKS))

    
    # Verifico si TECH_STACK_LABEL está.
    if TECH_STACK_LABEL not in data.profile.summary:
        raise ValueError(f"El texto '{TECH_STACK_LABEL}' no está en summary.")



    # Separo el resumen en dos partes.
    # TODO: Poner en linkedin y splitearlo.
    TEXT_SOBRE_MI = (
        "Programo soluciones end-to-end en <b>Python</b>, soy resolutivo y me motivan mucho los desafíos.<br/>"
        "Con gran interés en colaborar en proyectos de software/datos junto a otros profesionales."
    )
    TEXT_OBJETIVO_PROFESIONAL = (
        "Poder aplicar <b>Python</b> donde sea posible, especialmente en <b>Ciencia de Datos</b>."
    )
    TEXT_PERSONAL_PROJECTS = (
        "● Tool para músicos usando Machine Learning.<br/>"
        "➣ Descomposición de instrumentos en pistas.<br/>"
        "➣ Cálculo de tempo, análisis de espectrograma,...<br/><br/>"

        "● Teledetección de barcos para pesca ilegal.<br/>"
        "➣ Deep Learning para detección de objetos.<br/>"
        "➣ Pausada por falta de hardware.<br/><br/>"

        "● Chatbot de Whatsapp con IA para restaurant.<br/>"
        "➣ El producto final tomará el pedido del usuario.<br/><br/>"

        "● Automatizaciones para streamer.<br/>"
        "➣ Desarrollé un juego en Python con interacción.<br/>"
        "➣ Scripting para resolver tareas repetitivas.<br/>"
    )
    # TODO: Poner en linkedin y splitearlo.
    summary_parts = data.profile.summary.split(TECH_STACK_LABEL)
    summary_parts = [p.strip() for p in summary_parts]

    content.append(Spacer(1, DIST_BETWEEN_TITLE_TEXT_SIDEBAR))
    content.extend(draw_title_text_sidebar(title="Sobre mi", text=TEXT_SOBRE_MI, styles=styles))
    content.append(Spacer(1, DIST_BETWEEN_TITLE_TEXT_SIDEBAR))
    content.extend(draw_title_text_sidebar(title="Objetivo profesional", text=TEXT_OBJETIVO_PROFESIONAL, styles=styles))
    content.append(Spacer(1, DIST_BETWEEN_TITLE_TEXT_SIDEBAR))
    content.extend(draw_title_text_sidebar(title="Resumen técnico", text=summary_parts[0], styles=styles))
    content.append(Spacer(1, DIST_BETWEEN_TITLE_TEXT_SIDEBAR))
    content.extend(draw_title_text_sidebar(title="Proyectos personales", text=TEXT_PERSONAL_PROJECTS, styles=styles))
    content.append(Spacer(1, DIST_BETWEEN_TITLE_TEXT_SIDEBAR))
    content.extend(draw_title_text_sidebar(title="Stack tecnológico", text=summary_parts[1], styles=styles))


    frame = Frame(
        sizes_cv.margin_left + FRAME_MARGIN_LEFT,
        sidebar_text_bottom,
        sizes_cv.column_left_wifth - FRAME_MARGIN_LEFT - FRAME_MARGIN_RIGHT,
        sidebar_height,
        showBoundary=0
    )

    frame.addFromList(content, c)


def draw_positions(
    *,
    c: Canvas,
    data: LinkedinData,
    sizes_cv: SizesCV,
    style_cv: StyleCV,
    styles: StyleSheet1,
    path_python_icon: Path,
    page_width: float,
    page_height: float
) -> List[Tuple[float, float, float, float]]:
    class IconTitle(Flowable):
        def __init__(
            self,
            img_path: Path,
            text: str,
            style: ParagraphStyle,
            img_size: float
        ) -> None:
            super().__init__()
            self.img_path = img_path
            self.p = Paragraph(text, style)
            self.img_size = img_size
            self._height = 0

        def wrap(self, availWidth: float, availHeight: float) -> Tuple[float, float]:
            text_w, text_h = self.p.wrap(
                availWidth - self.img_size - DIST_PYTHON_ICON_TO_TITLE,
                availHeight
            )
            self._height = max(text_h, self.img_size)
            return text_w + self.img_size + DIST_PYTHON_ICON_TO_TITLE, self._height

        def draw(self) -> None:
            y_img = (self._height - self.img_size) / 2
            self.canv.drawImage(
                str(self.img_path), 0, y_img,
                width=self.img_size, height=self.img_size,
                preserveAspectRatio=True, mask="auto"
            )
            self.p.drawOn(
                self.canv,
                self.img_size + DIST_PYTHON_ICON_TO_TITLE,
                (self._height - self.p.height) / 2
            )

    x = sizes_cv.margin_left + sizes_cv.column_left_wifth + SIDEBAR_TO_BODY_GAP
    x_i = x + DIST_LINE_SPACING_LEFT
    
    width = page_width - x - sizes_cv.margin
    y_cursor = page_height - sizes_cv.margin
    usable_height = y_cursor - sizes_cv.margin

    icon_size = LEN_PYTHON_ICON * mm
    lines: List[Tuple[float, float, float, float]] = []
    icon_ys: List[float] = []  # lista para coordenadas Y de iconos

    for idx, position in enumerate(data.positions):
        # 1) Crear flowable y medir altura del icono
        icon = IconTitle(
            path_python_icon,
            f"<b>{position.text_title}</b>",
            styles["JobTitle"],
            icon_size
        )
        _, h_icon = icon.wrap(width, usable_height)

        # calcular la Y donde se dibujará el icono
        y_icon = y_cursor - h_icon
        icon_ys.append(y_icon)

        # medir subtítulo y descripción
        subtitle = Paragraph(f"<b>➤➤ {position.text_sub_title}</b>", styles["JobSubTitle"])
        _, h_sub = subtitle.wrap(width, usable_height)
        desc = Paragraph(position.description or "Sin descripción", styles["JobDesc"])
        _, h_desc = desc.wrap(width, usable_height)

        # altura total del bloque
        block_height = h_icon + h_sub + h_desc + SPACER_HEIGHT + LINE_THICKNESS

        # 2) salto de página si no cabe el bloque
        if y_cursor - block_height < sizes_cv.margin:
            c.showPage()
            draw_background(c=c, color=style_cv.background, page_width=page_width, page_height=page_height)
            draw_sidebar(c=c, data=data, sizes_cv=sizes_cv, style_cv=style_cv, styles=styles,
                         age=0, location="", page_height=page_height)
            y_cursor = page_height - sizes_cv.margin
            # recalcular Y del icono tras salto
            y_icon = y_cursor - h_icon
            icon_ys[-1] = y_icon

        # 3) dibujar icono y texto
        icon.drawOn(c, x, y_icon)
        y_cursor = y_icon - LINE_THICKNESS
        subtitle.drawOn(c, x, y_cursor - h_sub)
        y_cursor -= h_sub + LINE_THICKNESS
        desc.drawOn(c, x, y_cursor - h_desc)
        y_cursor -= h_desc + SPACER_HEIGHT

        # 4) línea separadora (entre bloques)
        if idx < len(data.positions) - 1:
            #y_line = y_cursor + (SPACER_HEIGHT / 2)
            y_line = y_icon
            lines.append((
                x + DIST_LINE_SPACING_LEFT,
                y_line,
                page_width - sizes_cv.margin - DIST_LINE_SPACING_RIGHT,
                y_line
            ))

    final_text = Paragraph(
        """<br/><br/><br/><br/><br/><br/><a href="https://github.com/AlejoPrietoDavalos/linkedin2cv">
        <i><b>Curriculum programado/generado por mí a partir de los datos extraídos de LinkedIn.</b></i>
        </a>""",
        styles["JobDesc"]
    )
    _, h_final = final_text.wrap(width, usable_height)
    final_text.drawOn(c, x, y_cursor - h_final)
    y_cursor -= h_final + SPACER_HEIGHT

    return lines, x_i