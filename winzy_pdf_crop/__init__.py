import winzy
import fitz  # PyMuPDF
import os
import random
from winzy_convert import create_pdf_file


def extract_region_from_pdf(pdf_path, pages, rects, output_folder):
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    if pages is None:
        pages = sorted(random.sample(range(total_pages), min(3, total_pages)))

    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(output_folder, exist_ok=True)
    png_files = []
    for page_num in pages:
        page = doc.load_page(page_num)
        for idx, rect in enumerate(rects):
            clip_rect = fitz.Rect(*rect)
            pix = page.get_pixmap(clip=clip_rect, dpi=360)
            output_path = os.path.join(
                output_folder, f"{basename}_page{page_num+1}_rect{idx+1}.png"
            )
            pix.save(output_path)
            print(f"Saved: {output_path}")
            png_files.append(output_path)
    doc.close()
    return png_files


def create_parser(subparser):
    parser = subparser.add_parser("pdfcrop", description="Get images from pdf")
    # Add subprser arguments here.
    parser.add_argument("pdfs", nargs="+", help="Paths to one or more PDF files")
    parser.add_argument(
        "-p",
        "--pages",
        type=int,
        nargs="+",
        default=None,
        help="Page numbers (1-indexed) to capture. If omitted, 3 random pages will be selected",
    )
    parser.add_argument(
        "-cr",
        "--crop-rect",
        type=float,
        nargs=4,
        action="append",
        metavar=("x0", "y0", "x1", "y1"),
        help="Crop rectangle as x0 y0 x1 y1. Can be specified multiple times. [[50, 70, 800, 500]]",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        default="/tmp",
        help="Folder to save output PNGs (default: /tmp)",
    )

    return parser


class WinzyPlugin:
    """Get images from pdf"""

    __name__ = "pdfcrop"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # add actual call here
        pages = [p - 1 for p in args.pages] if args.pages else None

        if args.crop_rect:
            crop_rects = args.crop_rect
        else:
            # Generate random y1 values to vary the crop region vertically
            crop_rects = []
            for _ in range(1):  # generate 3 different regions by default
                y0 = random.randint(70, 400)
                height = random.randint(200, 400)
                y1 = y0 + height
                crop_rects.append([50, y0, 800, y1])

        for pdf in args.pdfs:
            pngfiles = extract_region_from_pdf(
                pdf, pages, crop_rects, args.output_folder
            )
            outfile = os.path.join(
                args.output_folder, f"pdf-{os.path.basename(pdf)}"
            )
            create_pdf_file(pngfiles, outfile)
            print(f"created {outfile}")

    def hello(self, args):
        # this routine will be called when 'winzy pdfcrop' is called.
        print("Hello! This is an example ``winzy`` plugin.")


pdfcrop_plugin = WinzyPlugin()
