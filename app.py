from flask import Flask
from flask import render_template, request
from socitey_data import get_all_notices, get_all_legal_matters, get_all_documents
from socitey_data import get_society_fund, get_maintenance_fund, get_current_statement, get_monthly_totals

from datetime import datetime
from math import ceil
import os
import time

from aws_s3 import refresh_s3_link, double_render
from jinja2 import Template





app = Flask(__name__)

APP_START_TIME = time.time()
FIRST_RUN = True
ITEMS_PER_PAGE = 6


def paginate_data(data, page=1, per_page=ITEMS_PER_PAGE):
    """Helper function to paginate data"""
    total_items = len(data)
    total_pages = ceil(total_items / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_data = data[start_idx:end_idx]

    return {
        'items': paginated_data,
        'total_pages': total_pages,
        'current_page': page,
        'total_items': total_items
    }


def filter_data_by_category(data, category):
    """Helper function to filter data by category"""
    if category and category.lower() != 'all':
        return [item for item in data if item['category'].lower() == category.lower()]
    return data


def filter_legal_by_status(data, status):
    """Helper function to filter legal matters by status"""
    if status and status.lower() != 'all':
        return [item for item in data if item['status'].lower() == status.lower()]
    return data


@app.route('/')
def home():

    # Get data from data source
    notices = get_all_notices()
    legal_cases = get_all_legal_matters()
    society_documents = get_all_documents()
    society_fund = get_society_fund()
    maintenance_fund = get_maintenance_fund()
    current_statement = get_current_statement()
    monthly_totals = get_monthly_totals()

    # Get pagination and filtering parameters
    notice_page = int(request.args.get('notice_page', 1))
    legal_page = int(request.args.get('legal_page', 1))
    doc_page = int(request.args.get('doc_page', 1))
    notice_category = request.args.get('notice_category', 'all')
    legal_status = request.args.get('legal_status', 'all')

    # Filter data by category
    filtered_notices = filter_data_by_category(notices, notice_category)
    filtered_legal = filter_legal_by_status(legal_cases, legal_status)

    # Paginate filtered data
    notices_paginated = paginate_data(filtered_notices, notice_page)
    legal_paginated = paginate_data(filtered_legal, legal_page)
    docs_paginated = paginate_data(society_documents, doc_page)

    # Pass all data to template
    return render_template('index.html',
                           notices=notices_paginated['items'],
                           notices_pagination=notices_paginated,
                           notice_category=notice_category,
                           legal_matters=legal_paginated['items'],
                           legal_pagination=legal_paginated,
                           legal_status=legal_status,
                           society_documents=docs_paginated['items'],
                           docs_pagination=docs_paginated,
                           society_fund=society_fund,
                           maintenance_fund=maintenance_fund,
                           current_statement=current_statement,
                           monthly_totals=monthly_totals,
                           current_month_year=datetime.now().strftime('%B %Y'),
                           year=datetime.now().year)


@app.route('/notice/<int:notice_id>')
def notice_detail(notice_id):
    notices = get_all_notices()
    notice = next((notice for notice in notices if notice['notice_id'] == notice_id), None)
    if notice:
        return render_template('notice_detail.html', notice=notice,
                               year=datetime.now().year)
    return 'Notice not found', 404


@app.route('/legal/<int:legal_id>')
def legal_detail(legal_id):
    legal_cases = get_all_legal_matters()
    case = next((case for case in legal_cases if case['legal_id'] == legal_id), None)

    case['full_notice_u'] = refresh_s3_link(case['full_notice_u'])
    case['full_notice_e'] = refresh_s3_link(case['full_notice_e'])

    if case:
        return render_template('legal_detail.html', case=case,
                               year=datetime.now().year)
    return 'Legal case not found', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)