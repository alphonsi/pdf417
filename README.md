# PDF417 Scanner & Encoder

## Overview

This repository contains a complete PDF417 barcode scanning and encoding solution built with Python. The project has been restructured into a professional package called **Penina** that provides both GUI and command-line interfaces for working with PDF417 barcodes.

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alphonsi/pdf417.git
   cd pdf417
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # GUI Application
   python -m penina
   
   # Or run the Windows executable
   dist/penina.exe
   ```

### Windows Executable

A pre-built Windows executable is available in the `dist/` folder:
- **File:** `dist/penina.exe`
- **Size:** ~73MB
- **Type:** Portable, single-file executable
- **Requirements:** Windows 10 or 11

## 📦 Package Structure

```
pdf417/
├── penina/                    # Main package
│   ├── __init__.py           # Package with author info
│   ├── main.py               # Main application entry point
│   ├── gui/                  # GUI application
│   ├── scanner/              # PDF417 scanning module
│   ├── encoder/              # PDF417 encoding module
│   ├── converter/            # XML to AAMVA converter
│   └── core/                 # Core utilities
├── tests/                    # Test files and examples
├── dist/                     # Distribution folder
│   └── penina.exe           # Windows executable
├── README_PENINA.md         # Detailed documentation
└── requirements.txt         # Dependencies
```

## 🎯 Features

### ✅ Complete PDF417 Solution
- **Scanning:** Extract data from PDF417 barcodes in images
- **Encoding:** Generate PDF417 barcodes from XML data
- **Validation:** AAMVA compliance checking and scoring
- **Conversion:** XML to ANSI AAMVA format conversion

### ✅ Professional GUI Application
- **Dual Interface:** Scanner and encoder tabs
- **Drag & Drop:** Easy file handling
- **Real-time Processing:** Background operations with progress indicators
- **Validation:** Built-in AAMVA compliance scoring
- **Export Options:** Multiple output formats

### ✅ Command Line Tools
```bash
# Scan PDF417 barcodes
python -m penina --scanner --image license.jpg --output results.xml

# Encode XML to PDF417
python -m penina --encoder --xml data.xml --output barcode.png

# Show application info
python -m penina --info
```

### ✅ Proven Functionality
- **Tested:** All functionality validated with real test files
- **Round-trip Tested:** Scan → Convert → Encode → Scan workflow verified
- **AAMVA Compliant:** Professional-grade encoding standards

## 🛠️ Development

### Building the Windows Executable

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script:**
   ```bash
   build_exe.bat
   ```

3. **Find the executable:**
   ```
   dist/penina.exe
   ```

### Dependencies

The project uses the following key libraries:
- **PIL/Pillow:** Image processing
- **zxing-cpp:** Barcode scanning
- **pylibdmtx:** PDF417 encoding
- **opencv-python:** Computer vision
- **numpy:** Numerical operations
- **treepoem:** Barcode generation
- **tkinter:** GUI framework

## 📋 Usage Examples

### Scanning PDF417 Barcodes

```python
from penina.scanner import PDF417Scanner

scanner = PDF417Scanner()
results = scanner.scan_image("license.jpg")
print(results)
```

### Encoding PDF417 Barcodes

```python
from penina.encoder import PDF417Encoder

encoder = PDF417Encoder()
encoder.encode_from_xml("data.xml", "barcode.png")
```

### GUI Application

The GUI provides a user-friendly interface for both scanning and encoding operations with drag-and-drop support and real-time validation.

## 🧪 Testing

The repository includes comprehensive test files:
- **Test Images:** `tests/original.jpg`, `tests/enhanced_barcode.png`
- **Test Data:** `tests/decoded_output.txt`, `tests/enhanced_output.txt`
- **Test Scripts:** `tests/decoder_xml.py`, `tests/encoder_xml.py`

## 📄 Documentation

- **README_PENINA.md:** Comprehensive documentation for the Penina package
- **Module Documentation:** Each module includes detailed docstrings
- **Usage Examples:** Code examples in test files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- **Email:** opiyoerick08@gmail.com
- **GitHub:** [alphonsi/pdf417](https://github.com/alphonsi/pdf417)

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

- **GUI Layer:** User interface and interaction handling
- **Business Logic:** Core scanning and encoding functionality
- **Utilities:** Shared helper functions and validation
- **Tests:** Comprehensive test suite for validation

## 🎨 Screenshots

[Include screenshots of the GUI application here when available]

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies:** Run `pip install -r requirements.txt`
2. **Permission Errors:** Ensure write permissions for output directories
3. **Large Files:** The Windows executable is ~73MB due to bundled dependencies

### Getting Help

- Check the detailed documentation in `README_PENINA.md`
- Review test files for usage examples
- Open an issue on GitHub for support

---

**Author:** Erick Ochieng Opiyo  
**Email:** opiyoerick08@gmail.com  
**GitHub:** https://github.com/alphonsi  
**Package:** Penina PDF417 Scanner & Encoder