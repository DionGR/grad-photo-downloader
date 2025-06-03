# Graduation Photo Magician

A comprehensive image processing application for downloading, processing, and enhancing graduation photos from snaphoto.gr. The application consists of three main stages:

1. **Image Downloader** - Downloads images from snaphoto.gr
2. **Watermark Remover** - Removes watermarks from images (coming soon)
3. **Image Upscaler** - Upscales images for better quality (coming soon)

## Project Structure

```
grad-photo-magician/
├── src/
│   └── tools/
│       ├── image_downloader/      # Stage 1: Download images
│       ├── watermark_remover/     # Stage 2: Remove watermarks
│       └── image_upscaler/        # Stage 3: Upscale images
├── data/
│   ├── img_source/               # Original downloaded images
│   ├── img_nowatermark/          # Images with watermarks removed
│   └── thumbnails/               # Thumbnail images from downloads
├── img_res/                      # Final processed images
├── download_images.py            # Main entry point for downloads
├── example_input.txt             # Example input file format
└── requirements.txt              # Python dependencies
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd grad-photo-magician
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Stage 1: Image Downloader

### Features

- Downloads graduation photos from snaphoto.gr
- Supports concurrent downloads for faster processing
- Handles both single photo IDs and ranges
- Progress tracking with visual progress bars
- Automatic retry mechanism for failed downloads
- Skips already downloaded files

### Usage

#### Command Line Interface

```bash
python download_images.py input_file.txt [options]
```

**Options:**
- `-o, --output DIR`: Output directory (default: `data/thumbnails`)
- `-c, --concurrent N`: Maximum concurrent downloads (default: 10)
- `--version`: Show version information

#### Input File Format

Create a text file with the following format:

```
GRADUATION_ID
PHOTO_ID_1
PHOTO_ID_2,PHOTO_ID_N
PHOTO_ID_RANGE_START,PHOTO_ID_RANGE_END
...
```

**Example (`example_input.txt`):**
```
12345
1001
1002,1010
1015
1020,1025
1030
```

This will download:
- Graduation ID: `12345`
- Photo ID: `1001`
- Photo IDs: `1002` through `1010` (inclusive)
- Photo ID: `1015`
- Photo IDs: `1020` through `1025` (inclusive)
- Photo ID: `1030`

#### Example Usage

```bash
# Basic usage
python download_images.py example_input.txt

# Custom output directory
python download_images.py example_input.txt -o data/my_photos

# Increase concurrent downloads for faster processing
python download_images.py example_input.txt -c 20

# Help
python download_images.py --help
```

### URL Format

The downloader constructs URLs in the following format:
```
https://img.snaphoto.gr/orkomosies/{GRADUATION_ID}/large/{PHOTO_ID}.jpg
```

### Programming Interface

You can also use the downloader programmatically:

```python
from src.tools.image_downloader import ImageDownloader

# Create downloader instance
downloader = ImageDownloader(output_dir="data/my_photos")

# Download from input file
downloader.download_from_file("input.txt", max_concurrent=10)

# Or use directly with graduation ID and photo IDs
import asyncio
graduation_id = "12345"
photo_ids = [1001, 1002, 1003]
successful, failed = asyncio.run(
    downloader.download_images(graduation_id, photo_ids)
)
```

## Error Handling

The application includes comprehensive error handling:

- **Invalid input format**: Warnings for malformed lines, continues processing
- **Network errors**: Automatic retry with exponential backoff
- **File system errors**: Graceful handling of permission issues
- **Missing files**: Clear error messages for non-existent input files

## Performance

- **Concurrent downloads**: Configurable concurrent download limit (default: 10)
- **Memory efficient**: Streams large files without loading into memory
- **Resume capability**: Skips already downloaded files on restart
- **Progress tracking**: Real-time progress bars using tqdm

## Requirements

- Python 3.7+
- aiohttp for async HTTP requests
- aiofiles for async file operations
- tqdm for progress bars
- Pillow for image processing (future stages)

## Contributing

This project is structured for easy extension. Each processing stage is modular and independent.

## License

See LICENSE file for details.

## Upcoming Features

- **Stage 2**: Watermark removal using AI/ML techniques
- **Stage 3**: Image upscaling using super-resolution algorithms
- **Batch processing**: Process entire directories
- **GUI interface**: User-friendly graphical interface
- **Configuration files**: YAML/JSON configuration support