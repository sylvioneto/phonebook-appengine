from google.cloud import firestore


def save_contact(contact):
    db = firestore.Client()
    doc_ref = db.collection(u'contacts').document()
    doc_ref.set(vars(contact))


def get_contacts():
    contacts = []
    db = firestore.Client()
    docs_ref = db.collection(u'contacts')
    docs = docs_ref.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
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
