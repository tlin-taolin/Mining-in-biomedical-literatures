#
# Directed graph - in-degree Distribution. G(15158, 20332). 1673 (0.1104) nodes with in-deg > avg deg (2.7), 350 (0.0231) with >2*avg.deg (Fri May 20 14:51:10 2016)
#

set title "Directed graph - in-degree Distribution. G(15158, 20332). 1673 (0.1104) nodes with in-deg > avg deg (2.7), 350 (0.0231) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png size 1000,800
set output 'inDeg.1.png'
plot 	"inDeg.1.tab" using 1:2 title "" with linespoints pt 6
