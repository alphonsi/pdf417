#!/usr/bin/env python3
"""
Barcode Scanning Test

This script generates a simple PDF417 barcode and provides instructions
for testing with external scanning tools.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_test_barcode():
    """Generate a test PDF417 barcode for external scanning"""
    try:
        import treepoem
        from PIL import Image
        
        # Simple test data
        test_data = "TEST123456789"
        print(f"Generating barcode with data: {test_data}")
        
        # Generate barcode with optimal settings for scanning
        barcode_image = treepoem.generate_barcode(
            barcode_type='pdf417',
            data=test_data,
            options={
                "columns": 8,           # Good balance of data density and readability
                "security_level": 3,    # Standard error correction
                "rows": 0               # Auto rows
            }
        )
        
        # Convert to high contrast black/white
        barcode_image = barcode_image.convert('1')
        
        # Save with clear filename
        output_file = "test_for_scanning.png"
        barcode_image.save(output_file)
        
        print(f"SUCCESS: Barcode saved as: {output_file}")
        print(f"  Image size: {barcode_image.size}")
        print(f"  Image mode: {barcode_image.mode}")
        
        return output_file, test_data
        
    except Exception as e:
        print(f"FAILED: Failed to generate barcode: {e}")
        return None, None

def print_scanning_instructions():
    """Print instructions for testing with external tools"""
    print("\n" + "="*60)
    print("BARCODE SCANNING TEST INSTRUCTIONS")
    print("="*60)
    print()
    print("The generated barcode can be tested with:")
    print()
    print("1. MOBILE APPS:")
    print("   - Download 'Barcode Scanner' (ZXing) from your app store")
    print("   - Open the app and point your camera at the barcode image")
    print("   - The app should read: 'TEST123456789'")
    print()
    print("2. COMMAND LINE (if zbar is installed):")
    print("   zbarimg test_for_scanning.png")
    print()
    print("3. ONLINE SCANNERS:")
    print("   - Upload the image to online barcode readers")
    print("   - Search for 'online PDF417 barcode reader'")
    print()
    print("4. DESKTOP APPLICATIONS:")
    print("   - Use any PDF417-compatible scanning software")
    print("   - Point the camera at the screen or load the image file")
    print()
    print("TIPS FOR SUCCESSFUL SCANNING:")
    print("- Ensure good lighting conditions")
    print("- Hold the camera steady and focus on the barcode")
    print("- Make sure the entire barcode is visible in the camera frame")
    print("- The barcode should be at least 2-3 inches wide for best results")
    print("- Avoid glare or reflections on the screen")
    print()
    print("="*60)

def main():
    """Main function"""
    print("PDF417 Barcode Scanning Test")
    print("="*40)
    
    # Generate test barcode
    barcode_file, test_data = generate_test_barcode()
    
    if barcode_file:
        print_scanning_instructions()
        print(f"\nGenerated barcode file: {barcode_file}")
        print(f"Expected scan result: '{test_data}'")
        print("\nOpen the image file and test with the methods above!")
    else:
        print("Failed to generate test barcode.")

if __name__ == "__main__":
    main()