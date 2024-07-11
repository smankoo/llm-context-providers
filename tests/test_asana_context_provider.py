import os
import pytest
from unittest.mock import patch, AsyncMock
from llm_context_providers import AsanaContextProvider
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_fetch_context_async():
    provider = AsanaContextProvider(
        project_id=os.getenv("ASANA_PROJECT_ID", "test_project_id"),
        timezone="America/Toronto",
        fields={
            "Task": "name",
            "Task ID": "gid",
            "Created At": "created_at",
            "Modified At": "modified_at",
            "Completed": "completed",
            "Assignee": "assignee",
            "Due On": "due_on",
            "Notes": "notes"
        }
    )
    with patch.object(provider, 'get_project_info', new=AsyncMock(return_value={
            'name': 'Test Project', 
            'gid': '12345', 
            'created_at': '2024-07-07T11:00:00Z', 
            'modified_at': '2024-07-10T12:34:00Z',
            'owner': {'name': 'Test Owner'},
            'notes': '',
            'start_on': None,
            'due_on': None
        })), \
         patch.object(provider, 'get_tasks_info', new=AsyncMock(return_value=[])):
        await provider.fetch_context_async()
        context = provider.get_context()
        assert context is not None
        assert "Project:" in context

def test_fetch_context_sync():
    provider = AsanaContextProvider(
        project_id=os.getenv("ASANA_PROJECT_ID", "test_project_id"),
        timezone="America/Toronto",
        fields={
            "Task": "name",
            "Task ID": "gid",
            "Created At": "created_at",
            "Modified At": "modified_at",
            "Completed": "completed",
            "Assignee": "assignee",
            "Due On": "due_on",
            "Notes": "notes"
        }
    )
    with patch.object(provider, 'get_project_info_sync', return_value={
            'name': 'Test Project', 
            'gid': '12345', 
            'created_at': '2024-07-07T11:00:00Z', 
            'modified_at': '2024-07-10T12:34:00Z',
            'owner': {'name': 'Test Owner'},
            'notes': '',
            'start_on': None,
            'due_on': None
        }), \
         patch.object(provider, 'get_tasks_info_sync', return_value=[]):
        provider.fetch_context()
        context = provider.get_context()
        assert context is not None
        assert "Project:" in context

def test_missing_project_id():
    with pytest.raises(ValueError, match="Asana project ID is not set"):
        AsanaContextProvider(
            project_id=None,
            timezone="America/Toronto",
            fields={
                "Task": "name",
                "Task ID": "gid",
                "Created At": "created_at",
                "Modified At": "modified_at",
                "Completed": "completed",
                "Assignee": "assignee",
                "Due On": "due_on",
                "Notes": "notes"
            }
        )
