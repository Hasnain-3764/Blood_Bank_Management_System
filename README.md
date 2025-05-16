# Blood_Bank_Management_System
Blood Bank Management System

# 🩸 Blood Bank Management System

A web-based application designed to streamline blood donation and transfusion processes by connecting donors, recipients, and administrators.

## 📌 Overview

This project aims to facilitate efficient management of blood donations and requests. It provides functionalities for users to register as donors or recipients, and for administrators to manage blood inventories and user requests.

## 🔧 Features

- **User Registration & Authentication**: Secure sign-up and login for donors and recipients.
- **Blood Request Management**: Users can request specific blood types; admins can approve or reject requests.
- **Donation Tracking**: Donors can log their donations; the system maintains a history.
- **Inventory Management**: Admins can monitor and update blood stock levels.
- **Responsive Design**: Accessible on various devices with a user-friendly interface.

## 🛠️ Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask framework)
- **Database**: MySQL

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- MySQL Server

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hasnain-3764/Blood_Bank_Management_System.git
   cd Blood_Bank_Management_System
````

2. **Create a virtual environment (optional but recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL**:

   * Create a database in your MySQL server.
   * Update your MySQL credentials in the config or `routes.py` file.

5. **Run the application**:

   ```bash
   python run.py
   ```

6. **Access the application**:
   Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

## 📁 Project Structure

```
Blood_Bank_Management_System/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
├── old_version/
├── requirements.txt
├── run.py
└── README.md
```

* `app/`: Contains the main application code, including routes, models, templates, and static files.
* `old_version/`: Archive of previous versions for reference.
* `requirements.txt`: List of Python dependencies.
* `run.py`: Entry point to start the Flask application.

## 👥 Contributors

* [Hasnain-3764](https://github.com/Hasnain-3764)
* [pari23367](https://github.com/pari23367)
* [pranaybansal19](https://github.com/pranaybansal19)
* [daksh345](https://github.com/daksh345)

## 📞 Contact

For help or doubts, feel free to [create an issue](https://github.com/Hasnain-3764/Blood_Bank_Management_System/issues) on this repository.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```
```
