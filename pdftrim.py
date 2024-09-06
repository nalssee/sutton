import sys
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

def trim_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Convert PDF page to image
        images = convert_from_path(input_path, first_page=page_num+1, last_page=page_num+1)
        img = images[0]
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Find non-empty rows and columns
        rows = np.any(img_array < 250, axis=1)
        cols = np.any(img_array < 250, axis=0)
        
        # Find the boundaries
        row_indices = np.where(rows)[0]
        col_indices = np.where(cols)[0]
        
        if len(row_indices) > 0 and len(col_indices) > 0:
            rmin, rmax = row_indices[[0, -1]]
            cmin, cmax = col_indices[[0, -1]]
            
            # Crop the page
            page.mediabox.lower_left = (cmin, page.mediabox.top - rmax)
            page.mediabox.upper_right = (cmax, page.mediabox.top - rmin)
        else:
            print(f"Warning: Page {page_num + 1} appears to be blank or contains no detectable text.")
        
        writer.add_page(page)

    # Save the result
    with open(output_path, 'wb') as f:
        writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.pdf output.pdf")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    trim_pdf(input_path, output_path)
    print(f"Trimmed PDF saved to {output_path}")