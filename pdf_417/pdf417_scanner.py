#!/usr/bin/env python3
"""
PDF417 Barcode Scanner

This script provides functionality to scan and decode PDF417 barcodes from images.
It uses the pdf417decoder library for barcode detection and decoding.
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
        decode_result = decoder.decode()
        
        if decode_result > 0:
            # Get the decoded data from the first barcode
            result = decoder.barcode_data
            print(f"SUCCESS: Decoded data: {repr(result)}")
            return result
        else:
            print("No PDF417 barcodes found in the image")
            return ""
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pdf417decoder pillow")
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
        decode_result = decoder.decode()
        
        results = []
        if decode_result > 0:
            # Get data from the first barcode
            result = decoder.barcode_data
            results.append(result)
            print(f"SUCCESS: Found {len(results)} barcode(s):")
            print(f"  Barcode 1: {repr(result)}")
        else:
            print("No PDF417 barcodes found in the image")
        
        return results
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pdf417decoder pillow")
        return []
    except Exception as e:
        print(f"ERROR: Failed to scan barcodes: {e}")
        return []

def decode_to_file(image_path, output_file="decoded_data.txt"):
    """
    Scan and decode PDF417 barcodes and save results to a file.
    
    Args:
        image_path (str): Path to the image file containing the barcode(s)
        output_file (str): Output filename for the decoded data
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from pdf417decoder import PDF417Decoder
        from PIL import Image
        
        print(f"Scanning image for decoding: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        print(f"Image loaded: {img.size}, mode: {img.mode}")
        
        # Convert to RGB for decoding
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Decode all barcodes
        decoder = PDF417Decoder(img)
        decode_result = decoder.decode()
        
        results = []
        if decode_result > 0:
            # Get data from the first barcode
            result = decoder.barcode_data
            results.append(result)
        
        # Save results to file
        if results:
            with open(output_file, 'w', encoding='utf-8') as f:
                for i, result in enumerate(results):
                    f.write(f"Barcode {i+1}:\n")
                    f.write(f"Data: {result}\n")
                    f.write("-" * 40 + "\n")
            
            print(f"SUCCESS: Decoded data saved to: {output_file}")
            print(f"Found {len(results)} barcode(s)")
            return True
        else:
            print("No PDF417 barcodes found in the image")
            return False
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pdf417decoder pillow")
        return False
    except Exception as e:
        print(f"ERROR: Failed to scan barcodes: {e}")
        return False

def scan_with_detailed_info(image_path):
    """
    Scan and decode PDF417 barcodes with detailed information.
    
    Args:
        image_path (str): Path to the image file containing the barcode(s)
    
    Returns:
        list: List of dictionaries containing detailed barcode information
    """
    try:
        from pdf417decoder import PDF417Decoder
        from PIL import Image
        
        print(f"Scanning image for detailed barcode information: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        print(f"Image loaded: {img.size}, mode: {img.mode}")
        
        # Convert to RGB for decoding
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Decode all barcodes
        decoder = PDF417Decoder(img)
        decode_result = decoder.decode()
        
        # Get detailed barcode information
        detailed_info = []
        if hasattr(decoder, '_barcodes_info'):
            detailed_info = decoder._barcodes_info
        
        if decode_result > 0:
            result = decoder.barcode_data
            print(f"SUCCESS: Found {1} barcode(s):")
            print(f"  Barcode 1: {repr(result)}")
            if detailed_info:
                info = detailed_info[0]
                print(f"    Position: {info['rect']}")
                print(f"    Polygon: {info['polygon']}")
        else:
            print("No PDF417 barcodes found in the image")
        
        return detailed_info
        
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pdf417decoder pillow")
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
        
        # Check if user wants to save to file
        save_to_file = len(sys.argv) > 2 and sys.argv[2] == "--save"
        output_file = "decoded_data.txt"
        if len(sys.argv) > 3:
            output_file = sys.argv[3]
        
        if save_to_file:
            # Decode to file
            success = decode_to_file(image_path, output_file)
            if success:
                print(f"\nDecoded data saved to: {output_file}")
        else:
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
            
            # Show detailed information
            print("\n" + "-" * 30)
            print("Detailed barcode information...")
            detailed_info = scan_with_detailed_info(image_path)
        
    else:
        print("Usage: python pdf417_scanner.py <image_path> [options]")
        print("\nOptions:")
        print("  --save [output_file]  Save decoded data to file")
        print("\nExamples:")
        print("  python pdf417_scanner.py generated_barcode.png")
        print("  python pdf417_scanner.py test_complete_pdf417.png")
        print("  python pdf417_scanner.py barcode.png --save")
        print("  python pdf417_scanner.py barcode.png --save results.txt")

if __name__ == "__main__":
    main()
