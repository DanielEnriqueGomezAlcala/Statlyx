from PIL import Image as PILImage
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

from functions.write_presentation.constants import (
    SLIDE_H, MARGIN_L, MARGIN_T, CONTENT_W,
)
from functions.write_presentation.helpers import (
    add_text_box, add_image, real_height, remove_placeholders,
)

def chart_slide(presentacion: Presentation, title: str, img_path: str | None, text: str | None, img_path2: str | None = None):
    layout = presentacion.slide_layouts[1]
    slide = presentacion.slides.add_slide(layout)
    remove_placeholders(slide)

    add_text_box(slide, title, left=MARGIN_L, top=MARGIN_T, width=CONTENT_W, height=Inches(0.55), size=18, bold=True)

    top_content = Inches(1.15)
    available_h = SLIDE_H - top_content - Inches(0.22)

    TEXT_RESERVE = Inches(1.1) if text else Inches(0)
    GAP_CT       = Inches(0.15) if text else Inches(0)
    GAP_H        = Inches(0.2)

    chart_area_h = available_h - TEXT_RESERVE - GAP_CT

    if img_path and img_path2:
        right_col_w  = int(CONTENT_W * 0.5)
        left_col_w   = int(CONTENT_W - right_col_w - GAP_H)
        right_col_left = MARGIN_L + left_col_w + GAP_H

        line_w = left_col_w
        line_h = real_height(img_path, line_w)
        if line_h > chart_area_h:
            with PILImage.open(img_path) as im:
                orig_w, orig_h = im.size
            line_w = int(chart_area_h * orig_w / orig_h)
            line_h = chart_area_h
        line_left = MARGIN_L + (left_col_w - line_w) // 2
        line_top  = top_content + (chart_area_h - line_h) // 2

        add_image(slide, img_path, line_left, line_top, line_w)

        table_w = right_col_w
        table_h = real_height(img_path2, table_w)
        if table_h > chart_area_h:
            with PILImage.open(img_path2) as im:
                tw, th = im.size
            table_w = int(chart_area_h * tw / th)
            table_h = chart_area_h
        table_left = right_col_left + (right_col_w - table_w) // 2
        table_top  = top_content + (chart_area_h - table_h) // 2
        table_top  = max(table_top, top_content)

        add_image(slide, img_path2, table_left, table_top, table_w)

        if text:
            text_top = top_content + chart_area_h + GAP_CT
            text_h   = SLIDE_H - text_top - Inches(0.22)
            add_text_box(
                slide, text,
                left=MARGIN_L, top=text_top,
                width=CONTENT_W, height=text_h,
                size=12,
            )

    elif img_path:
        if text:
            TEXT_COL_W = Inches(3.8)
            IMG_COL_W  = int(CONTENT_W - TEXT_COL_W - GAP_H)
            text_left  = MARGIN_L + IMG_COL_W + GAP_H
        else:
            IMG_COL_W = int(CONTENT_W)
            text_left = None

        img_area_h = available_h
        line_w = IMG_COL_W
        line_h = real_height(img_path, line_w)
        if line_h > img_area_h:
            with PILImage.open(img_path) as im:
                orig_w, orig_h = im.size
            line_w = int(img_area_h * orig_w / orig_h)
            line_h = img_area_h
        line_left = MARGIN_L + (IMG_COL_W - line_w) // 2
        line_top  = top_content + (img_area_h - line_h) // 2

        add_image(slide, img_path, line_left, line_top, line_w)

        if text and text_left is not None:
            add_text_box(
                slide, text,
                left=text_left, top=top_content,
                width=TEXT_COL_W, height=available_h,
                size=12, align=PP_ALIGN.JUSTIFY,
            )

    elif text:
        add_text_box(
            slide, text,
            left=MARGIN_L, top=top_content,
            width=CONTENT_W, height=available_h,
            size=14,
        )
