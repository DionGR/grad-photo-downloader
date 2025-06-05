"""
Command-line interface for the Image Downloader
"""

import argparse
import sys
from pathlib import Path
from .downloader import ImageDownloader


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Download graduation photos from snaphoto.gr",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example input file format:
  12345
  1001
  1002,1010
  1015
  1020,1025

The first line is the graduation ID.
Subsequent lines can be either:
- Single photo IDs (e.g., 1001)
- Ranges in the format FROM,TO (e.g., 1002,1010)

Images will be downloaded to:
- data/large/ for full-size images
- data/thumb/ for thumbnail images
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        default='input.txt',
        help='Input file containing graduation ID and photo IDs (default: input.txt)'
    )
    
    parser.add_argument(
        '--sizes',
        nargs='+',
        choices=['large', 'thumb'],
        default=['large', 'thumb'],
        help='Image sizes to download (default: both large and thumb)'
    )
    
    parser.add_argument(
        '--max-concurrent',
        type=int,
        default=10,
        help='Maximum number of concurrent downloads (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    # Create downloader and start download
    try:
        downloader = ImageDownloader()
        downloader.download_from_file(
            args.input_file, 
            sizes=args.sizes,
            max_concurrent=args.max_concurrent
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 