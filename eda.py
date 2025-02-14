# -*- coding: utf-8 -*-
"""EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ePezBOrANof6QwPR8ljdURFqV3e3kJe2
"""

# Commented out IPython magic to ensure Python compatibility.
# first line is to print the graph not just calculating
# the data we used is https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data

# %matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('train.csv')

data.head()

# we will know number of rows and columns in the data
data.shape

# checking the null values in the complete data frame
missing = data.isnull().sum()
missing = missing[missing > 0]
missing.sort_values(inplace=True)
missing.plot.bar()

# we got to know the number of missing values in each column where from lotfronatge to poolqc they are alot.
# as we can see total no. of rows are 1460 and for poolqc there are almost 1400 missing values
# so we can conclude that column is useless to predict the house price

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.distplot(data['SalePrice'], kde=True, bins =20)

# here bins is that the data is divided in 20 intervals to visualise the data
# we can change it as per our wish
# we are using histogram to identify the skewness, detect outlier
# KDE helps better visualise the shape

data['SalePrice'].describe()

# 50% or 50th percentile is median, here median < mean and the plot shown above
# right skewed

sns.kdeplot(data['SalePrice'])

# next step is correlation- correlation heatmap
# we will know which column has good relation with our target variable/column
# can choose by knowing which is better than randomly choosing
# we cant do correlation for categorical types(ordinal,nominal) but only for numerical

numeric_features = data.select_dtypes(include=[np.number])
numeric_features.columns

categorical_features = data.select_dtypes(include=[object])
categorical_features.columns

# correlation for just numeric data type columns
# this is between salesprice and every other numeric column
correlation = numeric_features.corr()
print(correlation['SalePrice'].sort_values(ascending=False),'\n')

f, ax= plt.subplots(figsize=(10,8))
sns.heatmap(correlation, vmax=.8, square=True)

# lets draw a heatmap only to specific no of columns
k =11
cols = correlation.nlargest(k,'SalePrice')['SalePrice'].index
print(cols)
cm = np.corrcoef(data[cols].values.T)
f,ax= plt.subplots(figsize=(14,12))
sns.heatmap(cm,vmax=0.8,linewidths=0.01,square=True,annot=True,cmap='viridis',linecolor='white',
            xticklabels=cols.values,yticklabels=cols.values,annot_kws={'size':12})

# here multicollinearity arised which means 2 independent predicors/variables are
# highly correlated with target variable and higly correlated within themselves too.
# this is a disadvantage because its difficult to assess which predictor has
# more effect on target variable which will mislead the results.
# this destroys model performance, so soln is to just drop either one of them.
# GARAGE CARS - GARAGE AREA

# @title Scatter Plot
# we can see the correlation, how two features varies with each other and we call also see outliers

sns.scatterplot(x=data['GarageCars'],y=data['SalePrice'])

# this is also a scatter plot but it is fitting a line, best thing is to to use regplot so that we can change the fir_red
# to true or false accordingly
sns.regplot(x=data['GarageCars'],y=data['SalePrice'],fit_reg=True)

# scatter plots between most correlated variables
fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(ncols=2,nrows=3,figsize=(14,10))
sns.regplot(x=data['OverallQual'],y=data['SalePrice'],fit_reg=True, ax = ax1)
sns.regplot(x=data['GrLivArea'],y=data['SalePrice'],fit_reg=True, ax=ax2)
sns.regplot(x=data['GarageArea'],y=data['SalePrice'],fit_reg=True, ax=ax3)
sns.regplot(x=data['TotalBsmtSF'],y=data['SalePrice'],fit_reg=True, ax=ax4)
sns.regplot(x=data['1stFlrSF'],y=data['SalePrice'],fit_reg=True, ax=ax5)
sns.regplot(x=data['FullBath'],y=data['SalePrice'],fit_reg=True, ax=ax6)

# @title BoxPlot
# the quartiles in boxplot are used to divide the data into equal parts, and these help summarize
# the distribution of data
# we need min, max, median, 1st quartile/lower quartile, 3rd quartile/upper quartile to plot boxplot
# Interquartile range(IQR) = Q3-Q1

sns.boxplot(x=data['SalePrice'])

f, ax = plt.subplots(figsize=(16,10))
ax = sns.boxplot(x=data['SaleType'],y=data['SalePrice'])
xt = plt.xticks(rotation=45)

f, ax = plt.subplots(figsize=(12,8))
ax = sns.boxplot(x=data['OverallQual'],y=data['SalePrice'])

# @title Remove Outliers

first_quartile = data['SalePrice'].quantile(0.25)
third_quartile = data['SalePrice'].quantile(0.75)
IQR = third_quartile - first_quartile

new_boundary = third_quartile + 3*IQR

data.drop(data[data['SalePrice'] > new_boundary].index,axis = 0,inplace  = True)

data.shape

# before removing outliers there are 1460 rows now there are 1448.
# that means we successfully removed outliers

# @title Removing bad features from the data
# firstly, we have to remove muticollinear variables
# next, features with missing values more than 20%
# and last, features with poor correlation with target variable(SalesPrice)

col_to_remove = ['BsmtFinSF1','LotFrontage', 'WoodDeckSF','2ndFlrSF','OpenPorchSF',
'HalfBath','LotArea','BsmtFullBath','BsmtUnfSF','BedroomAbvGr','ScreenPorch','PoolArea',
'MoSold','3SsnPorch','BsmtFinSF2','BsmtHalfBath','MiscVal','Id','LowQualFinSF',
                 'YrSold','OverallCond','MSSubClass','EnclosedPorch','KitchenAbvGr']

# dropping these columns
data.drop(col_to_remove,axis=1,inplace=True)

data.head()

data.shape