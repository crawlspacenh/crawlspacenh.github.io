#!/usr/bin/env python3
"""
Script to update content/posters.md based on images in static/images/posters/

This script scans the static/images/posters/ directory for JPG files,
assumes they are named in YYYY-MM-DD.jpg format, and generates the
posters.md file with all posters listed in reverse chronological order.

Usage:
    python3 update-posters.py
"""

import os
from pathlib import Path
from datetime import datetime, timezone

# Configuration
SCRIPT_DIR = Path(__file__).parent
POSTERS_DIR = SCRIPT_DIR / "static" / "images" / "posters"
OUTPUT_FILE = SCRIPT_DIR / "content" / "posters.md"

# Template for the posters.md file
HEADER_TEMPLATE = """+++
title = 'Posters'
date = 2024-08-13T23:03:12-04:00
lastmod = {lastmod}
draft = false
+++
<!-- markdownlint-disable MD025 MD033 MD045 -->

<style>
  .poster-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }

  .poster-item {
    aspect-ratio: 1/1.5; /* Common poster ratio */
    overflow: hidden;
    position: relative;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .poster-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  }

  .poster-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .poster-grid {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 15px;
    }
  }

  @media (max-width: 480px) {
    .poster-grid {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 10px;
    }
  }
</style>

<div class="poster-grid">
"""

POSTER_TEMPLATE = """  <div class="poster-item">
    <a href="/images/posters/{filename}" target="_blank">
      <img src="/images/posters/{filename}" alt="Poster for {date} show" />
    </a>
  </div>
"""

FOOTER = """</div>
"""


def get_poster_files():
    """
    Get all JPG files from the posters directory and sort them
    in reverse chronological order (newest first).

    Returns:
        list: Sorted list of poster filenames
    """
    if not POSTERS_DIR.exists():
        print(f"Error: Posters directory not found: {POSTERS_DIR}")
        return []

    # Get all .jpg files
    poster_files = [f.name for f in POSTERS_DIR.glob("*.jpg")]

    # Sort in reverse chronological order (newest first)
    # Assumes filenames are in YYYY-MM-DD.jpg format
    poster_files.sort(reverse=True)

    return poster_files


def validate_filename(filename):
    """
    Validate that the filename follows the expected YYYY-MM-DD.jpg format.

    Args:
        filename (str): The filename to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Remove .jpg extension and try to parse as date
        date_str = filename.replace(".jpg", "")
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def generate_posters_md(poster_files):
    """
    Generate the content for posters.md file.

    Args:
        poster_files (list): List of poster filenames

    Returns:
        str: Complete content for posters.md
    """
    # Generate current timestamp in Hugo's expected format (ISO 8601 with timezone)
    now = datetime.now(timezone.utc).astimezone()
    current_date = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Insert colon in timezone offset (e.g., -0400 -> -04:00)
    current_date = current_date[:-2] + ":" + current_date[-2:]

    content = HEADER_TEMPLATE.format(lastmod=current_date)

    for filename in poster_files:
        if not validate_filename(filename):
            print(f"Warning: Skipping file with invalid name format: {filename}")
            continue

        date = filename.replace(".jpg", "")
        content += POSTER_TEMPLATE.format(filename=filename, date=date)

    content += FOOTER

    return content


def main():
    """Main function to update the posters.md file."""
    print(f"Scanning for posters in: {POSTERS_DIR}")

    # Get poster files
    poster_files = get_poster_files()

    if not poster_files:
        print("No poster files found!")
        return

    print(f"Found {len(poster_files)} poster(s)")

    # Generate content
    content = generate_posters_md(poster_files)

    # Write to file
    print(f"Writing to: {OUTPUT_FILE}")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(content)

    print(f"Successfully updated {OUTPUT_FILE}")
    print(f"Total posters: {len(poster_files)}")


if __name__ == "__main__":
    main()
