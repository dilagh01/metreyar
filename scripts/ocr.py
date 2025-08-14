import sys
from pathlib import Path

def ocr_image(fp):
    from PIL import Image
    import pytesseract
    img = Image.open(fp)
    return pytesseract.image_to_string(img, lang='eng')

def ocr_pdf(fp):
    from pdf2image import convert_from_path
    import pytesseract
    text = []
    for img in convert_from_path(fp):
        text.append(pytesseract.image_to_string(img, lang='eng'))
    return "\n".join(text)

def to_html(name, text):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
<style>
body {{ font-family: Arial; background:white; color:black; padding:20px; white-space:pre-wrap; }}
</style>
</head>
<body>
<pre>{text}</pre>
</body>
</html>"""

if __name__ == "__main__":
    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    base_name = sys.argv[3]

    ext = input_path.suffix.lower().lstrip(".")
    if ext in ("png","jpg","jpeg","bmp"):
        text = ocr_image(input_path)
    elif ext == "pdf":
        text = ocr_pdf(input_path)
    else:
        print(f"Unsupported file type: {ext}")
        sys.exit(0)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{base_name}.html").write_text(to_html(base_name, text), encoding="utf-8")
