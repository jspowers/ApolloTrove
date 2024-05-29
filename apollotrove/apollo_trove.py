import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

from apollotrove import create_apollo_trove
from apollotrove.extensions import apollo_db


apollo_trove = create_apollo_trove()    
with apollo_trove.app_context():
    apollo_db.create_all()
    apollo_trove.run(debug=True, port=8000)