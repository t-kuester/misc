"""Download and parse times from race results websites.
"""

import urllib2
import numpy as np
import matplotlib.pyplot as plt


def parse_berlinhalf(f):
	"""Parse result pages of Berlin Halfmarathon 2017.
	"""
	# skip preamble
	times = []
	while next(f) != "<tbody>\n":
		pass
	# now we are inside the table with the results
	for line in f:
		# fast-forward to next netto time
		while not line.startswith("  <td><a target"):
			line = next(f)
			if line.startswith("</tbody>"):
				return times
			
		# next line holds netto time
		line = next(f)
		times.append(line[6:14])
	return times

def download(base_url, first, last, filename, parser):
	"""Mass-download result pages and parse times using specific parsers.
	"""
	for i in range(first, last + 1):
		url = base_url % i
		print(url)
		f = urllib2.urlopen(url)
		with open(filename, "a") as output:
			for time in parser(f):
				output.write(time + "\n")
		f.close()

def plot(filename):
	"""Load previously parsed times from file and plot as histogram.
	"""
	seconds = []
	# read from results file
	with open(filename) as f:
		for time in f:
			h, m, s = map(int, time.split(":"))
			secs = 60 * 60 * h + 60 * m + s
			seconds.append(secs)

	# print ascii histogram
	hist, bins = np.histogram(seconds, bins=100)
	for c, t in zip(hist, bins):
		print("%3d %s" % (t, "*" * (c/10)))

	# print mathplotlib histogram
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.show()


url = "http://results.berliner-halbmarathon.de/2017/?page=%d&event=HML&num_results=100&pid=search&search[nation]=%%25&search_sort=place_nosex"
result = "result.txt"
#~ download(url, 1, 156, result, parse_berlinhalf)
plot(result)
