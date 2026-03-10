"""
Penina PDF417 Scanner & Encoder

A comprehensive application for scanning PDF417 barcodes and encoding XML data
into PDF417 barcodes with AAMVA validation.

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi

Usage:
    from penina import main
    main.run()
"""

__version__ = "1.0.0"
__author__ = "Erick Ochieng Opiyo"
__author_phone__ = "+254751015001/+254110479722"
__author_email__ = "opiyoerick08@gmail.com"
__github__ = "https://github.com/alphonsi"
__description__ = "PDF417 Scanner & Encoder with AAMVA validation"

# Package exports
from . import gui
from . import scanner
from . import encoder
from . import converter
from . import core

__all__ = ['gui', 'scanner', 'encoder', 'converter', 'core']