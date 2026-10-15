# Gym Management System

A menu-driven gym management system developed with Python. The application helps manage gym operations, including users, halls, group classes, class enrollments, subscriptions, wallet transactions, workout plans, and management reports.

The project is built using Object-Oriented Programming (OOP) principles and a modular structure that separates data models, repositories, business logic, and user menus.

## Features

### 1. User Management and Authentication
- Separate login options for Managers, Coaches, and Members.
- User registration and user information management.
- Username, password, and email validation.
- Account activation and deactivation.
- Role-based access to different application panels.
- Retry login or return to the main menu after an unsuccessful login.

### 2. Hall Management
- Add new halls.
- Edit hall information.
- View registered halls.
- Activate or deactivate halls.
- Manage the availability of halls for group classes.

### 3. Group Class Management
- Create, edit, and view group classes.
- Assign coaches and halls to classes.
- Activate or deactivate classes.
- Define and manage class capacity.
- Display class availability and remaining places.

### 4. Class Enrollment
- Browse available classes.
- Register for group classes.
- Cancel class registrations.
- View personal enrollment information and tracking numbers.
- Check membership eligibility and class capacity before enrollment.

### 5. Subscription Management
- Register subscriptions for members.
- View subscription information and status.
- Check subscription validity.
- Access subscription and payment information.

### 6. Wallet and Payment Management
- View wallet balance.
- Charge a member's wallet.
- View wallet transaction history.
- Make payments using the available payment workflow.
- Pay for or renew subscriptions.
- Record deposits and withdrawals.
- Validate payment details through a simulated bank API.

**Note:** The bank API is simulated for this project and does not process real bank transactions.

### 7. Workout Plan Management
- Allow coaches to create and manage workout plans for members.
- Add and manage exercises within workout plans.
- Allow members to view their assigned workout plans.
- Connect workout plans with the class enrollment system.

### 8. Management Reports
- View the number of active members.
- View the number of active coaches.
- View the number of active classes.
- Calculate and display total revenue based on stored transaction data.

## Project Structure

The application is organized into separate modules, each responsible for a specific part of the gym management system.

```text
Gym_management/
├── main.py
├── README.md
└── gym/
    ├── application.py
    ├── errors.py
    ├── classes/
    ├── enrollments/
    ├── halls/
    ├── menus/
    ├── payments/
    ├── reports/
    ├── subscriptions/
    ├── users/
    └── workouts/

```

### Main Components

- **`main.py`** — Entry point of the application.
- **`application.py`** — Initializes repositories and connects the application's services and managers.
- **`users/`** — User models, authentication, validation, storage, and user management.
- **`halls/`** — Hall models, data storage, and hall management operations.
- **`classes/`** — Group class models, repositories, and class management.
- **`enrollments/`** — Class enrollment records and enrollment-related business logic.
- **`subscriptions/`** — Subscription models, storage, and subscription management.
- **`payments/`** — Wallet operations, payment processing, transaction records, and the simulated bank API.
- **`workouts/`** — Workout plan models, storage, and workout plan management.
- **`reports/`** — Management reports and revenue calculations.
- **`menus/`** — The main menu and the separate Manager, Coach, and Member panels.
- **`errors/`** — Custom exceptions used to handle application errors.
- **`data/`** — Persistent application data stored in JSON and text files.

## Technologies

- **Python 3** — Main programming language.
- **Object-Oriented Programming (OOP)** — Organizing the application around classes and objects.
- **JSON** — Storing structured application data.
- **Text files** — Storing transaction records.
- **Git and GitHub** — Version control and collaborative development.

## Getting Started

### Prerequisites

- Python 3 installed on your system.
- Git, if you want to clone the repository.

The application uses JSON and text files for data persistence rather than a database server.

### Installation

Clone the repository:

```bash
git clone https://github.com/Marziye94/Gym_management.git
```

Navigate to the project directory:

```bash
cd Gym_management
```

### Initial Data Setup

Before using the application, make sure the initial Manager account is available in `gym/data/users.json`.

The application loads users from this file. If the file does not exist, the user repository returns an empty user list, so there will be no account available for the first login.

A Manager record should follow the project's user data structure. For example:

```json
[
  {
    "user_id": 1,
    "name": "Gym Manager",
    "username": "manager",
    "password": "ChangeMe1@",
    "role": "Manager",
    "is_active": true,
    "email": "manager@example.com"
  }
]
```

Replace the example credentials with your own values before using the application. The password must contain at least one English letter, one digit, and either `@` or `&`. Usernames must be unique.

**Important:** This example is intended for initial setup only. Do not use example credentials as permanent or shared account credentials.

### Running the Application

Run the following command from the repository root:

```bash
python main.py
```

The main menu provides the following options:

1. Manager Login
2. Coach Login
3. Member Login
4. Exit

After a successful login, the user is directed to the panel corresponding to their role.

## Data Storage

The application stores its data in files under `gym/data/`. Depending on the module, these files include:

- `users.json` — User accounts and account information.
- `halls.json` — Hall records.
- `classes.json` — Group class records.
- `subscriptions.json` — Subscription records.
- `wallets.json` — Member wallet data.
- `transactions.txt` — Payment and wallet transaction records.
- `enrollments.json` — Class enrollment records.
- `workout_plans.json` — Workout plan data.

The application loads these files during initialization. Some features may be unavailable if their corresponding data cannot be loaded or contains invalid data.

Keep a backup of important data files before making manual changes.

## Error Handling and Validation

The project includes input validation and error-handling mechanisms to help prevent invalid data from entering the system. Stored user data is also validated when loaded.

When a data file cannot be loaded, the application can report the problem and disable the features that depend on the unavailable data, while allowing other menus to remain accessible when possible.

## Project Status

This project is being developed collaboratively and may continue to evolve as new features are added and existing functionality is improved.

