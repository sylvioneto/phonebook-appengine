from base64 import decode
from crypt import methods
from flask import Flask, redirect, url_for, render_template, request, redirect, url_for
from contact import Contact
import gcp_firestore
import gcp_redis


# Flask initialization
app = Flask(__name__)


# App Engine warmup feature
@app.route('/_ah/warmup')
def warmup():
    return '', 200


@app.route('/')
def index():
    contacts = gcp_firestore.get_contacts()
    return render_template('list.html', title='Phonebook', contacts=contacts)


@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html', title='New contact')


@app.route('/save', methods=['POST'])
def save():
    contact = Contact(request.form['firstname'], request.form['lastname'],
                      request.form['phonenumber'], request.form['email'])                    
    gcp_firestore.save_contact(contact)
    return redirect(url_for('index'))


@app.route('/contact/<id>')
def contact(id):

    contact=gcp_redis.get_contact(id)

    if not contact:
        # Cache miss
        contact=gcp_firestore.get_contact(id)

        if contact:
            # Cache fill
            gcp_redis.set_contact(contact)

    return render_template('details.html', title='Contact details', contact=contact)

# def accounts(id):
#     tracer = app.config['TRACER']
#     with tracer.start_as_current_span("/accounts/{}".format(id)) as current_span:
#         with tracer.start_as_current_span("gcp_redis.get_account"):
#             account = gcp_redis.get_account(id)

#         # Cache missed
#         if not account:
#             current_span.add_event(name="cache_missed")
#             with tracer.start_as_current_span("gcp_firestore.get_account"):
#                 account = gcp_firestore.get_account(id)

#         if account:
#             with tracer.start_as_current_span("gcp_firestore.set_account"):
#                 gcp_redis.set_account(account)
#             return account, 200
#         else:
#             return 'Account not found', 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
