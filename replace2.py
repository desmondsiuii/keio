import fitz  # PyMuPDF


def replace_multiple_texts(input_pdf_path, output_pdf_path, replacement_map):
    """
    Searches for multiple text targets in a PDF, replaces them, and saves as a new PDF.
    
    :param input_pdf_path: Path to original PDF
    :param output_pdf_path: Path to save modified PDF
    :param replacement_map: Dictionary mapping {search_text: new_text}
    """
    try:
        doc = fitz.open(input_pdf_path)
        total_replacements = 0

        for page in doc:
            for search_text, replace_text in replacement_map.items():
                # Search for all instances of the current text target
                text_instances = page.search_for(search_text)

                for inst in text_instances:
                    # 1. Erase/redact the old text
                    page.add_redact_annot(inst, fill=(1, 1, 1))  # Fill with white background
                    page.apply_redactions()

                    # 2. Draw the replacement text in the exact position
                    page.insert_text(
                        (inst.x0, inst.y1 - 2),  # Position coordinates
                        replace_text,
                        fontsize=11,  # Adjust font size if needed
                        color=(0, 0, 0)
                    )
                    total_replacements += 1

        doc.save(output_pdf_path)
        doc.close()

        print(f"Success! Performed {total_replacements} replacement(s).")
        print(f"Saved modified file to '{output_pdf_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = "test.pdf"
    output_file = "result2.pdf"

    # Define all find-and-replace rules in a dictionary
    replacements = {
        "1117": "1108",
        "2026-09-17": "2026-09-15",
        "2026/9/17": "2026/9/15",
        "14:10:33": "22:56:33",
        "1:13": "9:56"
    }

    replace_multiple_texts(input_file, output_file, replacements)