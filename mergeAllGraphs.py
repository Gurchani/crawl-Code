import createDatabase
def merge(country, parties, db):
    createDatabase.completeGraph(country, db)
    for i in parties:
        query = 'Insert into '+country+'completeGraph select * from '+i+'Friends'
        print(query)
        db.execute(query)
        db.commit()


#Testing Code
databseLocation = "C:\sqlite\db\\"
desiredReferanceScore = input('What percentage of graph you want:')
country = input('Country Name:')
db = createDatabase.createCountrydb(country, databseLocation)
merge('Pakistan', ['PTI', 'JUIF'], db)