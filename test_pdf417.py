from PIL import Image
from pdf417decoder import PDF417Decoder
import treepoem

print("All libraries imported successfully!")
# Removed version check as treepoem doesn't have __version__ attribute

# Generate a simple test PDF417 barcode
test_data = "@\n\x1E\rANSI 636014TEST01DLTEST stessy Opiyo Test Nairobi KE 2026"
print("Generating barcode with data:", test_data[:50], "...")

barcode_image = treepoem.generate_barcode(
    barcode_type='pdf417',
    data=test_data,
    options={
        "columns": 12,           # Wider = more data per row
        "security_level": 4,     # Error correction (2-8; 4-5 is good balance)
        "rows": 0                # 0 = auto
    }
)

barcode_image = barcode_image.convert('1')  # Make it pure black/white for better scanning
barcode_image.save("test_generated_pdf417.png")
print("Success! Saved as: test_generated_pdf417.png")
print("Open the file in any image viewer to see the barcode.")
print("You can now scan it with a phone app like 'Barcode Scanner' to verify.")