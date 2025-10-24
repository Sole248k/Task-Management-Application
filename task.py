"""
Task class representing a single task entity.
"""

from datetime import datetime
from typing import Optional, Dict, Any


class Task:
    """
    Represents a task with encapsulated attributes.
    
    Attributes are protected using name mangling to demonstrate encapsulation.
    Access to attributes is provided through properties.
    """
    
    def __init__(self, title: str, description: str, due_date: str, 
                 priority: str, status: str = "Pending",
                 task_id: Optional[int] = None, 
                 created_at: Optional[datetime] = None):
        """
        Initialize a Task object.
        
        Args:
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level (Low, Medium, High)
            status: Task status (Pending, In Progress, Completed)
            task_id: Unique task identifier (auto-generated if None)
            created_at: Creation timestamp (auto-generated if None)
        
        Raises:
            ValueError: If any required field is empty or invalid
        """
        # Validate inputs
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if not due_date or not due_date.strip():
            raise ValueError("Due date cannot be empty")
        if not priority or not priority.strip():
            raise ValueError("Priority cannot be empty")
        if not status or not status.strip():
            raise ValueError("Status cannot be empty")
        
        # Private attributes using name mangling for encapsulation
        self.__task_id: Optional[int] = task_id
        self.__title: str = title.strip()
        self.__description: str = description.strip()
        self.__due_date: str = due_date.strip()
        self.__priority: str = priority.strip().capitalize()
        self.__status: str = status.strip().capitalize()
        self.__created_at: datetime = created_at if created_at else datetime.now()
    
    # Property decorators for controlled access to attributes
    
    @property
    def task_id(self) -> Optional[int]:
        """Get task ID."""
        return self.__task_id
    
    @task_id.setter
    def task_id(self, value: int) -> None:
        """Set task ID (used when loading from database)."""
        if value is not None and value <= 0:
            raise ValueError("Task ID must be a positive integer")
        self.__task_id = value
    
    @property
    def title(self) -> str:
        """Get task title."""
        return self.__title
    
    @title.setter
    def title(self, value: str) -> None:
        """Set task title with validation."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self.__title = value.strip()
    
    @property
    def description(self) -> str:
        """Get task description."""
        return self.__description
    
    @description.setter
    def description(self, value: str) -> None:
        """Set task description with validation."""
        if not value or not value.strip():
            raise ValueError("Description cannot be empty")
        self.__description = value.strip()
    
    @property
    def due_date(self) -> str:
        """Get due date."""
        return self.__due_date
    
    @due_date.setter
    def due_date(self, value: str) -> None:
        """Set due date with validation."""
        if not value or not value.strip():
            raise ValueError("Due date cannot be empty")
        # Validate date format
        try:
            datetime.strptime(value.strip(), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        self.__due_date = value.strip()
    
    @property
    def priority(self) -> str:
        """Get priority level."""
        return self.__priority
    
    @priority.setter
    def priority(self, value: str) -> None:
        """Set priority level with validation."""
        valid_priorities = ['low', 'medium', 'high']
        if not value or value.strip().lower() not in valid_priorities:
            raise ValueError("Priority must be Low, Medium, or High")
        self.__priority = value.strip().capitalize()
    
    @property
    def status(self) -> str:
        """Get task status."""
        return self.__status
    
    @status.setter
    def status(self, value: str) -> None:
        """Set task status with validation."""
        valid_statuses = ['pending', 'in progress', 'completed']
        if not value or value.strip().lower() not in valid_statuses:
            raise ValueError("Status must be Pending, In Progress, or Completed")
        self.__status = value.strip().capitalize()
    
    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self.__created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task object to dictionary representation.
        
        Returns:
            Dictionary containing all task attributes
        """
        return {
            'task_id': self.__task_id,
            'title': self.__title,
            'description': self.__description,
            'due_date': self.__due_date,
            'priority': self.__priority,
            'status': self.__status,
            'created_at': self.__created_at
        }
    
    def __str__(self) -> str:
        """String representation of the task."""
        return (f"Task(ID={self.__task_id}, Title='{self.__title}', "
                f"Priority={self.__priority}, Status={self.__status}, "
                f"Due={self.__due_date})")
    
    def __repr__(self) -> str:
        """Developer-friendly representation of the task."""
        return self.__str__()
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality based on task ID.
        
        Args:
            other: Another Task object
        
        Returns:
            True if task IDs are equal, False otherwise
        """
        if not isinstance(other, Task):
            return False
        return self.__task_id == other.__task_id
    
    def __hash__(self) -> int:
        """
        Hash function based on task ID.
        
        Returns:
            Hash value of task ID
        """
        return hash(self.__task_id)