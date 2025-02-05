Project to Single File Converter
======================

This is a simple, lightweight Python script designed to merge files from a directory and subdirectories into a single output file, while skipping specified folders and files. This can be useful for creating a consolidated text version of a project for documentation or review purposes.

Key Features
--------

*   **Configuration**: Uses JSON files to load configuration settings.
*   **File Processing**: Walks through directories, reads allowed files, and writes their content to an output file.
*   **Skipping Logic**: Skips specified folders and files based on the configuration.

Key Technical Highlights
--------------------------

*   **Data Classes**: Utilizes Python's `dataclasses` module to define a `Config` class for managing configuration settings in a clean and efficient manner.
*   **Type Hints**: Employs type hints throughout the script to improve code readability and facilitate debugging.
*   **Generators**: Uses generator functions (`walk_directory`, `handle_file`, `read_file`) to efficiently process files and directories, which is particularly useful for handling large datasets.
*   **Modular Design**: Organizes the code into distinct classes and functions, promoting modularity and making the script easier to maintain and extend.
*   **Error Handling**: Implements robust error handling for file operations and JSON parsing, ensuring the script can gracefully handle unexpected issues.
*   **Logging**: Incorporates detailed logging to provide insights into the script's execution flow and assist with debugging.
*   **Configuration Management**: Loads configuration settings from multiple JSON files, allowing for flexible and dynamic configuration.
*   **File Processing Optimization**: Reads files line by line to optimize memory usage, especially when dealing with large files.
*   **Comment Syntax Handling**: Dynamically determines the comment syntax based on the project language, making the script adaptable to different programming languages.

Installation
------------

1.  Clone the repository:
    
        git clone https://github.com/ryanlevee/project-to-single-file-converter.git
        cd project-to-single-file-converter
        
    
2.  Ensure you have Python 3.7 or later installed, as the script relies on the dataclasses module introduced in Python 3.7.


Configuration
-------------

The script uses the following JSON configuration files:

*   `allowed_extensions.json`: Specifies the file extensions to include.
*   `skip_folders.json`: Lists the folders to skip.
*   `skip_files.json`: Lists the files to skip.
*   `project_config.json`: Contains the main configuration settings.

Example of `project_config.json`:
    
    {
        "root_path": "C:\\Users\\user\\Documents\\Coding",
        "project_dir": "project-to-single-file-converter",
        "output_dir": "output",
        "output_filename": "single-file-project",
        "output_extension": "txt",
        "project_language": "python"
    }
    

Usage
-----

1.  Ensure the configuration files are correctly set up.
2.  Run the script:
    
        python main.py
        

Script Overview
---------------

### Imports and Configuration

The script imports necessary modules and sets up logging:

    import json
    import logging
    import os
    from dataclasses import dataclass, field
    from typing import Dict, Generator, List
    
    logging.basicConfig(level=logging.INFO)
    

### Config Data Class

A `Config` data class is defined to hold configuration settings:

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
    

### FileMerger Class

The `FileMerger` class handles the merging of files:

*   **Initialization**: Sets up the configuration.
*   **start()**: Begins the file processing.
*   **walk\_directory()**: Walks through directories and yields lines from allowed files.
*   **handle\_file()**: Handles individual files or directories.
*   **go\_to\_next\_file()**: Determines whether to skip a file based on its extension and name.
*   **read\_file()**: Reads the content of a file.
*   **get\_comment\_syntax()**: Returns the comment syntax for the project language.

### Helper Functions

*   **load\_json()**: Loads a JSON file and returns its content.
*   **unpack\_dict\_to\_dataclass()**: Converts a dictionary to a `Config` data class instance.

### Main Function

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
    

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
