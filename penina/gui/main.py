#!/usr/bin/env python3
"""
Penina GUI Application

A simple desktop application for scanning PDF417 barcodes and encoding XML data
into PDF417 barcodes with AAMVA validation.

Features:
- Scan PDF417 barcodes from images
- Encode XML data into PDF417 barcodes
- AAMVA validation and compliance scoring
- Professional PDF417 encoding
- Drag & drop file support
- Preview and save results

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from datetime import datetime
from PIL import Image, ImageTk
import io


class PDF417App:
    def __init__(self, root):
        self.root = root
        self.root.title("Penina PDF417 Scanner & Encoder")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Set up the main layout
        self.setup_ui()
        
        # Initialize file paths
        self.current_image = None
        self.current_xml = None
        
    def setup_ui(self):
        """Set up the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Penina PDF417 Scanner & Encoder", 
                               font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Scanner tab
        self.scanner_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.scanner_frame, text="Scanner")
        self.setup_scanner_tab()
        
        # Encoder tab
        self.encoder_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.encoder_frame, text="Encoder")
        self.setup_encoder_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 0))
        
    def setup_scanner_tab(self):
        """Set up the scanner tab interface"""
        # Left panel - Image display
        left_frame = ttk.LabelFrame(self.scanner_frame, text="Image Preview", padding="10")
        left_frame.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky=(tk.N, tk.S, tk.W, tk.E))
        self.scanner_frame.columnconfigure(1, weight=1)
        self.scanner_frame.rowconfigure(0, weight=1)
        
        # Image canvas
        self.image_canvas = tk.Canvas(left_frame, width=400, height=300, bg='white', relief=tk.SUNKEN)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Controls and results
        right_frame = ttk.Frame(self.scanner_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
        
        # Controls
        controls_frame = ttk.LabelFrame(right_frame, text="Controls", padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File selection
        ttk.Label(controls_frame, text="Image File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.image_path_var = tk.StringVar()
        image_entry = ttk.Entry(controls_frame, textvariable=self.image_path_var, width=50)
        image_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        browse_btn = ttk.Button(controls_frame, text="Browse...", command=self.browse_image)
        browse_btn.grid(row=1, column=1, padx=(10, 0), pady=(0, 5))
        
        scan_btn = ttk.Button(controls_frame, text="Scan PDF417", command=self.scan_image)
        scan_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Results
        results_frame = ttk.LabelFrame(right_frame, text="Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=60)
        self.results_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Save button
        save_frame = ttk.Frame(right_frame)
        save_frame.grid(row=2, column=0, sticky=(tk.E))
        
        save_btn = ttk.Button(save_frame, text="Save Results", command=self.save_scanner_results)
        save_btn.pack(side=tk.RIGHT)
        
        # Instructions
        ttk.Label(left_frame, text="Load image using Browse button", foreground="gray").pack(expand=True)
        
    def setup_encoder_tab(self):
        """Set up the encoder tab interface"""
        # Left panel - XML input
        left_frame = ttk.LabelFrame(self.encoder_frame, text="XML Input", padding="10")
        left_frame.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky=(tk.N, tk.S, tk.W, tk.E))
        self.encoder_frame.columnconfigure(1, weight=1)
        self.encoder_frame.rowconfigure(0, weight=1)
        
        # XML text area
        xml_frame = ttk.Frame(left_frame)
        xml_frame.pack(fill=tk.BOTH, expand=True)
        
        self.xml_text = scrolledtext.ScrolledText(xml_frame, height=20, width=50)
        self.xml_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X)
        
        ttk.Label(controls_frame, text="XML File:").pack(side=tk.LEFT)
        
        self.xml_path_var = tk.StringVar()
        xml_entry = ttk.Entry(controls_frame, textvariable=self.xml_path_var, width=30)
        xml_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        browse_xml_btn = ttk.Button(controls_frame, text="Browse...", command=self.browse_xml)
        browse_xml_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        load_xml_btn = ttk.Button(controls_frame, text="Load XML", command=self.load_xml_file)
        load_xml_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right panel - Controls and preview
        right_frame = ttk.Frame(self.encoder_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
        
        # Encoding controls
        encode_frame = ttk.LabelFrame(right_frame, text="Encoding Controls", padding="10")
        encode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(encode_frame, text="Output Image:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.output_path_var = tk.StringVar()
        output_entry = ttk.Entry(encode_frame, textvariable=self.output_path_var, width=40)
        output_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        browse_output_btn = ttk.Button(encode_frame, text="Browse...", command=self.browse_output)
        browse_output_btn.grid(row=1, column=1, padx=(10, 0), pady=(0, 5))
        
        encode_btn = ttk.Button(encode_frame, text="Encode to PDF417", command=self.encode_xml)
        encode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Preview
        preview_frame = ttk.LabelFrame(right_frame, text="Barcode Preview", padding="10")
        preview_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=(0, 10))
        
        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=200, bg='white', relief=tk.SUNKEN)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status and validation
        status_frame = ttk.LabelFrame(right_frame, text="Status & Validation", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        self.compliance_var = tk.StringVar()
        self.compliance_var.set("Compliance: Not checked")
        compliance_label = ttk.Label(status_frame, textvariable=self.compliance_var, font=("Helvetica", 10, "bold"))
        compliance_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.validation_text = scrolledtext.ScrolledText(status_frame, height=8, width=50)
        self.validation_text.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Save button
        save_frame = ttk.Frame(right_frame)
        save_frame.grid(row=3, column=0, sticky=(tk.E))
        
        save_encoded_btn = ttk.Button(save_frame, text="Save Barcode", command=self.save_encoded_barcode)
        save_encoded_btn.pack(side=tk.RIGHT)
        
    def browse_image(self):
        """Open file dialog to select image"""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.image_path_var.set(file_path)
            self.load_image(file_path)
            
    def browse_xml(self):
        """Open file dialog to select XML file"""
        file_path = filedialog.askopenfilename(
            title="Select XML File",
            filetypes=[("XML files", "*.xml *.txt")]
        )
        if file_path:
            self.xml_path_var.set(file_path)
            
    def browse_output(self):
        """Open file dialog to select output file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Barcode Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path_var.set(file_path)
            
    def load_image(self, image_path):
        """Load and display image"""
        try:
            # Load image
            pil_img = Image.open(image_path)
            
            # Resize for display
            display_img = pil_img.copy()
            display_img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            
            # Convert to Tkinter format
            tk_img = ImageTk.PhotoImage(display_img)
            
            # Display image
            self.image_canvas.delete("all")
            self.image_canvas.create_image(200, 150, image=tk_img, anchor=tk.CENTER)
            self.image_canvas.image = tk_img  # Keep reference
            
            self.current_image = image_path
            self.status_var.set(f"Loaded: {os.path.basename(image_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            
    def load_xml_file(self):
        """Load XML file into text area"""
        file_path = self.xml_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("Warning", "Please select a valid XML file")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            self.xml_text.delete(1.0, tk.END)
            self.xml_text.insert(tk.END, xml_content)
            self.status_var.set(f"Loaded XML: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load XML file: {e}")
            
    def scan_image(self):
        """Scan PDF417 barcode from image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "Please select an image file first")
            return
            
        # Run scanning in background thread
        def scan_thread():
            try:
                self.status_var.set("Scanning PDF417 barcode...")
                
                # Import scanner functionality from tests folder
                sys.path.insert(0, os.path.abspath("."))
                from tests.decoder_xml import decode_pdf417_xml, save_xml_results
                
                # Scan the image
                results = decode_pdf417_xml(self.current_image)
                
                if results:
                    # Generate XML output
                    from tests.decoder_xml import create_xml_output
                    xml_content = create_xml_output(self.current_image, results)
                    
                    # Display results
                    self.root.after(0, self.display_scanner_results, xml_content)
                    self.status_var.set("Scan completed successfully")
                else:
                    self.root.after(0, messagebox.showinfo, "Info", "No PDF417 barcodes found in image")
                    self.status_var.set("No barcodes found")
                    
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Error", f"Scanning failed: {e}")
                self.status_var.set("Scanning failed")
                
        threading.Thread(target=scan_thread, daemon=True).start()
        
    def display_scanner_results(self, xml_content):
        """Display scanner results in text area"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, xml_content)
        
    def save_scanner_results(self):
        """Save scanner results to file"""
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No results to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Scanner Results",
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Results saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                
    def encode_xml(self):
        """Encode XML data to PDF417 barcode"""
        xml_content = self.xml_text.get(1.0, tk.END).strip()
        if not xml_content:
            messagebox.showwarning("Warning", "Please enter XML data or load an XML file")
            return
            
        output_path = self.output_path_var.get()
        if not output_path:
            messagebox.showwarning("Warning", "Please specify output file path")
            return
            
        # Run encoding in background thread
        def encode_thread():
            try:
                self.status_var.set("Encoding XML to PDF417...")
                
                # Import encoder functionality from tests folder
                sys.path.insert(0, os.path.abspath("."))
                from tests.encoder_xml import build_aamva_string_from_xml, encode_pdf417_barcode_enhanced
                from tests.xml_to_aamva_converter import validate_aamva_compliance
                
                # Convert XML to AAMVA string
                aamva_string = build_aamva_string_from_xml(xml_content)
                
                if aamva_string:
                    # Validate AAMVA compliance
                    compliance = validate_aamva_compliance(aamva_string.replace('\x1e', '{RS}'))
                    
                    # Update compliance display
                    self.root.after(0, self.update_compliance_display, compliance)
                    
                    # Encode to PDF417
                    success = encode_pdf417_barcode_enhanced(aamva_string, output_path)
                    
                    if success:
                        self.root.after(0, self.display_encoded_barcode, output_path)
                        self.status_var.set("Encoding completed successfully")
                    else:
                        self.root.after(0, messagebox.showerror, "Error", "Failed to create barcode image")
                        self.status_var.set("Encoding failed")
                else:
                    self.root.after(0, messagebox.showerror, "Error", "Failed to convert XML to AAMVA format")
                    self.status_var.set("Conversion failed")
                    
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Error", f"Encoding failed: {e}")
                self.status_var.set("Encoding failed")
                
        threading.Thread(target=encode_thread, daemon=True).start()
        
    def update_compliance_display(self, compliance):
        """Update compliance display in GUI"""
        score = compliance['compliance_score']
        self.compliance_var.set(f"Compliance: {score:.1f}%")
        
        # Clear validation text
        self.validation_text.delete(1.0, tk.END)
        
        # Add validation results
        if compliance['valid']:
            self.validation_text.insert(tk.END, "✓ AAMVA Validation: PASSED\n\n")
        else:
            self.validation_text.insert(tk.END, "✗ AAMVA Validation: FAILED\n\n")
            
        if compliance['errors']:
            self.validation_text.insert(tk.END, "Errors:\n")
            for error in compliance['errors']:
                self.validation_text.insert(tk.END, f"  - {error}\n")
            self.validation_text.insert(tk.END, "\n")
            
        if compliance['warnings']:
            self.validation_text.insert(tk.END, "Warnings:\n")
            for warning in compliance['warnings']:
                self.validation_text.insert(tk.END, f"  - {warning}\n")
                
    def display_encoded_barcode(self, image_path):
        """Display encoded barcode preview"""
        try:
            pil_img = Image.open(image_path)
            display_img = pil_img.copy()
            display_img.thumbnail((400, 200), Image.Resampling.LANCZOS)
            
            tk_img = ImageTk.PhotoImage(display_img)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(200, 100, image=tk_img, anchor=tk.CENTER)
            self.preview_canvas.image = tk_img  # Keep reference
            
        except Exception as e:
            self.validation_text.insert(tk.END, f"\nFailed to load preview: {e}")
            
    def save_encoded_barcode(self):
        """Save encoded barcode (if different path needed)"""
        if not self.output_path_var.get():
            messagebox.showwarning("Warning", "No barcode generated yet")
            return
            
        # File is already saved by encode_xml, just confirm
        messagebox.showinfo("Success", f"Barcode saved to: {self.output_path_var.get()}")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PDF417App(root)
    root.mainloop()


if __name__ == "__main__":
    main()