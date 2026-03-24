"""
rgb_to_cmyk.py

Utilities to convert RGB SVG files to CMYK PDF using CairoSVG + Ghostscript.

Features:
- Single file conversion
- Batch folder conversion
- Auto-detect Ghostscript path (with Homebrew support on macOS)
- Robust error handling and logging

Created by: Mai Hong, 2026-03-24
"""

import subprocess
import shutil
import tempfile
import os
from pathlib import Path
import cairosvg


class RGBToCMYKConverter:
    """
    A utility class to convert RGB SVG files to CMYK PDFs using CairoSVG and Ghostscript.
    """

    def __init__(self, gs_path: str | None = None):
        """
        Initialize the converter.

        :param gs_path: Optional path to Ghostscript executable.
                        If not provided, it will be auto-detected.
        """
        # Ensure Homebrew path (useful on macOS)
        os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

        self.gs_path = gs_path or shutil.which("gs")
        if self.gs_path is None:
            raise RuntimeError(
                "Ghostscript ('gs') not found. Install with: brew install ghostscript"
            )

    def svg_to_cmyk_pdf(self, input_svg: str | Path, output_pdf: str | Path):
        """
        Convert a single SVG file to a CMYK PDF.

        :param input_svg: Path to the input SVG file.
        :param output_pdf: Path to the output PDF file.
        """
        input_svg = Path(input_svg)
        output_pdf = Path(output_pdf)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            temp_pdf = tmp.name

        try:
            # Step 1: SVG → RGB PDF
            cairosvg.svg2pdf(url=str(input_svg), write_to=temp_pdf)

            # Step 2: RGB → CMYK PDF using Ghostscript
            cmd = [
                self.gs_path,
                "-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=pdfwrite",
                "-sColorConversionStrategy=CMYK",
                "-dProcessColorModel=/DeviceCMYK",
                f"-sOutputFile={output_pdf}",
                temp_pdf,
            ]

            subprocess.run(cmd, check=True)

        finally:
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

    def batch_convert(self, input_folder: str | Path, output_folder: str | Path):
        """
        Convert all SVG files in a folder to CMYK PDFs.

        :param input_folder: Folder containing SVG files.
        :param output_folder: Destination folder for PDFs.
        """
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)

        if not input_folder.exists():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")

        output_folder.mkdir(parents=True, exist_ok=True)

        svg_files = list(input_folder.glob("*.svg"))
        if not svg_files:
            print("No SVG files found.")
            return

        print(f"Found {len(svg_files)} SVG files.\n")

        success = 0
        failed = 0

        for svg_file in svg_files:
            output_pdf = output_folder / f"{svg_file.stem}.pdf"

            try:
                self.svg_to_cmyk_pdf(svg_file, output_pdf)
                print(f"✅ {svg_file.name}")
                success += 1
            except Exception as e:
                print(f"❌ Failed: {svg_file.name}")
                print(f"   {e}\n")
                failed += 1

        print("\n--- Done ---")
        print(f"Successful: {success}")
        print(f"Failed: {failed}")