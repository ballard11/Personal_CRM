# Personal CRM

A desktop Personal Customer Relationship Management (CRM) application built with Python and PyQt5. This application allows users to manage their contacts, including features such as contact details, categorization, birthday reminders, and data import/export capabilities.

![Personal CRM Screenshot](assets/crm_screenshot.png)

## Features

- Add, edit, and delete contacts
- Categorize contacts
- Search functionality
- Birthday reminders
- Data validation
- Import/Export contacts (JSON format)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/personal-crm.git
   cd personal-crm
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Notes on the Implemented Features
MVC Architecture: The code is restructured into Model (models.py), View (main.py), and Controller (controller.py).
UI Improvements:
Date Picker: QDateEdit is used for the birthday input.
Input Validation: Regular expressions are used to validate email and phone inputs.
Search Functionality: A search bar filters contacts in real-time.
Customizable Categories: Users can add new categories via a dialog.
Improved Layout: QFormLayout organizes form fields neatly.
Feature Improvements:
Delete Contact: A "Delete Contact" button allows users to remove contacts.
Profile Pictures: Users can upload images for contacts.
Export Data: Enhanced to allow users to choose the save location.
Code Improvements:
Modular Code: Database operations are moved to DatabaseManager, and models are defined in models.py.
Error Handling: Try-except blocks and input validations prevent crashes.
Logging: Important actions are logged for debugging purposes.
Virtual Environment:
It's assumed that you're using a virtual environment (venv) for this project. Ensure you activate your virtual environment before running the app.
Future Work
User Authentication: Planning to add user authentication to secure data.
Interaction History: Could be implemented by adding an interactions table and corresponding UI elements.
Reminders: Implement reminders for birthdays and other important dates.
Import/Export in Multiple Formats: Extend the export functionality to support CSV and vCard formats.


