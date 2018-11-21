
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

b18			=[	597.961325966851, 1.20941463305307, 0.263530270897063, 0.519337016574586, 22.2430939226519, 29.5359116022099,\
				3234.79961045407, 74.9498683548821, 30.8839779005525, 7.97790055248619,	4.19889502762431]
eb18		=[	1093.00357000861, 13.1064831934754, 0.369497128439535, 4.03813923074724, 37.6512729508433, 41.7942723730434,\
				6608.11853235636, 26.6774076382953, 50.2731739563354, 4.13784136034583, 12.6180734088065]

webMetrics	=[i for i in range(11)]
ewebMetrics	=[0 for i in range(11)]
Country = ['Your Url', 'BEST OF 2018']
x_pos = np.arange(len(Country))

for mno in range(11):
	col='red'
	if mno in [1,4,6,9,10]:
		col='blue'
	CTEs	= [webMetrics[mno],b18[mno]]
	error 	= [[min(webMetrics[mno],ewebMetrics[mno]),min(b18[mno],eb18[mno])],[ewebMetrics[mno],eb18[mno]]]
	fig 	= Figure(figsize=(6,6))
	ax 		= fig.add_subplot(111)

	ax.bar(x_pos, CTEs, yerr=error, align='center', color=col,alpha=0.5, ecolor='black', capsize=20)
	ax.set_xticks(x_pos)

	lprop 	= {'fontsize':20,'weight':'bold'}

	ax.set_xticklabels(Country,fontdict=lprop)
	ax.yaxis.set_tick_params(labelsize=20)
	ax.yaxis.grid(True)

	canvas 	= FigureCanvasAgg(fig)

	canvas.print_figure('/home/abhiavk/git/mysite/pageEval/static/pageEval/images/'+str(mno)+'.png', dpi=80)
