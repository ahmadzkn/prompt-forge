import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

class PromptSession(Base):
    __tablename__ = 'prompt_sessions'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    topic_group = Column(String(255))
    raw_prompt = Column(Text)
    # Storing JSON as Text for broad compatibility
    structured_elements_json = Column(Text) 
    final_prompt = Column(Text)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "topic_group": self.topic_group,
            "raw_prompt": self.raw_prompt,
            "structured_elements": json.loads(self.structured_elements_json) if self.structured_elements_json else {},
            "final_prompt": self.final_prompt
        }

class DatabaseManager:
    def __init__(self, db_path: str = "prompt_forge.db"):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def add_session(self, raw_prompt: str, structured_elements: Dict, final_prompt: str, topic_group: str = "General") -> PromptSession:
        session = self.Session()
        try:
            new_entry = PromptSession(
                raw_prompt=raw_prompt,
                structured_elements_json=json.dumps(structured_elements),
                final_prompt=final_prompt,
                topic_group=topic_group,
                timestamp=datetime.now()
            )
            session.add(new_entry)
            session.commit()
            session.refresh(new_entry)
            return new_entry
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_history(self, limit: int = 50) -> List[PromptSession]:
        session = self.Session()
        try:
            return session.query(PromptSession).order_by(PromptSession.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def get_session(self, session_id: int) -> Optional[PromptSession]:
        session = self.Session()
        try:
            return session.query(PromptSession).get(session_id)
        finally:
            session.close()

    def close(self):
        self.Session.remove()
