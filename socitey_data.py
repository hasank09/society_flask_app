# socitey_data.py
from sqlalchemy.orm import Session
from db_config import engine
from models import Notice, LegalMatter, Document, SocietyFund, MaintenanceFund, CurrentStatement
from datetime import datetime
from aws_s3 import refresh_s3_link
import re
import pandas as pd

def get_text_dir(text):
    check = re.findall(r'[a-zA-Z]', text)

    # print(len(text), len(check))
    if check:
        if len(check) >= len(text) /2 :
            return "ltr"
        else:
            return "rtl"
    else:
        return "rtl"

def clean_html_tags(text):
    tags = ['<p>', '</p>', '<br>', '<strong>', '</strong>', '<em>', '</em>', '<ul>', '</ul>', '<li>', '</li>',
            '<h1>', '</h1>', '<h2>', '</h2>', '<h3>', '</h3>', '<h4>', '</h4>', '<h5>', '</h5>', '<h6>', '</h6>']
    for tag in tags:
        text = text.replace(tag, '')
    return text


def get_all_notices():
    with Session(engine) as session:
        notices = session.query(Notice).all()

        notices_list = []
        for notice in notices:
            level = {'urgent': 'danger', 'event': 'success', 'maintenance': 'warning', 'general': 'info'}

            notice_dict = {
                'notice_id': notice.notice_id,
                'title': notice.title,
                'description': notice.description,
                'date': notice.date,
                'date2': notice.date.strftime('%b %d, %Y'),
                'posted_by': notice.posted_by,
                'category': notice.category.lower(),
                'level': level.get(notice.category.lower(), 'info'),
                'full_notice_u': notice.full_notice_u,
                'full_notice_e': notice.full_notice_e,
                'content':  clean_html_tags(notice.full_notice_u[:200]) + '...'
            }

            # pre-rendering Urdu Version
            notice_dict['full_notice_u'] = refresh_s3_link(notice_dict['full_notice_u'])

            # pre-rendering English Version
            notice_dict['full_notice_e'] = refresh_s3_link(notice_dict['full_notice_e'])

            # add text direction
            notice_dict['title_dir'] = get_text_dir(notice_dict['title'])
            notice_dict['description_dir'] = get_text_dir(notice_dict['description'])

            notices_list.append(notice_dict)

        # Sort by date descending
        notices_list.sort(key=lambda x: x['date'], reverse=True)
        return notices_list


def get_all_legal_matters():
    with Session(engine) as session:
        legal_matters = session.query(LegalMatter).all()

        legal_list = []
        for legal in legal_matters:
            priority = {'urgent': 'danger', 'resolved': 'success', 'pending': 'warning', 'in-progress': 'info'}

            legal_dict = {
                'legal_id': legal.legal_id,
                'case_id': legal.case_id,
                'title': legal.title,
                'case_type': legal.case_type,
                'status': legal.status.lower(),
                'filing_date': legal.filing_date,
                'date2': legal.filing_date.strftime('%b %d, %Y'),
                'priority': priority.get(legal.status.lower(), 'info'),
                'description': legal.description,
                'full_notice_u': legal.full_notice_u,
                'full_notice_e': legal.full_notice_e,
                'suit_money': legal.suit_money,
                'suit_money_2': '{:,.2f}'.format(legal.suit_money)
            }

            # pre-rendering Urdu Version
            legal_dict['full_notice_u'] = refresh_s3_link(legal_dict['full_notice_u'])

            # pre-rendering English Version
            legal_dict['full_notice_e'] = refresh_s3_link(legal_dict['full_notice_e'])

            # add text direction
            legal_dict['description_dir'] = get_text_dir(legal_dict['description'])
            legal_dict['title_dir'] = get_text_dir(legal_dict['title'])

            legal_list.append(legal_dict)

        # Sort by date descending
        legal_list.sort(key=lambda x: x['filing_date'], reverse=True)
        return legal_list


def get_all_documents():
    with Session(engine) as session:
        documents = session.query(Document).all()

        doc_list = []
        for doc in documents:
            doc_dict = {
                'document_id': doc.document_id,
                'title': doc.title,
                'date_added': doc.date_added,
                'date2': doc.date_added.strftime('%b %d, %Y'),
                'file_url': doc.file_url
            }
            if 'get_s3url' in doc_dict['file_url']:
                doc_dict['file_url'] = refresh_s3_link(doc_dict['file_url'])
            doc_list.append(doc_dict)

        # Sort by date descending
        doc_list.sort(key=lambda x: x['date_added'], reverse=True)
        return doc_list


def get_society_fund():
    with Session(engine) as session:
        funds = session.query(SocietyFund).all()

        fund_list = []
        for fund in funds:
            fund_dict = {
                'description': fund.description,
                'credit': fund.credit,
                'debit': fund.debit,
                'balance': fund.balance
            }
            fund_list.append(fund_dict)

        # Add the total row
        total_credit = sum(fund.credit for fund in funds)
        total_debit = sum(fund.debit for fund in funds)
        total_balance = sum(fund.balance for fund in funds)

        fund_list.append({
            'description': 'Total',
            'credit': total_credit,
            'debit': total_debit,
            'balance': total_balance
        })

        return fund_list


def get_maintenance_fund():
    with Session(engine) as session:
        maintenance = session.query(MaintenanceFund).all()

        maintenance_list = []
        for item in maintenance:
            maint_dict = {
                'month': item.month,
                'month2': item.month.strftime('%b-%Y'),
                'collection': item.collection,
                'expense': item.expense,
                'balance': item.balance
            }
            maintenance_list.append(maint_dict)

        # Sort by month ascending
        maintenance_list.sort(key=lambda x: x['month'])
        return maintenance_list


def get_current_statement():
    with Session(engine) as session:
        statements = session.query(CurrentStatement).all()

        statement_list = []
        for statement in statements:
            statement_dict = {
                'particulars': statement.particulars,
                'income': statement.income,
                'expense': statement.expense,
                'balance': statement.balance
            }
            statement_list.append(statement_dict)

        return statement_list


def get_monthly_totals():
    with Session(engine) as session:
        statements = session.query(CurrentStatement).all()

        total_income = sum(statement.income for statement in statements)
        total_expense = sum(statement.expense for statement in statements)

        monthly_totals = {
            'income': total_income,
            'expense': total_expense,
            'balance': total_income - total_expense
        }

        return monthly_totals


if __name__ == '__main__':
    # all_data = get_current_statement()
    all_data = get_all_notices()
    # all_data = get_all_legal_matters()
    # all_data = get_all_documents()
    # all_data = get_maintenance_fund()

    for data in all_data:
    #     print(data['legal_id'],data['full_notice_e'])
    #     print(data['file_url'])
        print(data)
    df_data = pd.DataFrame(all_data)
    print(df_data)
    df_data.to_csv('notices.csv',index=False)
    # text1 = "المسلم کوآپریٹو ہاؤسنگ سوسائٹی کی نئی کمیٹی کی منظور شدہ قرارداد کا خلاصہ"
    # text2 =  "Housing Society Files Application for Probe into Ex-Management's Alleged Corruption"
    # test = get_text_dir(text1)
    #
    # print(test)

