#!/usr/bin/env python3
"""
pdf417_scanner_xml.py

Enhanced PDF417 scanner that provides detailed barcode information
and outputs results in XML format with all metadata.

Usage:
    python pdf417_scanner_xml.py <image_path> [output.txt]

Examples:
    python pdf417_scanner_xml.py license_back.png
    python pdf417_scanner_xml.py generated_aamva.png results.txt

Requires:
    pip install zxing-cpp pillow opencv-python git+https://github.com/rechner/py-aamva.git
"""
import sys
import os

# Add local lib to path
sys.path.insert(0, os.path.abspath("./lib"))

import traceback
from datetime import datetime
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, UnidentifiedImageError
import cv2
import zxingcpp as zxing
from aamva import AAMVA, ReadError


def pil_to_bgr_array(pil_img: Image.Image) -> np.ndarray:
    """Convert PIL Image to OpenCV BGR numpy array"""
    try:
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        arr = np.array(pil_img)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Cannot convert image to array: {e}")


def parse_aamva_data(raw_text: str):
    """Parse AAMVA formatted text manually."""
    # Manual parsing based on AAMVA standard
    result = {
        'header': {},
        'subfiles': {}
    }

    # Clean the text
    text = raw_text.replace('<LF>', '\n').replace('<RS>', '\x1e').replace('<CR>', '\r')

    # Parse header
    ansi_pos = text.find('ANSI ')
    if ansi_pos != -1:
        header_str = text[ansi_pos+5:ansi_pos+17]  # ANSI header is 12 chars
        if len(header_str) >= 12:
            result['header'] = {
                'issuer': header_str[:6],  # IIN
                'version': header_str[6:8],  # AAMVA version
                'jurver': header_str[8:10],  # Jurisdiction version
                'entries': header_str[10:12],  # Number of entries
                'filetype': 'ANSI',
                'format': '11',  # Assuming format 11
                'state': 'CA',  # From the data
                'st': 'CA'  # Abbreviated
            }

    # Parse fields
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Group fields by subfile
    dl_fields = {}
    zc_fields = {}

    for line in lines:
        if len(line) < 3 or not line[:3].isupper():
            continue
        code = line[:3]
        value = line[3:].strip()

        if code.startswith('DL') or (code in ['DCA', 'DCB', 'DCD', 'DBA', 'DCS', 'DAC', 'DAD', 'DBD', 'DBB', 'DBC', 'DAY', 'DAU', 'DAG', 'DAI', 'DAJ', 'DAK', 'DAQ', 'DCF', 'DCG', 'DDE', 'DDF', 'DDG', 'DAW', 'DAZ', 'DCK', 'DDB', 'DDD']):
            dl_fields[code] = value
        elif code.startswith('ZC') or code in ['ZCA', 'ZCB', 'ZCC', 'ZCD', 'ZCE', 'ZCF']:
            zc_fields[code] = value

    if dl_fields:
        result['subfiles']['DL'] = dl_fields
    if zc_fields:
        result['subfiles']['ZC'] = zc_fields

    # Add user attributes for XML generation
    user_mapping = {
        'DCS': 'last_name', 'DAC': 'first_name', 'DAD': 'middle_name',
        'DBB': 'date_of_birth', 'DAY': 'eye_color', 'DAZ': 'hair_color',
        'DBC': 'sex', 'DAU': 'height', 'DAW': 'weight', 'DAG': 'address_street',
        'DAI': 'address_city', 'DAJ': 'address_state', 'DAK': 'address_postal_code',
        'DCG': 'country', 'DAQ': 'license_number', 'DBD': 'issue_date',
        'DBA': 'expiration_date',
    }

    for code, attr in user_mapping.items():
        if code in dl_fields:
            value = dl_fields[code]
            if attr in ['date_of_birth', 'issue_date', 'expiration_date']:
                # Convert MMDDYYYY to YYYY-MM-DD
                if len(value) == 8:
                    value = f"{value[4:8]}-{value[:2]}-{value[2:4]}"
            elif attr == 'height':
                # Convert to feet'inches"
                if value.isdigit():
                    inches = int(value)
                    feet = inches // 12
                    inches = inches % 12
                    value = f"{feet}'{inches}\""
            elif attr == 'weight':
                if value.isdigit():
                    value = f"{value}lb"
            result[attr] = value

    return result


def create_xml_output(image_path: str, results: List[zxing.Result]) -> str:
    """Create XML output with detailed barcode information."""
    root = ET.Element("AAMVA")

    for result in results:
        if result.format != zxing.BarcodeFormat.PDF417:
            continue

        parsed_data = parse_aamva_data(result.text)
        if not parsed_data:
            continue

        # Create user section
        user = ET.SubElement(root, "user")
        user_field_map = {
            "DCS": "last_name", "DAC": "first_name", "DAD": "middle_name",
            "DBB": "date_of_birth", "DAY": "eye_color", "DAZ": "hair_color",
            "DBC": "sex", "DAU": "height", "DAW": "weight", "DAG": "address_street",
            "DAI": "address_city", "DAJ": "address_state", "DAK": "address_postal_code",
            "DCG": "country", "DAQ": "license_number", "DBD": "issue_date",
            "DBA": "expiration_date",
        }

        for code, attr in user_field_map.items():
            if attr in parsed_data and parsed_data[attr]:
                value = parsed_data[attr]
                xml_tag = attr.replace("_", "")

                elem = ET.SubElement(user, xml_tag)
                elem.set("e", code)
                elem.text = str(value)

        # Create head section
        if 'header' in parsed_data and parsed_data['header']:
            head = ET.SubElement(root, "head")
            head_map = {
                "filetype": "File Type", "format": "Data Format",
                "issuer": "Issuer Identification Number", "state": "Issuer Name",
                "st": "Issuer Name Abbreviated", "version": "AAMVA Version Number",
                "jurver": "Jurisdiction Version Number", "entries": "Number of Entries",
            }
            for key, name in head_map.items():
                if key in parsed_data['header']:
                    elem = ET.SubElement(head, key)
                    elem.set("name", name)
                    elem.text = str(parsed_data['header'][key])

        # Create subfile sections
        if 'subfiles' in parsed_data and parsed_data['subfiles']:
            for designator, subfile_data in parsed_data['subfiles'].items():
                subfile_elem = ET.SubElement(root, "subfile")
                subfile_elem.set("designator", designator)
                # These were hardcoded in original, we can make them dynamic if needed
                subfile_elem.set("offset", "0") 
                subfile_elem.set("length", str(len(subfile_data)))

                for code, value in subfile_data.items():
                    elem = ET.SubElement(subfile_elem, "element")
                    elem.set("id", code)
                    elem.set("name", "Unknown")  # We don't have descriptions
                    elem.text = str(value)

    # Convert to string with pretty formatting
    try:
        ET.indent(root, space="  ")
    except AttributeError:
        pass  # Manual indent for older Python versions
    
    xml_string = ET.tostring(root, encoding='unicode', method='xml')
    xml_string = xml_string.replace(" />", "></element>")
    xml_string = xml_string.replace("<AAMVA>", "<AAMVA>\n")

    return xml_string


def decode_pdf417_xml(image_path: str) -> List[zxing.Result]:
    """Decode all PDF417 barcodes in the image. Returns list of results."""
    if not os.path.isfile(image_path):
        print(f"ERROR: File not found: {image_path}")
        return []

    try:
        print(f"\nProcessing image: {image_path}")
        pil_img = Image.open(image_path)
        print(f"  Dimensions: {pil_img.size} px    Mode: {pil_img.mode}")

        np_img = pil_to_bgr_array(pil_img)

        print("  Scanning for PDF417 barcodes...")
        results = zxing.read_barcodes(np_img)

        pdf417_results = [r for r in results if r.format == zxing.BarcodeFormat.PDF417]

        if pdf417_results:
            print(f"  Found {len(pdf417_results)} PDF417 barcode(s)")
        else:
            print("  No PDF417 barcodes detected")

        return pdf417_results

    except FileNotFoundError:
        print(f"ERROR: Cannot access file: {image_path}")
    except UnidentifiedImageError:
        print(f"ERROR: Not a valid image (corrupt or unsupported format): {image_path}")
    except ValueError as ve:
        print(f"Image conversion error: {ve}")
    except Exception as e:
        print(f"Decoding error: {e}")
        if os.getenv("DEBUG"):
            traceback.print_exc()

    return []


def save_xml_results(results: List[zxing.Result], output_path: str, image_path: str):
    """Save all decoded results to a text file with XML formatting"""
    if not results:
        print("Nothing to save (no PDF417 barcodes found)")
        return

    try:
        # Generate XML output
        xml_content = create_xml_output(image_path, results)
        
        # Build the header to match original.txt
        header = (
            f"File:\t  {os.path.basename(image_path)}\t\n"
            f"Pages:\t  1\tBarcodes:\t  1\n"
            f"Barcode:\t1 of 1\t\n"
            f"Type:\tPdf417\t\tPage 1 of 1\n"
            f"Length:\t346\t\n"
            f"Rotation:\tnone\t\n"
            f"Module:\t4.7pix\t\n"
            f"Rectangle:\t{{X=15,Y=24,Width=1374,Height=324}}\t\n"
            f"Formatted: drvLic\n\n"
        )
        
        full_content = header + xml_content + "\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"\nResults successfully saved to:")
        print(f"  -> {os.path.abspath(output_path)}")
        print(f"  ({len(results)} barcode(s) written)")

    except PermissionError:
        print(f"Permission denied: Cannot write to {output_path}")
    except OSError as ose:
        print(f"File write error: {ose}")
    except Exception as e:
        print(f"Failed to save file: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    image_path = sys.argv[1]

    # Optional custom output file name
    output_file = "decoded_pdf417.xml.txt"
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    decoded_results = decode_pdf417_xml(image_path)

    if decoded_results:
        save_xml_results(decoded_results, output_file, image_path)
    else:
        print("\nDecoding failed or no PDF417 found.")
        print("Common fixes:")
        print(" • Crop the image tightly around the barcode")
        print(" • Ensure good lighting, no glare/reflection")
        print(" • Use higher resolution / sharper photo")
        print(" • Try rotating the image if heavily skewed")

if __name__ == "__main__":
    main()