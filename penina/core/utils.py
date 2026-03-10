#!/usr/bin/env python3
"""
penina/core/utils.py

Shared utilities and common functionality for the Penina application.

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi
"""

import os
import sys
from datetime import datetime
from typing import Optional


def validate_file_path(file_path: str, check_exists: bool = True, check_readable: bool = True) -> bool:
    """
    Validate a file path for existence and readability.
    
    Args:
        file_path: Path to validate
        check_exists: Whether to check if file exists
        check_readable: Whether to check if file is readable
        
    Returns:
        True if path is valid, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    if check_exists and not os.path.exists(file_path):
        return False
    
    if check_readable and not os.access(file_path, os.R_OK):
        return False
    
    return True


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp in specified format.
    
    Args:
        format_str: Timestamp format string
        
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_str)


def get_app_version() -> str:
    """Get application version from package."""
    try:
        from .. import __version__
        return __version__
    except ImportError:
        return "1.0.0"


def get_app_name() -> str:
    """Get application name."""
    return "Penina PDF417 Scanner & Encoder"


def get_author_info() -> dict:
    """Get author information."""
    return {
        "name": "Erick Ochieng Opiyo",
        "email": "opiyoerick08@gmail.com",
        "github": "https://github.com/alphonsi"
    }


def ensure_directory(path: str) -> bool:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return os.path.splitext(filename)[1].lower()


def is_image_file(filename: str) -> bool:
    """Check if file is an image file."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif'}
    return get_file_extension(filename) in image_extensions


def is_xml_file(filename: str) -> bool:
    """Check if file is an XML file."""
    xml_extensions = {'.xml', '.txt'}
    return get_file_extension(filename) in xml_extensions


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove invalid characters for Windows/Linux file systems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:250] + ext
    
    return sanitized


def get_temp_directory() -> str:
    """Get temporary directory path."""
    import tempfile
    return tempfile.gettempdir()


def cleanup_temp_files(pattern: str = "*.tmp", max_age_hours: int = 24) -> int:
    """
    Clean up temporary files older than specified age.
    
    Args:
        pattern: File pattern to match
        max_age_hours: Maximum age in hours
        
    Returns:
        Number of files cleaned up
    """
    import glob
    import time
    
    temp_dir = get_temp_directory()
    pattern_path = os.path.join(temp_dir, pattern)
    
    cleaned_count = 0
    max_age_seconds = max_age_hours * 3600
    
    for file_path in glob.glob(pattern_path):
        try:
            if os.path.getctime(file_path) < time.time() - max_age_seconds:
                os.remove(file_path)
                cleaned_count += 1
        except Exception:
            pass  # Skip files that can't be removed
    
    return cleaned_count


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    elif seconds < 60:
        return f"{seconds:.1f} s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes} min {remaining_seconds:.0f} s"


def get_system_info() -> dict:
    """Get basic system information."""
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "memory_total": format_file_size(psutil.virtual_memory().total),
        "memory_available": format_file_size(psutil.virtual_memory().available),
        "cpu_count": psutil.cpu_count(),
    }


def log_message(message: str, level: str = "INFO", timestamp: bool = True) -> None:
    """
    Log a message with optional timestamp.
    
    Args:
        message: Message to log
        level: Log level (INFO, WARNING, ERROR)
        timestamp: Whether to include timestamp
    """
    if timestamp:
        timestamp_str = get_timestamp("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp_str}] {level}: {message}")
    else:
        print(f"{level}: {message}")


def check_dependencies() -> dict:
    """
    Check if required dependencies are available.
    
    Returns:
        Dictionary with dependency status
    """
    dependencies = {
        'PIL': False,
        'zxingcpp': False,
        'pylibdmtx': False,
        'cv2': False,
        'numpy': False,
        'treepoem': False,
        'xml.etree.ElementTree': False,
    }
    
    for dep in dependencies:
        try:
            if dep == 'xml.etree.ElementTree':
                import xml.etree.ElementTree
            else:
                __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies


def validate_dependencies() -> bool:
    """Validate that all required dependencies are available."""
    deps = check_dependencies()
    required = ['PIL', 'zxingcpp', 'pylibdmtx', 'cv2', 'numpy', 'treepoem', 'xml.etree.ElementTree']
    
    missing = [dep for dep in required if not deps[dep]]
    
    if missing:
        print(f"Missing required dependencies: {', '.join(missing)}")
        print("Please install them using: pip install " + " ".join(missing))
        return False
    
    return True