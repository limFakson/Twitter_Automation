
"""
Replacement for the removed imghdr module (removed in Python 3.13).
This polyfill provides the 'what' function used by legacy libraries.
"""

from os import PathLike

__all__ = ["what"]

def what(file, h=None):
    """
    Detect the type of image contained in a file or byte stream.
    """
    if h is None:
        if isinstance(file, (str, PathLike)):
            try:
                with open(file, 'rb') as f:
                    h = f.read(32)
            except OSError:
                return None
        else:
            # Assume file-like object
            try:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
            except (AttributeError, OSError):
                return None
            
    if not h:
        return None

    # Basic magic number detection
    if h.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'
    if h.startswith(b'BM'):
        return 'bmp'
    if h.startswith(b'\x00\x00\x01\x00'):
        return 'ico'
        
    return None
