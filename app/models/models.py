from sqlite3 import Date
from tokenize import String

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import *


class Theme(Base):
    __tablename__ = 'themes'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    questions = relationship("Question", back_populates="theme_relationship")
    recommendations = relationship("Recommendation", back_populates="theme_relationship")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"theme_name={self.name!r}")

    def __repr__(self):
        return str(self)


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int_pk]
    theme: Mapped[str] = mapped_column(ForeignKey("themes.name"), nullable=False)
    question: Mapped[str_uniq]
    answer: Mapped[str]

    theme_relationship = relationship("Theme", back_populates="questions")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"question_theme={self.theme!r},"
                f"question={self.question}")

    def __repr__(self):
        return str(self)


class IPR(Base):
    __tablename__ = 'iprs'

    id: Mapped[int_pk]
    progress: Mapped[int]
    is_approved: Mapped[bool]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"ipr_progress={self.progress!r},"
                f"ipr_status={self.is_approved}")

    def __repr__(self):
        return str(self)


class Test(Base):
    __tablename__ = 'tests'

    id: Mapped[int_pk]
    trainee: Mapped[str_uniq]
    result: Mapped[int]
    recommendations: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"trainee={self.trainee!r},"
                f"result={self.result!r})")

    def __repr__(self):
        return str(self)


class Recommendation(Base):
    __tablename__ = 'recommendations'

    id: Mapped[int_pk]
    theme: Mapped[str] = mapped_column(ForeignKey("themes.name"), nullable=False)
    material: Mapped[str_uniq]

    theme_relationship = relationship("Theme", back_populates="recommendations")

    def __str__(self):
        materials = ', '.join([material.material for material in self.theme_relationship.recommendations])
        return (f"{self.__class__.__name__}(theme={self.theme}, "
                f"materials=[{materials}]")
    
    def __repr__(self):
        return str(self)


class Interview(Base):
    __tablename__ = 'interviews'

    id: Mapped[int_pk]
    interviewer: Mapped[str]
    candidate: Mapped[str]
    date: Mapped[Date]
    position: Mapped[str]
    comment: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"interviewer={self.interviewer!r},"
                f"date={self.date!r}),"
                f"position={self.position!r},"
                f"comment={self.comment!r})")

    def __repr__(self):
        return str(self)


class Chosen_materials(Base):
    __tablename__ = 'chosen_materials'

    id: Mapped[int_pk]
    materials: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"materials={self.materials!r}")

    def __repr__(self):
        return str(self)
