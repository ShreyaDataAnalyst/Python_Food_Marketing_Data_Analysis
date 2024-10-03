#!/usr/bin/env python
# coding: utf-8

# # Food Marketing Data Analaysis

# ## Importing the data

# In[4]:


import pandas as pd

food=pd.read_csv(r'/Users/shreyaarora/Downloads/u_food_marketing (1).csv')
                 
food.head()


# In[7]:


pd.set_option('display.max.rows',2300)
pd.set_option('display.max.columns',60)

food.head()


# ## Data Cleaning

# In[6]:


#showing count of duplicate data

food[food.duplicated()].count() 


# In[ ]:


#deleting duplicates:

food.drop_duplicates(keep=False, inplace=True)


# In[7]:


#joining tables :

food['Total Childern']=food[['Kidhome','Teenhome']].sum(axis=1)

food.head()


# In[172]:


#numbering the marital status

food['marital_Divorced']=food['marital_Divorced'].replace({1:5,0:0})#if there is one which means divorced then change it to 5
food['marital_Married']=food['marital_Married'].replace({1:4,0:0})
food['marital_Single']=food['marital_Single'].replace({1:3,0:0})
food['marital_Together']=food['marital_Together'].replace({1:2,0:0})
food['marital_Widow']=food['marital_Widow'].replace({1:1,0:0})


# In[178]:


#changing int to string of marital status
food['Marital_Status']=food[['marital_Divorced','marital_Married','marital_Single','marital_Together','marital_Widow']].sum(axis=1)


# In[179]:


food['Marital_Status_str']=food['Marital_Status'].map({5:'Divorced',4:'Married',3:'Single',2:'Together',1:'Widow'})


# In[180]:


#numbering the education level


food['education_2n Cycle']=food['education_2n Cycle'].replace({1:1,0:0})#if there is one which means divorced then change it to 5
food['education_Basic']=food['education_Basic'].replace({1:2,0:0})
food['education_Graduation']=food['education_Graduation'].replace({1:3,0:0})
food['education_Master']=food['education_Master'].replace({1:4,0:0})
food['education_PhD']=food['education_PhD'].replace({1:5,0:0})


# In[181]:


#changing int to string of education status
food['Education_Status']=food[['education_2n Cycle','education_Basic','education_Graduation','education_Master','education_PhD']].sum(axis=1)


# In[183]:


## putting different campgin acceptance all as 1 so we will know if the people has accepted more than once

food['Accepted_Camapigns']=food[['AcceptedCmp3','AcceptedCmp4','AcceptedCmp5','AcceptedCmp1','AcceptedCmp2','Response']].sum(axis=1)


# In[184]:


food['Accepted_Camapigns']=(food['Accepted_Camapigns']!=0).astype(int)


# In[185]:


food.corr(method='pearson')['Accepted_Camapigns'].sort_values(ascending=False)


# In[186]:


food[food['Accepted_Camapigns']!=0].head()


# In[187]:


all_correlations=food.corr(method='pearson')
all_correlations=all_correlations[(all_correlations>0.3)&(all_correlations<1)]


# In[188]:


all_correlations['Accepted_Camapigns']


# ## Exploratory Data Analysis

# In[189]:


# age range created

age_range=[(23,30),(31,40),(41,50),(51,60),(61,70),(71,85)]

def assign_age_group(Age):
    for age_group in age_range:
        if age_group[0] <= Age <= age_group[1]:
            return f'{age_group[0]}-{age_group[1]}'
    return("Unkown")

food['Age_Group']=food['Age'].apply(assign_age_group)


# In[190]:


food[['Age','Age_Group']].head()


# In[191]:


import seaborn as sns


# In[192]:


age_order=['23-30','31-40','41-50','51-60','61-70','71-85']

sns.pointplot(data=food, x='Age_Group', y='Accepted_Camapigns',order=age_order)


# In[193]:


counts = food['Age_Group'].value_counts()

counts


# In[194]:


percentage=counts/food.shape[0] 

#food.shape means return all the rows and column, 
#Indexes [0]- means rows axis indexes: [1] means column axis indexes
#since we have said [0] it means we want to return all rows as we are calling row index


# In[195]:


percent_food=percentage.reset_index()


# In[196]:


percent_food.columns=['Age_Group','percentage']


# In[197]:


percent_food.sort_values('Age_Group')


# In[198]:


import matplotlib.pyplot as plt
sns.barplot(x='Age_Group',y='percentage',data=percent_food,order=age_order)
plt.title('Percentage of Accepted Campaigns per Age Group')
plt.show()


# In[199]:


# Age segmentation: Core audience for accepting campign right now is 31-70 

# it looks like age group 23-30 and 71-85 reprensts a small faction of perecentage who are participating but their acceptance rate is high


# In[200]:


## comparing amount spent with age group


# In[201]:


grouped_food= food.groupby('Age_Group')['MntTotal'].sum().reset_index()

sns.barplot(x='Age_Group',y='MntTotal',data=grouped_food,order=age_order)
plt.title('Amount spent per Age Group')
plt.show()


# In[202]:


acct_camp= food[food['Accepted_Camapigns']!=0]

grouped_food= acct_camp.groupby('Age_Group')['MntTotal'].sum().reset_index()

sns.barplot(x='Age_Group',y='MntTotal',data=grouped_food,order=age_order)
plt.title('Amount spent per Age Group')
plt.show()


# In[203]:


# People who accepted the campaigns within age group of 31-70 are spending more money 


# In[204]:


# Age segmentation: Core audience for accepting campign right now is 31-70 

# it looks like age group 23-30 and 71-85 reprensts a small faction of perecentage who are participating but their acceptance rate is high


# In[205]:


food[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum()


# In[206]:


#created data frame of the above extracted column

sum_food=pd.DataFrame(food[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum(), columns=['Sum'])


# In[207]:


sum_food=sum_food.reset_index()
sum_food


# In[208]:


sum_food.rename(columns={'index':'Type_of_purchase'},inplace=True)


# In[209]:


sum_food


# In[210]:


sns.barplot(x='Type_of_purchase',y='Sum',data=sum_food)


# In[252]:


#seeing with 
acct_camp= food[food['Accepted_Camapigns']!=0]

sum_food=pd.DataFrame(acct_camp[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum(), columns=['Sum'])
sum_food=sum_food.reset_index()
sum_food.rename(columns={'index':'Type_of_purchase'},inplace=True)
sns.barplot(x='Type_of_purchase',y='Sum',data=sum_food)


# In[215]:


# 2 directions: Boost up the higher percentage catalog customer. OR FOCUS ON INSTORE /WEB purchases cuz they have more traffic


# In[216]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.regplot(x='Total Childern', y='MntTotal', data=food)

plt.xlim(-0.1, 3.3) 

plt.show()


# In[217]:


#negative correlation: as people with less children spend more money


# In[218]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.regplot(x='Total Childern', y='Accepted_Camapigns', data=food)

plt.xlim(-0.3, 3.3) 

plt.show()


# In[219]:


#Less kids more likely to accept campaign


# In[220]:


# people with more kids are spending more money and accepting less campaigns at much lower rate


# In[221]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.regplot(x='Education_Status', y='Accepted_Camapigns', data=food)

plt.xlim(0.5, 5.5) 

plt.show()


# In[222]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.regplot(x='Education_Status', y='MntTotal', data=food)

plt.xlim(0.5, 5.5) 

plt.show()


# In[223]:


#education is not really significant in our segmentation


# In[230]:


sns.countplot(x='Marital_Status_str', data=food)


# In[245]:




rel_food= food.groupby('Marital_Status_str')['MntTotal'].sum().reset_index()


# In[246]:


sns.barplot(x='Marital_Status_str', y= "MntTotal", data=rel_food)


# In[249]:


acct_camp= food[food['Accepted_Camapigns']!=0]


rel_food= acct_camp.groupby('Marital_Status_str')['MntTotal'].sum().reset_index()


# In[250]:


sns.barplot(x='Marital_Status_str', y= "MntTotal", data=rel_food)


# In[ ]:


#Marriage - Married, single and together are spending a lot more than widow and divorced. we should focus more on this segment.


# In[254]:


total= food['Marital_Status_str'].value_counts()
accepted= food[food['Accepted_Camapigns']==1]['Marital_Status_str'].value_counts()


# In[255]:


percent_marital= accepted/total*100


# In[257]:


pect_food=percent_marital.reset_index()


# In[258]:


pect_food.columns=['Marital_Status','Percentage']


# In[259]:


sns.barplot(x='Marital_Status', y= 'Percentage', data=pect_food)


# In[ ]:





# In[ ]:





# # Overall findings:
# 
# #### 1 Customers aged 30-70 spend the most but are less likely to engage with campaigns, despite their high volume of spending.
# #### 2 Catalog buyers are more likely to accept campaigns, even though most purchases happen in physical stores.
# #### 3 Customers with no or fewer children are more likely to accept campaigns and spend more.
# #### 4 Education has minimal impact on campaign engagement—targeting based on education isn’t necessary.
# #### 5 Marital status isn’t a strong factor, but married, single, and partnered customers tend to spend more.

# # Recommendation:
# 
# #### Money making-- Targeting people who are most likely to accept campign and most likey to spend more money 
# Target middle-aged, high-income customers with no children across different platforms. These customers are most likely to accept campaigns and spend more money.
# 

# In[ ]:





# In[ ]:





# In[ ]:




