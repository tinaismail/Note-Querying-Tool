#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def convert_pdf_to_txt():
    """
    Convert all PDF files in the current directory to text files using pdftotext.
    Each PDF file will create a text file with the same base name.
    """
    # Get current directory
    current_dir = Path.cwd()
    
    # Find all PDF files in the current directory
    pdf_files = list(current_dir.glob("*.pdf")) + list(current_dir.glob("*.PDF"))
    
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    # Check if pdftotext is available
    try:
        subprocess.run(["pdftotext", "-v"], capture_output=True, check=False)
    except FileNotFoundError:
        print("Error: 'pdftotext' command not found. Please install it first.")
        print("On Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("On macOS: brew install poppler")
        print("On Fedora: sudo dnf install poppler-utils")
        sys.exit(1)
    
    # Convert each PDF file
    successful = 0
    failed = 0
    
    for pdf_path in pdf_files:
        # Create output text file path with the same base name
        txt_path = pdf_path.with_suffix(".txt")
        
        print(f"Converting: {pdf_path.name} -> {txt_path.name}")
        
        try:
            # Run pdftotext command
            # -layout: maintain original layout
            # -enc UTF-8: use UTF-8 encoding
            result = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf_path), str(txt_path)],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if output file was created
            if txt_path.exists():
                print(f"  ✓ Successfully created {txt_path.name}")
                successful += 1
            else:
                print(f"  ✗ Failed to create {txt_path.name}")
                failed += 1
                
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error converting {pdf_path.name}: {e.stderr}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Unexpected error with {pdf_path.name}: {str(e)}")
            failed += 1
    
    # Print summary
    print(f"\nConversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\nText files saved in: {current_dir}")

def main():
    """Main function to run the PDF to text conversion."""
    print("PDF to Text Converter")
    print("=" * 50)
    
    try:
        convert_pdf_to_txt()
    except KeyboardInterrupt:
        print("\n\nConversion interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
