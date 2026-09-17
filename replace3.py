import fitz  # PyMuPDF


def replace_text_with_original_styling(input_pdf, output_pdf, replacement_map):
    doc = fitz.open(input_pdf)
    total_replacements = 0

    for page in doc:
        # Get detailed layout data (blocks -> lines -> spans)
        text_page = page.get_text("dict")
        
        for search_text, replace_text in replacement_map.items():
            # Find exact coordinates of all instances of search_text
            text_instances = page.search_for(search_text)

            for inst in text_instances:
                font_name = "helv"  # Fallback font
                font_size = 11      # Fallback size
                color = (0, 0, 0)   # Fallback color (black)
                found_style = False

                # Search through text spans to match the bounding box and extract styles
                for block in text_page.get("blocks", []):
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            span_rect = fitz.Rect(span["bbox"])
                            # Check if the text span overlaps with our searched text position
                            if span_rect.intersects(inst) and search_text in span["text"]:
                                font_size = span["size"]
                                font_name = span["font"]
                                # Convert sRGB integer color to normalized RGB tuple (0.0 to 1.0)
                                c_int = span["color"]
                                color = (
                                    ((c_int >> 16) & 0xFF) / 255.0,
                                    ((c_int >> 8) & 0xFF) / 255.0,
                                    (c_int & 0xFF) / 255.0,
                                )
                                found_style = True
                                break
                        if found_style:
                            break
                    if found_style:
                        break

                # 1. Redact (erase) old text
                page.add_redact_annot(inst, fill=(1, 1, 1))
                page.apply_redactions()

                # 2. Insert replacement text using extracted styling
                try:
                    page.insert_text(
                        (inst.x0, inst.y1 - (font_size * 0.15)),  # Baseline alignment adjustment
                        replace_text,
                        fontsize=font_size,
                        fontname=font_name,
                        color=color
                    )
                except Exception:
                    # Fallback to standard Helvetica if the original font is not supported by PyMuPDF writer
                    page.insert_text(
                        (inst.x0, inst.y1 - (font_size * 0.15)),
                        replace_text,
                        fontsize=font_size,
                        fontname="helv",
                        color=color
                    )

                total_replacements += 1

    doc.save(output_pdf)
    doc.close()
    print(f"Successfully replaced {total_replacements} item(s) with matched fonts.")


if __name__ == "__main__":
    replacements = {
        "1117": "1108",
        "2026-09-17": "2026-09-15",
        "2026/9/17": "2026/9/15",
        "14:10:33": "22:56:33",
        "1:13": "9:56"
    }

    replace_text_with_original_styling("test.pdf", "result3.pdf", replacements)