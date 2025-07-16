import os
import pytest
import fitz
from winzy_pdf_crop import extract_region_from_pdf, WinzyPlugin
from argparse import ArgumentParser


def create_dummy_pdf(path, num_pages=5):
    doc = fitz.open()
    for _ in range(num_pages):
        page = doc.new_page()
        page.insert_text((50, 72), "This is a test page.")
    doc.save(path)
    doc.close()


@pytest.fixture
def dummy_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    create_dummy_pdf(pdf_path)
    return str(pdf_path)


def test_extract_region_from_pdf(dummy_pdf, tmp_path):
    output_folder = tmp_path / "output"
    pages = [0, 1]
    rects = [[50, 50, 200, 200]]

    png_files = extract_region_from_pdf(dummy_pdf, pages, rects, str(output_folder))

    assert len(png_files) == 2
    for png_file in png_files:
        assert os.path.exists(png_file)


def test_winzy_plugin_run(dummy_pdf, tmp_path, capsys):
    output_folder = tmp_path / "output"
    os.makedirs(output_folder, exist_ok=True)

    class Args:
        def __init__(self):
            self.pdfs = [dummy_pdf]
            self.pages = [1, 2]
            self.crop_rect = [[50, 50, 200, 200]]
            self.output_folder = str(output_folder)

    args = Args()
    plugin = WinzyPlugin()

    # Mock the subparser and parser setup
    subparser = ArgumentParser().add_subparsers()
    plugin.register_commands(subparser)

    plugin.run(args)

    captured = capsys.readouterr()

    assert f"created {output_folder}/pdf-test.pdf" in captured.out

    # Check if the output PDF is created
    output_pdf_path = output_folder / "pdf-test.pdf"
    assert output_pdf_path.exists()

    # Verify the contents of the created PDF
    doc = fitz.open(str(output_pdf_path))
    assert doc.page_count == 2  # Two pages from the two extracted PNGs
    doc.close()
