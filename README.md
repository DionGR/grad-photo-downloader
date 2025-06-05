# Graduation Photo Downloader

A Python tool for downloading graduation photos from snaphoto.gr in bulk. This tool fetches both full-size and thumbnail images and organizes them into separate directories.

The purpose of this tool is to be able to collect all your relevant photos, filter them so as to make an informed decision about which ones to purchase.

## Features

- **Bulk Download**: Download multiple photos at once using photo ID ranges or individual IDs
- **Dual Quality**: Automatically downloads both large and thumbnail versions
- **Organized Storage**: Saves images to `data/large/` and `data/thumb/` directories
- **Concurrent Downloads**: Fast parallel downloading with configurable concurrency
- **Flexible Input**: Supports individual photo IDs and ranges
- **Resume Support**: Skips already downloaded files

## Installation

1. Clone this repository:
```bash
git clone https://github.com/DionGR/grad-photo-downloader
cd grad-photo-magician
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Create an `input.txt` file with your graduation ID and photo IDs, then run:

```bash
python -m download_images.py
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Path to input file | `input.txt` |
| `--sizes` | Image sizes to download (`large`, `thumb`, or both) | `large thumb` |
| `--max-concurrent` | Maximum concurrent downloads | `10` |

## Input File Format

Create an `input.txt` file with the following format:

```
12345
00001
00005,0010
00015
00020,0025
00030
```

**Format Rules:**
- **First line**: Graduation ID (required)
- **Subsequent lines**: Photo IDs or ranges
  - Single photo ID: `00001`
  - Range: `00005,00010` (downloads 00005, 00006, 00007, 00008, 00009, 00010)
  - Padding is preserved (e.g., `00001` stays as `00001`, not `1`)

### Example Input File

```txt
2024GRAD123
00001
00002
00005,00015
00020
00025,00030
00035
00040,00045
```

This example will download:
- Graduation ID: `2024GRAD123`
- Individual photos: `0001`, `0002`, `0020`, `0035`
- Photo ranges: `0005-0015` (11 photos), `0025-0030` (6 photos), `0040-0045` (6 photos)
- **Total**: 26 photos in both large and thumbnail formats (52 files)



