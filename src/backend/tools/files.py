from enum import StrEnum
from typing import Any, Dict, List

import backend.crud.file as file_crud
import backend.crud.interview as interview_crud
from backend.tools.base import BaseTool


class FileToolsArtifactTypes(StrEnum):
    local_file = "file"

class ReadFileTool(BaseTool):
    """
    Tool to read a file from the file system.
    """

    NAME = "read_document"
    MAX_NUM_CHUNKS = 10
    SEARCH_LIMIT = 5

    def __init__(self):
        pass

    @classmethod
    def is_available(cls) -> bool:
        return True

    async def call(self, parameters: dict, **kwargs: Any) -> List[Dict[str, Any]]:
        file = parameters.get("file")

        session = kwargs.get("session")
        user_id = kwargs.get("user_id")
        if not file:
            return []

        _, file_id = file
        retrieved_file = file_crud.get_file(session, file_id, user_id)
        if not retrieved_file:
            return []

        return [
            {
                "text": retrieved_file.file_content,
                "title": retrieved_file.file_name,
                "url": retrieved_file.file_name,
            }
        ]

class SearchInterviewTool(BaseTool):
    """
    Tool to query a list of interviews.
    """

    NAME = "search_interview"
    MAX_NUM_CHUNKS = 10
    SEARCH_LIMIT = 5

    def __init__(self):
        pass

    @classmethod
    def is_available(cls) -> bool:
        return True

    async def call(
        self, parameters: dict, ctx: Any, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        files = parameters.get("files")

        session = kwargs.get("session")

        file_ids = [file_id for _, file_id in files]
        retrieved_files = interview_crud.get_files_by_ids(session, file_ids)
        if not retrieved_files:
            return []

        results = []
        for file in retrieved_files:
            results.append(
                {
                    "text": file.file_content,
                    "title": file.file_name,
                    "": file.id,
                }
            )
        return results
