from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, Column, Date, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, REAL, String, Table, Text, Uuid, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Dialogs(Base):
    __tablename__ = 'dialogs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dialogs_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    caption: Mapped[str] = mapped_column(String(128), nullable=False)
    frequency_penalty: Mapped[float] = mapped_column(REAL, nullable=False)

    users: Mapped[list['Users']] = relationship('Users', secondary='users_dialogs', back_populates='dialogs')
    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='dialog')


class Models(Base):
    __tablename__ = 'models'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='models_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[str] = mapped_column(String(32), nullable=False)

    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='model')


class ParticipantNames(Base):
    __tablename__ = 'participant_names'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='participant_names_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='name')


class ParticipantRoles(Base):
    __tablename__ = 'participant_roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='participant_roles_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[str] = mapped_column(String(128), nullable=False, server_default=text('USER'))

    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String(24), nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    deletion_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    dialogs: Mapped[list['Dialogs']] = relationship('Dialogs', secondary='users_dialogs', back_populates='users')


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = (
        ForeignKeyConstraint(['dialog_id'], ['dialogs.id'], ondelete='CASCADE', onupdate='CASCADE', name='messages_dialog_id_fkey'),
        ForeignKeyConstraint(['model_id'], ['models.id'], ondelete='SET NULL', onupdate='CASCADE', name='messages_model_id_fkey'),
        ForeignKeyConstraint(['name_id'], ['participant_names.id'], ondelete='SET NULL', onupdate='CASCADE', name='messages_name_id_fkey'),
        ForeignKeyConstraint(['role_id'], ['participant_roles.id'], ondelete='SET NULL', onupdate='CASCADE', name='messages_role_id_fkey'),
        PrimaryKeyConstraint('id', name='messages_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=2), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    dialog_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False)
    role_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    dialog: Mapped['Dialogs'] = relationship('Dialogs', back_populates='messages')
    model: Mapped['Models'] = relationship('Models', back_populates='messages')
    name: Mapped[Optional['ParticipantNames']] = relationship('ParticipantNames', back_populates='messages')
    role: Mapped[Optional['ParticipantRoles']] = relationship('ParticipantRoles', back_populates='messages')


t_users_dialogs = Table(
    'users_dialogs', Base.metadata,
    Column('users_id', Uuid, nullable=False),
    Column('dialogs_id', Uuid, nullable=False),
    ForeignKeyConstraint(['dialogs_id'], ['dialogs.id'], name='users_dialogs_dialogs_id_fkey'),
    ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='users_dialogs_users_id_fkey')
)
