Patient Record Management System

1. Project Overview

The Patient Record Management System is a Python application developed using Object-Oriented Programming (OOP). It provides a simple graphical user interface for registering patients, viewing patient information, updating records, and managing visit notes.

The application was developed as an educational project to demonstrate how OOP concepts can be applied to a real-world problem in the healthcare sector.

2. Technologies Used

- Python
- Tkinter for the graphical user interface
- Object-Oriented Programming
- Python dictionary for storing patient objects while the application is running

3. Main Features

- Register new patients.
- Validate patient codes and basic registration details.
- Prevent duplicate patient codes.
- View registered patient information.
- Update patient details.
- Add visit notes.
- Refresh the patient list.
- Delete a selected patient record.

4. Object-Oriented Programming

The project uses separate classes to organise its functionality.

- Patient: Represents a patient and manages the patient's information and visit notes.
- PatientRegistry: Stores and manages patient objects using a dictionary.
- PatientApp: Provides the graphical interface through which users interact with the system.

The project demonstrates attributes, objects, instance methods, a class method, and other object-oriented programming concepts.

5. How to Run the Application

1. Install Python on your computer.
2. Download or clone this repository.
3. Open the project in PyCharm or another Python editor.
4. Run the main Python source file.
5. Use fictional patient information to test the application's features.

The application uses Tkinter, which is included with many standard Python installations.

6. Example Usage

The following is an illustrative example of the kind of information a user can enter. It is not a record of an actual patient or a claim that a particular test was performed.

Sample input

- Patient code: P-0001
- Name: Test Patient
- Age: 25
- Gender: Male
- Condition: General check-up

Expected outcome: If the information passes the application's validation and the patient code is not already registered, the patient can be added to the application.

7. Digital Public Goods (DPG) Principles

This project considers the following principles:

Open Source

The source code is published in a public GitHub repository so that others can inspect and learn from it.

Inclusiveness and Accessibility

The application uses a graphical interface with labels and validation messages to help users interact with its functions. Formal accessibility testing has not been conducted.

Privacy and Data Protection

The application is an educational prototype. Patient information is held in application memory while it is running. It is not designed or approved for storing real patient information. Testing should use fictional data only.

Modularity and Reusability

The application separates patient information, record management, and the graphical interface into different classes, making the code easier to understand and maintain.

This project demonstrates consideration of DPG principles; it has not been formally certified as a Digital Public Good.

8. Limitations

- The application is an educational prototype, not a production healthcare system.
- Patient information is not permanently stored by the described in-memory registry.
- The application has not been formally security or accessibility tested.
- It should not be used to manage real patients' confidential information.

9. Author and Repository

Project: Patient Record Management System
Language: Python
Purpose: Object-Oriented Programming assignment

For source code and updates, see the files in this GitHub repository.
