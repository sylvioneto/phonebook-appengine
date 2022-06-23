from google.cloud import firestore


def save_contact(contact):
    db = firestore.Client()
    doc_ref = db.collection(u'contacts').document()
    doc_ref.set(vars(contact))


def get_contacts(page=None):
    page_limit=50
    page_offset=0
    if page:
        page_offset = page * page_limit

    contacts = []
    db = firestore.Client()
    docs_ref = db.collection(u'contacts')
    doc_query = docs_ref.order_by(u'email').offset(page_offset).limit(page_limit)
    docs = doc_query.stream()

    for doc in docs:
        c = doc.to_dict()
        c["id"] = doc.id
        contacts.append(c)
    return contacts


def get_contact(id):
    db = firestore.Client()
    doc = db.collection(u'contacts').document(id).get()
    if doc.exists:
        contact = doc.to_dict()
        contact["id"] = doc.id
        return contact
    else:
        return None
