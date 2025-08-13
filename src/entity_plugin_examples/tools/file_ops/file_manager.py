"""File manager plugin for basic file system operations."""

from __future__ import annotations
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class FileManagerPlugin(ToolPlugin):
    """
    File manager plugin for safe file system operations.
    
    Features:
    - List directory contents
    - Read file contents (text files only)
    - Create directories
    - Copy/move files (within allowed directories)
    - Get file information (size, modified date, etc.)
    - Safe operations with path validation
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        config = config or {}
        
        # Security: Restrict operations to allowed directories
        self.allowed_directories = config.get("allowed_directories", [tempfile.gettempdir()])
        self.max_file_size = config.get("max_file_size", 10 * 1024 * 1024)  # 10MB
        self.allowed_extensions = config.get("allowed_extensions", [
            ".txt", ".md", ".json", ".csv", ".log", ".yaml", ".yml", ".xml"
        ])
        self.read_only_mode = config.get("read_only_mode", True)
        
        # Ensure allowed directories exist and are absolute
        self.allowed_directories = [os.path.abspath(d) for d in self.allowed_directories]
    
    async def _execute_impl(self, context) -> str:
        """Execute file management operations."""
        command = (context.message or "").strip()
        
        if not command:
            return self._show_help()
        
        try:
            # Parse command
            parts = command.split(" ", 1)
            operation = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Route to appropriate operation
            if operation == "ls" or operation == "list":
                return self._list_directory(args or ".")
            elif operation == "read" or operation == "cat":
                return self._read_file(args)
            elif operation == "info" or operation == "stat":
                return self._get_file_info(args)
            elif operation == "mkdir":
                return self._create_directory(args)
            elif operation == "copy" or operation == "cp":
                return self._copy_file(args)
            elif operation == "help":
                return self._show_help()
            else:
                return f"Unknown operation: {operation}. Use 'help' for available commands."
                
        except Exception as e:
            return f"File Operation Error: {str(e)}"
    
    def _validate_path(self, path: str) -> str:
        """Validate and normalize path for security."""
        if not path:
            raise ValueError("Path cannot be empty")
        
        # Convert to absolute path
        abs_path = os.path.abspath(path)
        
        # Check if path is within allowed directories
        allowed = False
        for allowed_dir in self.allowed_directories:
            try:
                # Check if the path is under an allowed directory
                os.path.relpath(abs_path, allowed_dir)
                if abs_path.startswith(allowed_dir):
                    allowed = True
                    break
            except ValueError:
                # Different drives on Windows
                continue
        
        if not allowed:
            raise PermissionError(f"Path '{path}' is not within allowed directories")
        
        return abs_path
    
    def _list_directory(self, path: str) -> str:
        """List directory contents."""
        try:
            validated_path = self._validate_path(path)
            
            if not os.path.exists(validated_path):
                return f"Directory does not exist: {path}"
            
            if not os.path.isdir(validated_path):
                return f"Path is not a directory: {path}"
            
            items = []
            total_size = 0
            
            try:
                for item_name in sorted(os.listdir(validated_path)):
                    item_path = os.path.join(validated_path, item_name)
                    
                    try:
                        stat = os.stat(item_path)
                        is_dir = os.path.isdir(item_path)
                        size = stat.st_size if not is_dir else 0
                        
                        total_size += size
                        
                        # Format size
                        if is_dir:
                            size_str = "<DIR>"
                        else:
                            size_str = self._format_size(size)
                        
                        # Get extension
                        ext = Path(item_name).suffix.lower() if not is_dir else ""
                        
                        items.append({
                            "name": item_name,
                            "type": "directory" if is_dir else "file",
                            "size": size,
                            "size_str": size_str,
                            "extension": ext,
                            "accessible": True
                        })
                        
                    except PermissionError:
                        items.append({
                            "name": item_name,
                            "type": "unknown",
                            "size": 0,
                            "size_str": "N/A",
                            "extension": "",
                            "accessible": False
                        })
            
            except PermissionError:
                return f"Permission denied: Cannot list directory {path}"
            
            # Format output
            output = [f"📁 **Directory listing for:** {path}"]
            output.append(f"**Path:** {validated_path}")
            output.append(f"**Items:** {len(items)} | **Total size:** {self._format_size(total_size)}\\n")
            
            if not items:
                output.append("(Empty directory)")
                return "\\n".join(output)
            
            # Group by type
            directories = [item for item in items if item["type"] == "directory"]
            files = [item for item in items if item["type"] == "file"]
            
            if directories:
                output.append("**📁 Directories:**")
                for item in directories:
                    icon = "📁" if item["accessible"] else "🔒"
                    output.append(f"  {icon} {item['name']}/")
                output.append("")
            
            if files:
                output.append("**📄 Files:**")
                for item in files:
                    if not item["accessible"]:
                        icon = "🔒"
                    elif item["extension"] in self.allowed_extensions:
                        icon = "📄"
                    else:
                        icon = "📋"
                    
                    output.append(f"  {icon} {item['name']} ({item['size_str']})")
            
            return "\\n".join(output)
            
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def _read_file(self, path: str) -> str:
        """Read file contents."""
        try:
            if not path:
                return "Error: No file path provided"
            
            validated_path = self._validate_path(path)
            
            if not os.path.exists(validated_path):
                return f"File does not exist: {path}"
            
            if not os.path.isfile(validated_path):
                return f"Path is not a file: {path}"
            
            # Check file size
            file_size = os.path.getsize(validated_path)
            if file_size > self.max_file_size:
                return f"File too large: {self._format_size(file_size)} (max: {self._format_size(self.max_file_size)})"
            
            # Check extension
            file_ext = Path(validated_path).suffix.lower()
            if file_ext not in self.allowed_extensions:
                return f"File type not allowed: {file_ext}. Allowed: {', '.join(self.allowed_extensions)}"
            
            # Read file
            try:
                with open(validated_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Truncate if too long for display
                max_display = 2000
                if len(content) > max_display:
                    content = content[:max_display] + "\\n\\n... (truncated)"
                
                output = [f"📄 **File contents:** {path}"]
                output.append(f"**Path:** {validated_path}")
                output.append(f"**Size:** {self._format_size(file_size)}")
                output.append(f"**Extension:** {file_ext}\\n")
                output.append("```")
                output.append(content)
                output.append("```")
                
                return "\\n".join(output)
                
            except UnicodeDecodeError:
                return f"Error: File appears to be binary or uses unsupported encoding: {path}"
                
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _get_file_info(self, path: str) -> str:
        """Get file/directory information."""
        try:
            if not path:
                return "Error: No path provided"
            
            validated_path = self._validate_path(path)
            
            if not os.path.exists(validated_path):
                return f"Path does not exist: {path}"
            
            stat = os.stat(validated_path)
            is_dir = os.path.isdir(validated_path)
            
            output = [f"ℹ️  **Path information:** {path}"]
            output.append(f"**Full path:** {validated_path}")
            output.append(f"**Type:** {'Directory' if is_dir else 'File'}")
            output.append(f"**Size:** {self._format_size(stat.st_size)}")
            output.append(f"**Modified:** {self._format_timestamp(stat.st_mtime)}")
            output.append(f"**Accessed:** {self._format_timestamp(stat.st_atime)}")
            
            if not is_dir:
                file_ext = Path(validated_path).suffix.lower()
                output.append(f"**Extension:** {file_ext if file_ext else '(none)'}")
                output.append(f"**Readable:** {'Yes' if file_ext in self.allowed_extensions else 'No (extension not allowed)'}")
            
            return "\\n".join(output)
            
        except Exception as e:
            return f"Error getting file info: {str(e)}"
    
    def _create_directory(self, path: str) -> str:
        """Create directory (if not in read-only mode)."""
        if self.read_only_mode:
            return "Error: File manager is in read-only mode"
        
        try:
            if not path:
                return "Error: No directory path provided"
            
            validated_path = self._validate_path(path)
            
            if os.path.exists(validated_path):
                return f"Path already exists: {path}"
            
            os.makedirs(validated_path, exist_ok=True)
            return f"✅ Created directory: {path}"
            
        except Exception as e:
            return f"Error creating directory: {str(e)}"
    
    def _copy_file(self, args: str) -> str:
        """Copy file (if not in read-only mode)."""
        if self.read_only_mode:
            return "Error: File manager is in read-only mode"
        
        try:
            parts = args.split(" ", 1)
            if len(parts) != 2:
                return "Error: Copy requires source and destination paths"
            
            src_path, dst_path = parts
            validated_src = self._validate_path(src_path)
            validated_dst = self._validate_path(dst_path)
            
            if not os.path.exists(validated_src):
                return f"Source file does not exist: {src_path}"
            
            if not os.path.isfile(validated_src):
                return f"Source is not a file: {src_path}"
            
            shutil.copy2(validated_src, validated_dst)
            return f"✅ Copied file: {src_path} → {dst_path}"
            
        except Exception as e:
            return f"Error copying file: {str(e)}"
    
    def _show_help(self) -> str:
        """Show available commands."""
        mode_str = "read-only" if self.read_only_mode else "read-write"
        
        commands = [
            "📋 **File Manager Commands:**",
            f"**Mode:** {mode_str}",
            f"**Allowed directories:** {', '.join(self.allowed_directories)}\\n",
            
            "**Available commands:**",
            "• `ls [path]` or `list [path]` - List directory contents",
            "• `read <file>` or `cat <file>` - Read file contents",
            "• `info <path>` or `stat <path>` - Get file/directory information",
        ]
        
        if not self.read_only_mode:
            commands.extend([
                "• `mkdir <path>` - Create directory",
                "• `copy <src> <dst>` or `cp <src> <dst>` - Copy file",
            ])
        
        commands.extend([
            "• `help` - Show this help message\\n",
            
            f"**Supported file types:** {', '.join(self.allowed_extensions)}",
            f"**Maximum file size:** {self._format_size(self.max_file_size)}"
        ])
        
        return "\\n".join(commands)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        
        return f"{size_bytes:.1f} TB"
    
    def _format_timestamp(self, timestamp: float) -> str:
        """Format timestamp in readable format."""
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


# Example usage:
"""
file_mgr = FileManagerPlugin(resources={}, config={
    "allowed_directories": ["/tmp", "/home/user/documents"],
    "read_only_mode": True,
    "max_file_size": 5 * 1024 * 1024  # 5MB
})

# List directory
await file_mgr._execute_impl(Mock(message="ls /tmp"))

# Read file
await file_mgr._execute_impl(Mock(message="read /tmp/example.txt"))

# Get file info
await file_mgr._execute_impl(Mock(message="info /tmp/example.txt"))

# Create directory (if not read-only)
await file_mgr._execute_impl(Mock(message="mkdir /tmp/new_folder"))

# Show help
await file_mgr._execute_impl(Mock(message="help"))
"""