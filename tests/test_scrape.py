import pytest
from main import Scrape


# Test cases for the Scrape class


def test_default_values():
    # Test with default values, no files should be created
    scrape = Scrape
    assert not scrape.excel_write
    assert not scrape.save_directory


def test_create_excel_file():
    # Test creating an Excel file with excel_write=True
    scrape = Scrape(name="russia", excel_write=True)
    assert scrape.excel_write
    assert not scrape.save_directory
    # Add assertions to check if the Excel file was created successfully


def test_save_images_on_folder():
    # Test saving images to a directory with save_directory=True
    scrape = Scrape(name="russia", save_directory=True)
    assert not scrape.excel_write
    assert scrape.save_directory
    # Add assertions to check if the images were saved to the directory successfully


def test_create_excel_file_and_save_images_on_folder():
    # Test creating Excel file and saving images to a directory
    scrape = Scrape(name="russia", excel_write=True, save_directory=True)
    assert scrape.excel_write
    assert scrape.save_directory
    # Add assertions to check if both Excel file and images were created/saved successfully


# Add more test cases as needed


if __name__ == "__main__":
    pytest.main()
