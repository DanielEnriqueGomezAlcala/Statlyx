import os

from PIL import Image as PILImage
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def set_text(tf, text: str, size: int = 18, bold: bool = False, color: tuple = (33, 33, 33), align=PP_ALIGN.LEFT):
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color)

def add_text_box(slide, text: str, left, top, width, height, size: int = 14, bold: bool = False, color: tuple = (33, 33, 33), align=PP_ALIGN.LEFT, wrap: bool = True):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = wrap
    set_text(tf, text, size=size, bold=bold, color=color, align=align)
    return txb

def add_image(slide, img_path: str, left, top, width):
    if img_path and os.path.exists(img_path):
        slide.shapes.add_picture(img_path, left, top, width=width)

def real_height(img_path: str, width) -> float:
    if not img_path or not os.path.exists(img_path):
        return 0
    with PILImage.open(img_path) as im:
        orig_w, orig_h = im.size
    return int(width * orig_h / orig_w)

def remove_placeholders(slide):
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)