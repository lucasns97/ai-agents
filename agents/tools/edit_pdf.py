import os
import sys

# Add parent directory to path BEFORE other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging import get_logger
from smolagents import Tool
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

# Get the logger instance
logger = get_logger(__name__)


class MergePDFTool(Tool):
    name = "merge_pdf_tool"
    description = (
        "A tool for merging multiple PDF files into one document. "
        "Provide an array of file paths for the PDFs to be merged and specify the output file path for the merged PDF."
    )
    inputs = {
        "input_files": {
            "type": "array",
            "description": "An array of file paths to the PDF files to be merged.",
        },
        "output_file": {
            "type": "string",
            "description": "The file path for the resulting merged PDF.",
        },
    }
    output_type = "string"

    def forward(self, input_files: list, output_file: str) -> str:
        """
        Merges multiple PDF files into a single PDF document.
        
        Parameters:
            input_files (list): A list of file paths to the PDF files to be merged.
            output_file (str): The file path for the merged PDF.
            
        Returns:
            str: A message indicating the success or failure of the merge operation.
        """
        try:
            merger = PdfMerger()

            # Validate and append each PDF file to the merger
            for file_path in input_files:
                if not os.path.exists(file_path):
                    return f"Error: File '{file_path}' does not exist."
                if not file_path.lower().endswith(".pdf"):
                    return f"Error: File '{file_path}' is not a PDF."
                merger.append(file_path)

            merger.write(output_file)
            merger.close()

            return f"Merged PDF successfully created at '{output_file}'."
        except Exception as e:
            return f"Error merging PDFs: {str(e)}"


class SplitPDFTool(Tool):
    name = "split_pdf_tool"
    description = (
        "A tool for splitting a PDF file into individual page PDFs. "
        "Provide the file path of the PDF to split and an output directory where the resulting PDF pages will be saved."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "The file path of the PDF to be split.",
        },
        "output_dir": {
            "type": "string",
            "description": "The directory where the split PDF files will be saved.",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, output_dir: str) -> str:
        """
        Splits a PDF file into separate PDF files, each containing a single page.
        
        Parameters:
            file_path (str): The path to the PDF file to be split.
            output_dir (str): The directory where the split PDF files will be saved.
            
        Returns:
            str: A message indicating the success or failure of the splitting operation.
        """
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."
            if not file_path.lower().endswith(".pdf"):
                return f"Error: File '{file_path}' is not a PDF."
            
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            reader = PdfReader(file_path)
            num_pages = len(reader.pages)

            for i in range(num_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                output_path = os.path.join(output_dir, f"page_{i+1}.pdf")
                with open(output_path, "wb") as out_file:
                    writer.write(out_file)

            return f"Successfully split '{file_path}' into {num_pages} pages, saved in '{output_dir}'."
        except Exception as e:
            return f"Error splitting PDF: {str(e)}"


class WatermarkPDFTool(Tool):
    name = "watermark_pdf_tool"
    description = (
        "A tool for adding an image watermark to each page of a PDF file. "
        "Provide the PDF file path, the image file to be used as the watermark, "
        "and the placement parameters (x, y, width, and height in points). "
        "The watermark image will be placed over each PDF page at the specified location."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "The file path of the PDF to which the watermark will be added.",
        },
        "watermark_image": {
            "type": "string",
            "description": "The file path of the image to be used as a watermark.",
        },
        "output_file": {
            "type": "string",
            "description": "The file path for the watermarked PDF output.",
        },
        "x": {
            "type": "number",
            "description": "The x-coordinate (in points) for the placement of the watermark on each PDF page.",
        },
        "y": {
            "type": "number",
            "description": "The y-coordinate (in points) for the placement of the watermark on each PDF page.",
        },
        "width": {
            "type": "number",
            "description": "The width (in points) of the watermark image.",
        },
        "height": {
            "type": "number",
            "description": "The height (in points) of the watermark image.",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, watermark_image: str, output_file: str, x: float, y: float, width: float, height: float) -> str:
        """
        Adds an image watermark to each page of a PDF file at the specified location.
        
        Parameters:
            file_path (str): The path to the PDF file to be watermarked.
            watermark_image (str): The path to the image file to use as the watermark.
            output_file (str): The output path for the watermarked PDF.
            x (float): The x-coordinate for watermark placement (in points).
            y (float): The y-coordinate for watermark placement (in points).
            width (float): The width of the watermark image (in points).
            height (float): The height of the watermark image (in points).
        
        Returns:
            str: A message indicating the success or failure of the watermarking operation.
        """
        try:
            if not os.path.exists(file_path):
                return f"Error: PDF file '{file_path}' does not exist."
            if not os.path.exists(watermark_image):
                return f"Error: Watermark image '{watermark_image}' does not exist."
            if not file_path.lower().endswith(".pdf"):
                return f"Error: File '{file_path}' is not a PDF."
            
            reader = PdfReader(file_path)
            writer = PdfWriter()

            # Process each page of the original PDF
            for page in reader.pages:
                # Get the current page dimensions
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)

                # Create an in-memory PDF with the watermark image using ReportLab
                packet = io.BytesIO()
                c = canvas.Canvas(packet, pagesize=(page_width, page_height))
                c.drawImage(watermark_image, x, y, width=width, height=height, mask='auto')
                c.save()
                packet.seek(0)
                
                # Read the watermark overlay
                watermark_pdf = PdfReader(packet)
                watermark_page = watermark_pdf.pages[0]

                # Merge the watermark with the current page
                page.merge_page(watermark_page)
                writer.add_page(page)

            # Write the watermarked PDF to the output file
            with open(output_file, "wb") as f_out:
                writer.write(f_out)

            return (
                f"Successfully added watermark image '{watermark_image}' to '{file_path}'. "
                f"Output saved at '{output_file}'."
            )
        except Exception as e:
            return f"Error applying image watermark: {str(e)}"


class RotatePDFTool(Tool):
    name = "rotate_pdf_tool"
    description = (
        "A tool for rotating specified pages in a PDF file by a given angle. "
        "Provide the PDF file path, a list of page numbers (1-indexed) to rotate, "
        "the rotation angle in degrees (must be a multiple of 90), and the output file path."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "The file path of the PDF to be rotated.",
        },
        "output_file": {
            "type": "string",
            "description": "The file path for the rotated PDF output.",
        },
        "page_numbers": {
            "type": "array",
            "description": "An array of page numbers (1-indexed) to rotate. All other pages remain unchanged.",
        },
        "angle": {
            "type": "integer",
            "description": "The angle in degrees to rotate the specified pages (must be a multiple of 90).",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, output_file: str, page_numbers: list, angle: int) -> str:
        """
        Rotates specified pages in a PDF file by the given angle.
        
        Parameters:
            file_path (str): The PDF file to rotate.
            output_file (str): The output path for the rotated PDF.
            page_numbers (list): List of page numbers (1-indexed) to rotate.
            angle (int): The rotation angle (must be a multiple of 90).
        
        Returns:
            str: A success message or an error message.
        """
        try:
            if angle % 90 != 0:
                return "Error: Angle must be a multiple of 90 degrees."
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."
            if not file_path.lower().endswith(".pdf"):
                return f"Error: File '{file_path}' is not a PDF."

            reader = PdfReader(file_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)

            for i in range(total_pages):
                page = reader.pages[i]
                # Convert to 1-indexed page number for comparison
                if (i + 1) in page_numbers:
                    page.rotate(angle)
                writer.add_page(page)

            with open(output_file, "wb") as f_out:
                writer.write(f_out)

            return (
                f"Successfully rotated pages {page_numbers} in '{file_path}' by {angle} degrees. "
                f"Output saved at '{output_file}'."
            )
        except Exception as e:
            return f"Error rotating PDF: {str(e)}"


class AddPasswordToPDFTool(Tool):
    name = "add_password_to_pdf_tool"
    description = (
        "A tool for adding password protection to a PDF file. "
        "Provide the file path of the PDF to secure, the password to set, "
        "and the output file path for the encrypted PDF. The resulting PDF will require "
        "the provided password to be opened."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "The file path of the PDF to be password-protected.",
        },
        "password": {
            "type": "string",
            "description": "The password to apply to the PDF. Users will need this password to open the file.",
        },
        "output_file": {
            "type": "string",
            "description": "The file path for the output, password-protected PDF.",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, password: str, output_file: str) -> str:
        """
        Adds password protection to a PDF file.
        
        Parameters:
            file_path (str): The path to the PDF file to secure.
            password (str): The password to apply to the PDF.
            output_file (str): The output path for the password-protected PDF.
        
        Returns:
            str: A message indicating success or detailing any errors encountered.
        """
        try:
            # Validate the input PDF file.
            if not os.path.exists(file_path):
                return f"Error: PDF file '{file_path}' does not exist."
            if not file_path.lower().endswith(".pdf"):
                return f"Error: File '{file_path}' is not a PDF."
            
            # Read the original PDF.
            reader = PdfReader(file_path)
            writer = PdfWriter()

            # Copy all pages to the writer.
            for page in reader.pages:
                writer.add_page(page)
            
            # Apply password protection.
            writer.encrypt(user_password=password)
            
            # Write the secured PDF to the output file.
            with open(output_file, "wb") as f_out:
                writer.write(f_out)
            
            return f"Successfully added password protection to '{file_path}'. Encrypted PDF saved at '{output_file}'."
        except Exception as e:
            return f"Error adding password to PDF: {str(e)}"


if __name__ == '__main__':
    
    import shutil

    # Test the PDF tools
    test_file1 = r"C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\dummy.pdf"
    test_file2 = r"C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\sample_pages.pdf"
    test_output_dir = r"C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\.sandbox\test1"
    test_image_watermark = r"C:\Users\Lucas\OneDrive\Documentos\Projetos\Sandbox\ai-agents\samples\dummy.png"
    
    # Reset output dir
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)
    os.makedirs(test_output_dir)

    # Merge PDF
    merge_tool = MergePDFTool()
    merge_output = merge_tool.forward(
        input_files=[test_file1, test_file2],
        output_file=os.path.join(test_output_dir, "merged.pdf")
    )

    # Split PDF
    split_tool = SplitPDFTool()
    split_output = split_tool.forward(file_path=test_file2, output_dir=test_output_dir)
    logger.info(split_output)
    
    # Watermark PDF
    watermark_tool = WatermarkPDFTool()
    watermark_output = watermark_tool.forward(
        file_path=test_file1,
        watermark_image=test_image_watermark,
        output_file=os.path.join(test_output_dir, "watermarked.pdf"),
        x=100,
        y=100,
        width=200,
        height=100
    )
    logger.info(watermark_output)
    
    # Rotate PDF
    rotate_tool = RotatePDFTool()
    rotate_output = rotate_tool.forward(
        file_path=test_file2,
        output_file=os.path.join(test_output_dir, "rotated.pdf"),
        page_numbers=[1, 3],
        angle=90
    )
    logger.info(rotate_output)
    
    # Add password to PDF
    password_tool = AddPasswordToPDFTool()
    password_output = password_tool.forward(
        file_path=test_file1,
        password="123456",
        output_file=os.path.join(test_output_dir, "password_protected.pdf")
    )
    logger.info(password_output)
