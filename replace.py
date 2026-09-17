import fitz  # PyMuPDF


def replace_text_in_pdf(input_pdf_path, output_pdf_path, search_text, replace_text):
    """Searches for text in a PDF, replaces it, and saves the output as a new PDF."""
    try:
        # Open the original PDF
        doc = fitz.open(input_pdf_path)
        replacements_count = 0

        for page in doc:
            # Search for all occurrences of the target text
            text_instances = page.search_for(search_text)

            for inst in text_instances:
                # 1. Redact (erase) the old text block
                page.add_redact_annot(inst, fill=(1, 1, 1))  # Fill with white background
                page.apply_redactions()

                # 2. Insert the replacement text at the original position
                # inst is [x0, y0, x1, y1]; inst.y1 - 2 aligns the baseline properly
                page.insert_text(
                    (inst.x0, inst.y1 - 2),
                    replace_text,
                    fontsize=11,  # Adjust font size to match original PDF
                    color=(0, 0, 0)
                )
                replacements_count += 1

        # Save the updated document to the output path
        doc.save(output_pdf_path)
        doc.close()

        print(f"Success! Replaced '{search_text}' with '{replace_text}' ({replacements_count} times).")
        print(f"Saved result as '{output_pdf_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage
if __name__ == "__main__":
    input_file = "test.pdf"
    output_file = "result.pdf"

    replace_text_in_pdf(input_file, output_file, "1117", "1108")