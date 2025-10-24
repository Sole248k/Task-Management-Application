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
    Print tasks in a detailed format showing all attributes.
    
    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\n📭 No tasks to display.")
        return
    
    print()
    separator = "=" * 100
    
    for i, task in enumerate(tasks, 1):
        # Color coding for status and priority
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
        
        # Format creation timestamp
        if isinstance(task.created_at, datetime):
            created_str = task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_str = str(task.created_at)
        
        print(separator)
        print(f"Task #{i} - ID: {task.task_id}")
        print(separator)
        print(f"📌 Title       : {task.title}")
        print(f"📝 Description : {task.description}")
        print(f"📅 Due Date    : {task.due_date}")
        print(f"{priority_icon}  Priority    : {task.priority}")
        print(f"{status_icon}  Status      : {task.status}")
        print(f"🕐 Created At  : {created_str}")
        print()
    
    print(separator)


def format_timestamp(timestamp: datetime) -> str:
    """
    Format datetime object to readable string.
    
    Args:
        timestamp: Datetime object
    
    Returns:
        Formatted string
    """
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')