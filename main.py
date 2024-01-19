from dataclasses import dataclass, field
from functions import unsplash_image_url_title_scraper, save_images_on_folder, create_excel_file
import os

# Here is the default directory path for each user
default_directory = os.path.expanduser(r"~\DataspellProjects\Upslash Pictures")


@dataclass(kw_only=True)
class Scrape:
    name: str
    resolution: str = "1200w"
    excel_write: bool = field(default=False)
    excel_file_name: str = field(default="images.xlsx")
    save_directory: bool = field(default=False)
    full_file_path: str = field(default=default_directory)

    def __post_init__(self):
        self.check_resolution(res=self.resolution)
        self.name = self.name.lower()

        images = unsplash_image_url_title_scraper(name=self.name,
                                                  resolution=self.resolution)

        images_list = [(key, value) for key, value in images.items()]

        if self.excel_write and self.save_directory:
            save_images_on_folder(images_list, self.full_file_path)
            create_excel_file(images_list, self.excel_file_name)

        elif not self.excel_write and self.save_directory:
            save_images_on_folder(images_list, self.full_file_path)

        elif not self.save_directory and self.excel_write:
            create_excel_file(images_list, self.excel_file_name)

        else:
            print(images_list)

    def check_resolution(self, res: str) -> bool:
        if not "100w" <= res <= "2000w":
            raise ValueError("The resolution should be between 100 and 2000 w")


if __name__ == "__main__":
    imgs = Scrape(name="Azerbaijan Christmas",
                  resolution="1400w",
                  save_directory=True,
                  excel_write=False
                  )
