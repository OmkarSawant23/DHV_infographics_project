# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 19:45:01 2024

@author: OMKAR
"""

#import statements
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns


def file_name(file) :
    
    customer = pd.read_csv("customer_dim1.csv")
    item = pd.read_csv("item_dim1.csv")
    store = pd.read_csv("store_dim1.csv")
    time = pd.read_csv("time_dim1.csv")
    trans = pd.read_csv("Trans_dim1.csv")
    fact = pd.read_csv("fact_table1.csv")
    
    merged_df = pd.merge(customer,fact,on='coustomer_key', how='left')
    merged_df = pd.merge(merged_df,item,on='item_key', how='left')
    merged_df = pd.merge(merged_df,store,on='store_key', how='left')
    merged_df = pd.merge(merged_df,time,on='time_key', how='left')
    merged_df = pd.merge(merged_df,trans,on='payment_key', how='left')
    
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    merged_df_sorted = merged_df.sort_values(by='date')
    merged_df_sorted['date_only'] = merged_df_sorted['date'].dt.date
    merged_df_sorted = merged_df_sorted.drop(columns=['date'])
    selected_year = 2021
    #selected_entries = merged_df_sorted[merged_df_sorted['year'].merged_df_sorted.year == selected_year]
    selected_entries = merged_df_sorted[merged_df_sorted.year == selected_year]


    
    return merged_df,merged_df_sorted,selected_entries,selected_year

def bar_plot(top_supplier) :
    # Deciding figure size.
    plt.figure(figsize=(20, 15))
    # Producing bar plot using matplotlib.
    top_sup = selected_entries['supplier'].value_counts().nlargest(5)
    sns.barplot(x=top_sup.index, y=top_sup)
    #plt.legend(["DENIMACH LTD","Indo Count Industries Ltd","Friedola 1888 GmbH","CHROMADURLIN S.A.S","HARDFORD AB"],bbox_to_anchor=(1, 0.5))
    plt.title("Top 5 Suppliers")
    plt.xlabel("Supplier")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.show()

def pie_plot(top_product) :
    top_sold = selected_entries['item_name'].value_counts().nlargest(10)
    # plotting pie chart using matplotlib.
    sns.pie(top_sold,
           labels=selected_entries['item_name'], autopct='%1.0f%%')

    # Adding Title for pie chart
    plt.title('top sold item in year 2021')

    
    # displaying plot.
    plt.show()
    
     
#Main Function
merged_df,merged_df_sorted,selected_entries,selected_year = file_name("file")
#print(merged_df.head)
print(merged_df_sorted["date_only"])
print(selected_entries)
merged_df.to_csv('merged_data.csv', index=False)
merged_df_sorted.to_csv('sorted_data.csv', index = False)
selected_entries.to_csv(f'selected_entries_{selected_year}.csv', index=False)
bar_plot("top_supplier")
pie_plot("top_product")
