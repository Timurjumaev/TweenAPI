from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, Integer, Numeric, and_, Date
from models.stages import Stages
from models.workers import Workers
from models.works import Works


class StageWorks(Base):
    __tablename__ = 'stage_works'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(Integer, nullable=False)
    stage_id = Column(Integer, nullable=False)
    worker_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    bonus = Column(Numeric, nullable=True)
    date = Column(Date, default=datetime.today(), nullable=False)

    work = relationship('Works', foreign_keys=[work_id],
                        primaryjoin=lambda: and_(Works.id == StageWorks.work_id))

    stage = relationship('Stages', foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == StageWorks.stage_id))

    worker = relationship('Workers', foreign_keys=[worker_id],
                          primaryjoin=lambda: and_(Workers.id == StageWorks.worker_id))

