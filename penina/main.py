#!/usr/bin/env python3
"""
penina/main.py

Main entry point for the Penina PDF417 Scanner & Encoder application.

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi
"""

import sys
import os
import argparse
import traceback
from datetime import datetime

# Add current directory to path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .gui.main import PDF417App
    from .scanner.pdf417_scanner import decode_pdf417_xml, save_xml_results
    from .encoder.pdf417_encoder import build_aamva_string_from_xml, encode_pdf417_barcode_enhanced
    from .converter.xml_converter import validate_aamva_compliance
    from .core.utils import log_message, validate_dependencies, get_app_name, get_app_version, get_author_info, check_dependencies
except ImportError:
    # Fallback for when running as script
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gui.main import PDF417App
    from scanner.pdf417_scanner import decode_pdf417_xml, save_xml_results
    from encoder.pdf417_encoder import build_aamva_string_from_xml, encode_pdf417_barcode_enhanced
    from converter.xml_converter import validate_aamva_compliance
    from core.utils import log_message, validate_dependencies, get_app_name, get_app_version, get_author_info, check_dependencies


def run_gui():
    """Run the GUI application."""
    try:
        import tkinter as tk
        root = tk.Tk()
        app = PDF417App(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Please install tkinter or run in command line mode")
        sys.exit(1)
    except Exception as e:
        print(f"Error running GUI: {e}")
        if os.getenv("DEBUG"):
            traceback.print_exc()
        sys.exit(1)


def run_scanner(args):
    """Run the scanner in command line mode."""
    if not args.image:
        print("Error: --image argument is required for scanner mode")
        sys.exit(1)
    
    try:
        log_message(f"Starting PDF417 scanner on {args.image}")
        
        # Scan the image
        results = decode_pdf417_xml(args.image)
        
        if results:
            # Generate XML output
            try:
                from .scanner.pdf417_scanner import create_xml_output
            except ImportError:
                from scanner.pdf417_scanner import create_xml_output
            xml_content = create_xml_output(args.image, results)
            
            # Save results
            output_file = args.output or "decoded_pdf417.xml.txt"
            save_xml_results(results, output_file, args.image)
            
            log_message(f"Successfully scanned and saved to {output_file}")
        else:
            log_message("No PDF417 barcodes found in image", "WARNING")
            sys.exit(1)
            
    except Exception as e:
        log_message(f"Scanner error: {e}", "ERROR")
        if os.getenv("DEBUG"):
            traceback.print_exc()
        sys.exit(1)


def run_encoder(args):
    """Run the encoder in command line mode."""
    if not args.xml:
        print("Error: --xml argument is required for encoder mode")
        sys.exit(1)
    
    try:
        log_message(f"Starting PDF417 encoder with {args.xml}")
        
        # Read XML file
        with open(args.xml, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Convert XML to AAMVA string
        aamva_string = build_aamva_string_from_xml(xml_content)
        
        if not aamva_string:
            log_message("Failed to convert XML to AAMVA format", "ERROR")
            sys.exit(1)
        
        # Validate AAMVA compliance
        compliance = validate_aamva_compliance(aamva_string.replace('\x1e', '{RS}'))
        log_message(f"AAMVA Compliance Score: {compliance['compliance_score']:.1f}%")
        
        if not compliance['valid']:
            log_message("AAMVA data has validation errors:", "WARNING")
            for error in compliance['errors']:
                log_message(f"  - {error}", "WARNING")
        
        # Encode to PDF417
        output_file = args.output or "encoded_barcode.png"
        success = encode_pdf417_barcode_enhanced(aamva_string, output_file)
        
        if success:
            log_message(f"Successfully encoded PDF417 barcode to {output_file}")
        else:
            log_message("Failed to create barcode image", "ERROR")
            sys.exit(1)
            
    except Exception as e:
        log_message(f"Encoder error: {e}", "ERROR")
        if os.getenv("DEBUG"):
            traceback.print_exc()
        sys.exit(1)


def run_info():
    """Display application information."""
    print(f"{get_app_name()} v{get_app_version()}")
    print(f"Author: {get_author_info()['name']}")
    print(f"Email: {get_author_info()['email']}")
    print(f"GitHub: {get_author_info()['github']}")
    print()
    
    # Check dependencies
    print("Dependency Status:")
    deps = check_dependencies()
    for dep, status in deps.items():
        status_str = "OK" if status else "MISSING"
        print(f"  {status_str} {dep}")
    
    print()
    if not validate_dependencies():
        print("Warning: Some required dependencies are missing!")
        print("Please install them to use all features.")
    else:
        print("All required dependencies are available.")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Penina PDF417 Scanner & Encoder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run GUI application
  python -m penina
  
  # Scan PDF417 barcode from image
  python -m penina --scanner --image license.jpg
  
  # Encode XML to PDF417 barcode
  python -m penina --encoder --xml data.xml
  
  # Show application information
  python -m penina --info
        """
    )
    
    # Mode selection
    parser.add_argument('--gui', action='store_true', help='Run GUI application (default)')
    parser.add_argument('--scanner', action='store_true', help='Run scanner in command line mode')
    parser.add_argument('--encoder', action='store_true', help='Run encoder in command line mode')
    parser.add_argument('--info', action='store_true', help='Show application information')
    
    # Scanner arguments
    parser.add_argument('--image', help='Input image file for scanner')
    parser.add_argument('--output', help='Output file path')
    
    # Encoder arguments
    parser.add_argument('--xml', help='Input XML file for encoder')
    
    # Other options
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Set debug environment variable if requested
    if args.debug:
        os.environ['DEBUG'] = '1'
    
    # Determine mode
    if args.info:
        run_info()
    elif args.scanner:
        run_scanner(args)
    elif args.encoder:
        run_encoder(args)
    else:
        # Default to GUI mode
        run_gui()


if __name__ == "__main__":
    main()