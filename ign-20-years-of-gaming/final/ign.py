import pandas
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.charts import Donut, Histogram, HeatMap
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


def binary_relation_count(df, key1, key2):
	return df.groupby([key1, key2]).size().reset_index().pivot(index=key1, columns=key2)


def hovertool():
	return HoverTool(tooltips=[("value", "@top")])


ign = pandas.read_csv('../ign.csv')
ign['genre'].fillna('Not Specified', inplace=True)


# --- Basic ------------------------------------------------------------------------------------------------------------
total_num_games = ign.shape[0]

# score_phrase
total_score_phrase = count_attribute(ign, 'score_phrase')
index = ['Masterpiece', 'Amazing', 'Great', 'Good', 'Okay', 'Bad', 'Awful', 'Painful', 'Unbearable', 'Disaster']
index.reverse()
total_score_phrase = total_score_phrase.reindex(index)
hover_total_score_phrase = hovertool()
plot_total_score_phrase = figure(x_range=list(total_score_phrase.keys().values), tools=[hover_total_score_phrase, 'save'], title='评价')
plot_total_score_phrase.vbar(x=list(total_score_phrase.keys().values), width=0.5, bottom=0, top=total_score_phrase.get_values())

# score, distribution
plot_total_score = Histogram(ign['score'], bins=100, title="评分分布")

grid_total_score_and_phrase = gridplot([
	[plot_total_score_phrase, plot_total_score]
])

# platform
total_platform = count_attribute(ign, 'platform')
total_num_platform = total_platform.shape[0]

total_top_10_platform = top_n_and_other(10, total_platform)
hover_1 = hovertool()
plot_total_top_10_platform = figure(width=800, x_range=list(total_top_10_platform.keys().values), tools=[hover_1, 'save'], title='游戏最多的10个平台')
plot_total_top_10_platform.vbar(x=list(total_top_10_platform.keys().values), width=0.5, bottom=0, top=total_top_10_platform.get_values())

total_bottom_10_platform = total_platform.nsmallest(10)
plot_total_bottom_10_platform = figure(width=1000, x_range=list(total_bottom_10_platform.keys().values), title='游戏最少的10个平台')
plot_total_bottom_10_platform.vbar(x=list(total_bottom_10_platform.keys().values), width=0.5, bottom=0, top=total_bottom_10_platform.get_values())

grid_total_platform = gridplot([
	[plot_total_top_10_platform, plot_total_bottom_10_platform]
])

# genre
total_genre = count_attribute(ign, 'genre')
total_num_genre = total_genre.shape[0]

total_top_10_genre = top_n_and_other(10, total_genre)
hover_2 = hovertool()
plot_total_top_10_genre = figure(width=800, x_range=list(total_top_10_genre.keys().values), tools=[hover_2, 'save'], title='游戏最多的10个类型')
plot_total_top_10_genre.vbar(x=list(total_top_10_genre.keys().values), width=0.5, bottom=0, top=total_top_10_genre.get_values(), color="#CAB2D6")

total_bottom_10_genre = total_genre.nsmallest(10)
plot_total_bottom_10_genre = figure(width=1000, x_range=list(total_bottom_10_genre.keys().values), title='游戏最少的10个类型')
plot_total_bottom_10_genre.vbar(x=list(total_bottom_10_genre.keys().values), width=0.5, bottom=0, top=total_bottom_10_genre.get_values(), color="#CAB2D6")

grid_total_genre = gridplot([
	[plot_total_top_10_genre, plot_total_bottom_10_genre]
])


# release_year
total_release_year = count_attribute(ign, 'release_year')
plot_total_release_year = figure(title="年份")
plot_total_release_year.vbar(x=list(total_release_year.keys().values), width=0.5, bottom=0, top=total_release_year.get_values())

# release_month
total_release_month = count_attribute(ign, 'release_month')
plot_total_release_month = figure(title="月份")
plot_total_release_month.vbar(x=list(total_release_month.keys().values), width=0.5, bottom=0, top=total_release_month.get_values())

# release_day
total_release_day = count_attribute(ign, 'release_day')
plot_total_release_day = figure(title="日子")
plot_total_release_day.vbar(x=list(total_release_day.keys().values), width=0.5, bottom=0, top=total_release_day.get_values())

grid_total_release_time = gridplot([
	[plot_total_release_year, plot_total_release_month, plot_total_release_day]
])
# --- Basic End --------------------------------------------------------------------------------------------------------

# platform_year = binary_relation_count( 'release_year', 'platform')
# print(platform_year.shape, platform_year['iPod'])
hover4 = HoverTool(tooltips=[("Platform", "@x"), ("Year", "@y"), ("Count", "@values")])
hover5 = HoverTool(tooltips=[("Platform", "@x"), ("Year", "@y"), ("Score", "@values")])
platform_trend_count = HeatMap(ign, width=1800, height=800, x='platform', y='release_year',
						 	   tools=[hover4, 'save'], legend='bottom_right', title='Platform Trend: Number of Games')
platform_trend_mean = HeatMap(ign, width=1800, height=800, x='platform', y='release_year', values='score', stat='mean',
						      tools=[hover5, 'save'], legend='bottom_right', title='Platform Trend: Average Score')

hover6 = HoverTool(tooltips=[("Platform", "@x"), ("Year", "@y"), ("Count", "@values")])
hover7 = HoverTool(tooltips=[("Platform", "@x"), ("Year", "@y"), ("Score", "@values")])
genre_trend_count = HeatMap(ign, width=1800, height=800, x='genre', y='release_year',
							tools=[hover6, 'save'], legend='bottom_right', title='Genre Trend: Number of Games')
genre_trend_mean = HeatMap(ign, width=1800, height=800, x='genre', y='release_year', values='score', stat='mean',
						   tools=[hover7, 'save'], legend='bottom_right',title='Genre Trend: Average Score')

script, divs = components({
	'grid_total_score_and_phrase': grid_total_score_and_phrase,
	'grid_total_platform': grid_total_platform,
	'grid_total_genre': grid_total_genre,
	'grid_total_release_time': grid_total_release_time,
	'platform_trend_count': platform_trend_count,
	'platform_trend_mean': platform_trend_mean,
	'genre_trend_count': genre_trend_count,
	'genre_trend_mean': genre_trend_mean,
})
divs['script'] = script
divs['total_num_games'] = total_num_games
divs['total_num_platform'] = total_num_platform
divs['total_num_genre'] = total_num_genre

with open('template.jinja', 'r', encoding='utf8') as f:
	template = Template(f.read())
	html = template.render(divs)
	with open('ign.html', mode='w', encoding='utf-8') as f:
		f.write(html)

