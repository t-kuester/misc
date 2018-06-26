import sys, glob, os, re

if len(sys.argv) == 1:
	print("You have to provide a directory as first parameter.")
	exit()
	
directory = sys.argv[1]
os.chdir(directory)

files = glob.glob("*")
files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
files.sort(key=lambda s: [int(x) for x in re.findall(r"\d+", s)])

with open("imgs.html", "w") as f:
	f.write("<html><body>\n")
	n = len(files)
	for i, img in enumerate(files, start=1):
		f.write('%d/%d %s<br><img src="%s" width=100%%>\n' % (i, n, img, img))
	f.write("</body></html>\n")
