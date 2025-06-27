import os
from typing import List
from .base import StorageBackend, Item

class LocalStorageBackend(StorageBackend):
    def __init__(self, root_path: str):
        if not os.path.isdir(root_path):
            # In a container, the path might be created upon volume mount, so we don't error out.
            # We will log a warning or handle it gracefully.
            print(f"Warning: Root path '{root_path}' does not exist yet. It will be used when available.")
        self.root_path = os.path.abspath(root_path)
        print(f"Initialized LocalStorageBackend with root: {self.root_path}")

    def list(self, path: str) -> List[Item]:
        # Sanitize path to prevent directory traversal attacks
        sanitized_path = os.path.normpath(path.strip('/'))
        full_path = os.path.join(self.root_path, sanitized_path)
        
        # Security check: ensure the resolved path is still within our root directory
        if not os.path.abspath(full_path).startswith(self.root_path):
             raise PermissionError("Access denied: Path is outside the root directory.")

        if not os.path.isdir(full_path):
            return []

        items = []
        for entry in os.scandir(full_path):
            # Construct the relative path for the API response
            item_path = os.path.join(sanitized_path, entry.name) if sanitized_path != '.' else entry.name
            item_type = 'folder' if entry.is_dir() else 'file'
            items.append(Item(name=entry.name, path=item_path, type=item_type))
        
        return sorted(items, key=lambda x: (x.type, x.name))