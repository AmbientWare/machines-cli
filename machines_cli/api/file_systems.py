from typing import Dict, List, Optional, Tuple, Any
from machines_cli.logging import logger
from machines_cli.api.base import BaseAPI
from pydantic import BaseModel
from machines_cli.api.utils import mb_to_gb


class MachineOptions(BaseModel):
    regions: List[str]
    options: Dict[str, List[int]]


class FileSystemAPI(BaseAPI):
    def __init__(self):
        super().__init__("file-systems")

    def list_file_systems(self) -> List[Dict]:
        """List all file systems"""
        try:
            res = self._get()

            return res

        except Exception as e:
            logger.error(f"Error listing file systems: {e}")
            return []

    def get_file_system(self, file_system_name: str) -> Dict[str, Any]:
        """Get file system by name"""

        def _get():
            res = self._get(params={"name": file_system_name})
            if res:
                return res[0]
            else:
                return None

        return self._run_with_spinner("Fetching file system...", _get)

    def create_file_system(
        self,
        name: str,
        size: int,
        region: str,
    ) -> Dict[str, Any]:
        """Create a new file system"""
        request_data = {
            "name": name,
            "size": size,
            "region": region.lower(),
        }

        def _create():
            return self._post(json=request_data)

        return self._run_with_spinner("Creating file system...", _create)

    def delete_file_system(
        self,
        id: int,
    ) -> Dict[str, Any]:
        """Delete a file system"""

        def _delete():
            return self._delete(json={"id": id})

        return self._run_with_spinner("Deleting file system...", _delete)

    def extend_volume(self, id: int, size: int) -> None:
        """Extend the volume of a file system"""

        def _extend():
            return self._put(json={"id": id, "size": size})

        return self._run_with_spinner("Extending volume...", _extend)


file_systems_api = FileSystemAPI()
