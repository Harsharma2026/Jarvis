"""
Code Handler - Manages file operations and code editor integration
Restricted to Jarvis_Work folder for safety
"""

import os
from pathlib import Path
import config

class CodeHandler:
    def __init__(self, memory=None):
        self.workspace = config.WORKSPACE_DIR
        self.memory = memory
        # Create workspace if it doesn't exist
        self.workspace.mkdir(parents=True, exist_ok=True)
        print(f"📁 Workspace: {self.workspace}")
    
    def read_file(self, file_path):
        """Read contents of a file (restricted to workspace)"""
        try:
            full_path = self.workspace / file_path
            
            # Security: ensure path is within workspace
            if not str(full_path.resolve()).startswith(str(self.workspace.resolve())):
                return "Error: Access denied - path outside workspace"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Record activity
            if self.memory:
                self.memory.record_file_activity(file_path, "read")
                self.memory.detect_project(file_path)
            
            return f"Successfully read {file_path}:\n\n{content}"
        except FileNotFoundError:
            return f"Error: File '{file_path}' not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, file_path, content):
        """Write content to a file (restricted to workspace)"""
        try:
            full_path = self.workspace / file_path
            
            # Security: ensure path is within workspace
            if not str(full_path.resolve()).startswith(str(self.workspace.resolve())):
                return "Error: Access denied - path outside workspace"
            
            # Create directory if it doesn't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists (create vs modify)
            action = "modified" if full_path.exists() else "created"
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Record activity
            if self.memory:
                self.memory.record_file_activity(file_path, action)
                self.memory.detect_project(file_path)
            
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_files(self, directory="."):
        """List files in a directory (restricted to workspace)"""
        try:
            full_path = self.workspace / directory
            
            # Security: ensure path is within workspace
            if not str(full_path.resolve()).startswith(str(self.workspace.resolve())):
                return "Error: Access denied - path outside workspace"
            
            files = []
            
            for item in full_path.iterdir():
                if item.is_file():
                    files.append(f"📄 {item.name}")
                elif item.is_dir():
                    files.append(f"📁 {item.name}/")
            
            if not files:
                return f"Directory '{directory}' is empty"
            
            return f"Contents of {directory}:\n" + "\n".join(sorted(files))
        except FileNotFoundError:
            return f"Error: Directory '{directory}' not found"
        except Exception as e:
            return f"Error listing files: {str(e)}"
