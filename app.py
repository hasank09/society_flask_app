from flask import Flask
from flask import render_template, request
from socitey_data import get_all_notices, get_all_legal_matters, get_all_documents
from socitey_data import get_society_fund, get_maintenance_fund, get_current_statement, get_monthly_totals

from datetime import datetime
from math import ceil




# notices = get_all_notices()
# legal_cases= get_all_legal_matters()
# society_documents = get_all_documents()
# society_fund = get_society_fund()
# maintenance_fund = get_maintenance_fund()
# current_statement = get_current_statement()
# monthly_totals = get_monthly_totals()


app = Flask(__name__)

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

    # Get pagination parameters (default to page 1)
    notice_page = int(request.args.get('notice_page', 1))
    legal_page = int(request.args.get('legal_page', 1))
    doc_page = int(request.args.get('doc_page', 1))

    # Paginate data
    notices_paginated = paginate_data(notices, notice_page)
    legal_paginated = paginate_data(legal_cases, legal_page)
    docs_paginated = paginate_data(society_documents, doc_page)

    # Pass all data to template
    return render_template('index.html',
                           notices=notices_paginated['items'],
                           notices_pagination=notices_paginated,
                           legal_matters=legal_paginated['items'],
                           legal_pagination=legal_paginated,
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
    if case:
        return render_template('legal_detail.html', case=case,
                              year=datetime.now().year)
    return 'Legal case not found', 404


if __name__ == '__main__':
    app.run()
