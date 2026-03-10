#!/usr/bin/env python3
"""
xml_to_aamva_converter.py

Converts AAMVA XML data to ANSI AAMVA format with comprehensive validation.
This module provides the core conversion logic used by the encoder.

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi
"""

import sys
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import xml.etree.ElementTree as ET


def validate_aamva_compliance(aamva_string: str) -> Dict[str, Any]:
    """
    Validate AAMVA data for compliance with AAMVA standards.
    
    Returns:
        Dict with validation results including compliance score
    """
    compliance = {
        'valid': True,
        'compliance_score': 0,
        'errors': [],
        'warnings': [],
        'total_checks': 0,
        'passed_checks': 0
    }
    
    # Parse the AAMVA string
    lines = [line.strip() for line in aamva_string.split('\n') if line.strip()]
    
    # Check for ANSI header
    compliance['total_checks'] += 1
    if not any(line.startswith('ANSI ') for line in lines):
        compliance['errors'].append("Missing ANSI header")
        compliance['valid'] = False
    else:
        compliance['passed_checks'] += 1
    
    # Extract header information
    header_line = next((line for line in lines if line.startswith('ANSI ')), None)
    if header_line:
        header_data = header_line[5:]  # Remove "ANSI " prefix
        if len(header_data) >= 12:
            iin = header_data[:6]
            version = header_data[6:8]
            jurver = header_data[8:10]
            entries = header_data[10:12]
            
            # Validate IIN (Issuer Identification Number)
            compliance['total_checks'] += 1
            if not re.match(r'^\d{6}$', iin):
                compliance['errors'].append(f"Invalid IIN format: {iin}")
                compliance['valid'] = False
            else:
                compliance['passed_checks'] += 1
            
            # Validate version
            compliance['total_checks'] += 1
            if not re.match(r'^\d{2}$', version) or int(version) < 1:
                compliance['errors'].append(f"Invalid version: {version}")
                compliance['valid'] = False
            else:
                compliance['passed_checks'] += 1
            
            # Validate entries
            compliance['total_checks'] += 1
            if not re.match(r'^\d{2}$', entries):
                compliance['errors'].append(f"Invalid entries count: {entries}")
                compliance['valid'] = False
            else:
                compliance['passed_checks'] += 1
        else:
            compliance['errors'].append("Invalid ANSI header length")
            compliance['valid'] = False
    
    # Check for required fields
    required_fields = ['DCS', 'DAC', 'DBB', 'DBC', 'DAQ']  # Last name, first name, DOB, sex, license number
    field_data = {}
    
    for line in lines:
        if len(line) >= 3 and line[:3].isupper():
            code = line[:3]
            value = line[3:].strip()
            field_data[code] = value
    
    for required_field in required_fields:
        compliance['total_checks'] += 1
        if required_field not in field_data or not field_data[required_field]:
            compliance['errors'].append(f"Missing required field: {required_field}")
            compliance['valid'] = False
        else:
            compliance['passed_checks'] += 1
    
    # Validate date formats
    date_fields = ['DBB', 'DBA', 'DBD']  # DOB, expiration, issue
    for date_field in date_fields:
        if date_field in field_data and field_data[date_field]:
            compliance['total_checks'] += 1
            date_value = field_data[date_field]
            if not re.match(r'^\d{8}$', date_value):
                compliance['errors'].append(f"Invalid date format for {date_field}: {date_value}")
                compliance['valid'] = False
            else:
                # Additional date validation
                try:
                    year = int(date_value[:4])
                    month = int(date_value[4:6])
                    day = int(date_value[6:8])
                    
                    if month < 1 or month > 12:
                        compliance['errors'].append(f"Invalid month in {date_field}: {month}")
                        compliance['valid'] = False
                    elif day < 1 or day > 31:
                        compliance['errors'].append(f"Invalid day in {date_field}: {day}")
                        compliance['valid'] = False
                    else:
                        compliance['passed_checks'] += 1
                except ValueError:
                    compliance['errors'].append(f"Invalid date components in {date_field}: {date_value}")
                    compliance['valid'] = False
    
    # Validate sex field
    if 'DBC' in field_data and field_data['DBC']:
        compliance['total_checks'] += 1
        sex = field_data['DBC'].upper()
        if sex not in ['M', 'F', 'X']:
            compliance['warnings'].append(f"Unusual sex value: {sex} (should be M, F, or X)")
        else:
            compliance['passed_checks'] += 1
    
    # Validate height format
    if 'DAU' in field_data and field_data['DAU']:
        compliance['total_checks'] += 1
        height = field_data['DAU']
        if not re.match(r'^\d{3}\s*IN$', height, re.IGNORECASE):
            compliance['warnings'].append(f"Height format may be non-standard: {height}")
        else:
            compliance['passed_checks'] += 1
    
    # Calculate compliance score
    if compliance['total_checks'] > 0:
        compliance['compliance_score'] = (compliance['passed_checks'] / compliance['total_checks']) * 100
    
    return compliance


def xml_to_aamva_ansi(xml_content: str) -> str:
    """
    Convert AAMVA XML data to ANSI AAMVA format.
    
    Args:
        xml_content: XML string containing AAMVA data
        
    Returns:
        ANSI AAMVA formatted string with {RS} separators
    """
    try:
        # Remove header lines and extract only the XML content
        lines = xml_content.split('\n')
        xml_lines = []
        in_xml = False

        for line in lines:
            line = line.strip()
            if line.startswith('<AAMVA>'):
                in_xml = True
            if in_xml:
                xml_lines.append(line)

        xml_content = '\n'.join(xml_lines)

        # Remove XML declaration if present
        xml_content = re.sub(r'<\?xml[^>]*\?>', '', xml_content, flags=re.IGNORECASE)

        # Parse XML
        root = ET.fromstring(xml_content.strip())

        # Extract user data
        user_data = {}
        user_elem = root.find('user')
        if user_elem is not None:
            for child in user_elem:
                # Map XML tag names to AAMVA field codes
                tag_mapping = {
                    'last': 'DCS', 'first': 'DAC', 'middle': 'DAD',
                    'dob': 'DBB', 'eyes': 'DAY', 'hair': 'DAZ', 'sex': 'DBC',
                    'height': 'DAU', 'weight': 'DAW', 'street': 'DAG',
                    'city': 'DAI', 'state': 'DAJ', 'postal': 'DAK',
                    'country': 'DCG', 'id': 'DAQ', 'issued': 'DBD', 'expires': 'DBA'
                }
                if child.tag in tag_mapping:
                    user_data[tag_mapping[child.tag]] = child.text or ""

        # Extract head data
        head_data = {}
        head_elem = root.find('head')
        if head_elem is not None:
            for child in head_elem:
                head_data[child.tag] = child.text or ""

        # Extract DL subfile elements
        dl_elements = {}
        dl_subfile = root.find('.//subfile[@designator="DL"]')
        if dl_subfile is not None:
            for element in dl_subfile.findall('element'):
                element_id = element.get('id', '')
                element_text = element.text or ""
                if element_id:
                    dl_elements[element_id] = element_text

        # Extract ZC subfile elements
        zc_elements = {}
        zc_subfile = root.find('.//subfile[@designator="ZC"]')
        if zc_subfile is not None:
            for element in zc_subfile.findall('element'):
                element_id = element.get('id', '')
                element_text = element.text or ""
                if element_id:
                    zc_elements[element_id] = element_text

        # Build ANSI AAMVA string
        ansi_parts = []
        
        # ANSI header
        ansi_header = "ANSI "
        if head_data:
            iin = head_data.get('issuer', '636014')
            version = head_data.get('version', '04')
            jurver = head_data.get('jurver', '00')
            entries = head_data.get('entries', '02')
            ansi_header += f"{iin}{version}{jurver}{entries}"
        else:
            ansi_header += "636014040002"
        
        ansi_parts.append(ansi_header)

        # Build DL subfile with proper field order
        dl_order = [
            'DCA', 'DCB', 'DCD', 'DBA', 'DCS', 'DAC', 'DAD', 'DBD', 
            'DBB', 'DBC', 'DAY', 'DAU', 'DAG', 'DAI', 'DAJ', 'DAK',
            'DAQ', 'DCF', 'DCG', 'DDE', 'DDF', 'DDG', 'DAW', 'DAZ',
            'DCK', 'DDB', 'DDD'
        ]
        
        for code in dl_order:
            if code in dl_elements:
                value = dl_elements[code]
            elif code in user_data:
                value = user_data[code]
            else:
                value = ""
            
            ansi_parts.append(f"{code}{value}")

        # Add ZC elements
        zc_order = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for code in zc_order:
            value = zc_elements.get(code, "")
            ansi_parts.append(f"{code}{value}")

        # Join with record separators
        return '{RS}'.join(ansi_parts) + '{RS}'

    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {e}")
    except Exception as e:
        raise ValueError(f"Error converting XML to AAMVA: {e}")


def format_aamva_date(date_str: str) -> str:
    """Convert YYYY-MM-DD to MMDDYYYY format"""
    if not date_str or len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        return date_str
    return f"{date_str[5:7]}{date_str[8:10]}{date_str[0:4]}"


def format_height(height_str: str) -> str:
    """Convert 5'9\" to 069 IN format"""
    if not height_str:
        return ""
    
    # Remove any existing IN suffix
    height_str = height_str.replace(' IN', '').replace('IN', '').strip()
    
    # Try to parse feet/inches format
    match = re.match(r'(\d+)\'(\d+)\"?', height_str)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        total_inches = feet * 12 + inches
        return f"{total_inches:03d} IN"
    
    # Try to parse just inches
    try:
        inches = int(height_str)
        return f"{inches:03d} IN"
    except:
        return height_str


def format_weight(weight_str: str) -> str:
    """Convert 205lb to 205LB format"""
    if not weight_str:
        return ""
    return weight_str.replace('lb', 'LB').replace(' ', '')


def main():
    """Test the converter with sample XML data"""
    if len(sys.argv) < 2:
        print("Usage: python xml_to_aamva_converter.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        print(f"Converting XML file: {xml_file}")
        
        # Convert to AAMVA
        ansi_data = xml_to_aamva_ansi(xml_content)
        print(f"\nGenerated AAMVA data:")
        print("-" * 50)
        lines = ansi_data.split('{RS}')
        for i, line in enumerate(lines[:15], 1):  # Show first 15 lines
            print(f"{i:2d}. {line}")
        if len(lines) > 15:
            print(f"... and {len(lines) - 15} more lines")
        print("-" * 50)
        
        # Validate
        compliance = validate_aamva_compliance(ansi_data.replace('{RS}', '\n'))
        print(f"\nAAMVA Compliance Score: {compliance['compliance_score']:.1f}%")
        
        if compliance['errors']:
            print("Errors:")
            for error in compliance['errors']:
                print(f"  - {error}")
        
        if compliance['warnings']:
            print("Warnings:")
            for warning in compliance['warnings']:
                print(f"  - {warning}")
        
        if compliance['valid']:
            print("✓ AAMVA data is valid")
        else:
            print("✗ AAMVA data has validation errors")
            
    except FileNotFoundError:
        print(f"ERROR: File not found: {xml_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()