from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from application import activeSession
from application.routes.auth_decorators import admin_login_required, user_login_required
from application.utilities.res import APIError, APIResponse
from application.utilities.serialization import serialize
from application.services.notes_service import NoteService
from application.schemas.note_schema import NoteCreate, NoteEdit
import math

note_service = NoteService()
notes_router = APIRouter()


@notes_router.post("/create")
@user_login_required
def create_note(request: Request, data: NoteCreate, db: Session = activeSession):
    user_id = request.state.user_id
    note = note_service.create_note(
        db=db, title=data.title, description=data.description, owner_id=user_id
    )
    if not note:
        return APIError(
            message="Unable to create note",
            data={},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        ).to_json()

    note_serialized = {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "owner_id": note.owner_id,
    }
    return APIResponse(
        message="Note created", data=serialize({"note": note_serialized})
    ).to_json()


@notes_router.get("/")
@user_login_required
def get_user_notes(request: Request, db: Session = activeSession):
    user_id = request.state.user_id
    role = request.state.role

    # Pagination and search params
    sort_by = request.query_params.get('sort_by', 'newest')
    search_key = request.query_params.get('q', '')

    if role == "admin":
        notes, total = note_service.list_notes(db=db, sort_by=sort_by, search_key=search_key)
    else:
        notes, total = note_service.list_notes_by_owner(db=db, owner_id=user_id,sort_by=sort_by, search_key=search_key)

    notes_list = [
        {
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "owner_id": note.owner_id,
            "created_at": note.created_at,
            "updated_at": note.updated_at
        }
        for note in notes
    ]
    return APIResponse(
        message="Notes list",
        data=serialize({
            "notes": notes_list,
            "total": total
        })
    ).to_json()


@notes_router.put("/edit/{note_id}")
@user_login_required
def edit_note(request: Request, note_id: int, data: NoteEdit, db: Session = activeSession):
    user_id = request.state.user_id
    role = request.state.role

    note = note_service.get_note_by_id(db=db, note_id=note_id)
    if not note:
        return APIError(message="Note not found", data={}, status=404).to_json()

    # Role-based validation
    if note.owner_id != user_id and role != "admin":
        return APIError(message="Unauthorized", data={}, status=403).to_json()

    note = note_service.edit_note(
        db=db, note_id=note_id, title=data.title, description=data.description
    )

    note_serialized = {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "owner_id": note.owner_id,
    }
    return APIResponse(message="Note updated", data=serialize({"note": note_serialized})).to_json()


@notes_router.delete("/delete/{note_id}")
@user_login_required
def delete_note(request: Request, note_id: int, db: Session = activeSession):
    user_id = request.state.user_id
    role = request.state.role

    note = note_service.get_note_by_id(db=db, note_id=note_id)
    if not note:
        return APIError(message="Note not found", data={}, status=404).to_json()

    # Role-based validation
    if note.owner_id != user_id and role != "admin":
        return APIError(message="Unauthorized", data={}, status=403).to_json()

    note_service.soft_delete_note(db=db, note_id=note_id)
    return APIResponse(
        message="Note deleted", data=serialize({"note_id": note_id})
    ).to_json()

@notes_router.get("/all")
@admin_login_required
def get_all_notes(request: Request, db: Session = activeSession):
    # Pagination and search params
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 10))
    sort_by = request.query_params.get('sort_by', 'newest')
    search_key = request.query_params.get('q', '')

    notes, total = note_service.list_notes(db=db, sort_by=sort_by, search_key=search_key)

    notes_list = []
    for note in notes :
        my_note =False
        if note.owner_id == request.state.user_id:
            my_note = True
        list_data={
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "owner_id": note.owner_id,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "my_note": my_note
            
        }
        notes_list.append(list_data)
       
    pages_count = math.ceil(total / limit) if total else 1
    return APIResponse(
        message="All notes",
        data=serialize({
            "notes": notes_list,
            "total": total,
            "page_size": limit,
            "has_next": page < pages_count,
            "has_prev": page > 1,
            "per_page": limit,
            "pages": pages_count
        })
    ).to_json()



@notes_router.post("/admin/create")
@admin_login_required
def admin_create_note(request: Request, data: NoteCreate, db: Session = activeSession):
    """
    Admin can create note for any user.
    """
    owner_id =  request.state.user_id # Admin must pass owner_id in request
    note = note_service.create_note(db=db, title=data.title, description=data.description, owner_id=owner_id)
    
    if not note:
        return APIError(
            message="Unable to create note", data={}, status=status.HTTP_406_NOT_ACCEPTABLE
        ).to_json()
    
    note_serialized = {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "owner_id": note.owner_id,
    }
    return APIResponse(
        message="Note created by admin", data=serialize({"note": note_serialized})
    ).to_json()

@notes_router.put("/admin/edit/{note_id}")
@admin_login_required
def admin_edit_note(request: Request, note_id: int, data: NoteEdit, db: Session = activeSession):
    """
    Admin can edit any user's note.
    """
    note = note_service.get_note_by_id(db=db, note_id=note_id)
    if not note:
        return APIError(
            message="Note not found", data={}, status=status.HTTP_404_NOT_FOUND
        ).to_json()
    
    note = note_service.edit_note(db=db, note_id=note_id, title=data.title, description=data.description)
    
    note_serialized = {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "owner_id": note.owner_id,
    }
    return APIResponse(
        message="Note updated by admin", data=serialize({"note": note_serialized})
    ).to_json()


@notes_router.delete("/admin/delete/{note_id}")
@admin_login_required
def admin_delete_any_note(request: Request, note_id: int, db: Session = activeSession):
    note = note_service.get_note_by_id(db=db, note_id=note_id)
    if not note:
        return APIError(message="Note not found", data={}, status=404).to_json()

    note_service.soft_delete_note(db=db, note_id=note_id)
    return APIResponse(message="Admin deleted note", data={"id": note_id}).to_json()
