import pandas
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot


def count_attribute(df, attribute):
	return df.get(attribute).value_counts().sort_index()


ign = pandas.read_csv('ign.csv')

# score_phrase
score_phrase = count_attribute(ign, 'score_phrase')
index = ['Masterpiece', 'Amazing', 'Great', 'Good', 'Okay', 'Bad', 'Awful', 'Painful', 'Unbearable', 'Disaster']
score_phrase = score_phrase.reindex(index)
plot_score_phrase = figure(width=800, x_range=list(score_phrase.keys().values))
plot_score_phrase.vbar(x=list(score_phrase.keys().values), width=0.5, bottom=0, top=score_phrase.get_values(), color="#CAB2D6")

# platform
platform = count_attribute(ign, 'platform')
platform = platform.nlargest(10)
plot_platform = figure(width=800, x_range=list(platform.keys().values))
plot_platform.vbar(x=list(platform.keys().values), width=0.5, bottom=0, top=platform.get_values(), color="#CAB2D6")

# score
score = count_attribute(ign, 'score')
plot_score = figure()
plot_score.vbar(x=list(score.keys().values), width=0.5, bottom=0, top=score.get_values(), color="#CAB2D6")

# genre = count_attribute(ign, 'genre')

# editors_choice = count_attribute(ign, 'genre')

# release_year = count_attribute(ign, 'release_year')

# release_month = count_attribute(ign, 'release_month')

# release_day = count_attribute(ign, 'release_day')


# output to static HTML file
output_file("ign.html")
grid = gridplot([
	[plot_score],
	[plot_platform,plot_score_phrase]
])
show(grid)
