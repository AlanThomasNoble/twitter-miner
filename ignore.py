'''add a stacked bar graph'''

			# Import seaborn as sns for nice plot styles
			# sns.set()
	def yearMonthDate(self): # add userInput?
		'''boxplot and bar graph'''
		#self.df = self.df.sort_values(by='post date-time')
		#interval = None # D, M, Y (there's a couple more as well)
		'''Interavl Code
		g.iat[0]-g.iat[-1] # Timedelta('-9 days +05:45:35')
		g.dt.day.iat[0]-g.dt.day.iat[-1]
		g.dt.year
		g.dt.month
		ax.set_xticklabels(labels=df_sample_grouped.index, rotation=70, rotation_mode="anchor", ha="right");
		
		'''
		# df['count'].resample('D', how='sum')
		# df['count'].resample('W', how='sum')
		# df['count'].resample('M', how='sum')
		# self.df['month year'] = self.df['post date-time'].dt.to_period('M')
		# self.df.boxplot(by='month year', column='account subjectivity',grid=False)
		# self.df['month year'] = self.df['post date-time'].dt.to_period('M')
		# self.df.boxplot(by='month year', column='account sentiment score',grid=False)

		#use this name for below code

		# pd.Grouper(level='timestamp', freq='W')

		'''bargraph'''
		#fig, ax = plt.subplots(figsize=(15,7))
		monthly = self.df.set_index('post date-time').resample('M')['account subjectivity'].mean()
		#plot data
		fig, ax = plt.subplots(figsize=(15,7))
		g = monthly.sort_index()
		g = g.fillna(0)
		g.plot(kind='bar',x='A',y='A','B','C')
		g.plot(kind='bar',ax=ax) # ax=ax?
		ax.set_title(title='Subjectivity Average Per Month', ylabel='Average', xlabel='Date')
		ax.set_ylabel('Average')
		ax.set_xlabel('Date')
		dateformat = '%b %Y' # then figure out how to map...sheesh.
		ax.set_xticklabels(g.index.strftime(dateformat).format(),rotation=70, rotation_mode="anchor", ha="right") # not sure what thething in format does.
		#plt.xticks(rotation=90)
		plt.show()
		plt.clf()
		# generate median as well..
		# plot median next to mean
		# .plot(legend=True)

		'''add a stacked boxplot'''
		'''add a median as well as average, plot next to mean'''



	def scoreChange(self):
		pass

		'''BoxPlot of Sentiment Score Changes Over Time'''
		# 'W' for week, maybe 'Y' for years
		# output daterange if yearrange < 2: use M
		# if mongth range is less than 1, use D
		'''
		plt.style.use('ggplot')
		months = [g for n, g in self.df.set_index('post date-time').groupby(pd.Grouper(freq='M'))]
		allmonths = pd.concat(months)# = self.df.groupby()
		fig, ax = plt.subplots(figsize=(15,7))
		'''
		#ax.set_xlabel('Month Years')
		#ax.set_ylablel('Sentiment Scores')

		# remember to sort values first
		
		#ax.set_ylim(bottom=0)
		#data.groupby(['date','type']).count()['amount'].unstack().plot(ax=ax)
		# import pdb;
		# pdb.set_trace()
		# self.df.groupby(['post date-time','account sentiment']).count()['account sentiment score'].unstack().plot(ax=ax)
		# ax.set_xlabel('Date')
		# plt.show()
		# import pdb; pdb.set_trace()
		# plt.imshow()
		# plt.clf()

		#gapminder_2007.boxplot(by='continent', 
              #         column=['lifeExp'], 
           #            grid=False)
		#Creates New Column
		#Not sure, perhaps there's a cleaner way to do this....