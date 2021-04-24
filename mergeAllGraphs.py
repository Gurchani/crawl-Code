import createDatabase
def merge(country, parties, db):
    createDatabase.completeGraph(country, db)
    for i in parties:
        query = 'Insert into '+country+'completeGraph (select * from '+i+'Friends )'
        db.execute(query)
