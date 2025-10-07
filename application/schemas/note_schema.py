from pydantic import BaseModel, Field
from typing import Optional


# Schema for creating a note
class NoteCreate(BaseModel):
    title: str = Field(..., max_length=256)
    description: Optional[str] = None


# Schema for editing a note
class NoteEdit(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None


# Schema for response
class NoteResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int

    class Config:
        orm_mode = True


# Schema for list of notes
class NotesListResponse(BaseModel):
    notes: list[NoteResponse]
