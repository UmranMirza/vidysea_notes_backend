from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from application.models.notes import Note

class NoteService:
    def create_note(self, db: Session, title: str, description: str, owner_id: int):
        note = Note(title=title, description=description, owner_id=owner_id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def get_notes_by_owner(self, db: Session, owner_id: int):
        return db.query(Note).filter(Note.owner_id == owner_id).all()

    def get_all_notes(self, db: Session):
        return db.query(Note).all()

    def get_note_by_id(self, db: Session, note_id: int):
        return db.query(Note).filter(Note.id == note_id).first()

    def edit_note(self, db: Session, note_id: int, title: str, description: str):
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            note.title = title
            note.description = description
            db.commit()
            db.refresh(note)
        return note

    def soft_delete_note(self, db: Session, note_id: int):
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            note.deleted_at = func.now()
            db.commit()
        return None

    def list_notes(self, db, sort_by='id', search_key=''):
        query = db.query(Note).filter(Note.deleted_at.is_(None))
        if search_key:
            query = query.filter(Note.title.ilike(f"%{search_key}%"))
        total = query.count()
        # Sorting logic
        if sort_by == "newest":
            query = query.order_by(desc(Note.created_at))
        elif sort_by == "oldest":
            query = query.order_by(asc(Note.created_at))
        else:
            sort_column = getattr(Note, sort_by.lstrip('-'), None)
            if sort_column is not None:
                if sort_by.startswith('-'):
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
        notes = query.all()
        return notes, total

    def list_notes_by_owner(self, db, owner_id, sort_by='id', search_key=''):
        query = db.query(Note).filter(Note.owner_id == owner_id, Note.deleted_at.is_(None))
        if search_key:
            query = query.filter(Note.title.ilike(f"%{search_key}%"))
        total = query.count()
        # Sorting logic
        if sort_by == "newest":
            query = query.order_by(desc(Note.created_at))
        elif sort_by == "oldest":
            query = query.order_by(asc(Note.created_at))
        else:
            sort_column = getattr(Note, sort_by.lstrip('-'), None)
            if sort_column is not None:
                if sort_by.startswith('-'):
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
        notes = query.all()
        return notes, total
