#!/usr/bin/env python3
"""
PDF417 Decoder Implementation

This module provides functionality to decode PDF417 barcodes from images.
It uses the pyzbar library for actual barcode detection and decoding.
"""

try:
    from pyzbar import pyzbar
    from PIL import Image
    import numpy as np
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False


class PDF417Decoder:
    """
    PDF417 Barcode Decoder
    
    This class provides methods to decode PDF417 barcodes from images.
    """
    
    def __init__(self, image=None):
        """
        Initialize the decoder.
        
        Args:
            image: PIL Image object or path to image file
        """
        if not PYZBAR_AVAILABLE:
            raise ImportError("pyzbar library is required for decoding. Install with: pip install pyzbar")
        
        self.image = image
        self._barcodes_info = []
    
    def decode(self, image=None):
        """
        Decode PDF417 barcodes from an image.
        
        Args:
            image: PIL Image object or path to image file (optional if provided in __init__)
            
        Returns:
            str: Decoded data from the first PDF417 barcode found, or empty string if none found
        """
        if image is not None:
            self.image = image
        
        if self.image is None:
            raise ValueError("No image provided for decoding")
        
        # Convert to PIL Image if it's a path
        if isinstance(self.image, str):
            self.image = Image.open(self.image)
        
        # Convert to RGB if needed
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        
        # Decode barcodes
        barcodes = pyzbar.decode(self.image)
        
        # Filter for PDF417 barcodes
        pdf417_barcodes = [barcode for barcode in barcodes if barcode.type == 'PDF417']
        
        if not pdf417_barcodes:
            return ""
        
        # Store barcode info for debugging
        self._barcodes_info = []
        for barcode in pdf417_barcodes:
            barcode_info = {
                'data': barcode.data.decode('utf-8', errors='ignore'),
                'rect': {
                    'left': barcode.rect.left,
                    'top': barcode.rect.top,
                    'width': barcode.rect.width,
                    'height': barcode.rect.height
                },
                'polygon': [(p.x, p.y) for p in barcode.polygon]
            }
            self._barcodes_info.append(barcode_info)
        
        # Return data from the first PDF417 barcode
        return pdf417_barcodes[0].data.decode('utf-8', errors='ignore')
    
    def decode_all(self, image=None):
        """
        Decode all PDF417 barcodes from an image.
        
        Args:
            image: PIL Image object or path to image file (optional if provided in __init__)
            
        Returns:
            list: List of decoded data strings from all PDF417 barcodes found
        """
        if image is not None:
            self.image = image
        
        if self.image is None:
            raise ValueError("No image provided for decoding")
        
        # Convert to PIL Image if it's a path
        if isinstance(self.image, str):
            self.image = Image.open(self.image)
        
        # Convert to RGB if needed
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        
        # Decode barcodes
        barcodes = pyzbar.decode(self.image)
        
        # Filter for PDF417 barcodes and decode all of them
        pdf417_barcodes = [barcode for barcode in barcodes if barcode.type == 'PDF417']
        
        results = []
        self._barcodes_info = []
        
        for barcode in pdf417_barcodes:
            try:
                data = barcode.data.decode('utf-8', errors='ignore')
                results.append(data)
                
                # Store barcode info
                barcode_info = {
                    'data': data,
                    'rect': {
                        'left': barcode.rect.left,
                        'top': barcode.rect.top,
                        'width': barcode.rect.width,
                        'height': barcode.rect.height
                    },
                    'polygon': [(p.x, p.y) for p in barcode.polygon]
                }
                self._barcodes_info.append(barcode_info)
            except Exception as e:
                print(f"Error decoding barcode: {e}")
                continue
        
        return results


def decode_pdf417(image_path):
    """
    Convenience function to decode a PDF417 barcode from an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Decoded data from the first PDF417 barcode found, or empty string if none found
    """
    decoder = PDF417Decoder()
    return decoder.decode(image_path)


def decode_pdf417_all(image_path):
    """
    Convenience function to decode all PDF417 barcodes from an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        list: List of decoded data strings from all PDF417 barcodes found
    """
    decoder = PDF417Decoder()
    return decoder.decode_all(image_path)


if __name__ == "__main__":
    # Test the decoder
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        try:
            decoder = PDF417Decoder()
            result = decoder.decode(image_path)
            print(f"Decoded: {result}")
            
            if hasattr(decoder, '_barcodes_info'):
                print(f"Barcodes info: {decoder._barcodes_info}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage: python pdf417decoder.py <image_path>")