from PIL import Image
import base64, io, os

def image_to_svg(src_path: str, suffix: str = ".svg", keep_original_name=True) -> str:
    # Validate file exists
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"File not found: {src_path}")
    
    # Load image in RGBA to handle transparency safely
    im = Image.open(src_path).convert("RGBA")
    width, height = im.size

    # Encode as PNG base64 (works for any input format)
    buffer = io.BytesIO()
    im.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

    # Create SVG content
    svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image href="data:image/png;base64,{b64}" x="0" y="0" width="{width}" height="{height}" />
</svg>
'''

    # Derive output path
    base, ext = os.path.splitext(src_path)
    if keep_original_name:
        out_path = base + suffix
    else:
        out_path = base + "-converted" + suffix

    # Write to file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return out_path


# Example usage
if __name__ == "__main__":
    src_path =  ""                    #ADD FILENAME HERE    # example : "/something/a.jpg"
    out_path = image_to_svg(src_path, keep_original_name=True)  # produces /something/a.svg
    print("Saved:", out_path)
