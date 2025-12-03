"""
Memory System - Knowledge Graph for JARVIS
Tracks projects, files, activities, and context
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class Memory:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.memory_file = workspace_dir / ".jarvis_memory.json"
        self.knowledge_graph = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load existing memory or create new"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "projects": {},
            "files": {},
            "activities": [],
            "preferences": {},
            "last_session": None
        }
    
    def _save_memory(self):
        """Save memory to disk"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.knowledge_graph, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
    
    def record_file_activity(self, file_path: str, action: str):
        """Record file creation/modification"""
        timestamp = datetime.now().isoformat()
        
        # Update file record
        if file_path not in self.knowledge_graph["files"]:
            self.knowledge_graph["files"][file_path] = {
                "created": timestamp,
                "last_modified": timestamp,
                "access_count": 1,
                "actions": []
            }
        else:
            self.knowledge_graph["files"][file_path]["last_modified"] = timestamp
            self.knowledge_graph["files"][file_path]["access_count"] += 1
        
        self.knowledge_graph["files"][file_path]["actions"].append({
            "action": action,
            "timestamp": timestamp
        })
        
        # Record activity
        self.knowledge_graph["activities"].append({
            "type": "file",
            "action": action,
            "target": file_path,
            "timestamp": timestamp
        })
        
        # Keep only last 100 activities
        if len(self.knowledge_graph["activities"]) > 100:
            self.knowledge_graph["activities"] = self.knowledge_graph["activities"][-100:]
        
        self._save_memory()
    
    def detect_project(self, file_path: str):
        """Auto-detect project from file path"""
        parts = Path(file_path).parts
        if len(parts) > 0:
            project_name = parts[0]
            
            if project_name not in self.knowledge_graph["projects"]:
                self.knowledge_graph["projects"][project_name] = {
                    "created": datetime.now().isoformat(),
                    "files": [],
                    "last_accessed": datetime.now().isoformat()
                }
            
            if file_path not in self.knowledge_graph["projects"][project_name]["files"]:
                self.knowledge_graph["projects"][project_name]["files"].append(file_path)
            
            self.knowledge_graph["projects"][project_name]["last_accessed"] = datetime.now().isoformat()
            self._save_memory()
    
    def get_recent_projects(self, limit: int = 5) -> List[Dict]:
        """Get recently accessed projects"""
        projects = []
        for name, data in self.knowledge_graph["projects"].items():
            projects.append({
                "name": name,
                "last_accessed": data["last_accessed"],
                "file_count": len(data["files"])
            })
        
        # Sort by last accessed
        projects.sort(key=lambda x: x["last_accessed"], reverse=True)
        return projects[:limit]
    
    def get_recent_files(self, limit: int = 5) -> List[Dict]:
        """Get recently modified files"""
        files = []
        for path, data in self.knowledge_graph["files"].items():
            files.append({
                "path": path,
                "last_modified": data["last_modified"],
                "access_count": data["access_count"]
            })
        
        files.sort(key=lambda x: x["last_modified"], reverse=True)
        return files[:limit]
    
    def get_context_summary(self) -> str:
        """Get a summary of recent context for AI"""
        recent_projects = self.get_recent_projects(3)
        recent_files = self.get_recent_files(5)
        
        summary = "Recent context:\n"
        
        if recent_projects:
            summary += "\nRecent projects:\n"
            for proj in recent_projects:
                summary += f"- {proj['name']} ({proj['file_count']} files, last accessed: {self._format_time(proj['last_accessed'])})\n"
        
        if recent_files:
            summary += "\nRecent files:\n"
            for file in recent_files:
                summary += f"- {file['path']} (modified: {self._format_time(file['last_modified'])})\n"
        
        return summary
    
    def _format_time(self, iso_time: str) -> str:
        """Format timestamp to human readable"""
        try:
            dt = datetime.fromisoformat(iso_time)
            now = datetime.now()
            diff = now - dt
            
            if diff.days == 0:
                if diff.seconds < 60:
                    return "just now"
                elif diff.seconds < 3600:
                    return f"{diff.seconds // 60} minutes ago"
                else:
                    return f"{diff.seconds // 3600} hours ago"
            elif diff.days == 1:
                return "yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return dt.strftime("%B %d")
        except:
            return "recently"
    
    def update_session(self):
        """Update last session time"""
        self.knowledge_graph["last_session"] = datetime.now().isoformat()
        self._save_memory()
    
    def get_project_info(self, project_name: str) -> Dict:
        """Get detailed info about a project"""
        if project_name in self.knowledge_graph["projects"]:
            return self.knowledge_graph["projects"][project_name]
        return None
