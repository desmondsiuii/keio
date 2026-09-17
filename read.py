from pypdf import PdfReader


def extract_pdf_to_text(pdf_path, output_txt_path):
    """Reads all text from a PDF file and writes it into a .txt file."""
    try:
        # Initialize the PDF reader
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        print(f"Processing '{pdf_path}' ({total_pages} pages)...")

        # Open the output text file for writing
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            for index, page in enumerate(reader.pages, start=1):
                # Extract text from the page
                text = page.extract_text()

                if text:
                    txt_file.write(f"--- Page {index} ---\n")
                    txt_file.write(text)
                    txt_file.write("\n\n")

        print(f"Success! Content saved to '{output_txt_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example Usage
if __name__ == "__main__":
    pdf_filename = "test.pdf"  # Replace with your PDF path
    output_filename = "test.txt"  # Output text file

    extract_pdf_to_text(pdf_filename, output_filename)