set pm3d
set hidden3d
set dgrid3d 30,30, qnorm 10
#set pm3d interpolate 40,40
set xlabel "{/Symbol a}"
set ylabel "{/Symbol m}"
set zlabel "Error"
set title "Error = |{/Symbol D}SCF(+1) - {/Symbol D}SCF(0) + IP|  

splot "combo.dat" u 1:2:3 w p ti ""
pause -1