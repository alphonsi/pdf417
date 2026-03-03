# PDF417 Barcode Implementation

This project provides a complete PDF417 barcode generation and decoding solution using Python.

## Overview

PDF417 is a two-dimensional stacked bar code symbology capable of encoding large amounts of data. This implementation provides:

- **Encoding**: Generate PDF417 barcodes from text data using the `treepoem` library
- **Decoding**: Read PDF417 barcodes from images using the `zxing` library
- **Testing**: Comprehensive test suite to verify encoding/decoding functionality

## Requirements

Install the required dependencies:

```bash
pip install treepoem zxing pillow
```

Note: You may also need to install Java for zxing to work properly on some systems.

## Project Structure

### Core Module (`pdf_417/`)

- `pdf417_encoder.py` - PDF417 barcode generation script
- `pdf417_scanner.py` - PDF417 barcode scanning script

### Test Suite (`tests/`)

- `pdf417_test_suite.py` - Comprehensive test suite
- `test_pdf417.py` - Basic encoding test (legacy)
- `test_barcode_scanning.py` - Basic scanning test (legacy)
- `test_complete_pdf417.py` - Complete test (legacy)

### Test Images

- `test_complete_pdf417.png` - Sample barcode for testing
- `test_for_scanning.png` - Simple barcode for external scanning
- `test_generated_pdf417.png` - Generated test barcode

## Usage

### 1. Encoding (Generate PDF417 Barcodes)

**From Text Data:**
```bash
python pdf_417/pdf417_encoder.py
```

This will generate a PDF417 barcode from sample data and save it as `generated_barcode.png`.

**From Text File:**
```bash
python pdf_417/pdf417_encoder.py input_data.txt
```

This reads data from `input_data.txt` and generates `encoded_barcode.png`.

**Custom Encoding:**
```python
from pdf_417.pdf417_encoder import generate_pdf417_barcode, encode_from_file

# Generate custom barcode from text
output_file = generate_pdf417_barcode(
    data="Your custom data here",
    output_file="my_barcode.png",
    columns=12,
    security_level=4
)

# Generate barcode from file
output_file = encode_from_file(
    input_file="input_data.txt",
    output_file="encoded_barcode.png",
    columns=12,
    security_level=4
)
```

### 2. Scanning (Decode PDF417 Barcodes)

**Basic Scanning:**
```bash
python pdf_417/pdf417_scanner.py generated_barcode.png
```

This will scan the specified image file and decode any PDF417 barcodes found.

**Save Decoded Data to File:**
```bash
# Default output file
python pdf_417/pdf417_scanner.py license_back.png

# Custom output file name
python pdf_417/pdf417_scanner.py aamva_generated.png my_results.txt
```

This saves decoded data to `decoded_data.txt` or a specified output file.

**AAMVA Data Parsing:**
```bash
python pdf_417/pdf417_scanner.py license_barcode.png --aamva
```

This parses AAMVA-compliant driver's license and ID card barcodes, displaying structured information including:
- Personal information (names, DOB, sex, eye/hair color, height, weight)
- Address information (street, city, state, ZIP, country)
- License information (number, class, restrictions, endorsements)
- Header information (version, issuer, jurisdiction)

**Programmatic Scanning:**
```python
from pdf_417.pdf417_scanner import scan_pdf417_barcode, decode_to_file

# Scan an image
result = scan_pdf417_barcode("my_barcode.png")
print(f"Decoded data: {result}")

# Scan with AAMVA parsing
aamva_result = scan_pdf417_barcode("license_barcode.png", parse_aamva=True)
if isinstance(aamva_result, dict):
    print(f"AAMVA Version: {aamva_result['version']}")
    print(f"License Number: {aamva_result['license_info']['license_number']}")

# Save decoded data to file
success = decode_to_file("barcode_image.png", "results.txt")
if success:
    print("Decoded data saved to results.txt")
```

### 3. Testing (Complete Workflow)

```bash
python tests/pdf417_test_suite.py
```

This runs comprehensive tests including:
- PDF417 barcode generation
- Image properties verification
- Decoding attempts with multiple approaches
- Round-trip encoding/decoding verification

## File Purposes

### Core Implementation
- **`pdf417_encoder.py`** - Standalone encoding script
- **`pdf417_scanner.py`** - Standalone scanning script
- **`pdf417_test_suite.py`** - Complete test suite

### Legacy Test Files (Keep for Reference)
- **`test_pdf417.py`** - Basic encoding test (legacy)
- **`test_barcode_scanning.py`** - Basic scanning test (legacy)
- **`test_complete_pdf417.py`** - Complete test (legacy)

## Advanced Usage

### Custom Encoding Parameters

```python
from pdf_417.pdf417_encoder import generate_pdf417_barcode

# High-density encoding (more data, smaller modules)
generate_pdf417_barcode(
    data="Large amount of data...",
    columns=16,           # More columns = more data per row
    security_level=6      # Higher error correction
)

# Low-density encoding (easier to scan)
generate_pdf417_barcode(
    data="Simple data",
    columns=6,            # Fewer columns = larger modules
    security_level=2      # Lower error correction
)
```

### Multiple Barcode Scanning

```python
from pdf_417.pdf417_scanner import scan_multiple_barcodes

# Scan for multiple barcodes in one image
results = scan_multiple_barcodes("image_with_multiple_barcodes.png")
for i, result in enumerate(results):
    print(f"Barcode {i+1}: {result}")
```

### Integration with Other Applications

```python
# Import the scanner functions directly
from pdf_417.pdf417_scanner import scan_pdf417_barcode, decode_to_file

def process_image(image_path):
    # Scan the image for PDF417 barcodes
    return scan_pdf417_barcode(image_path)

# Use in web applications, desktop apps, etc.
results = process_image("uploaded_image.png")
```

## Test Results

### Current Status

- ✅ **Encoding**: PDF417 barcode generation works correctly with treepoem
- ✅ **Decoding**: PDF417 barcode decoding works correctly with zxing
- ✅ **Compatibility**: treepoem + zxing combination resolves library compatibility issues

### Generated Barcodes

The system successfully generates PDF417 barcodes with:
- Proper dimensions (e.g., 546x30 pixels)
- Correct black/white format
- Standard PDF417 structure

### Decoding Solution

This implementation uses `zxing` for decoding, which provides excellent PDF417 support and works well with barcodes generated by `treepoem`. This combination resolves the compatibility issues found with other library combinations.

## Alternative Solutions

### Option 1: Current Recommended Combination

The current implementation uses:
- **Encoding**: `treepoem` library
- **Decoding**: `zxing` library
- **Installation**: `pip install treepoem zxing pillow`

### Option 2: Professional Alternative

For production use, consider:
- **Encoding**: `reportlab` library (professional-grade)
- **Decoding**: `zxing` library (reliable)
- **Installation**: `pip install reportlab zxing`

### Option 3: Manual Decoding

Implement custom PDF417 decoding algorithm (more complex but library-independent).

### Option 4: External Tools

Use command-line tools like `zbarimg` for decoding:

```bash
zbarimg barcode.png
```

## Mobile Testing

Generated barcodes can be tested with mobile apps:

1. **Download "Barcode Scanner"** (ZXing) from your app store
2. **Open the app** and point your camera at the barcode image
3. **The app should read** the encoded data

## License

This project is provided as-is for educational and testing purposes.

## Notes

- The generated barcodes can be scanned with mobile apps like "Barcode Scanner"
- For production use, consider testing with your specific scanning hardware
- Different PDF417 parameters (columns, security level, rows) affect barcode size and readability
- Always test encoding/decoding with your target scanning devices