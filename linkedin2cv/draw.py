from typing import Optional
from pathlib import Path

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer, Flowable
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.colors import Color

from linkedin2cv.models import LinkedinData, StyleCV, SizesCV

DIST_PYTHON_ICON_TO_TITLE = 4
DIST_BETWEEN_LINKS = 1
DIST_FULL_NAME_TO_HEADLINE = 6
DIST_HEADLINE_TO_LINKS = 4
DIST_LINE_SPACING_LEFT = 3 * mm  # Espaciado desde la barra lateral (izquierda)
DIST_LINE_SPACING_RIGHT = 3 * mm  # Espaciado desde el borde derecho
LINE_THICKNESS = 0.5  # Grosor de la línea horizontal
DIST_LINKS_TO_SUMMARY = 15
LEN_PYTHON_ICON = 3

SIDEBAR_TO_BODY_GAP = 0 * mm
PHOTO_TOP_PADDING = 10 * mm
SPACER_HEIGHT = 6
FRAME_MARGIN_LEFT = 1 * mm
FRAME_MARGIN_RIGHT = 1 * mm


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
        info_lines.append(f"<br/><b>➤➤ Mi página web ➤➤</b> <a href='{url_website}'>{url_website}</a>")
    if url_github:
        info_lines.append(f"<b>➤➤ GitHub ➤➤</b> <a href='{url_github}'>{url_github}</a>")

    for line in info_lines:
        content.append(Paragraph(line, styles["SidebarLinks"]))
        content.append(Spacer(1, DIST_BETWEEN_LINKS))

    # Summary del perfil
    content.append(Spacer(1, DIST_LINKS_TO_SUMMARY))
    content.append(Paragraph(data.profile.summary, styles["SidebarText"]))

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
        page_width: int,
        page_height: int
) -> list[tuple[float, float, float, float]]:
    class IconTitle(Flowable):
        def __init__(self, img_path: Path, text: str, style: ParagraphStyle, img_size: float):
            super().__init__()
            self.img_path = img_path
            self.text = text
            self.style = style
            self.img_size = img_size
            self.p = Paragraph(self.text, self.style)
            self._height = 0

        def wrap(self, availWidth, availHeight):
            text_w, text_h = self.p.wrap(availWidth - self.img_size - DIST_PYTHON_ICON_TO_TITLE, availHeight)
            self._p_width = text_w
            self._p_height = text_h
            self._height = max(text_h, self.img_size)
            return text_w + self.img_size + DIST_PYTHON_ICON_TO_TITLE, self._height

        def draw(self):
            y_img = (self._height - self.img_size) / 2
            self.canv.drawImage(
                str(self.img_path), 0, y_img,
                width=self.img_size, height=self.img_size,
                preserveAspectRatio=True, mask='auto'
            )
            self.p.drawOn(self.canv, self.img_size + DIST_PYTHON_ICON_TO_TITLE, (self._height - self._p_height) / 2)

    x = sizes_cv.margin + sizes_cv.column_left_wifth + SIDEBAR_TO_BODY_GAP
    width = page_width - x - sizes_cv.margin
    y_start = page_height - sizes_cv.margin
    usable_height = y_start - sizes_cv.margin

    icon_size = LEN_PYTHON_ICON * mm
    elements: list[Flowable] = []
    lines_to_draw: list[tuple[float, float, float, float]] = []  # Lista para las líneas

    for position in data.positions:
        elements.append(IconTitle(path_python_icon, position.text_title, styles["JobTitle"], icon_size))
        elements.append(Paragraph(f"➤ {position.text_sub_title}", styles["JobSubTitle"]))
        elements.append(Paragraph(position.description or "Sin descripción", styles["JobDesc"]))
        elements.append(Spacer(1, SPACER_HEIGHT))

    frame = Frame(x, sizes_cv.margin, width, usable_height, showBoundary=0)

    while elements:
        frame.addFromList(elements, c)
        if elements:  # Si quedan elementos sin dibujar, ir a nueva página
            c.showPage()
            draw_background(c=c, color=style_cv.background, page_width=page_width, page_height=page_height)
            draw_sidebar(
                c=c,
                data=data,
                sizes_cv=sizes_cv,
                style_cv=style_cv,
                styles=styles,
                age=0,
                location="",
                page_height=page_height
            )
            frame = Frame(x, sizes_cv.margin, width, usable_height, showBoundary=0)

        # Dibujar las líneas de separación después de agregar contenido a la página
        y_cursor = y_start  # Inicia al principio de la página
        for i, block in enumerate(elements):
            line_y = y_cursor - block.height
            lines_to_draw.append((
                x + DIST_LINE_SPACING_LEFT,
                line_y,
                page_width - sizes_cv.margin - DIST_LINE_SPACING_RIGHT,
                line_y
            ))
            y_cursor -= block.height + LINE_THICKNESS  # Ajustar la posición de las líneas

    return lines_to_draw  # Retorna las líneas que se deben dibujar

