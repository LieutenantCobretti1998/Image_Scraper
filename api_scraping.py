from dataclasses import dataclass, field
from functions import scrape_with_api, save_images_on_folder, create_excel_file
import os

default_directory = os.path.expanduser(r"~\DataspellProjects\Upslash Pictures")


@dataclass(kw_only=True)
class ApiData:
    name: str = "azerbaijan"
    count: int = 1
    excel_write: bool = field(default=False)
    excel_file_name: str = field(default="images.xlsx")
    save_directory: bool = field(default=False)
    full_file_path: str = field(default=default_directory)

    def __post_init__(self):
        self.name = self.name.lower()


class ApiAction(ApiData):
    def __init__(self, name, count,
                 excel_write=False,
                 excel_file_name="images.xlsx",
                 save_directory=False,
                 full_file_path=default_directory):

        super().__init__(name=name,
                         count=count,
                         excel_write=excel_write,
                         excel_file_name=excel_file_name,
                         save_directory=save_directory,
                         full_file_path=full_file_path)  # Pass the arguments as keyword arguments

        self.scrape_data_with_api()

    def validate_count(self) -> None:
        if not (self.count <= 30):
            raise ValueError("count must be between 1 and 30")

    def scrape_data_with_api(self) -> None:
        self.validate_count()
        scrape_with_api(name=self.name,
                        images_number=self.count)

        images_list = [(key, value) for key, value in scrape_with_api(name=self.name,
                                                                      images_number=self.count).items()]

        if self.excel_write and self.save_directory:
            save_images_on_folder(images_list, self.full_file_path)
            create_excel_file(images_list, self.excel_file_name)

        elif not self.excel_write and self.save_directory:
            save_images_on_folder(images_list, self.full_file_path)

        elif not self.save_directory and self.excel_write:
            create_excel_file(images_list, self.excel_file_name)

        else:
            print(images_list)


if __name__ == "__main__":
    action = ApiAction(name="BAKU",
                       count=25,
                       save_directory=True)
