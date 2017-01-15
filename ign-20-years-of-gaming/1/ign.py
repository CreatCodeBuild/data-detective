# This is not a pandas tutorial. I won't explain much about it in the video.
# If you feel confused by pandas code, ask questions in comments/issues, I will try my best to explain.

import pandas
from bokeh.charts import Histogram
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.io import show

ign = pandas.read_csv('../ign.csv')

# print(ign.shape, type(ign))

score_phrase = ign['score_phrase']
# print(score_phrase.shape, type(score_phrase))
# print(score_phrase)

count = score_phrase.value_counts()
print(type(count.keys()))

index = ['Masterpiece', 'Amazing', 'Great', 'Good', 'Okay', 'Bad', 'Awful', 'Painful', 'Unbearable', 'Disaster']
index.reverse()
count = count.reindex(index)
plot = figure(x_range=list(count.keys().values), title='评价')
plot.vbar(x=list(count.keys().values), width=0.5, bottom=0, top=count.get_values())

hist = Histogram(ign['score'], bins=100, title="评分分布")

grid_layout = gridplot([
	[plot, hist]
])


show(grid_layout)


# Bar Chart

# Histogram
