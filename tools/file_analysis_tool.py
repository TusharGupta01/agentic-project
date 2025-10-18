"""
File and folder analysis tools for the AI agent.
"""

import os
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
import hashlib


def _get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive information about a file."""
    try:
        path = Path(file_path)
        stat = path.stat()
        
        # Get file type
        mime_type, _ = mimetypes.guess_type(file_path)
        file_type = mime_type or "unknown"
        
        # Get file extension
        extension = path.suffix.lower()
        
        # Calculate file hash for identification
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:8]
        except:
            file_hash = "unknown"
        
        return {
            "name": path.name,
            "path": str(path.absolute()),
            "size": stat.st_size,
            "size_human": _format_file_size(stat.st_size),
            "extension": extension,
            "mime_type": file_type,
            "modified": stat.st_mtime,
            "hash": file_hash,
            "is_file": path.is_file(),
            "is_dir": path.is_dir()
        }
    except Exception as e:
        return {"error": str(e), "path": file_path}


def _format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def _is_text_file(file_path: str) -> bool:
    """Check if a file is likely a text file."""
    try:
        # Check by extension
        text_extensions = {
            '.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml', 
            '.yaml', '.yml', '.ini', '.cfg', '.conf', '.log', '.csv', '.sql',
            '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.go', '.rs',
            '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.swift',
            '.kt', '.scala', '.r', '.m', '.pl', '.lua', '.vim', '.dockerfile',
            '.gitignore', '.env', '.gitattributes', '.editorconfig'
        }
        
        extension = Path(file_path).suffix.lower()
        if extension in text_extensions:
            return True
        
        # Check by MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('text/'):
            return True
        
        # Check by reading first few bytes
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                # If it contains null bytes, it's likely binary
                if b'\x00' in chunk:
                    return False
                # Try to decode as UTF-8
                chunk.decode('utf-8')
                return True
        except:
            return False
            
    except:
        return False


def _read_file_safely(file_path: str, max_size: int = 100000) -> str:
    """Safely read a text file with size limits."""
    try:
        if not _is_text_file(file_path):
            return f"[Binary file - cannot read content]"
        
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            return f"[File too large ({_format_file_size(file_size)}) - showing first {_format_file_size(max_size)}]"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return content
            
    except Exception as e:
        return f"[Error reading file: {str(e)}]"


@tool
def list_folder_contents(folder_path: str, include_hidden: bool = False, max_depth: int = 2) -> str:
    """List the contents of a folder with detailed information."""
    try:
        folder_path = os.path.expanduser(folder_path)
        if not os.path.exists(folder_path):
            return f"Error: Folder '{folder_path}' does not exist."
        
        if not os.path.isdir(folder_path):
            return f"Error: '{folder_path}' is not a folder."
        
        result = f"📁 Folder Contents: {folder_path}\n"
        result += "=" * 60 + "\n\n"
        
        # Get folder info
        folder_info = _get_file_info(folder_path)
        result += f"📊 Folder Statistics:\n"
        result += f"   Path: {folder_info['path']}\n"
        result += f"   Modified: {folder_info['modified']}\n\n"
        
        # List contents
        items = []
        for item in os.listdir(folder_path):
            if not include_hidden and item.startswith('.'):
                continue
            
            item_path = os.path.join(folder_path, item)
            item_info = _get_file_info(item_path)
            items.append(item_info)
        
        # Sort by type (folders first) then by name
        items.sort(key=lambda x: (not x.get('is_dir', False), x.get('name', '').lower()))
        
        result += f"📋 Contents ({len(items)} items):\n\n"
        
        for item in items:
            if 'error' in item:
                result += f"❌ {item['name']} - Error: {item['error']}\n"
                continue
            
            icon = "📁" if item.get('is_dir', False) else "📄"
            name = item['name']
            size = item.get('size_human', 'unknown')
            ext = item.get('extension', '')
            
            result += f"{icon} {name}"
            if ext:
                result += f" ({ext})"
            if not item.get('is_dir', False):
                result += f" - {size}"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error listing folder contents: {str(e)}"


@tool
def read_file_content(file_path: str, max_lines: int = 100) -> str:
    """Read the content of a text file with line limits."""
    try:
        file_path = os.path.expanduser(file_path)
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' is not a file."
        
        file_info = _get_file_info(file_path)
        
        result = f"📄 File: {file_info['name']}\n"
        result += f"📊 Size: {file_info['size_human']}\n"
        result += f"📝 Type: {file_info['mime_type']}\n"
        result += "=" * 60 + "\n\n"
        
        content = _read_file_safely(file_path)
        
        if content.startswith("[Binary file"):
            return result + content
        
        if content.startswith("[File too large"):
            return result + content
        
        if content.startswith("[Error reading"):
            return result + content
        
        # Limit lines if requested
        lines = content.split('\n')
        if len(lines) > max_lines:
            result += f"[Showing first {max_lines} lines of {len(lines)} total lines]\n\n"
            content = '\n'.join(lines[:max_lines])
        
        result += content
        
        if len(lines) > max_lines:
            result += f"\n\n... ({len(lines) - max_lines} more lines)"
        
        return result
        
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def analyze_folder_structure(folder_path: str, include_hidden: bool = False) -> str:
    """Analyze the structure and contents of a folder."""
    try:
        folder_path = os.path.expanduser(folder_path)
        if not os.path.exists(folder_path):
            return f"Error: Folder '{folder_path}' does not exist."
        
        if not os.path.isdir(folder_path):
            return f"Error: '{folder_path}' is not a folder."
        
        result = f"🔍 Folder Analysis: {folder_path}\n"
        result += "=" * 60 + "\n\n"
        
        # Statistics
        total_files = 0
        total_dirs = 0
        total_size = 0
        file_types = {}
        largest_files = []
        
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden directories if requested
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            
            total_dirs += len(dirs)
            
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                
                try:
                    file_info = _get_file_info(file_path)
                    file_size = file_info.get('size', 0)
                    total_size += file_size
                    
                    # Track file types
                    ext = file_info.get('extension', 'no_extension')
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
                    # Track largest files
                    largest_files.append((file_path, file_size))
                    
                except:
                    continue
        
        # Sort largest files
        largest_files.sort(key=lambda x: x[1], reverse=True)
        
        result += f"📊 Statistics:\n"
        result += f"   Total Files: {total_files}\n"
        result += f"   Total Directories: {total_dirs}\n"
        result += f"   Total Size: {_format_file_size(total_size)}\n\n"
        
        # File types
        if file_types:
            result += f"📁 File Types:\n"
            sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:10]:  # Top 10
                ext_display = ext if ext != 'no_extension' else '(no extension)'
                result += f"   {ext_display}: {count} files\n"
            result += "\n"
        
        # Largest files
        if largest_files:
            result += f"📏 Largest Files:\n"
            for file_path, size in largest_files[:5]:  # Top 5
                rel_path = os.path.relpath(file_path, folder_path)
                result += f"   {rel_path} - {_format_file_size(size)}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error analyzing folder: {str(e)}"


@tool
def search_files_in_folder(folder_path: str, search_term: str, file_extensions: str = "", case_sensitive: bool = False) -> str:
    """Search for text content in files within a folder."""
    try:
        folder_path = os.path.expanduser(folder_path)
        if not os.path.exists(folder_path):
            return f"Error: Folder '{folder_path}' does not exist."
        
        if not os.path.isdir(folder_path):
            return f"Error: '{folder_path}' is not a folder."
        
        # Parse file extensions
        extensions = set()
        if file_extensions:
            for ext in file_extensions.split(','):
                ext = ext.strip().lower()
                if not ext.startswith('.'):
                    ext = '.' + ext
                extensions.add(ext)
        
        result = f"🔍 Search Results for '{search_term}' in {folder_path}\n"
        result += "=" * 60 + "\n\n"
        
        matches = []
        search_lower = search_term.lower() if not case_sensitive else search_term
        
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Filter by extension if specified
                if extensions:
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext not in extensions:
                        continue
                
                # Skip binary files
                if not _is_text_file(file_path):
                    continue
                
                try:
                    content = _read_file_safely(file_path, max_size=50000)  # Smaller limit for search
                    if content.startswith('['):  # Error or binary file
                        continue
                    
                    content_search = content.lower() if not case_sensitive else content
                    if search_lower in content_search:
                        # Count matches
                        match_count = content_search.count(search_lower)
                        rel_path = os.path.relpath(file_path, folder_path)
                        matches.append((rel_path, match_count, file_path))
                        
                except:
                    continue
        
        if not matches:
            result += "No matches found.\n"
        else:
            # Sort by match count
            matches.sort(key=lambda x: x[1], reverse=True)
            
            result += f"Found {len(matches)} files with matches:\n\n"
            
            for rel_path, match_count, full_path in matches:
                result += f"📄 {rel_path} ({match_count} matches)\n"
        
        return result
        
    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def get_file_summary(file_path: str) -> str:
    """Get a summary of a file including key information and content overview."""
    try:
        file_path = os.path.expanduser(file_path)
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' is not a file."
        
        file_info = _get_file_info(file_path)
        
        result = f"📄 File Summary: {file_info['name']}\n"
        result += "=" * 60 + "\n\n"
        
        result += f"📊 Basic Information:\n"
        result += f"   Path: {file_info['path']}\n"
        result += f"   Size: {file_info['size_human']}\n"
        result += f"   Type: {file_info['mime_type']}\n"
        result += f"   Extension: {file_info['extension']}\n"
        result += f"   Modified: {file_info['modified']}\n\n"
        
        # For text files, provide content analysis
        if _is_text_file(file_path):
            content = _read_file_safely(file_path, max_size=10000)
            
            if not content.startswith('['):
                lines = content.split('\n')
                non_empty_lines = [line for line in lines if line.strip()]
                
                result += f"📝 Content Analysis:\n"
                result += f"   Total Lines: {len(lines)}\n"
                result += f"   Non-empty Lines: {len(non_empty_lines)}\n"
                result += f"   Characters: {len(content)}\n\n"
                
                # Show first few lines as preview
                preview_lines = lines[:5]
                result += f"📖 Preview (first 5 lines):\n"
                for i, line in enumerate(preview_lines, 1):
                    result += f"   {i}: {line}\n"
                
                if len(lines) > 5:
                    result += f"   ... ({len(lines) - 5} more lines)\n"
        else:
            result += f"📝 Content: Binary file - cannot analyze content\n"
        
        return result
        
    except Exception as e:
        return f"Error getting file summary: {str(e)}"
