"""
Task Management Application
A command-line application for managing daily tasks with database persistence.
"""

import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
from task import Task
from database import DatabaseManager
from utils import (
    validate_date, validate_priority, validate_status,
    clear_screen, print_header, print_task_table
)


class TaskManager:
    """
    Manages task operations including CRUD operations, filtering, and sorting.
    
    This class acts as the main business logic layer, handling task management
    operations and coordinating between the Task objects and the database.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the TaskManager with a database manager.
        
        Args:
            db_manager: DatabaseManager instance for database operations
        """
        self.__db_manager = db_manager
        self.__tasks_cache: Dict[int, Task] = {}
        self.__load_tasks_from_db()
    
    def __load_tasks_from_db(self) -> None:
        """Load all tasks from database into memory cache."""
        try:
            task_data_list = self.__db_manager.fetch_all_tasks()
            self.__tasks_cache.clear()
            
            for task_data in task_data_list:
                task = Task(
                    title=task_data['title'],
                    description=task_data['description'],
                    due_date=task_data['due_date'],
                    priority=task_data['priority'],
                    status=task_data['status'],
                    task_id=task_data['task_id'],
                    created_at=task_data['created_at']
                )
                self.__tasks_cache[task.task_id] = task
        except Exception as e:
            print(f"Error loading tasks from database: {e}")
    
    def add_task(self, title: str, description: str, due_date: str, 
                 priority: str, status: str = "Pending") -> Optional[Task]:
        """
        Add a new task to the system.
        
        Args:
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level (Low, Medium, High)
            status: Task status (default: Pending)
        
        Returns:
            Task object if successful, None otherwise
        """
        try:
            # Create new task
            task = Task(title, description, due_date, priority, status)
            
            # Persist to database
            task_id = self.__db_manager.insert_task(task.to_dict())
            
            if task_id:
                task.task_id = task_id
                self.__tasks_cache[task_id] = task
                return task
            return None
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            Task object if found, None otherwise
        """
        return self.__tasks_cache.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all Task objects
        """
        return list(self.__tasks_cache.values())
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """
        Update task details.
        
        Args:
            task_id: Task ID to update
            **kwargs: Fields to update (title, description, due_date, priority, status)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            task = self.__tasks_cache.get(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return False
            
            # Update task attributes
            for key, value in kwargs.items():
                if hasattr(task, f'_{Task.__name__}__{key}'):
                    setattr(task, f'_{Task.__name__}__{key}', value)
            
            # Persist to database
            success = self.__db_manager.update_task(task_id, kwargs)
            return success
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def mark_completed(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Task ID to mark as completed
        
        Returns:
            True if successful, False otherwise
        """
        return self.update_task(task_id, status="Completed")
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the system.
        
        Args:
            task_id: Task ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if task_id not in self.__tasks_cache:
                print(f"Task with ID {task_id} not found.")
                return False
            
            # Delete from database
            success = self.__db_manager.delete_task(task_id)
            
            if success:
                del self.__tasks_cache[task_id]
            
            return success
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def filter_tasks(self, due_date: Optional[str] = None, 
                     priority: Optional[str] = None,
                     status: Optional[str] = None) -> List[Task]:
        """
        Filter tasks based on criteria using custom filtering algorithm.
        
        Args:
            due_date: Filter by due date (YYYY-MM-DD)
            priority: Filter by priority level
            status: Filter by status
        
        Returns:
            List of filtered Task objects
        """
        filtered_tasks = self.get_all_tasks()
        
        # Custom filtering algorithm - sequential filtering
        if due_date:
            filtered_tasks = [t for t in filtered_tasks if t.due_date == due_date]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority.lower() == priority.lower()]
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status.lower() == status.lower()]
        
        return filtered_tasks
    
    def sort_tasks(self, tasks: List[Task], sort_by: str = "due_date", 
                   reverse: bool = False) -> List[Task]:
        """
        Sort tasks using custom merge sort algorithm.
        
        Args:
            tasks: List of tasks to sort
            sort_by: Field to sort by (due_date, priority, created_at)
            reverse: Sort in descending order if True
        
        Returns:
            Sorted list of tasks
        """
        if len(tasks) <= 1:
            return tasks
        
        # Priority mapping for sorting
        priority_map = {"low": 1, "medium": 2, "high": 3}
        
        def get_sort_key(task: Task) -> Any:
            """Get the sorting key based on sort_by parameter."""
            if sort_by == "priority":
                return priority_map.get(task.priority.lower(), 0)
            elif sort_by == "created_at":
                return task.created_at
            else:  # default to due_date
                return task.due_date
        
        def merge_sort(arr: List[Task]) -> List[Task]:
            """
            Custom merge sort implementation for sorting tasks.
            Time Complexity: O(n log n)
            """
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            
            return merge(left, right)
        
        def merge(left: List[Task], right: List[Task]) -> List[Task]:
            """Merge two sorted arrays."""
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if get_sort_key(left[i]) <= get_sort_key(right[j]):
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            return result
        
        sorted_tasks = merge_sort(tasks)
        return sorted_tasks[::-1] if reverse else sorted_tasks


class TaskCLI:
    """
    Command-line interface for the Task Management Application.
    
    Handles user interaction and input validation.
    """
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the CLI with a TaskManager instance.
        
        Args:
            task_manager: TaskManager instance for handling operations
        """
        self.__task_manager = task_manager
    
    def run(self) -> None:
        """Main loop for the CLI application."""
        while True:
            try:
                self.__display_menu()
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == "1":
                    self.__add_task_ui()
                elif choice == "2":
                    self.__list_tasks_ui()
                elif choice == "3":
                    self.__update_task_ui()
                elif choice == "4":
                    self.__mark_completed_ui()
                elif choice == "5":
                    self.__delete_task_ui()
                elif choice == "6":
                    self.__filter_tasks_ui()
                elif choice == "7":
                    print("\nThank you for using Task Manager. Goodbye!")
                    sys.exit(0)
                else:
                    print("\n❌ Invalid choice. Please enter a number between 1 and 7.")
                
                input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("\nPress Enter to continue...")
    
    def __display_menu(self) -> None:
        """Display the main menu."""
        clear_screen()
        print_header("TASK MANAGEMENT SYSTEM")
        print("\n1. Add New Task")
        print("2. List All Tasks")
        print("3. Update Task")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. Filter/Sort Tasks")
        print("7. Exit")
    
    def __add_task_ui(self) -> None:
        """User interface for adding a new task."""
        clear_screen()
        print_header("ADD NEW TASK")
        
        try:
            title = input("\nEnter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty.")
                return
            
            description = input("Enter task description: ").strip()
            if not description:
                print("❌ Description cannot be empty.")
                return
            
            due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            if not validate_date(due_date):
                print("❌ Invalid date format. Use YYYY-MM-DD.")
                return
            
            priority = input("Enter priority (Low/Medium/High): ").strip()
            if not validate_priority(priority):
                print("❌ Invalid priority. Choose Low, Medium, or High.")
                return
            
            status = input("Enter status (Pending/In Progress/Completed) [Default: Pending]: ").strip()
            if not status:
                status = "Pending"
            elif not validate_status(status):
                print("❌ Invalid status. Choose Pending, In Progress, or Completed.")
                return
            
            task = self.__task_manager.add_task(title, description, due_date, priority, status)
            
            if task:
                print(f"\n✅ Task added successfully! Task ID: {task.task_id}")
            else:
                print("\n❌ Failed to add task.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def __list_tasks_ui(self) -> None:
        """User interface for listing all tasks."""
        clear_screen()
        print_header("ALL TASKS")
        
        tasks = self.__task_manager.get_all_tasks()
        
        if not tasks:
            print("\n📭 No tasks found.")
            return
        
        # Sort tasks by due date
        sorted_tasks = self.__task_manager.sort_tasks(tasks, sort_by="due_date")
        print_task_table(sorted_tasks)
        print(f"\nTotal tasks: {len(tasks)}")
    
    def __update_task_ui(self) -> None:
        """User interface for updating a task."""
        clear_screen()
        print_header("UPDATE TASK")
        
        try:
            task_id = int(input("\nEnter Task ID to update: ").strip())
            
            task = self.__task_manager.get_task(task_id)
            if not task:
                print(f"\n❌ Task with ID {task_id} not found.")
                return
            
            print(f"\nCurrent task details:")
            print_task_table([task])
            
            print("\nLeave blank to keep current value.")
            
            title = input(f"New title [{task.title}]: ").strip()
            description = input(f"New description [{task.description}]: ").strip()
            due_date = input(f"New due date [{task.due_date}]: ").strip()
            priority = input(f"New priority [{task.priority}]: ").strip()
            status = input(f"New status [{task.status}]: ").strip()
            
            updates = {}
            if title:
                updates['title'] = title
            if description:
                updates['description'] = description
            if due_date:
                if not validate_date(due_date):
                    print("❌ Invalid date format.")
                    return
                updates['due_date'] = due_date
            if priority:
                if not validate_priority(priority):
                    print("❌ Invalid priority.")
                    return
                updates['priority'] = priority
            if status:
                if not validate_status(status):
                    print("❌ Invalid status.")
                    return
                updates['status'] = status
            
            if updates:
                if self.__task_manager.update_task(task_id, **updates):
                    print("\n✅ Task updated successfully!")
                else:
                    print("\n❌ Failed to update task.")
            else:
                print("\n⚠️ No changes made.")
        except ValueError:
            print("\n❌ Invalid Task ID. Please enter a number.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def __mark_completed_ui(self) -> None:
        """User interface for marking a task as completed."""
        clear_screen()
        print_header("MARK TASK AS COMPLETED")
        
        try:
            task_id = int(input("\nEnter Task ID to mark as completed: ").strip())
            
            if self.__task_manager.mark_completed(task_id):
                print(f"\n✅ Task {task_id} marked as completed!")
            else:
                print(f"\n❌ Failed to mark task as completed.")
        except ValueError:
            print("\n❌ Invalid Task ID. Please enter a number.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def __delete_task_ui(self) -> None:
        """User interface for deleting a task."""
        clear_screen()
        print_header("DELETE TASK")
        
        try:
            task_id = int(input("\nEnter Task ID to delete: ").strip())
            
            task = self.__task_manager.get_task(task_id)
            if not task:
                print(f"\n❌ Task with ID {task_id} not found.")
                return
            
            print(f"\nTask to delete:")
            print_task_table([task])
            
            confirm = input("\n⚠️ Are you sure you want to delete this task? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                if self.__task_manager.delete_task(task_id):
                    print(f"\n✅ Task {task_id} deleted successfully!")
                else:
                    print(f"\n❌ Failed to delete task.")
            else:
                print("\n❌ Deletion cancelled.")
        except ValueError:
            print("\n❌ Invalid Task ID. Please enter a number.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def __filter_tasks_ui(self) -> None:
        """User interface for filtering and sorting tasks."""
        clear_screen()
        print_header("FILTER & SORT TASKS")
        
        print("\nFilter options (leave blank to skip):")
        due_date = input("Filter by due date (YYYY-MM-DD): ").strip() or None
        priority = input("Filter by priority (Low/Medium/High): ").strip() or None
        status = input("Filter by status (Pending/In Progress/Completed): ").strip() or None
        
        if due_date and not validate_date(due_date):
            print("❌ Invalid date format.")
            return
        
        if priority and not validate_priority(priority):
            print("❌ Invalid priority.")
            return
        
        if status and not validate_status(status):
            print("❌ Invalid status.")
            return
        
        tasks = self.__task_manager.filter_tasks(due_date, priority, status)
        
        if not tasks:
            print("\n📭 No tasks found matching the criteria.")
            return
        
        print("\nSort by:")
        print("1. Due Date")
        print("2. Priority")
        print("3. Created At")
        sort_choice = input("Enter choice (1-3) [Default: 1]: ").strip() or "1"
        
        sort_map = {"1": "due_date", "2": "priority", "3": "created_at"}
        sort_by = sort_map.get(sort_choice, "due_date")
        
        sorted_tasks = self.__task_manager.sort_tasks(tasks, sort_by=sort_by)
        
        clear_screen()
        print_header("FILTERED & SORTED TASKS")
        print_task_table(sorted_tasks)
        print(f"\nTotal tasks: {len(sorted_tasks)}")


def main():
    """Main entry point for the application."""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        
        # Initialize task manager
        task_manager = TaskManager(db_manager)
        
        # Start CLI
        cli = TaskCLI(task_manager)
        cli.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()