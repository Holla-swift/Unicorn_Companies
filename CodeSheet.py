## Analysis of Unicorn Companies in the World

Unicorns are companies that have attained a financial valuation of at least 1 billion USD. Unicorns can provide insights into the level of performance of the domestic economy. 
In this analysis, an exploratory data analysis (EDA) is carried out to examine the overall status of unicorn companies . In this EDA, analysis of the number of years it took to ascertain unicorn status, the industry with the best return on investment, as well as the amount of funding received by industry was analysis. Also, countries with opportunities to ascertain unicorn status quickly was also identified.

The dataset used in this analysis is provided by Maven Analytics, in its Maven Unicorn Challenge https://raw.githubusercontent.com/kauvinlucas/maven-unicorn-challenge/main/data/Unicorn_Companies.csv

##### Importing the neccesary libraries

# analysis packages
import pandas as pd
import os

# viz packages
import matplotlib.pyplot as plt
import seaborn as sns

# NLP
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from wordcloud import WordCloud

##### Path and Dataset

working_directory = os.getcwd()
path = working_directory + '/Unicorn_Companies.csv'
df = pd.read_csv(path)
df.head(10)

# overview of the unicorn company space

stop_words = set(stopwords.words('english'))
df['title_no_stopwords'] = df['Company'].apply(lambda x: [item for item in str(x).split() if item not in stop_words])

all_words = list([a for b in df['title_no_stopwords'].tolist() for a in b])
all_words_str = ' '.join(all_words) 

def plot_cloud(wordcloud):
    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud) 
    plt.axis("off");

wordcloud = WordCloud(width = 3000, height = 1500, random_state=1, background_color='white', 
                      colormap='viridis', collocations=False).generate(all_words_str)
plot_cloud(wordcloud)

### Data pre-processing

df.info()

df.shape

# rename the columns for with space using underscore, for easy access

df.columns = df.columns.str.replace(' ', '_')
df['Date_Joined'] = pd.to_datetime(df['Date_Joined'])
df['year_joined'] = df['Date_Joined'].dt.year
df['month'] = df['Date_Joined'].apply(lambda x: x.strftime('%B'))
df.head(2)

#### Most Valuable unicorn companies in the world based on current valuation

# plot vertical barplot
sns.set(rc={'figure.figsize':(8,8)})
ax = sns.barplot(x='Company', y='Valuation', data=df[0:10])

# set title of barplot
ax.set_title('Most Valuable Unicorn Companies in the World', fontsize=16)
ax.set_ylabel('Current Company Valuation')
ax.set_xticklabels(df.Company[0:10],rotation=45)

# label for each bar
for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + p.get_width()/2,
           y= height+4,
            s = '${:.0f}bn'.format(height),
           ha='center')

### Analysis of unicorn companies by continent

# list of continents in the dataset

list(set(df.Continent))

#### Number of unicorn companies by continent

# Number of unicorn companies by continent

continent = df.groupby('Continent').count()
continent = continent.sort_values(by='Company', ascending=False)
continent = pd.DataFrame(continent.Company).reset_index()
continent = continent.rename(columns={'Company':"No of Unicorn companies per continent"}, inplace=False)
continent

# plot vertical barplot
sns.set(rc={'figure.figsize':(8,8)})
ax = sns.barplot(x='Continent', y='No of Unicorn companies per continent', data=continent)

# set title of barplot
ax.set_title('Number of Unicorn companies per continent', fontsize=16)
ax.set_ylabel('No of Companies')

# label for each bar
for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + p.get_width()/2,
           y= height+10,
            s = '{:.0f}'.format(height),
           ha='center')

#### Total Funding received $bn per continent

continent_funding = df.groupby('Continent').agg({'Funding': 'sum'})
continent_funding = continent_funding.sort_values(by='Funding', ascending=False)
continent_funding = pd.DataFrame(continent_funding.Funding).reset_index()
continent_funding = continent_funding.rename(columns={'Funding':"Total Funding received $bn per continent"}, inplace=False)
continent_funding

# plot vertical barplot
sns.set(rc={'figure.figsize':(10,5)})
chart = sns.barplot(x='Total Funding received $bn per continent', y='Continent', data=continent_funding, orient='horizontal')

# set title of barplot
chart.set_title('Funding received by unicorn companies per continent', fontsize=16, color='black')
plot.set_ylabel('Continent')

# label each bar in barplot
for p in chart.patches:
    height = p.get_height()
    width = p.get_width()
    chart.text(x = width+1,
           y = p.get_y()+(height/2),
           s = '${:.0f}bn'.format(width),
           va = 'center')

##### Relationship between current valuation status and geographical location

cont = sns.scatterplot(data = df, x = 'Valuation', y = 'Continent')
cont.set_title('Avg Valuation of Unicorn companies by Continent', fontsize=16)
cont.set_xlabel('Valuation in $bn')

##### Industries and No of Unicorns

list(set(df.Industry))

# Industry classification of Unicorns

Industy_unicorn = df.groupby('Industry').count()
Industy_unicorn = Industy_unicorn.sort_values(by='Company', ascending=False)
Industy_unicorn = pd.DataFrame(Industy_unicorn.Company).reset_index()
Industy_unicorn = Industy_unicorn.rename(columns={'Company':"No of Unicorn Companies"}, inplace=False)
Industy_unicorn

# Graphical illustration

ax2 = sns.barplot(data = Industy_unicorn, x='No of Unicorn Companies', y= 'Industry')
ax2.set_title('Number of Unicorn companies by Industry', size=16)
ax2.set_xlabel('No of Unicorn companies')

# label for each bar
for container in ax2.containers:
    ax2.bar_label(container)


##### Analyse the industry with the fastest chance to become a Unicorn as well as the associated return on investment

# calculating the years it takes to becoming a unicorn per sector and corresponding returns

Years_unicorn = df.groupby('Industry').mean()
Years_unicorn = Years_unicorn.sort_values(by='Year_to_be_a_unicorn', ascending=True)
Years_unicorn = Years_unicorn.iloc[:,3:5]
Years_unicorn = pd.DataFrame(Years_unicorn).reset_index()
Years_unicorn

# Graphical illustration
sns.set(rc={'figure.figsize':(12,8)})

sec = sns.barplot(data = Years_unicorn, x='Industry', y='Year_to_be_a_unicorn')
plt.title('Avg Number of years to become a Unicorn per Sector', size=16)
plt.xlabel('Industry')
plt.ylabel('Average number of years')
plt.xticks(rotation=80, size=10)



# label for each bar
for p in sec.patches:
    height = p.get_height()
    sec.text(x = p.get_x() + p.get_width()/2,
           y= height+0.2,
            s = '{:.1f}yrs'.format(height),
           ha='center')


##### Investment  returns by number of years used to attain unicorn status

sns.set(rc={'figure.figsize':(12,8)})

ROI = sns.scatterplot(data = Years_unicorn, 
                      x = 'Return_on_investment', 
                      y = 'Year_to_be_a_unicorn', 
                      hue='Industry', 
                      s=1000, 
                      c='coral')
ROI.set_title('Relationship between No of years to be a unicorn company and ROI', fontsize=16)
ROI.set_xlabel('ROI(x)')
ROI.legend(bbox_to_anchor=(1.02,1), loc='upper left', borderaxespad=0)

##### ROI by Industry

ROI_sector = df.groupby('Industry').mean().round(2)
ROI_sector = ROI_sector.sort_values(by='Return_on_investment', ascending=False)
ROI_sector = ROI_sector.iloc[:,4]
ROI_sector = pd.DataFrame(ROI_sector).reset_index()
ROI_sector = ROI_sector.rename(columns={'Return_on_investment':'ROI(x)'})
ROI_sector

# Graphical illustration

ax3 = sns.barplot(data = ROI_sector, x='Industry', y= 'ROI(x)')
ax3.set_title('ROI of Unicorn companies per sector', size=16)
ax3.set_xlabel('No of Unicorn companies')
plt.xticks(rotation=80, size=12)

# label for each bar
for p in ax3.patches:
    height = p.get_height()
    ax3.text(x = p.get_x() + p.get_width()/2,
           y= height+0.05,
            s = '{:.2f}x'.format(height),
           ha='center')



#### Country Unicorn Analysis

### no of countries that have Unicorns

len(list(set(df.Country)))

country_unicorn = df.groupby('Country').count()
country_unicorn = country_unicorn.sort_values(by='Valuation', ascending=False)
country_unicorn = pd.DataFrame(country_unicorn.Company).reset_index()
country_unicorn = country_unicorn.rename(columns={'Company':"No of Unicorn Companies"}, inplace=False)
country_unicorn

# Average Valuation figures $bn per country

country_unicorns = df.groupby('Country').mean('Valuation')
country_unicorns = country_unicorns.sort_values('Valuation', ascending=False)
country_unicorns = country_unicorns.reset_index()
country_unicorns = country_unicorns.round(1)
country_unicorns = country_unicorns.iloc[:,[0,1,3,4,5]]
country_unicorns

unicorn_yr = country_unicorns.sort_values(by='Year_to_be_a_unicorn', ascending=True)[0:26]

# bar chart
unicorn_years = sns.barplot(data=unicorn_yr , x='Year_to_be_a_unicorn', y='Country')
plt.title('Number of years to become a Unicorns', size=14)
plt.xlabel('No of years')

#define plot size for all plots
plt.rcParams['figure.figsize'] = [11, 8]

# label for each bar
for container in unicorn_years.containers:
    unicorn_years.bar_label(container)
    
plt.show()

##### Total Unicorn funding received by country in $'bn

# Total funding received by countries

country_funding = df.groupby('Country').sum('Funding').round(2)
country_funding = pd.DataFrame(country_funding.Funding)
country_funding = country_funding.sort_values(by='Funding', ascending=False)
country_funding = country_funding.rename(columns={'Funding':"Total funding received in $bn"}).reset_index()
country_funding

sns.set(rc={'figure.figsize':(12,8)})

# bar chart
f = sns.barplot(x ='Total funding received in $bn', y= 'Country', data=country_funding[0:21])
plt.title('Total Funding received by Unicorn companies per Country $bn', size=16)
plt.xlabel('Amount received $bn')

# label each bar in barplot
for p in f.patches:
    height = p.get_height()
    width = p.get_width()
    f.text(x = width+1,
           y = p.get_y()+(height/2),
           s = '${:.0f}bn'.format(width),
           va = 'center')
    
#define plot size for all plots
plt.rcParams['figure.figsize'] = [6.4, 7]

plt.show()

#### Number of companies that attain unicorn status per annum

joined_unicorn = df.groupby('year_joined').count()
joined_unicorn = pd.DataFrame(joined_unicorn.Company).reset_index()
joined_unicorn = joined_unicorn.rename(columns={'Company':'No of companies that became unicorn'})
joined_unicorn

sns.set(rc={'figure.figsize':(10,8)})

n = sns.lineplot(data=joined_unicorn, x='year_joined', y='No of companies that became unicorn')

plt.title('Number of companies that became unicorn coy per annum', size=16)
plt.xlabel('Year')
plt.xticks(rotation=30)

# label points on the plot
for x, y in zip(joined_unicorn['year_joined'], joined_unicorn['No of companies that became unicorn']):
    plt.text(x = x,
             y = y+10,
             s = '{:.0f}'.format(y),
             va = 'bottom',
             color = 'red').set_backgroundcolor('#add8e6')

data1 = df.pivot_table(index="month", columns="Year_Founded", values="Funding", aggfunc='sum')
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October' , 'November', 'December']

data1 = data1.reindex(months)
data1 = data1.fillna(0).astype(int)

#### HeatMap of funds raised by Unicorn companies

# heatmap from 2006 through 2020, excluding periods before 2006

hmp = sns.heatmap(data1.iloc[:, -16:-1],
                 annot=True, 
                  fmt="d",
                  annot_kws={"size":13},
                 cmap="Spectral")

hmp.set_title('Heatmap of funds raised by unicorn companies in $bn', 
              fontsize=16)

hmp.set_xlabel('Year fund was raised')

##### Countries with the best ROI

country_ROI = df.groupby('Country').mean('Return_on_investment').round(2)
country_ROI = pd.DataFrame(country_ROI.Return_on_investment)
country_ROI = country_ROI.sort_values(by='Return_on_investment',
                                      ascending=False).reset_index()
country_ROI

sns.set(rc={'figure.figsize':(10,8)})

# bar chart
r = sns.barplot(data=country_ROI[0:21],y='Return_on_investment',x='Country')
plt.title('Avg ROI of Unicorn Companies by ountry', size=14)
plt.xlabel('Country')
plt.xticks(rotation=80)

# label for each bar
for p in r.patches:
    height = p.get_height()
    r.text(x = p.get_x() + p.get_width()/2,
           y= height+0.3,
            s = '{:.1f}x'.format(height),
           ha='center')

    
plt.show()

##### Investor Analysis in Unicorn funding

stop_words = set(stopwords.words('english'))
df['title_no_stopwords'] = df['Select_Investors'].apply(lambda x: [item for item in str(x).split() if item not in stop_words])

all_words = list([a for b in df['title_no_stopwords'].tolist() for a in b])
all_words_str = ' '.join(all_words) 

def plot_cloud(wordcloud):
    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud) 
    plt.axis("off");

wordcloud = WordCloud(width = 1000, height = 500, random_state=1, background_color='white', 
                      colormap='viridis', collocations=False).generate(all_words_str)
plot_cloud(wordcloud)

##### Cities with the highest number of Unicorns

### number of cities with atleast a Unicorn company

len(list(set(df.City)))

stop_words = set(stopwords.words('english'))
df['title_no_stopwords'] = df['City'].apply(lambda x: [item for item in str(x).split() if item not in stop_words])

all_words = list([a for b in df['title_no_stopwords'].tolist() for a in b])
all_words_str = ' '.join(all_words) 

def plot_cloud(wordcloud):
    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud) 
    plt.axis("off");

wordcloud = WordCloud(width = 1000, height = 500, random_state=1, background_color='white', 
                      colormap='viridis', collocations=False).generate(all_words_str)
plot_cloud(wordcloud)

...till we meet again, for comments, suggestions and further areas of improvement.

#### LinkedIn: Adeoti Sheriffdeen
#### Twitter: @SheriffHolla
#### contact me at s.adeoti86@gmail.com