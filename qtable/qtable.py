#cnl   col-names-list  no-duplicate-names
#rnl   rowname-names-list  no-duplicate-names

#init
import pandas as pd
import numpy as np
import elist.elist as elel
import edict.edict as eded


#df = pd.DataFrame(np.arange(16).reshape((4,4)), columns=['one', 'two', 'three','four'],index=['a', 'b', 'c','d'])


#rowname col
def _getitem(df,rowname,colname):
    return(df[colname][rowname])

def _setitem(df,rowname,colname,value):
    df.loc[rowname,colname] = value

#swapcol
#df = df.reindex(columns=['four','one', 'two', 'three'])

def _swapcol(df,col1,col2):
    columns = elel.vswap(list(df.columns),col1,col2)
    return(df.reindex(columns=columns))

def _reindex_cols(df,columns):
    return(df.reindex(columns=columns))


#swaprowname
#df.reindex(index=['b','a','c','d'])
def _swaprow(df,rowname1,rowname2):
    index = elel.vswap(list(df.index),rowname1,rowname2)
    return(df.reindex(index=index))

def _reindex_rows(df,index):
    return(df.reindex(index=index))

#col

def _col(df,colname):
    return(df[[colname]])

#cols
def _cols(df,*colnames):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    return(df[colnames])


#row

def _row(df,rowname):
    return(df[rowname:rowname])

#rows

def _rows(df,*rownames):
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    return(df.loc[rownames,:])

#_subtb(df,["b","c"],["two","four"])

def _subtb(df,rownames,colnames):
    return(df.loc[rownames,colnames])

#####################

def _columns_map(df):
    return(elel.ivmd(list(df.columns)))

def _index_map(df):
    return(elel.ivmd(list(df.index)))

#############################################
#_insert_col(df,"color",["r","g","b","a"])
#_insert_col(df,{"color":["r","g","b","a"]})
#_insert_col(df,'color','a','b','c','d')
#要知道当前的index 排列
#elel.batsorted(referer,l1,l2,l3)

#df = pd.DataFrame(np.arange(16).reshape((4,4)), columns=['one', 'two', 'three','four'],index=['a', 'b', 'c','d'])


def _insert_col(df,*args):
    args = list(args)
    if(args.__len__() == 1):
        colname = list(args[0].keys())[0]
        values = list(args[0].values())[0]
    else:
        colname = args[0]
        if(isinstance(args[1],list)):
            values = args[1]
        else:
            values = args[1:]
    df[colname] = values
    return(df)

# ###################################################################
# _insert_cols(df,"color1","r1","g1","b1","a1","color2","r2","g2","b2","a2")

def _insert_cols(df,*args):
    args = list(col_dicts)
    if(isinstance(args[0],dict)):
        col_dicts = args[0]
    else:
        if(isinstance(args[1],list)):
            col_dicts = eded.list2d(args)
        else:
            col_dicts = eded.brkl2d(args,df.index.__len__()+1)
    for colname in col_dicts:
        df[colname] = col_dicts[colname]
    return(df)


#insert_row
#df.loc["e"] = [2, 3, 4,5]
def _insert_row(df,*args):
    args = list(args)
    if(args.__len__() == 1):
        rowname = list(args[0].keys())[0]
        values = list(args[0].values())[0]
    else:
        rowname = args[0]
        values = args[1]
    df.loc[rowname] = values
    return(df)


#insert_rows
def _insert_rows(df,*args):
    args = list(row_dicts)
    if(isinstance(args[0],dict)):
        row_dicts = args[0]
    else:
        if(isinstance(args[1],list)):
            row_dicts = eded.list2d(args)
        else:
            row_dicts = eded.brkl2d(args,df.columns.__len__()+1)
    for rowname in row_dicts:
        df[rowname] = row_dicts[rowname]
    return(df)


################
################

def _rmcol(df,colname):
    df = df.drop(colname,1)
    return(df)

def _rmcols(df,*colnames):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df = df.drop(colnames,1)
    return(df)


def _rmrow(df,colname):
    df = df.drop(colname,0)
    return(df)

def _rmrows(df,*colnames):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df = df.drop(colnames,0)
    return(df)


def _replcol(df,*args):
    df = _insert_col(df,*args)
    return(df)

def _replcols(df,*args):
    df = _insert_cols(df,*args)
    return(df)

def _replrow(df,*args):
    df = _insert_row(df,*args)
    return(df)

def _replrows(df,*args):
    df = _insert_rows(df,*args)
    return(df)



#mapv
#mapiv

class Qtable():
    def __init__():
        pass        



