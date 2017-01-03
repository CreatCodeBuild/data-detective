import pandas
from bokeh.plotting import figure, output_file, show


ign = pandas.read_csv('ign.csv')

release_year = ign.get('release_year')
counts = release_year.value_counts()
counts.sort_index(inplace=True)


### Bokeh
# output to static HTML file
output_file("ign.html")

# create a new plot with a title and axis labels
p = figure(title="Release Year", x_axis_label='Year', y_axis_label='Quantity')

# add a line renderer with legend and line thickness
p.line(counts.keys(), counts.get_values(), legend="Temp.", line_width=2)

# show the results
show(p)
