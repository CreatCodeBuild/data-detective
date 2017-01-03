import pandas
from bokeh.plotting import figure, output_file, show


def count_attribute(df, attribute):
	return df.get(attribute).value_counts().sort_index()


ign = pandas.read_csv('ign.csv')
score_phrase = count_attribute(ign, 'score_phrase')
# platform = count_attribute(ign, 'platform')
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

plot = figure(width=600, height=600, x_range=list(score_phrase.keys().values))
plot.vbar(x=list(score_phrase.keys().values), width=0.5, bottom=0, top=score_phrase.get_values(), color="#CAB2D6")

show(plot)
