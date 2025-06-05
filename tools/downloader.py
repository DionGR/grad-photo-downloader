"""
Image Downloader for photos
"""

import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import List, Tuple, Literal
from tqdm.asyncio import tqdm


class ImageDownloader:
    BASE_URL = "https://img.snaphoto.gr/orkomosies"
    
    def __init__(self, output_dir: str = "data"):
        """
        Initialize the ImageDownloader
        
        Args:
            output_dir: Base directory to save downloaded images
        """
        self.output_dir = Path(output_dir)
        # Create subdirectories for large and thumb images
        self.large_dir = self.output_dir / "large"
        self.thumb_dir = self.output_dir / "thumb"
        
        self.large_dir.mkdir(parents=True, exist_ok=True)
        self.thumb_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_input_file(self, file_path: str) -> Tuple[str, List[str]]:
        """
        Parse the input file to extract graduation ID and photo IDs
        
        Args:
            file_path: Path to the input file
            
        Returns:
            Tuple of (graduation_id, list_of_photo_ids)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if not lines:
            raise ValueError("Input file is empty")
            
        graduation_id = lines[0]
        photo_ids = []
        
        for line in lines[1:]:
            if ',' in line:
                # Handle range format "FROM,TO"
                try:
                    start_str, end_str = line.split(',')
                    start = int(start_str)
                    end = int(end_str)
                    
                    # Determine padding length from the input format
                    padding_length = len(start_str)
                    
                    for photo_id in range(start, end + 1):
                        # Maintain the same padding as the input
                        padded_id = str(photo_id).zfill(padding_length)
                        photo_ids.append(padded_id)
                except ValueError:
                    print(f"Warning: Invalid range format '{line}', skipping...")
            else:
                # Handle single photo ID - keep as string to preserve padding
                photo_ids.append(line)
        
        return graduation_id, photo_ids
    
    def generate_url(self, graduation_id: str, photo_id: str, size: Literal["large", "thumb"]) -> str:
        """
        Generate the download URL for a photo
        
        Args:
            graduation_id: The graduation ID
            photo_id: The photo ID (as string to preserve padding)
            size: The size type ("large" or "thumb")
            
        Returns:
            Complete URL for the photo
        """
        return f"{self.BASE_URL}/{graduation_id}/{size}/{photo_id}.jpg"
    
    def get_output_path(self, graduation_id: str, photo_id: str, size: Literal["large", "thumb"]) -> Path:
        """
        Generate the output file path for a photo
        
        Args:
            graduation_id: The graduation ID
            photo_id: The photo ID (as string to preserve padding)
            size: The size type ("large" or "thumb")
            
        Returns:
            Path object for the output file
        """
        filename = f"{graduation_id}_{photo_id}.jpg"
        if size == "large":
            return self.large_dir / filename
        else:  # thumb
            return self.thumb_dir / filename
    
    async def download_single_image(self, session: aiohttp.ClientSession, 
                                  graduation_id: str, photo_id: str, 
                                  size: Literal["large", "thumb"],
                                  semaphore: asyncio.Semaphore) -> bool:
        """
        Download a single image
        
        Args:
            session: aiohttp client session
            graduation_id: The graduation ID
            photo_id: The photo ID (as string to preserve padding)
            size: The size type ("large" or "thumb")
            semaphore: Semaphore to limit concurrent downloads
            
        Returns:
            True if download was successful, False otherwise
        """
        async with semaphore:
            url = self.generate_url(graduation_id, photo_id, size)
            output_path = self.get_output_path(graduation_id, photo_id, size)
            
            # Skip if file already exists
            if output_path.exists():
                return True
                
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(output_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                await f.write(chunk)
                        return True
                    else:
                        print(f"Failed to download {url}: HTTP {response.status}")
                        return False
                        
            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")
                return False
    
    async def download_images(self, graduation_id: str, photo_ids: List[str], 
                            sizes: List[Literal["large", "thumb"]] = ["large", "thumb"],
                            max_concurrent: int = 10) -> Tuple[int, int]:
        """
        Download multiple images concurrently
        
        Args:
            graduation_id: The graduation ID
            photo_ids: List of photo IDs to download (as strings to preserve padding)
            sizes: List of sizes to download ("large", "thumb", or both)
            max_concurrent: Maximum number of concurrent downloads
            
        Returns:
            Tuple of (successful_downloads, failed_downloads)
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for photo_id in photo_ids:
                for size in sizes:
                    tasks.append(
                        self.download_single_image(session, graduation_id, photo_id, size, semaphore)
                    )
            
            results = await tqdm.gather(*tasks, desc="Downloading images")
            
        successful = sum(results)
        failed = len(results) - successful
        
        return successful, failed
    
    def download_from_file(self, input_file: str, 
                          sizes: List[Literal["large", "thumb"]] = ["large", "thumb"],
                          max_concurrent: int = 10) -> None:
        """
        Download images based on input file
        
        Args:
            input_file: Path to the input file
            sizes: List of sizes to download ("large", "thumb", or both)
            max_concurrent: Maximum number of concurrent downloads
        """
        try:
            graduation_id, photo_ids = self.parse_input_file(input_file)
            
            print(f"Graduation ID: {graduation_id}")
            print(f"Total photos to download: {len(photo_ids)}")
            print(f"Sizes to download: {', '.join(sizes)}")
            print(f"Output directory: {self.output_dir}")
            print(f"Large images: {self.large_dir}")
            print(f"Thumbnail images: {self.thumb_dir}")
            
            successful, failed = asyncio.run(
                self.download_images(graduation_id, photo_ids, sizes, max_concurrent)
            )
            
            print(f"\nDownload completed!")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            raise 