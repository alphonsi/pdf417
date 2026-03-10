# Penina PDF417 Scanner & Encoder

**Author:** Erick Ochieng Opiyo  
**Email:** [opiyoerick08@gmail.com](mailto:opiyoerick08@gmail.com)  
**GitHub:** [https://github.com/alphonsi](https://github.com/alphonsi)  
**Version:** 1.0.0

## Overview

Penina is a comprehensive Python package for scanning PDF417 barcodes and encoding XML data into PDF417 barcodes with AAMVA validation. It provides both command-line tools and a user-friendly desktop GUI application.

## Features

### 📸 **PDF417 Scanning**
- Scan PDF417 barcodes from images
- Extract AAMVA data from driver's licenses and IDs
- Output results in XML format compatible with online scanners
- Support for various image formats (JPG, PNG, BMP, etc.)

### 🔐 **AAMVA Validation**
- Comprehensive AAMVA data validation
- 100% compliance scoring
- Field-specific validation (dates, formats, required fields)
- Header validation (issuer ID, version, entries)

### 🏷️ **PDF417 Encoding**
- Convert XML data to professional PDF417 barcodes
- pylibdmtx integration with treepoem fallback
- 600 DPI professional quality output
- Industry-standard barcode dimensions (1390x324 pixels)

### 🖥️ **Desktop GUI**
- User-friendly desktop application
- Drag & drop file support
- Real-time validation and compliance scoring
- Preview and save results
- Background processing with status updates

## Installation

### Prerequisites
```bash
pip install pyinstaller
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### GUI Application
```bash
# Start the desktop application
python -m penina

# Or run the built executable
dist/Penina_PDF417_Scanner_Encoder.exe
```

### Command Line Tools

#### Scanning PDF417 Barcodes
```bash
# Scan an image and save results
python -m penina --scanner --image license.jpg --output results.xml

# Scan with default output filename
python -m penina --scanner --image license.jpg
```

#### Encoding XML to PDF417
```bash
# Encode XML to PDF417 barcode
python -m penina --encoder --xml data.xml --output barcode.png

# Encode with default output filename
python -m penina --encoder --xml data.xml
```

#### Application Information
```bash
# Show application info and dependency status
python -m penina --info
```

## Package Structure

```
pdf417/
├── penina/                    # Main package
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main application entry point
│   ├── gui/                  # GUI application
│   │   ├── __init__.py
│   │   └── main.py           # Main GUI application
│   ├── scanner/              # Scanner module
│   │   ├── __init__.py
│   │   └── pdf417_scanner.py # Scanner functionality
│   ├── encoder/              # Encoder module
│   │   ├── __init__.py
│   │   └── pdf417_encoder.py # Encoder functionality
│   ├── converter/            # Converter module
│   │   ├── __init__.py
│   │   └── xml_converter.py  # XML to ANSI converter
│   └── core/                 # Core utilities
│       ├── __init__.py
│       └── utils.py          # Shared utilities
├── tests/                    # Test files and examples
├── penina_app.spec          # PyInstaller configuration
├── build_exe.bat            # Windows build script
├── requirements.txt         # Dependencies
└── README_PENINA.md        # This file
```

## Building Windows Executable

### Quick Build
```bash
# Run the build script
build_exe.bat
```

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Install dependencies
pip install -r requirements.txt

# Build with spec file
pyinstaller penina_app.spec

# Or direct build
pyinstaller --onefile --windowed --name "Penina_PDF417_Scanner_Encoder" penina/main.py
```

### Build Output
- **Executable Location:** `dist/Penina_PDF417_Scanner_Encoder.exe`
- **Estimated File Size:** 50-100MB (due to native dependencies)
- **Compatibility:** Windows 10 & 11

## Supported Formats

### Input Formats
- **Images:** JPG, JPEG, PNG, BMP, GIF, TIFF
- **XML:** AAMVA XML format
- **Text:** Raw AAMVA data

### Output Formats
- **Images:** PNG (600 DPI, professional quality)
- **XML:** Scanner-compatible format
- **Text:** Human-readable AAMVA data

## AAMVA Compliance

The package includes comprehensive AAMVA validation:

- ✅ **Header Validation:** IIN, version, entries
- ✅ **Field Validation:** Dates, formats, required fields
- ✅ **Data Integrity:** Cross-field validation
- ✅ **Compliance Scoring:** 0-100% compliance rating

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **PyInstaller Build Failures**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify native libraries are available

3. **Scanning Failures**
   - Ensure good image quality
   - Check lighting and focus
   - Crop image tightly around barcode

### Dependencies

The package requires several native libraries that may need special installation:

- **zxing-cpp:** For PDF417 scanning
- **pylibdmtx:** For PDF417 encoding
- **OpenCV:** For image processing
- **Pillow:** For image handling

## Development

### Testing
```bash
# Test GUI application
python -m penina

# Test individual modules
python -m penina --scanner --image tests/original.jpg --output test_output.xml
python -m penina --encoder --xml tests/decoded_output.txt --output test_barcode.png
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- **Email:** [opiyoerick08@gmail.com](mailto:opiyoerick08@gmail.com)
- **GitHub:** [https://github.com/alphonsi](https://github.com/alphonsi)

## Changelog

### v1.0.0 (Current)
- ✅ Complete package structure
- ✅ GUI application with scanner and encoder
- ✅ AAMVA validation and compliance scoring
- ✅ Professional PDF417 encoding
- ✅ Windows executable build system
- ✅ Comprehensive documentation