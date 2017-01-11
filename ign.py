import pandas
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.charts import Donut, Histogram
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.models.sources import ColumnDataSource
from bokeh.embed import file_html, components
from jinja2 import Template


def count_attribute(df, attribute):
	return df.get(attribute).value_counts().sort_index()


def top_n_and_other(n, series):
	top_n = series.nlargest(n)
	other = series.nsmallest(series.shape[0] - n).sum()
	return top_n.append(pandas.Series([other], ['Other']))


def bottom_n_and_other(n, series):
	bottom_n = series.nsmallest(n)
	other = series.nlargest(series.shape[0] - n).sum()
	return bottom_n.append(pandas.Series([other], ['Other']))


def hovertool():
	return HoverTool(tooltips=[("index", "$index"), ("value", "@top")])


ign = pandas.read_csv('ign.csv')


# --- Basic ------------------------------------------------------------------------------------------------------------
total_num_games = ign.shape[0]

# score_phrase
total_score_phrase = count_attribute(ign, 'score_phrase')
index = ['Masterpiece', 'Amazing', 'Great', 'Good', 'Okay', 'Bad', 'Awful', 'Painful', 'Unbearable', 'Disaster']
index.reverse()
total_score_phrase = total_score_phrase.reindex(index)
hover_total_score_phrase = hovertool()
plot_total_score_phrase = figure(x_range=list(total_score_phrase.keys().values), tools=[hover_total_score_phrase], title='评价')
plot_total_score_phrase.vbar(x=list(total_score_phrase.keys().values), width=0.5, bottom=0, top=total_score_phrase.get_values())

# score, distribution
plot_total_score = Histogram(ign['score'], bins=100, title="评分分布")

grid_total_score_and_phrase = gridplot([
	[plot_total_score_phrase, plot_total_score]
])

# platform
total_platform = count_attribute(ign, 'platform')
total_num_platform = total_platform.shape[0]

total_top_15_platform = top_n_and_other(15, total_platform)
plot_total_top_15_platform = figure(width=1800, x_range=list(total_top_15_platform.keys().values), title='游戏最多的15个平台')
plot_total_top_15_platform.vbar(x=list(total_top_15_platform.keys().values), width=0.5, bottom=0, top=total_top_15_platform.get_values())

total_bottom_15_platform = total_platform.nsmallest(15)
plot_total_bottom_15_platform = figure(width=1800, x_range=list(total_bottom_15_platform.keys().values), title='游戏最少的15个平台')
plot_total_bottom_15_platform.vbar(x=list(total_bottom_15_platform.keys().values), width=0.5, bottom=0, top=total_bottom_15_platform.get_values())

# # genre
# genre = count_attribute(ign, 'genre')
# genre = genre.nlargest(20)
# plot_genre = figure(width=1600, x_range=list(genre.keys().values))
# plot_genre.vbar(x=list(genre.keys().values), width=0.5, bottom=0, top=genre.get_values(), color="#CAB2D6")
#
# # editors_choice
# editors_choice = count_attribute(ign, 'editors_choice')
# plot_editors_choice = figure(x_range=list(editors_choice.keys().values))
# plot_editors_choice.vbar(x=list(editors_choice.keys().values), width=0.5, bottom=0, top=editors_choice.get_values())
#
# # release_year
# release_year = count_attribute(ign, 'release_year')
# plot_release_year = figure()
# plot_release_year.vbar(x=list(release_year.keys().values), width=0.5, bottom=0, top=release_year.get_values())
#
# # release_month
# release_month = count_attribute(ign, 'release_month')
# plot_release_month = figure()
# plot_release_month.vbar(x=list(release_month.keys().values), width=0.5, bottom=0, top=release_month.get_values())
#
# # release_day
# release_day = count_attribute(ign, 'release_day')
# plot_release_day = figure(width=1200)
# plot_release_day.vbar(x=list(release_day.keys().values), width=0.5, bottom=0, top=release_day.get_values())
# --- Basic End --------------------------------------------------------------------------------------------------------



# --- 2010 - 2016 ---
# games = ign[(ign['release_year'] >= 2015) & (ign['release_year'] <= 2016)]
# print(games.shape[0], 'games from 2010 to 2016')
#
#
# hover2 = hovertool()
#
# # Platform
# platform = count_attribute(games, 'platform')
# top10 = top_10_and_other(platform)
# plot_platform = figure(width=900, x_range=list(top10.keys().values), tools=[hover1], title='TOP 10 游戏平台')
# plot_platform.vbar(x=list(top10.keys().values), width=0.5, bottom=0, top=top10.get_values())
#
# # Genre
# genre = count_attribute(games, 'genre')
# top10_genre = top_10_and_other(genre)
# plot_genre = figure(width=900, x_range=list(top10_genre.keys().values), tools=[hover2], title='TOP 10 游戏类型')
# plot_genre.vbar(x=list(top10_genre.keys().values), width=0.5, bottom=0, top=top10_genre.get_values())
#
# editors_choice = count_attribute(games, 'editors_choice')
# plot_editors_choice = Donut(editors_choice, title='Editors Choice', plot_height=600, plot_width=600)
#
# # Best Platform by average scores of games
# average_score_of_platform = games.groupby('platform')['score'].mean().sort_values()
# plot_average_score_of_platform = figure(width=1600, x_range=list(average_score_of_platform.keys().values))
# plot_average_score_of_platform.vbar(x=list(average_score_of_platform.keys().values), width=0.5, bottom=0, top=average_score_of_platform.get_values())
#
# median_score_of_platform = games.groupby('platform')['score'].median().sort_values()
# plot_median_score_of_platform = figure(width=1600, x_range=list(median_score_of_platform.keys().values))
# plot_median_score_of_platform.vbar(x=list(median_score_of_platform.keys().values), width=0.5, bottom=0,  top=median_score_of_platform.get_values())
#
# # 10 Genres with Best Games
# # 10 Genres with Worst Games
# average_score_of_genre = games.groupby('genre')['score'].mean().sort_values()
# plot_average_score_of_genre = figure(x_range=list(average_score_of_genre.nlargest(10).keys().values))
# plot_average_score_of_genre.vbar(x=list(average_score_of_genre.nlargest(10).keys().values), width=0.5, bottom=0,
# 								 top=average_score_of_genre.nlargest(10).get_values())
#
# plot_worst_genre = figure(x_range=list(average_score_of_genre.nsmallest(10).keys().values))
# plot_worst_genre.vbar(x=list(average_score_of_genre.nsmallest(10).keys().values), width=0.5, bottom=0,
# 								 top=average_score_of_genre.nsmallest(10).get_values())
#
# median_score_of_genre = games.groupby('genre')['score'].median().sort_values()
# plot_median_score_of_genre = figure(width=1600, x_range=list(median_score_of_genre.keys().values))
# plot_median_score_of_genre.vbar(x=list(median_score_of_genre.keys().values), width=0.5, bottom=0,  top=median_score_of_genre.get_values())
#
# # grid = gridplot([
# # 	[plot_platform, plot_genre, plot_editors_choice],
# # 	[plot_average_score_of_platform],
# # 	[plot_median_score_of_platform],
# # 	[plot_average_score_of_genre, plot_worst_genre],
# # 	[plot_median_score_of_genre]
# # ])


# --- 2010 - 2016 End ---

script, divs = components({
	'grid_total_score_and_phrase': grid_total_score_and_phrase,
	'total_top_15_platform': plot_total_top_15_platform,
	'total_bottom_15_platform': plot_total_bottom_15_platform
	# 'plot_platform': plot_platform,
	# 'plot_genre': plot_genre,
	# 'plot_editors_choice': plot_editors_choice
})
divs['script'] = script
divs['total_num_games'] = total_num_games
divs['total_num_platform'] = total_num_platform

with open('template.jinja', 'r', encoding='utf8') as f:
	template = Template(f.read())
	html = template.render(divs)
	with open('out.html', mode='w', encoding='utf-8') as f:
		f.write(html)

