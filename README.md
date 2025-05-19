# Blood_Bank_Management_System

**screenshots**

![image](https://github.com/user-attachments/assets/4054e3a1-d7ae-432f-9ca0-4a45c7018e54)


 ![image](https://github.com/user-attachments/assets/57ed6b24-b3d2-46f3-bc89-b0e4722ef8dd)

 

# 🩸 Blood Bank Management System

A web-based application designed to streamline blood donation and transfusion processes by connecting donors, recipients, and administrators.

## 📌 Overview

This project aims to facilitate the efficient management of blood donations and requests. It provides functionalities for users to register as donors or recipients, and for administrators to manage blood inventories and user requests.

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

````
## 🔑 Additional Resources

- To get sample users and passwords, [click here](https://docs.google.com/document/d/1KERAR1CE8AaVnowDRec_lVvMLt1GuXQmkKWqwuMxJjA/edit?usp=sharing).
- To get a detailed view of our database design and queries, [click here](https://docs.google.com/document/d/1uotHiBb2fFlsTfjUPEzBt_DvCAADdTyjzzKw5lAtoy4/edit?usp=sharing).
- To get a detailed view of the relationship schema, [click here](https://lucid.app/lucidchart/a26e0787-038c-4228-b9dc-b8f602fa5e56/edit?viewport_loc=2309%2C-8537%2C2217%2C1036%2C0_0&invitationId=inv_1406b0ed-c9d8-4526-8826-c5bd8dbe6974).
- To get a detailed view of the ER diagram, [click here](https://lucid.app/lucidchart/408e70e1-31ca-4df8-9f47-d6ed7a878e37/edit?viewport_loc=8653%2C5757%2C2217%2C1036%2C0_0&invitationId=inv_a8399097-eed9-4a75-8172-3bbf4b3ac477).


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
