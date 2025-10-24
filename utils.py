"""
Utility functions for the Task Management Application.
"""

import os
from datetime import datetime
from typing import List
from task import Task


def validate_date(date_string: str) -> bool:
    """
    Validate if a string is in YYYY-MM-DD format.
    
    Args:
        date_string: Date string to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_priority(priority: str) -> bool:
    """
    Validate if priority is one of the allowed values.
    
    Args:
        priority: Priority string to validate
    
    Returns:
        True if valid, False otherwise
    """
    valid_priorities = ['low', 'medium', 'high']
    return priority.strip().lower() in valid_priorities


def validate_status(status: str) -> bool:
    """
    Validate if status is one of the allowed values.
    
    Args:
        status: Status string to validate
    
    Returns:
        True if valid, False otherwise
    """
    valid_statuses = ['pending', 'in progress', 'completed']
    return status.strip().lower() in valid_statuses


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str) -> None:
    """
    Print a formatted header.
    
    Args:
        title: Header title
    """
    width = 60
    print("=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_task_table(tasks: List[Task]) -> None:
    """
    Print tasks in a formatted table.
    
    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\n📭 No tasks to display.")
        return
    
    # Define column widths
    col_id = 6
    col_title = 25
    col_priority = 10
    col_status = 12
    col_due = 12
    
    # Print header
    print()
    print("-" * (col_id + col_title + col_priority + col_status + col_due + 16))
    print(f"{'ID':<{col_id}} | {'Title':<{col_title}} | {'Priority':<{col_priority}} | "
          f"{'Status':<{col_status}} | {'Due Date':<{col_due}}")
    print("-" * (col_id + col_title + col_priority + col_status + col_due + 16))
    
    # Print tasks
    for task in tasks:
        # Truncate title if too long
        title = task.title if len(task.title) <= col_title else task.title[:col_title-3] + "..."
        
        # Color coding for status
        status_icon = {
            'Pending': '⏳',
            'In progress': '🔄',
            'Completed': '✅'
        }.get(task.status, '•')
        
        priority_icon = {
            'Low': '🟢',
            'Medium': '🟡',
            'High': '🔴'
        }.get(task.priority, '•')
        
        print(f"{task.task_id:<{col_id}} | {title:<{col_title}} | "
              f"{priority_icon} {task.priority:<{col_priority-2}} | "
              f"{status_icon} {task.status:<{col_status-2}} | {task.due_date:<{col_due}}")
    
    print("-" * (col_id + col_title + col_priority + col_status + col_due + 16))


def format_timestamp(timestamp: datetime) -> str:
    """
    Format datetime object to readable string.
    
    Args:
        timestamp: Datetime object
    
    Returns:
        Formatted string
    """
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')