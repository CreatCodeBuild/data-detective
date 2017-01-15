# This is not a pandas tutorial. I won't explain much about it in the video.
# If you feel confused by pandas code, ask questions in comments/issues, I will try my best to explain.

import pandas
from bokeh.charts import Histogram
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.io import show


def count_attribute(df, attribute, sort_by='value'):
	if sort_by == 'value':
		return df.get(attribute).value_counts()
	else:
		return df.get(attribute).value_counts().sort_index()


def top_n_and_other(n, series):
	top_n = series.nlargest(n)
	other = series.nsmallest(series.shape[0] - n).sum()
	return top_n.append(pandas.Series([other], ['Other']))


def bottom_n_and_other(n, series):
	bottom_n = series.nsmallest(n)
	other = series.nlargest(series.shape[0] - n).sum()
	return bottom_n.append(pandas.Series([other], ['Other']))



ign = pandas.read_csv('../ign.csv')

# print(ign.shape, type(ign))

score_phrase = ign['score_phrase']
# print(score_phrase.shape, type(score_phrase))
# print(score_phrase)

count = score_phrase.value_counts()
# print(type(count.keys()))

index = ['Masterpiece', 'Amazing', 'Great', 'Good', 'Okay', 'Bad', 'Awful', 'Painful', 'Unbearable', 'Disaster']
index.reverse()
count = count.reindex(index)
plot = figure(x_range=list(count.keys().values), title='评价')
plot.vbar(x=list(count.keys().values), width=0.5, bottom=0, top=count.get_values())

hist = Histogram(ign['score'], bins=100, title="评分分布")


# platform
platform = count_attribute(ign, 'platform')
total_top_10_platform = top_n_and_other(10, platform)
plot_total_top_10_platform = figure(width=800,
									x_range=list(total_top_10_platform.keys().values),
									title='游戏最多的10个平台')
plot_total_top_10_platform.vbar(x=list(total_top_10_platform.keys().values),
								width=0.5, bottom=0,
								top=total_top_10_platform.get_values())

total_bottom_10_platform = platform.nsmallest(10)
plot_total_bottom_10_platform = figure(width=1000, x_range=list(total_bottom_10_platform.keys().values), title='游戏最少的10个平台')
plot_total_bottom_10_platform.vbar(x=list(total_bottom_10_platform.keys().values), width=0.5, bottom=0, top=total_bottom_10_platform.get_values())


genre = count_attribute(ign, 'genre')
top10_genre = top_n_and_other(10, genre)
top10_genre_plot = figure(width=800, x_range=list(top10_genre.keys().values), title='游戏最多的10个平台')
top10_genre_plot.vbar(x=list(top10_genre.keys().values), width=0.5, bottom=0, top=top10_genre.get_values())

bottom10_genre = genre.nsmallest(10)
bottom10_genre_plot = figure(width=1000, x_range=list(bottom10_genre.keys().values), title='游戏最少的10个平台')
bottom10_genre_plot.vbar(x=list(bottom10_genre.keys().values), width=0.5, bottom=0, top=bottom10_genre.get_values())


year = count_attribute(ign, 'release_year', sort_by='index')
month = count_attribute(ign, 'release_month', sort_by='index')
day = count_attribute(ign, 'release_day', sort_by='index')

year_plot = figure(title='评价')
year_plot.vbar(x=list(year.keys().values), width=0.5, bottom=0, top=year.get_values())

month_plot = figure(title='评价')
month_plot.vbar(x=list(month.keys().values), width=0.5, bottom=0, top=month.get_values())

day_plot = figure(title='评价')
day_plot.vbar(x=list(day.keys().values), width=0.5, bottom=0, top=day.get_values())

grid_layout = gridplot([
	[plot, hist],
	[plot_total_top_10_platform, plot_total_bottom_10_platform],
	[top10_genre_plot, bottom10_genre_plot],
	[year_plot, month_plot, day_plot]
])

show(grid_layout)


# Bokeh
# 探索性、统计式
# 了解数据的信息


# D3， Bokeh
# 解释性
# 已经了解信息，想给别人传达一种观点


