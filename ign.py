import pandas
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.charts import Donut
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from jinja2 import Template



def count_attribute(df, attribute):
	return df.get(attribute).value_counts().sort_index()


def top_10_and_other(series):
	top_10 = series.nlargest(10)
	other = series.nsmallest(series.shape[0] - 10).sum()
	return top_10.append(pandas.Series([other], ['Other']))


ign = pandas.read_csv('ign.csv')


# --- Basic ------------------------------------------------------------------------------------------------------------
def basic():
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

	# genre
	genre = count_attribute(ign, 'genre')
	genre = genre.nlargest(20)
	plot_genre = figure(width=1600, x_range=list(genre.keys().values))
	plot_genre.vbar(x=list(genre.keys().values), width=0.5, bottom=0, top=genre.get_values(), color="#CAB2D6")

	# editors_choice
	editors_choice = count_attribute(ign, 'editors_choice')
	plot_editors_choice = figure(x_range=list(editors_choice.keys().values))
	plot_editors_choice.vbar(x=list(editors_choice.keys().values), width=0.5, bottom=0, top=editors_choice.get_values())

	# release_year
	release_year = count_attribute(ign, 'release_year')
	plot_release_year = figure()
	plot_release_year.vbar(x=list(release_year.keys().values), width=0.5, bottom=0, top=release_year.get_values())

	# release_month
	release_month = count_attribute(ign, 'release_month')
	plot_release_month = figure()
	plot_release_month.vbar(x=list(release_month.keys().values), width=0.5, bottom=0, top=release_month.get_values())

	# release_day
	release_day = count_attribute(ign, 'release_day')
	plot_release_day = figure(width=1200)
	plot_release_day.vbar(x=list(release_day.keys().values), width=0.5, bottom=0, top=release_day.get_values())
	# --- Basic End --------------------------------------------------------------------------------------------------------


# --- 2010 - 2016 ---
def games_2010_2016():
	games = ign[(ign['release_year'] >= 2010) & (ign['release_year'] <= 2016)]
	print(games.shape[0], 'games from 2010 to 2016')

	hover = HoverTool(
		tooltips=[
			("index", "$index"),
			("(x,y)", "($x, $y)"),
		]
	)

	# Platform
	platform = count_attribute(games, 'platform')
	top10 = top_10_and_other(platform)
	print(top10)
	plot_platform = Donut(top10, title='Platform', plot_height=600, plot_width=600,
						  tools=[hover])

	# Genre
	genre = count_attribute(games, 'genre')
	plot_genre = Donut(top_10_and_other(genre), title='Genre', plot_height=600, plot_width=600)

	editors_choice = count_attribute(games, 'editors_choice')
	plot_editors_choice = Donut(editors_choice, title='Editors Choice', plot_height=600, plot_width=600)

	# Best Platform by average scores of games
	average_score_of_platform = games.groupby('platform')['score'].mean().sort_values()
	plot_average_score_of_platform = figure(width=1600, x_range=list(average_score_of_platform.keys().values))
	plot_average_score_of_platform.vbar(x=list(average_score_of_platform.keys().values), width=0.5, bottom=0, top=average_score_of_platform.get_values())

	median_score_of_platform = games.groupby('platform')['score'].median().sort_values()
	plot_median_score_of_platform = figure(width=1600, x_range=list(median_score_of_platform.keys().values))
	plot_median_score_of_platform.vbar(x=list(median_score_of_platform.keys().values), width=0.5, bottom=0,  top=median_score_of_platform.get_values())

	# 10 Genres with Best Games
	# 10 Genres with Worst Games
	average_score_of_genre = games.groupby('genre')['score'].mean().sort_values()
	plot_average_score_of_genre = figure(x_range=list(average_score_of_genre.nlargest(10).keys().values))
	plot_average_score_of_genre.vbar(x=list(average_score_of_genre.nlargest(10).keys().values), width=0.5, bottom=0,
									 top=average_score_of_genre.nlargest(10).get_values())

	plot_worst_genre = figure(x_range=list(average_score_of_genre.nsmallest(10).keys().values))
	plot_worst_genre.vbar(x=list(average_score_of_genre.nsmallest(10).keys().values), width=0.5, bottom=0,
									 top=average_score_of_genre.nsmallest(10).get_values())

	median_score_of_genre = games.groupby('genre')['score'].median().sort_values()
	plot_median_score_of_genre = figure(width=1600, x_range=list(median_score_of_genre.keys().values))
	plot_median_score_of_genre.vbar(x=list(median_score_of_genre.keys().values), width=0.5, bottom=0,  top=median_score_of_genre.get_values())

	# grid = gridplot([
	# 	[plot_platform, plot_genre, plot_editors_choice],
	# 	[plot_average_score_of_platform],
	# 	[plot_median_score_of_platform],
	# 	[plot_average_score_of_genre, plot_worst_genre],
	# 	[plot_median_score_of_genre]
	# ])

	# show(grid)

	sciprt, divs = components({
		'plot_platform': plot_platform,
		'plot_genre': plot_genre,
		'plot_editors_choice': plot_editors_choice
	})
	divs['script'] = sciprt

	with open('template.jinja', 'r') as f:
		template = Template(f.read())
		# html = file_html([plot_platform, plot_genre, plot_editors_choice], CDN, template=template, template_variables )
		html = template.render(divs)
		with open('out.html', mode='w', encoding='utf-8') as f:
			f.write(html)


games_2010_2016()
# --- 2010 - 2016 End ---
