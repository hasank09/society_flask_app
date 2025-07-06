# models.py
from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from db_config import Base


class Notice(Base):
    __tablename__ = "notices"

    notice_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    posted_by = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    full_notice_e = Column(Text, nullable=False)
    full_notice_u = Column(Text, nullable=False)


class LegalMatter(Base):
    __tablename__ = "legal_matters"

    legal_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    case_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    filing_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    suit_money = Column(Float, nullable=False)
    full_notice_e = Column(Text, nullable=False)
    full_notice_u = Column(Text, nullable=False)


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date_added = Column(Date, nullable=False)
    file_url = Column(String(255), nullable=False)


class SocietyFund(Base):
    __tablename__ = "society_fund"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    credit = Column(Float, nullable=False)
    debit = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)


class MaintenanceFund(Base):
    __tablename__ = "maintenance_fund"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Date, nullable=False)
    collection = Column(Float, nullable=False)
    expense = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)


class CurrentStatement(Base):
    __tablename__ = "current_statement"

    id = Column(Integer, primary_key=True, index=True)
    particulars = Column(String(255), nullable=False)
    income = Column(Float, nullable=False)
    expense = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)