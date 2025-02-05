import json
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, Generator, List

logging.basicConfig(level=logging.INFO)


@dataclass
class Config:
    skip_folders: List[str] = field(default_factory=list)
    skip_files: List[str] = field(default_factory=list)
    allowed_extensions: List[str] = field(default_factory=list)
    root_path: str = field(default_factory=str)
    project_dir: str = field(default_factory=str)
    output_dir: str = field(default_factory=str)
    output_filename: str = field(default_factory=str)
    output_extension: str = field(default_factory=str)
    project_language: str = field(default_factory=str)


class FileMerger:
    """
    A class to merge files from a directory and any subdirectories, skipping
    specified folders and files, and writing the content of allowed files to an
    output file.
    """

    def __init__(self, config: Config) -> None:
        """
        Initializes the FileMerger with the given configuration.

        Args:
            config (Config): An instance of the Config data class containing
            configuration settings.
        """
        self.root_path: str = config.root_path
        self.project_dir: str = config.project_dir
        self.output_dir: str = config.output_dir
        self.output_filename: str = config.output_filename
        self.output_extension: str = config.output_extension
        self.project_language: str = config.project_language
        self.skip_folders: List[str] = config.skip_folders
        self.skip_files: List[str] = config.skip_files
        self.allowed_extensions: List[str] = config.allowed_extensions

    def start(self) -> None:
        """
        Starts the file processing by walking through the directory and writing
        the content of allowed files to the output file.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = f"{self.output_filename}.{self.output_extension}"
        output_path = os.path.join(self.output_dir, output_file)

        lines = self.walk_directory(self.root_path, self.project_dir)
        try:
            with open(output_path, "w+") as f:
                for line in lines:
                    f.write(line)
        except IOError as e:
            logging.error(f"Error writing to file {output_path}: {e}")

    def walk_directory(
        self, path: str, dir: str
    ) -> Generator[str, None, None]:
        """
        Walks through the directory and yields lines from allowed files.

        Args:
            path (str): The current directory path.
            dir (str): The directory to walk through.

        Yields:
            str: Lines from allowed files.
        """
        next_path = os.path.join(path, dir)
        try:
            files = os.listdir(next_path)
        except OSError as e:
            logging.error(f"Error accessing directory {next_path}: {e}")
            return

        for file in files:
            yield from self.handle_file(next_path, file)

    def handle_file(self, path: str, file: str) -> Generator[str, None, None]:
        """
        Handles a single file or directory, yielding lines from allowed files.

        Args:
            path (str): The current directory path.
            file (str): The file or directory to handle.

        Yields:
            str: Lines from allowed files.
        """
        if file in self.skip_folders:
            return

        new_file = os.path.join(path, file)

        if os.path.isdir(new_file):
            yield from self.walk_directory(path, file)

        if self.go_to_next_file(file):
            return

        header = f"```\n/*\nfile: {new_file}\n*/\n"
        yield header
        lines = self.read_file(new_file)
        yield from [
            l
            for l in lines
            if not l.lstrip().startswith(self.get_comment_syntax())
        ]
        yield "\n```\n\n"

    def go_to_next_file(self, file: str) -> bool:
        """
        Determines whether to skip the file based on its extension and name.

        Args:
            file (str): The file name.

        Returns:
            bool: True if the file should be skipped, False otherwise.
        """
        return (
            not any(file.endswith(ext) for ext in self.allowed_extensions)
            or file in self.skip_files
        )

    def read_file(self, new_file: str) -> Generator[str, None, None]:
        """
        Reads the content of a file.

        Args:
            new_file (str): The file path.

        Returns:
            List[str]: A list of lines from the file.
        """
        try:
            with open(new_file, "r") as f:
                for line in f:
                    yield line

        except IOError as e:
            logging.error(f"Error reading file {new_file}: {e}")

    def get_comment_syntax(self) -> str:
        """
        Returns the comment syntax for the project language.

        Returns:
            str: The comment syntax.
        """
        match self.project_language.lower():
            case "python" | "py":
                return "#"
            case "javascript" | "js":
                return "//"
            case _:
                logging.warning(
                    f"Unknown project language: {self.project_language}"
                )
                return "#"


def load_json(file_path: str) -> Dict:
    """
    Loads a JSON file and returns its content.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict: The content of the JSON file.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        return {}


ConfigDataType = List[str] | Dict[str, str] | str


def unpack_dict_to_dataclass(data: Dict[str, ConfigDataType]) -> Config:
    """
    Converts a dictionary to a Config data class instance.

    Args:
        data (Dict[str, ConfigDataType]): The dictionary containing configuration data.

    Returns:
        Config: An instance of the Config data class.
    """
    sanitized_data: dict = {}
    sanitized_data.update(data)
    return Config(**sanitized_data)


def run() -> None:
    """
    Loads configuration data from JSON files and starts the file processing.
    """
    config_files: Dict[str, str] = {
        "skip_folders": "skip_folders.json",
        "skip_files": "skip_files.json",
        "allowed_extensions": "allowed_extensions.json",
        "project_config": "project_config.json",
    }

    config_data: Dict[str, ConfigDataType] = {
        key: load_json(os.path.join('config', path)) for key, path in config_files.items()
    }

    project_data: ConfigDataType = config_data.pop("project_config")

    if not isinstance(project_data, dict):
        raise TypeError("Expected 'project_config' to be a dictionary")

    config_data.update(project_data)
    typed_config: Config = unpack_dict_to_dataclass(config_data)
    file_merger = FileMerger(typed_config)
    file_merger.start()


if __name__ == "__main__":
    run()
