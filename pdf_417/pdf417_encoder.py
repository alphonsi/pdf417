#!/usr/bin/env python3
"""
PDF417 Barcode Encoder

This script generates PDF417 barcodes from text data using the treepoem library.
It creates high-quality barcodes optimized for scanning.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_pdf417_barcode(data, output_file="generated_barcode.png", columns=12, security_level=4):
    """
    Generate a PDF417 barcode from text data.
    
    Args:
        data (str): The data to encode in the barcode
        output_file (str): Output filename for the generated barcode
        columns (int): Number of columns (data density)
        security_level (int): Error correction level (2-8, 4-5 is good balance)
    
    Returns:
        str: Path to the generated barcode file, or None if failed
    """
    try:
        import treepoem
        from PIL import Image
        
        print(f"Generating PDF417 barcode with data: {repr(data)}")
        
        # Generate barcode with optimal settings
        barcode_image = treepoem.generate_barcode(
            barcode_type='pdf417',
            data=data,
            options={
                "columns": columns,           # Wider = more data per row
                "security_level": security_level,     # Error correction
                "rows": 0                     # 0 = auto
            }
        )
        
        # Convert to pure black/white for better scanning
        barcode_image = barcode_image.convert('1')
        
        # Save the image
        barcode_image.save(output_file)
        
        print(f"SUCCESS: Barcode generated and saved as: {output_file}")
        print(f"  Image size: {barcode_image.size}")
        print(f"  Image mode: {barcode_image.mode}")
        
        return output_file
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install treepoem pillow")
        return None
    except Exception as e:
        print(f"ERROR: Failed to generate barcode: {e}")
        return None

def main():
    """Main function for command-line usage"""
    print("PDF417 Barcode Encoder")
    print("=" * 30)
    
    # Example data
    test_data = "@\n\x1E\rANSI 636014TEST01DLTEST stessy Opiyo Test Nairobi KE 2026"
    
    # Generate barcode
    output_file = generate_pdf417_barcode(
        data=test_data,
        output_file="generated_barcode.png",
        columns=12,
        security_level=4
    )
    
    if output_file:
        print(f"\nGenerated barcode: {output_file}")
        print("You can now scan this barcode with a phone app or barcode scanner.")
        print("\nTo encode custom data, modify the 'test_data' variable in this script.")
    else:
        print("Failed to generate barcode.")

if __name__ == "__main__":
    main()