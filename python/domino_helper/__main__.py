"""Allow running as: python -m domino_helper [selector] [image_path]"""

import sys
from .main import main

if __name__ == '__main__':
    sel = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    img_path = sys.argv[2] if len(sys.argv) > 2 else None
    main(selector=sel, image_path=img_path)
