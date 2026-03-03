#!/usr/bin/env python3
"""
PDF417 Complete Test Suite

This script provides comprehensive testing for both PDF417 encoding and decoding.
It tests the complete workflow from data encoding to barcode scanning.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_encoding():
    """Test PDF417 encoding with treepoem"""
    print("=== Testing PDF417 Encoding ===")
    
    try:
        import treepoem
        from PIL import Image
        
        # Test data
        test_data = "@\n\x1E\rANSI 636014TEST01DLTEST stessy Opiyo Test Nairobi KE 2026"
        print(f"Original data: {repr(test_data)}")
        
        # Generate barcode
        barcode_image = treepoem.generate_barcode(
            barcode_type='pdf417',
            data=test_data,
            options={
                "columns": 12,
                "security_level": 4,
                "rows": 0
            }
        )
        
        # Convert to pure black/white
        barcode_image = barcode_image.convert('1')
        
        # Save the image
        output_file = "test_complete_pdf417.png"
        barcode_image.save(output_file)
        print(f"SUCCESS: Barcode generated and saved as: {output_file}")
        
        # Verify image properties
        print(f"Image size: {barcode_image.size}")
        print(f"Image mode: {barcode_image.mode}")
        
        return output_file, test_data
        
    except Exception as e:
        print(f"FAILED: Encoding failed: {e}")
        return None, None

def test_decoding(image_path):
    """Test PDF417 decoding with pyzbar"""
    print("\n=== Testing PDF417 Decoding ===")
    
    try:
        from pdf417decoder import PDF417Decoder
        from PIL import Image
        
        # Load image
        img = Image.open(image_path)
        print(f"Loaded image: {image_path}")
        print(f"Image size: {img.size}")
        print(f"Image mode: {img.mode}")
        
        # Convert to RGB for decoding
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Decode
        decoder = PDF417Decoder(img)
        result = decoder.decode()
        
        print(f"Decoded result: {repr(result)}")
        
        # Check for multiple barcodes
        all_results = decoder.decode_all()
        print(f"All decoded results: {all_results}")
        
        # Check barcode info
        if hasattr(decoder, '_barcodes_info') and decoder._barcodes_info:
            print(f"Found {len(decoder._barcodes_info)} barcode(s)")
            for i, info in enumerate(decoder._barcodes_info):
                print(f"  Barcode {i+1}:")
                print(f"    Data: {repr(info['data'])}")
                print(f"    Position: {info['rect']}")
        else:
            print("No barcodes detected by pyzbar")
        
        return result
        
    except Exception as e:
        print(f"✗ Decoding failed: {e}")
        return None

def test_with_different_libraries():
    """Test decoding with alternative libraries"""
    print("\n=== Testing with Alternative Libraries ===")
    
    try:
        from PIL import Image
        import pyzbar.pyzbar as pyzbar
        
        img = Image.open("test_complete_pdf417.png")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Try direct pyzbar decoding
        barcodes = pyzbar.decode(img)
        print(f"pyzbar found {len(barcodes)} total barcodes")
        
        pdf417_barcodes = [b for b in barcodes if b.type == 'PDF417']
        print(f"PDF417 barcodes: {len(pdf417_barcodes)}")
        
        for i, barcode in enumerate(pdf417_barcodes):
            try:
                data = barcode.data.decode('utf-8', errors='ignore')
                print(f"  Barcode {i+1}: {repr(data)}")
            except Exception as e:
                print(f"  Barcode {i+1}: Error decoding - {e}")
        
        return len(pdf417_barcodes) > 0
        
    except Exception as e:
        print(f"Alternative library test failed: {e}")
        return False

def test_round_trip():
    """Test complete encoding/decoding round trip"""
    print("\n=== Testing Round-Trip Encoding/Decoding ===")
    
    # Test data
    original_data = "Hello World! This is a test of PDF417 encoding and decoding."
    
    try:
        # Encode
        import treepoem
        from PIL import Image
        
        barcode_image = treepoem.generate_barcode(
            barcode_type='pdf417',
            data=original_data,
            options={
                "columns": 10,
                "security_level": 3,
                "rows": 0
            }
        )
        
        barcode_image = barcode_image.convert('1')
        barcode_image.save("round_trip_test.png")
        
        # Decode
        from pdf417decoder import PDF417Decoder
        
        decoder = PDF417Decoder(barcode_image)
        decoded_data = decoder.decode()
        
        print(f"Original: {repr(original_data)}")
        print(f"Decoded:  {repr(decoded_data)}")
        
        if original_data == decoded_data:
            print("SUCCESS: Round-trip test passed!")
            return True
        else:
            print("WARNING: Round-trip test failed - data mismatch")
            return False
            
    except Exception as e:
        print(f"Round-trip test failed: {e}")
        return False

def main():
    """Main test function"""
    print("PDF417 Complete Test Suite")
    print("=" * 50)
    
    # Test encoding
    image_path, original_data = test_encoding()
    
    if image_path is None:
        print("FAILED: Encoding test failed - cannot proceed with decoding")
        return
    
    # Test decoding
    decoded_data = test_decoding(image_path)
    
    # Test with alternative approach
    alt_success = test_with_different_libraries()
    
    # Test round-trip
    round_trip_success = test_round_trip()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if original_data and decoded_data:
        if original_data == decoded_data:
            print("SUCCESS: ENCODING/DECODING SUCCESS: Data matches perfectly!")
        else:
            print("WARNING: ENCODING/DECODING PARTIAL: Data differs")
            print(f"   Original: {repr(original_data)}")
            print(f"   Decoded:  {repr(decoded_data)}")
    else:
        print("FAILED: ENCODING/DECODING FAILED: Could not complete round-trip")
    
    if alt_success:
        print("SUCCESS: Alternative library decoding: SUCCESS")
    else:
        print("FAILED: Alternative library decoding: FAILED")
    
    if round_trip_success:
        print("SUCCESS: Round-trip test: SUCCESS")
    else:
        print("FAILED: Round-trip test: FAILED")
    
    print(f"\nGenerated files:")
    print(f"  - {image_path}")
    print(f"  - round_trip_test.png")
    print("\nYou can open these files to view the barcodes and test with phone apps.")

if __name__ == "__main__":
    main()