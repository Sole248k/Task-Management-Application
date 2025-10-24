"""
Database manager for handling MySQL database operations.
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """
    Manages all database operations for the Task Management Application.
    
    Handles connection management, CRUD operations, and query execution
    without using any ORM.
    """
    
    def __init__(self):
        """
        Initialize database manager with configuration.
        
        Configuration is loaded from environment variables or defaults.
        """
        self.__host = os.getenv('DB_HOST', 'localhost')
        self.__port = int(os.getenv('DB_PORT', 3306))
        self.__user = os.getenv('DB_USER', 'root')
        self.__password = os.getenv('DB_PASSWORD', '')
        self.__database = os.getenv('DB_NAME', 'task_management')
        self.__connection: Optional[pymysql.Connection] = None
    
    def connect(self) -> None:
        """
        Establish connection to MySQL database.
        Creates database if it doesn't exist.
        
        Raises:
            Exception: If connection fails
        """
        try:
            # First connect without database to create it if needed
            self.__connection = pymysql.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            
            # Create database if not exists
            with self.__connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__database}")
                cursor.execute(f"USE {self.__database}")
            
            self.__connection.commit()
            print(f"✅ Connected to MySQL database '{self.__database}'")
        except pymysql.Error as e:
            raise Exception(f"Database connection failed: {e}")
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.__connection:
            self.__connection.close()
            print("✅ Database connection closed")
    
    def create_tables(self) -> None:
        """
        Create necessary tables if they don't exist.
        
        Schema design:
        - tasks table: stores all task information
        - Indexes on status and due_date for efficient filtering
        """
        try:
            with self.__connection.cursor() as cursor:
                # Create tasks table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
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
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
            
            self.__connection.commit()
            print("✅ Database tables created/verified")
        except pymysql.Error as e:
            raise Exception(f"Failed to create tables: {e}")
    
    def insert_task(self, task_data: Dict[str, Any]) -> Optional[int]:
        """
        Insert a new task into the database.
        
        Args:
            task_data: Dictionary containing task information
        
        Returns:
            Task ID of inserted task, None if failed
        """
        try:
            with self.__connection.cursor() as cursor:
                query = """
                    INSERT INTO tasks (title, description, due_date, priority, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (
                    task_data['title'],
                    task_data['description'],
                    task_data['due_date'],
                    task_data['priority'],
                    task_data['status'],
                    task_data['created_at']
                ))
            
            self.__connection.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            self.__connection.rollback()
            print(f"Error inserting task: {e}")
            return None
    
    def fetch_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Fetch all tasks from the database.
        
        Returns:
            List of task dictionaries
        """
        try:
            with self.__connection.cursor() as cursor:
                query = """
                    SELECT task_id, title, description, due_date, 
                           priority, status, created_at
                    FROM tasks
                    ORDER BY task_id
                """
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert date objects to strings
                for row in results:
                    if isinstance(row['due_date'], datetime):
                        row['due_date'] = row['due_date'].strftime('%Y-%m-%d')
                    elif hasattr(row['due_date'], 'isoformat'):
                        row['due_date'] = row['due_date'].isoformat()
                
                return results
        except pymysql.Error as e:
            print(f"Error fetching tasks: {e}")
            return []
    
    def fetch_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single task by ID.
        
        Args:
            task_id: Task ID to fetch
        
        Returns:
            Task dictionary if found, None otherwise
        """
        try:
            with self.__connection.cursor() as cursor:
                query = """
                    SELECT task_id, title, description, due_date, 
                           priority, status, created_at
                    FROM tasks
                    WHERE task_id = %s
                """
                cursor.execute(query, (task_id,))
                result = cursor.fetchone()
                
                if result and isinstance(result['due_date'], datetime):
                    result['due_date'] = result['due_date'].strftime('%Y-%m-%d')
                
                return result
        except pymysql.Error as e:
            print(f"Error fetching task: {e}")
            return None
    
    def update_task(self, task_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a task's fields.
        
        Args:
            task_id: Task ID to update
            updates: Dictionary of fields to update
        
        Returns:
            True if successful, False otherwise
        """
        if not updates:
            return False
        
        try:
            # Build dynamic UPDATE query
            set_clauses = []
            values = []
            
            for key, value in updates.items():
                set_clauses.append(f"{key} = %s")
                values.append(value)
            
            values.append(task_id)
            
            with self.__connection.cursor() as cursor:
                query = f"""
                    UPDATE tasks
                    SET {', '.join(set_clauses)}
                    WHERE task_id = %s
                """
                cursor.execute(query, values)
            
            self.__connection.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            self.__connection.rollback()
            print(f"Error updating task: {e}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the database.
        
        Args:
            task_id: Task ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.__connection.cursor() as cursor:
                query = "DELETE FROM tasks WHERE task_id = %s"
                cursor.execute(query, (task_id,))
            
            self.__connection.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            self.__connection.rollback()
            print(f"Error deleting task: {e}")
            return False
    
    def __del__(self):
        """Destructor to ensure connection is closed."""
        self.disconnect()