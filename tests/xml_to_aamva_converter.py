#!/usr/bin/env python3
"""
XML to ANSI AAMVA Converter
Converts XML AAMVA data to raw ANSI format with {RS} separators for PDF417 encoding
"""

import xml.etree.ElementTree as ET
import re
import datetime


def extract_xml_from_content(content):
    """
    Extract XML content from scanner output that may contain headers
    
    Args:
        content (str): Content that may contain scanner headers and XML
        
    Returns:
        str: Pure XML content
    """
    
    # Find the start of XML content
    xml_start = content.find('<AAMVA>')
    if xml_start == -1:
        # Try to find any XML tag
        xml_start = content.find('<')
    
    if xml_start != -1:
        # Extract from the first XML tag to the end
        xml_content = content[xml_start:]
        return xml_content
    
    # If no XML found, return original content
    return content


def xml_to_aamva_ansi(xml_content):
    """
    Convert XML AAMVA data to raw ANSI format with {RS} separators
    
    Args:
        xml_content (str): XML content to convert (can include scanner headers)
        
    Returns:
        str: Raw ANSI AAMVA format with {RS} separators
    """
    
    # Extract pure XML content if needed
    pure_xml = extract_xml_from_content(xml_content)
    
    # Parse XML content
    try:
        root = ET.fromstring(pure_xml)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML content: {e}")
    
    # ANSI header components
    header_parts = []
    
    # Extract header information from <head> section
    head_section = root.find('.//head')
    if head_section is not None:
        # Get issuer identification number (6 digits)
        issuer_elem = head_section.find('.//issuer')
        issuer_id = issuer_elem.text if issuer_elem is not None else "636014"
        
        # Get AAMVA version (2 digits)
        version_elem = head_section.find('.//version')
        version = version_elem.text if version_elem is not None else "04"
        
        # Get jurisdiction version (2 digits)
        jurver_elem = head_section.find('.//jurver')
        jurver = jurver_elem.text if jurver_elem is not None else "00"
        
        # Get number of entries (2 digits)
        entries_elem = head_section.find('.//entries')
        entries = entries_elem.text if entries_elem is not None else "02"
        
        # Build ANSI header with 12 digits total: issuer(6) + version(2) + jurver(2) + entries(2)
        header_parts = [issuer_id, version, jurver, entries]
    
    # Build ANSI header
    ansi_header = f"ANSI {''.join(header_parts)}"
    
    # Process subfiles
    subfile_data = []
    
    # Find all subfile elements
    subfiles = root.findall('.//subfile')
    
    for subfile in subfiles:
        # Process elements within each subfile
        elements = subfile.findall('.//element')
        
        for element in elements:
            # Get element ID and value
            element_id = element.get('id', '')
            element_value = element.text or ""
            
            if element_id:  # Only add if we have an ID
                subfile_data.append(f"{element_id}{element_value}")
    
    # Combine all parts with {RS} separators
    all_parts = [ansi_header] + subfile_data
    ansi_output = "{RS}".join(all_parts)
    
    return ansi_output


def parse_xml_to_dict(xml_content):
    """
    Parse XML to a structured dictionary for easier processing
    
    Args:
        xml_content (str): XML content to parse
        
    Returns:
        dict: Structured data with header and subfile information
    """
    
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML content: {e}")
    
    result = {
        'header': {},
        'subfiles': []
    }
    
    # Parse header
    head_section = root.find('.//head')
    if head_section is not None:
        for child in head_section:
            result['header'][child.tag] = child.text
    
    # Parse subfiles
    subfiles = root.findall('.//subfile')
    for subfile in subfiles:
        subfile_data = {
            'designator': subfile.get('designator', ''),
            'offset': subfile.get('offset', ''),
            'length': subfile.get('length', ''),
            'elements': []
        }
        
        elements = subfile.findall('.//element')
        for element in elements:
            element_data = {
                'id': element.get('id', ''),
                'name': element.get('name', ''),
                'value': element.text or ""
            }
            subfile_data['elements'].append(element_data)
        
        result['subfiles'].append(subfile_data)
    
    return result


def validate_aamva_format(ansi_data):
    """
    Validate that the ANSI data follows AAMVA format
    
    Args:
        ansi_data (str): ANSI format data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    
    # Check if it starts with ANSI
    if not ansi_data.startswith('ANSI '):
        return False
    
    # Check for {RS} separators
    if '{RS}' not in ansi_data:
        return False
    
    # Split into parts
    parts = ansi_data.split('{RS}')
    
    # Should have at least header + some data
    if len(parts) < 2:
        return False
    
    # Check header format (should be "ANSI" + 12 digits for standard format)
    header = parts[0]
    if not re.match(r'^ANSI \d{12}$', header):
        return False
    
    return True


def validate_aamva_data(parsed_data):
    """
    Comprehensive AAMVA data validation
    
    Args:
        parsed_data (dict): Parsed XML data
        
    Returns:
        list: List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate header data
    head_data = parsed_data.get('head', {})
    if 'issuer' in head_data:
        issuer = head_data['issuer']
        if not re.match(r'^\d{6}$', issuer):
            errors.append(f"Invalid issuer ID format: {issuer} (should be 6 digits)")
    
    if 'version' in head_data:
        version = head_data['version']
        if not re.match(r'^\d{2}$', version):
            errors.append(f"Invalid AAMVA version format: {version} (should be 2 digits)")
    
    # Validate user data
    user_data = parsed_data.get('user', {})
    
    # Validate dates
    for date_field in ['dob', 'issued', 'expires']:
        if date_field in user_data and user_data[date_field]:
            date_str = user_data[date_field]
            if not validate_date_format(date_str):
                errors.append(f"Invalid date format for {date_field}: {date_str}")
    
    # Validate required fields
    required_fields = ['last', 'first', 'dob', 'id']
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate field lengths and formats
    field_validations = {
        'sex': (r'^[MF12]$', 'M/F or 1/2'),
        'eyes': (r'^[A-Z]{3}$', '3 uppercase letters'),
        'hair': (r'^[A-Z]{3}$', '3 uppercase letters'),
        'state': (r'^[A-Z]{2}$', '2 uppercase letters'),
        'postal': (r'^\d{5}(-\d{4})?$', '5 or 9 digits'),
        'country': (r'^[A-Z]{3}$', '3 uppercase letters')
    }
    
    for field, (pattern, description) in field_validations.items():
        if field in user_data and user_data[field]:
            if not re.match(pattern, user_data[field]):
                errors.append(f"Invalid {field} format: {user_data[field]} (should be {description})")
    
    # Validate DL elements
    dl_elements = parsed_data.get('dl_elements', {})
    
    # Validate specific DL fields
    if 'DBC' in dl_elements:  # Sex
        sex = dl_elements['DBC']
        if sex not in ['1', '2', 'M', 'F']:
            errors.append(f"Invalid sex code: {sex} (should be 1/M or 2/F)")
    
    if 'DAY' in dl_elements:  # Eye color
        eyes = dl_elements['DAY']
        valid_eyes = ['BLK', 'BLU', 'BRO', 'GRY', 'GRN', 'HAZ', 'MAR', 'PNK', 'SDN']
        if eyes not in valid_eyes:
            errors.append(f"Invalid eye color: {eyes}")
    
    if 'DAZ' in dl_elements:  # Hair color
        hair = dl_elements['DAZ']
        valid_hair = ['BAL', 'BLK', 'BLD', 'BRO', 'BRN', 'GRY', 'RED', 'SDY', 'WHI']
        if hair not in valid_hair:
            errors.append(f"Invalid hair color: {hair}")
    
    # Validate height format (should be 3 digits + " IN")
    if 'DAU' in dl_elements:
        height = dl_elements['DAU']
        if height and not re.match(r'^\d{3} IN$', height):
            errors.append(f"Invalid height format: {height} (should be XXX IN)")
    
    # Validate weight format (should be digits + "LB")
    if 'DAW' in dl_elements:
        weight = dl_elements['DAW']
        if weight and not re.match(r'^\d{2,3}LB$', weight):
            errors.append(f"Invalid weight format: {weight} (should be XXLB or XXXLB)")
    
    return errors


def validate_date_format(date_str):
    """
    Validate date format (supports YYYY-MM-DD and MMDDYYYY)
    """
    # YYYY-MM-DD format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    # MMDDYYYY format
    if re.match(r'^\d{8}$', date_str):
        try:
            datetime.datetime.strptime(date_str, '%m%d%Y')
            return True
        except ValueError:
            return False
    
    return False


def validate_aamva_compliance(ansi_data):
    """
    Validate AAMVA compliance including data integrity
    
    Args:
        ansi_data (str): ANSI format data
        
    Returns:
        dict: Validation results with errors and warnings
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'compliance_score': 0
    }
    
    # Basic format validation
    if not validate_aamva_format(ansi_data):
        result['valid'] = False
        result['errors'].append("Invalid AAMVA format")
        return result
    
    # Parse and validate data
    try:
        # Extract header info
        parts = ansi_data.split('{RS}')
        header = parts[0]
        
        # Check issuer ID
        issuer_match = re.search(r'ANSI (\d{6})', header)
        if issuer_match:
            issuer = issuer_match.group(1)
            # Common issuer IDs (this is not exhaustive)
            if issuer not in ['636014', '636026', '636045']:  # CA, NY, TX examples
                result['warnings'].append(f"Unknown issuer ID: {issuer}")
        
        # Check AAMVA version
        version_match = re.search(r'ANSI \d{6}(\d{2})', header)
        if version_match:
            version = version_match.group(1)
            if version not in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
                result['warnings'].append(f"Unknown AAMVA version: {version}")
        
        # Validate data fields
        data_parts = parts[1:]
        field_count = len(data_parts)
        
        # Check for minimum required fields
        required_fields = ['DCS', 'DAC', 'DBB', 'DAQ']  # Last, First, DOB, ID
        found_fields = [part[:3] for part in data_parts if part]
        
        missing_fields = [field for field in required_fields if field not in found_fields]
        if missing_fields:
            result['errors'].append(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Calculate compliance score
        total_checks = 10
        passed_checks = 10 - len(result['errors']) - len(result['warnings'])
        result['compliance_score'] = max(0, (passed_checks / total_checks) * 100)
        
        if result['errors']:
            result['valid'] = False
        
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Validation error: {e}")
    
    return result


def format_for_debugging(ansi_data):
    """
    Format ANSI data for human-readable debugging
    
    Args:
        ansi_data (str): Raw ANSI data
        
    Returns:
        str: Formatted output for debugging
    """
    
    if not ansi_data:
        return "No data to format"
    
    parts = ansi_data.split('{RS}')
    output_lines = []
    
    # Header line
    if parts:
        output_lines.append(f"Header: {parts[0]}")
        output_lines.append("-" * 50)
    
    # Data lines
    for i, part in enumerate(parts[1:], 1):
        if part:  # Skip empty parts
            field_id = part[:3] if len(part) >= 3 else part
            field_value = part[3:] if len(part) > 3 else ""
            output_lines.append(f"{i:2d}. {field_id}: {field_value}")
    
    return "\n".join(output_lines)


def convert_xml_file(input_file, output_file=None):
    """
    Convert XML file to ANSI format
    
    Args:
        input_file (str): Path to input XML file
        output_file (str, optional): Path to output file. If None, prints to console
        
    Returns:
        str: Converted ANSI data
    """
    
    # Read XML file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")
    
    # Convert to ANSI
    try:
        ansi_data = xml_to_aamva_ansi(xml_content)
    except Exception as e:
        raise Exception(f"Error converting XML to ANSI: {e}")
    
    # Write output or print
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(ansi_data)
            print(f"Successfully converted {input_file} to {output_file}")
        except Exception as e:
            raise Exception(f"Error writing output file: {e}")
    else:
        print("Converted ANSI data:")
        print("=" * 60)
        print(ansi_data)
        print("=" * 60)
        print("\nFormatted for debugging:")
        print(format_for_debugging(ansi_data))
        
        # Validate output
        if not validate_aamva_format(ansi_data):
            print("\nWARNING: Generated ANSI data is not in valid AAMVA format")
            print("This may still be usable, but check the format carefully.")
        else:
            print("\n✓ ANSI data validation passed")
    
    return ansi_data


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python xml_to_aamva_converter.py <input_xml_file> [output_file]")
        print("Example: python xml_to_aamva_converter.py decoded_output.txt converted.ansi")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_xml_file(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)