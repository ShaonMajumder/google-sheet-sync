# Google Sheets Sync Python Package

## Overview

The `google_sheets_crud` Python package provides a simple and efficient way to perform CRUD (Create, Read, Update, Delete) operations on Google Sheets. This package is designed for users who want to interact with Google Sheets programmatically, with support for reading, appending, prepending, updating, and deleting rows. It also supports creating new sheets and spreadsheets, as well as inserting data into them.

---

## Features

- **Read Data**: Retrieve data from a specified sheet.
- **Append Row**: Add a new row to the end of a sheet.
- **Prepend Row**: Insert a new row at the top of the sheet.
- **Update Row**: Modify data in a specific row.
- **Delete Row**: Remove a row from the sheet.
- **Delete and Shift Up**: Remove a row and shift subsequent rows up.
- **Create Spreadsheet**: Create a new spreadsheet and optionally populate it with data.
- **Create Sheet**: Create a new sheet in an existing spreadsheet.
- **Create Sheet and Insert Data**: Create a new sheet and insert data into it.

---

## Installation

1. **Install the Package**:

   First, clone the repository or download the package files. Navigate to the package directory where `setup.py` is located and install the package using:

   ```sh
   python setup.py install
   ```

​	Alternatively, if you want to install it in editable mode for development:

    ```sh
    python setup.py develop
    ```

2. **Dependencies**:

    Ensure you have the following Python packages installed:

    google-auth
    google-auth-oauthlib
    google-api-python-client
    python-dotenv

    Install these dependencies with:
    ```sh
    pip install google-auth google-auth-oauthlib google-api-python-client python-dotenv
    ```

## Usage

1. **Setup**:

    Create a `.env` file in your project directory with the following content:
    ```sh
    CREDENTIALS_FILE=your_credential_file.json
    SPREADSHEET_ID=your_spreadsheet_id
    ```
    Replace your_credential_file.json and your_spreadsheet_id with actual Data.
2. **Script Example**:

    Use the GoogleSheetsCRUD class to perform operations on your Google Sheet. Below is an example script demonstrating how to use the package:

    ```sh
    from google_sheets_sync import GoogleSheetsCRUD

    def main():
        # Initialize the CRUD class
        sheets_crud = GoogleSheetsCRUD()

        # Read data from the sheet
        print("Reading data...")
        data = sheets_crud.readSheet("testsheet")
        print("Current data in the sheet:")
        for row in data:
            print(row)

        # Append a new row
        print("\nAppending a new row...")
        append_response = sheets_crud.appendRow(["New", "Data"], "testsheet")
        print(f"Append response: {append_response}")

        # Prepend a new row
        print("\nPrepending a new row...")
        prepend_response = sheets_crud.prependRow(["Prepended", "Data"], "testsheet")
        print(f"Prepend response: {prepend_response}")

        # Update a specific row
        print("\nUpdating row 2...")
        update_response = sheets_crud.updateRow(2, ["Updated", "Data"], "testsheet")
        print(f"Update response: {update_response}")

        # Delete a specific row
        print("\nDeleting row 3...")
        sheets_crud.deleteRow(3, "testsheet")

        # Delete and shift rows up
        print("\nDeleting row 2 and shifting rows up...")
        sheets_crud.deleteRowAndShiftUp(2, "testsheet")

    if __name__ == "__main__":
        main()
    ```

3. **Running the Script**:

    Execute the script using:

    ```sh
    python use_google_sheets.py
    ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on the GitHub repository.

## Contact
For any questions or feedback, please contact smazoomder@gmail.com .