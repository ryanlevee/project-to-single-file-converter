### Project to Single File Converter

This is a simple, lightweight Python script designed to merge files from a directory and subdirectories into a single output file, while skipping specified folders and files. This can be useful for creating a consolidated text version of a project for documentation or review purposes.

* * *

### Table of Contents

1.  Key Features
2.  Key Technical Highlights
3.  Dynamic Type Checking with `unpack_dict_to_dataclass`
4.  Installation
5.  Configuration
6.  Usage
7.  Script Overview
    *   Imports and Configuration
    *   Config Data Class
    *   FileMerger Class
    *   Helper Functions
    *   Main Function
8.  License

* * *

### Key Features

*   **Programming Languages**: Designed to work with any programming language.
*   **Configuration**: Uses JSON files to load configuration settings.
*   **File Processing**: Walks through directories, reads allowed files, and writes their content to an output file.
*   **Skipping Logic**: Skips specified folders and files based on the configuration.
*   **Comment Handling**: Processes file comments based on the project's programming language syntax.

* * *

### Key Technical Highlights

*   **Data Classes**: Utilizes Python's `dataclasses` module to define a `Config` class for managing configuration settings in a clean and efficient manner.
*   **Type Hints**: Employs rigorous type hinting throughout the script to improve code readability and facilitate debugging.
*   **Generators**: Uses generator functions (`walk_directory`, `handle_file`, `read_file`, `process_file`) to efficiently process files and directories, which is particularly useful for handling large datasets.
*   **Modular Design**: Organizes the code into distinct classes and functions, promoting modularity and making the script easier to maintain and extend.
*   **Error Handling**: Implements robust error handling for file operations and JSON parsing, ensuring the script can gracefully handle unexpected issues.
*   **Logging**: Incorporates detailed logging to provide insights into the script's execution flow and assist with debugging.
*   **Configuration Management**: Loads configuration settings from multiple JSON files, allowing for flexible and dynamic configuration.
*   **File Processing Optimization**: Reads files line by line to optimize memory usage, especially when dealing with large files.
*   **Comment Syntax Handling**: Dynamically determines the comment syntax based on the project language, making the script adaptable to different programming languages.
*   **Output File Writing**: Writes the collected lines to an output file, ensuring the final output is well-organized and formatted.

* * *

### Dynamic Type Checking with `unpack_dict_to_dataclass`

The `unpack_dict_to_dataclass` function is a key component of the script, designed to dynamically convert a dictionary into an instance of the `Config` data class. This function ensures that each key in the dictionary matches the corresponding field name in the `Config` data class and that the value is of the expected type. The expected type is determined using the `default_factory` of each field, providing a robust and flexible way to handle configuration data.

**Key Features:**

*   **Dynamic Type Checking**: Validates that each key in the dictionary matches the corresponding field name in the `Config` data class and that the value is of the expected type.
*   **Error Handling**: Raises a `KeyError` if a required key is missing and a `TypeError` if a value is not of the expected type, ensuring that the configuration data is accurate and reliable.
*   **Flexibility**: Uses the `default_factory` of each field to determine the expected type, allowing for a wide range of configuration data to be handled dynamically.

**Function Signature:**

    def unpack_dict_to_dataclass(data: Dict[str, ConfigDataType]) -> Config:
        """
        Converts a dictionary to a Config data class instance.
    
        Args:
            data (Dict[str, ConfigDataType]): The dictionary containing configuration data.
    
        Raises:
            KeyError: If a key in the dictionary does not match the corresponding field name in the Config data class.
            TypeError: If a value in the dictionary is not of the expected type.
    
        Returns:
            Config: An instance of the Config data class with fields populated from the dictionary.
        """
    

This function enhances the script's robustness and flexibility, making it easier to manage and validate configuration data dynamically.

* * *

### Installation

1.  Clone the repository:
    
        git clone https://github.com/ryanlevee/project-to-single-file-converter.git
        cd project-to-single-file-converter
        
    
2.  Ensure you have Python 3.7 or later installed, as the script relies on the dataclasses module introduced in Python 3.7.
    

* * *

### Configuration

The script uses the following JSON files for configuration:

*   `allowed_extensions.json`: Specifies the file extensions to include.
*   `skip_folders.json`: Lists the folders to skip.
*   `skip_files.json`: Lists the files to skip.
*   `project_config.json`: Contains the main configuration settings.

Example of `project_config.json`:

    {
        "root_path": "C:\\Users\\[your-username]\\Documents",
        "project_dir": "project-to-single-file-converter",
        "output_dir": "output",
        "output_filename": "single-file-project",
        "output_extension": "txt",
        "project_language": "python"
    }
    

* * *

### Usage

1.  Ensure the configuration files are correctly set up.
    
2.  Run the script:
    
        python main.py
        
    

* * *

### Script Overview

#### Imports and Configuration

The script imports necessary modules and sets up logging:

    import json
    import logging
    import os
    from dataclasses import dataclass, field, fields
    from typing import Dict, Generator, List
    
    logging.basicConfig(level=logging.INFO)
    

#### Config Data Class

A `Config` data class is defined to hold configuration settings. The `LanguageSyntax`, `WalkingFilters`, and `ProjectConfig` data classes are used to manage comment syntax and file filtering settings, respectively. The `Config` class inherits from these to consolidate all configuration settings.

    BlockCommentType = Dict[str, str]
    InlineCommentType = str
    FiltersType = List[str]
    ConfigDataType = BlockCommentType | InlineCommentType | FiltersType | str
    ProjectConfigType = Dict[str, str] | str
    LanguageSyntaxType = Dict[str, Dict[str, str] | str]
    
    @dataclass
    class LanguageSyntax:
        block_comment: BlockCommentType = field(default_factory=dict)
        inline_comment: InlineCommentType = field(default_factory=str)
    
    @dataclass
    class WalkingFilters:
        skip_folders: FiltersType = field(default_factory=list)
        skip_files: FiltersType = field(default_factory=list)
        allowed_extensions: FiltersType = field(default_factory=list)
    
    @dataclass
    class ProjectConfig:
        root_path: str = field(default_factory=str)
        project_dir: str = field(default_factory=str)
        output_dir: str = field(default_factory=str)
        output_filename: str = field(default_factory=str)
        output_extension: str = field(default_factory=str)
        project_language: str = field(default_factory=str)
    

#### FileMerger Class

The `FileMerger` class handles the merging of files:

*   **Initialization**: Sets up the configuration.
*   **start()**: Begins the file processing.
*   **walk\_directory()**: Walks through directories and yields lines from allowed files.
*   **handle\_file()**: Handles individual files or directories.
*   **should\_skip\_file()**: Determines whether to skip a file based on its extension and name.
*   **process\_file()**: Processes a file, yielding lines while handling comments.
*   **read\_file()**: Reads the content of a file.
*   **write\_output\_file()**: Writes the collected lines to the output file.

#### Helper Functions

*   **load\_json()**: Loads a JSON file and returns its content.
*   **get\_language\_syntax()**: Returns the comment syntax for the specified project language.
*   **unpack\_dict\_to\_dataclass()**: Converts a dictionary to a `Config` data class instance.

#### Main Function

The `run()` function loads configuration data from JSON files and starts the file processing:

    def run() -> None:
        config_files: Dict[str, str] = {
            "skip_folders": "skip_folders.json",
            "skip_files": "skip_files.json",
            "allowed_extensions": "allowed_extensions.json",
            "project_config": "project_config.json",
        }
        config_data: Dict[str, ConfigDataType] = {
            key: load_json(path) for key, path in config_files.items()
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
    

* * *

### License

This project is licensed under the MIT License - see the LICENSE file for details.
