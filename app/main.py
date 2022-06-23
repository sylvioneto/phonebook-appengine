from base64 import decode
from crypt import methods
from flask import Flask, redirect, url_for, render_template, request, redirect, url_for
from contact import Contact
import gcp_firestore
import gcp_redis
import gcp_devops


# Flask initialization
app = Flask(__name__)


# GCP DevOps Flask initialization
gcp_devops.initialize_profiler()
app.config['TRACER'] = gcp_devops.initialize_tracer()


# App Engine warmup feature
@app.route('/_ah/warmup')
def warmup():
    return '', 200


@app.route('/')
def index():
    contacts = gcp_firestore.get_contacts()
    return render_template('list.html', title='Phonebook', contacts=contacts, next_page=1)


@app.route('/<page>')
def page(page):
    page = int(page)
    next_page=page+1
    previous_page=page-1
    if page == 0:
        next_page = 1
        previous_page = 0
    contacts = gcp_firestore.get_contacts(page)
    return render_template('list.html', title='Phonebook', contacts=contacts, next_page=next_page, previous_page=previous_page)


@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html', title='New contact')


@app.route('/save', methods=['POST'])
def save():
    contact = Contact(request.form['first_name'], request.form['last_name'],
                      request.form['phone_number'], request.form['email'], request.form['country_code'])                    
    gcp_firestore.save_contact(contact)
    return redirect(url_for('index'))


@app.route('/api/save', methods=['POST'])
def api_save():
    content = request.json
    contact = Contact(content['first_name'], content['last_name'],
                      content['phone_number'], content['email'], content['country_code'])                    
    gcp_firestore.save_contact(contact)
    return '', 200


# This method has instrumentation for Cloud Trace in order to evaluate requests served from Firestore vs Redis
@app.route('/contact/<id>')
def contact(id):
    tracer = app.config['TRACER']
    with tracer.start_as_current_span("/contact/{}".format(id)) as current_span:

        with tracer.start_as_current_span("gcp_redis.get_contact"):
            contact=gcp_redis.get_contact(id)
            
        if not contact:
            # Cache miss
            with tracer.start_as_current_span("gcp_firestore.get_contact"):
                contact=gcp_firestore.get_contact(id)
                if contact:
                    # Cache fill
                    gcp_redis.set_contact(contact)

    return render_template('details.html', title='Contact details', contact=contact)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
