# Task Management Application

A command-line Task Management application built with Python 3.x and MySQL, demonstrating core Python fundamentals, object-oriented programming principles, and database interaction.

## 📋 Features

- ✅ Add new tasks with title, description, due date, priority, and status
- 📝 List all tasks in a formatted table
- 🔄 Update existing task details
- ✔️ Mark tasks as completed
- 🗑️ Delete tasks
- 🔍 Filter tasks by due date, priority, or status
- 📊 Sort tasks by due date, priority, or creation time
- 💾 Persistent storage using MySQL database
- 🎨 Clean command-line interface with input validation

## 🏗️ Architecture

### Object-Oriented Design

The application follows OOP best practices:

- **Task Class**: Encapsulated task entity with private attributes and property accessors
- **TaskManager Class**: Business logic layer handling CRUD operations and task management
- **DatabaseManager Class**: Database abstraction layer for MySQL operations
- **TaskCLI Class**: User interface layer for command-line interaction

### Key Design Principles

- **Encapsulation**: Private attributes using name mangling (`__attribute`)
- **Separation of Concerns**: Each class has a single, well-defined responsibility
- **Custom Algorithms**: Implemented merge sort for sorting and custom filtering logic
- **No ORM**: Direct SQL queries using PyMySQL
- **Error Handling**: Comprehensive try-except blocks with meaningful error messages
- **Input Validation**: All user inputs are validated before processing

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd task-management-app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL**
   
   Ensure MySQL server is running on your machine. The application will automatically create the database and tables on first run.

5. **Configure database connection** (optional)
   
   Create a `.env` file in the project root or set environment variables:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=task_management
   ```
   
   If not configured, defaults will be used (localhost, port 3306, root user, empty password).

### Running the Application

```bash
python task_manager.py
```

## 📁 Project Structure

```
task-management-app/
│
├── task_manager.py       # Main application entry point with TaskManager and CLI
├── task.py               # Task class definition
├── database.py           # DatabaseManager for MySQL operations
├── utils.py              # Utility functions (validation, formatting)
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # Database configuration (optional)
```

## 💻 Usage

### Main Menu

When you run the application, you'll see:

```
============================================================
               TASK MANAGEMENT SYSTEM
============================================================

1. Add New Task
2. List All Tasks
3. Update Task
4. Mark Task as Completed
5. Delete Task
6. Filter/Sort Tasks
7. Exit
```

### Adding a Task

Select option 1 and provide:
- **Title**: Task name (required)
- **Description**: Detailed description (required)
- **Due Date**: Format YYYY-MM-DD (e.g., 2025-10-30)
- **Priority**: Low, Medium, or High
- **Status**: Pending, In Progress, or Completed (default: Pending)

### Listing Tasks

Select option 2 to view all tasks in a formatted table showing:
- Task ID
- Title
- Priority (with color icons)
- Status (with status icons)
- Due Date

### Updating a Task

Select option 3, enter the Task ID, and update any fields. Leave blank to keep current values.

### Marking as Completed

Select option 4 and enter the Task ID to mark it as completed.

### Deleting a Task

Select option 5, enter the Task ID, and confirm deletion.

### Filtering and Sorting

Select option 6 to:
1. Filter tasks by due date, priority, and/or status
2. Sort results by due date, priority, or creation time

## 🗄️ Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    priority ENUM('Low', 'Medium', 'High') NOT NULL,
    status ENUM('Pending', 'In progress', 'Completed') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_due_date (due_date),
    INDEX idx_priority (priority)
);
```

## 🔧 Technical Highlights

### Custom Algorithms

1. **Merge Sort Implementation**
   - Time Complexity: O(n log n)
   - Used for sorting tasks by various criteria
   - Stable sorting algorithm

2. **Sequential Filtering**
   - Efficient filtering with multiple criteria
   - Supports combination of filters

### Data Structures

- **Dictionary (Hash Map)**: Used for in-memory task caching for O(1) lookups
- **List**: Used for storing and manipulating collections of tasks

### Error Handling

- Database connection errors
- Invalid user inputs
- Data validation errors
- Transaction rollback on failures

### Code Quality

- Follows PEP 8 style guide
- Comprehensive docstrings for all classes and methods
- Type hints for better code clarity
- Meaningful variable and function names

## 📦 Dependencies

```
PyMySQL==1.1.0
python-dotenv==1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

To test the application:

1. Run the application: `python task_manager.py`
2. Add several tasks with different priorities and due dates
3. Test filtering by different criteria
4. Test sorting by different fields
5. Update and delete tasks
6. Restart the application to verify persistence

## 🚧 Future Enhancements 

- Multithreading for concurrent operations
- Export tasks to CSV/JSON
- Task search functionality
- Recurring tasks
- Task categories/tags
- Due date reminders

## 👤 Author

CARL LAWRENCE LONTAC (Sole248k)

Created as part of the Junior Data Engineer/Analyst technical assessment.

## 📝 Notes

- This application was built without using ORM frameworks (like SQLAlchemy) to demonstrate understanding of direct database interaction
- Custom algorithms were implemented instead of using library functions where appropriate
- The code emphasizes clarity, maintainability, and adherence to Python best practices

## 🐛 Troubleshooting

### MySQL Connection Error

If you encounter connection errors:
1. Ensure MySQL server is running
2. Verify credentials in `.env` file or environment variables
3. Check if the user has proper permissions to create databases

### Module Import Error

Ensure all files are in the same directory and you're running from the project root.

### Port Already in Use

If MySQL port 3306 is in use, change the `DB_PORT` environment variable to an available port.

---

For questions or issues, please contact the repository maintainer.
