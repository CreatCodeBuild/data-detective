import pandas
from bokeh.charts import Bar, output_file, show


def count_attribute(df, attribute):
	return df.get(attribute).value_counts().sort_index()


ign = pandas.read_csv('ign.csv')
score_phrase = count_attribute(ign, 'score_phrase')
platform = count_attribute(ign, 'platform')
# score = count_attribute(ign, 'score')
# genre = count_attribute(ign, 'genre')
# editors_choice = count_attribute(ign, 'genre')
# release_year = count_attribute(ign, 'release_year')
# release_month = count_attribute(ign, 'release_month')
# release_day = count_attribute(ign, 'release_day')

### Bokeh
# prepare some date

# output to static HTML file
output_file("ign.html")

data = {
    'sample': ['1st', '2nd', '1st', '2nd', '1st', '2nd'],
    'interpreter': ['python', 'python', 'pypy', 'pypy', 'jython', 'jython'],
    'timing': [-2, 5, 12, 40, 22, 30]
}

# create a new plot and add a renderer
left = Bar(data,legend='top_right', plot_width=400)

# create another new plot and add a renderer

# show the results
show(left)
