import pandas
print(pandas.__version__)
ign = pandas.read_csv('ign.csv')

release_year = ign.get('release_year')
counts = release_year.value_counts()
counts.sort_index(inplace=True)
print(counts)