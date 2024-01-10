#import statements
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.gridspec import GridSpec

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
    selected_entries = merged_df_sorted[merged_df_sorted.year == selected_year]


    
    return merged_df,merged_df_sorted,selected_entries,selected_year

def bar_plot(selected_entries,grid) :
    plt.subplot(grid[0,0])
    top_sup = selected_entries['supplier'].value_counts().nlargest(10)
    sns.barplot(x=top_sup.index, y=top_sup)
    plt.title("Top 10 Product Suppliers in year 2021")
    plt.xlabel("Supplier")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)

def pie_plot(selected_entries,grid) :
    plt.subplot(grid[0,1])
    trans = selected_entries['trans_type'].value_counts()
    top_trans_names = trans.index
    top_trans_counts = trans.values
    explode = [0.3, 0, 0]
    plt.pie(top_trans_counts, labels=top_trans_names, 
            autopct='%1.0f%%', explode = explode)
    plt.title('Types of Payment Methods used in 2021')
    
def lineplot_monthly(selected_entries,grid):
    plt.subplot(grid[0,2])
    top_sup = selected_entries['item_name'].value_counts().nlargest(10)
    selected_entries['date_only'] = pd.to_datetime(selected_entries['date_only'],
                                                   format='%Y-%m-%d')
    selected_entries_filter = selected_entries.loc[selected_entries
                                            ["item_name"].isin(top_sup.index) ]
    selected_entries_filter['month'] = selected_entries_filter['date_only'].dt.month
    table = pd.pivot_table(selected_entries_filter, values='quantity', 
                           index=['item_name'],
                       columns=['month'], aggfunc="sum")
    print(table)
    selected_entries['month'] = selected_entries['date_only'].dt.month
    monthly_data = selected_entries.groupby('month')['quantity'].sum()
    print(table.iloc[0,:].values)
    print(table.columns)
    sns.lineplot(y=table.iloc[0,:].values,x=table.columns,
                 marker='o', label = table.index[0] )
    sns.lineplot(y=table.iloc[1,:].values,x=table.columns,
                 marker='o', label = table.index[1] )
    sns.lineplot(y=table.iloc[2,:].values,x=table.columns,
                 marker='o', label = table.index[2] )
    sns.lineplot(y=table.iloc[3,:].values,x=table.columns,
                 marker='o', label = table.index[3] )
    sns.lineplot(y=table.iloc[4,:].values,x=table.columns,
                 marker='o', label = table.index[4] )
    plt.title('Monthly Trend for Top Products in year 2021')
    plt.legend()
    plt.xlabel('Months')
    plt.ylabel('Number of Products sold')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
 
    
def bar_plot_one(selected_entries,grid) :
    plt.subplot(grid[1,2])
    top_sup = selected_entries['item_name'].value_counts().nlargest(10)
    sns.barplot(x=top_sup, y=top_sup.index)
    plt.title("Top 10 Products sold in 2021")
    plt.xlabel("Count")
    plt.ylabel("Products")
    
def data_info() :
     plt.subplot(grid[1,0])
     text = "Key Note\n\n"\
           "This dashboard is comprehensive study of\n"\
           "E_commerce trade in india\n"\
           "about the top selling products and the top suppliers\n"\
           "which provides us uderstanding of in demand products in India"
     plt.text(0.1 , 0.1 , text , ha='left' , va='center' , fontsize=12 ,
             fontstyle='italic' , fontweight='bold')
     plt.axis('off')
     plt.subplot(grid[1 , 1])
     text = "Student Name: Omkar Shashikant Sawant\n" \
           "Student ID: 22080770"
     plt.text(0.1 , 0.1 , text , ha='center' , va='center' , fontsize=12,
             fontstyle='italic' , fontweight='bold')
     plt.axis('off')
     fig.suptitle('E-Commerce Data Analysis for Year 2021' ,
                  fontsize=25 , fontweight='bold')
    
     
#Main Function
merged_df,merged_df_sorted,selected_entries,selected_year = file_name("file")
print(merged_df.head)
print(merged_df_sorted["date_only"])
print(selected_entries)
merged_df.to_csv('merged_data.csv', index=False)
merged_df_sorted.to_csv('sorted_data.csv', index = False)
selected_entries.to_csv(f'selected_entries_{selected_year}.csv', index=False)
sns.set_theme()
fig = plt.figure(figsize=(20,10),dpi= 300)
grid = GridSpec(2,3, width_ratios=[1,1,1], height_ratios=[1,1])
bar_plot(selected_entries,grid)
pie_plot(selected_entries,grid)
lineplot_monthly(selected_entries,grid)
bar_plot_one(selected_entries,grid)
data_info()
fig.savefig("22080770.png", dpi=300)