# -*- coding: UTF-8 -*-

# @Time    : 2021/8/2 13:08
# @Author  : IrvingBei
# @File    : main.py
# @Software: PyCharm

import os
import pandas as pd
import xlrd

def read_dictionary(dictionary_path):
    # read from dictionary
    file_list=os.listdir(dictionary_path)
    print(f"the number of files is: {len(file_list)} as follow:")
    result=[]
    for one in file_list:
        print(one)
        if "xls" in one or "xlsx" in one:
            result.append(one)
        else:
            print(f"{one} is not a excel file,ignored")
    return result

def read_files(file_list):
    # read table from every file
    # all_df=pd.DataFrame({"number":[1],"city":[1],"type":[1]})
    all_df=pd.DataFrame()

    for one_file in file_list:
        df = pd.read_excel("./excel_file/"+one_file)

        # 要求必须有列名，则不需要重新命名
        # df=df.rename(columns={0:'number',1:'city',2:"type"})

        # 添加一个字段
        df.insert(0,"文件名",[f"{one_file}"]*(df.shape[0]))

        # merge
        all_df=pd.concat([all_df,df],ignore_index=True)

    return all_df


def find_dup_item(df,col_list):

    # 判断是否重复
    cond=df.loc[:, col_list].duplicated(keep=False)
    # 获取重复的项
    df_duplicate_item = df[cond]
    return df_duplicate_item



def get_col(df):
    col_list = list(df.columns)
    col_i_x = [(i, x) for i, x in enumerate(col_list)]
    print("序号 列名")
    print(col_i_x)
    # 获取需要判断重复的列号，通过列号获取列名
    col = input("请输入需要去重的列序号（多列请用空格隔开）：")
    col_num_list = [int(i) for i in col.split()]
    # 判断输入是否合法
    for one in col_num_list:
        if one >= len(col_list):
            exit("输入不正确！")
    col_get = [col_list[one] for one in col_num_list]

    return  col_get


def drop_duplicates(df,col_get):

    # inplace=True
    df.drop_duplicates(subset=col_get,inplace=True)
    return df

def data_write(df,filename):
    # index=False
    df.to_excel(f"{filename}.xlsx", index=False)

if __name__ == '__main__':

    # set dir path
    dictionary_path="./excel_file"

    # get all file name in excel_file dictionary
    file_list=read_dictionary(dictionary_path)

    # get all data in file_list
    df=read_files(file_list)

    # get col to compare
    col_list=get_col(df)

    # find duplicate
    df_dup=find_dup_item(df,col_list)
    data_write(df_dup,"df_dup")

    # drop_duplicates
    df=drop_duplicates(df,col_list)

    # write to excel
    data_write(df,"out")

    print("finished!")