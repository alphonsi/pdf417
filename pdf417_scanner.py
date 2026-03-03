#!/usr/bin/env python3
"""
PDF417 Barcode Scanner

This script provides functionality to scan and decode PDF417 barcodes from images.
It uses the pyzbar library for barcode detection and decoding.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def scan_pdf417_barcode(image_path):
    """
    Scan and decode a PDF417 barcode from an image file.
    
    Args:
        image_path (str): Path to the image file containing the barcode
    
    Returns:
        str: Decoded data from the first PDF417 barcode found, or empty string if none found
    """
    try:
        from pdf417decoder import PDF417Decoder
        from PIL import Image
        
        print(f"Scanning image: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        print(f"Image loaded: {img.size}, mode: {img.mode}")
        
        # Convert to RGB for decoding
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Decode
        decoder = PDF417Decoder(img)
        result = decoder.decode()
        
        if result:
            print(f"SUCCESS: Decoded data: {repr(result)}")
        else:
            print("No PDF417 barcodes found in the image")
        
        return result
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pyzbar pillow")
        return ""
    except Exception as e:
        print(f"ERROR: Failed to scan barcode: {e}")
        return ""

def scan_multiple_barcodes(image_path):
    """
    Scan and decode all PDF417 barcodes from an image file.
    
    Args:
        image_path (str): Path to the image file containing the barcode(s)
    
    Returns:
        list: List of decoded data strings from all PDF417 barcodes found
    """
    try:
        from pdf417decoder import PDF417Decoder
        from PIL import Image
        
        print(f"Scanning image for multiple barcodes: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        print(f"Image loaded: {img.size}, mode: {img.mode}")
        
        # Convert to RGB for decoding
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Decode all barcodes
        decoder = PDF417Decoder(img)
        results = decoder.decode_all()
        
        if results:
            print(f"SUCCESS: Found {len(results)} barcode(s):")
            for i, result in enumerate(results):
                print(f"  Barcode {i+1}: {repr(result)}")
        else:
            print("No PDF417 barcodes found in the image")
        
        return results
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pyzbar pillow")
        return []
    except Exception as e:
        print(f"ERROR: Failed to scan barcodes: {e}")
        return []

def main():
    """Main function for command-line usage"""
    print("PDF417 Barcode Scanner")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        if not os.path.exists(image_path):
            print(f"ERROR: File not found: {image_path}")
            return
        
        # Scan for single barcode
        result = scan_pdf417_barcode(image_path)
        
        if result:
            print(f"\nDecoded data: {result}")
        else:
            print("\nNo barcodes detected. Try:")
            print("1. Ensuring good lighting conditions")
            print("2. Making sure the entire barcode is visible")
            print("3. Using a high-contrast black/white barcode")
            print("4. Checking that the image is not blurry")
        
        # Also try scanning for multiple barcodes
        print("\n" + "-" * 30)
        print("Scanning for multiple barcodes...")
        all_results = scan_multiple_barcodes(image_path)
        
    else:
        print("Usage: python pdf417_scanner.py <image_path>")
        print("\nExample:")
        print("  python pdf417_scanner.py generated_barcode.png")
        print("  python pdf417_scanner.py test_complete_pdf417.png")

if __name__ == "__main__":
    main()