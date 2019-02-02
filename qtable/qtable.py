import pandas as pd
import numpy as np
import elist.elist as elel
import edict.edict as eded
import copy

#all operations will not change the original df 
#columns   col-names-list      no-duplicate-names-permitted
#index     rowname-names-list  no-duplicate-names-permitted


def _getitem(df,rowname,colname):
    return(df[colname][rowname])

def _setitem(df,rowname,colname,value):
    df.loc[rowname,colname] = value

def _row(df,rowname):
    return(df[rowname:rowname])

def _col(df,colname):
    return(df[[colname]])

def _rows(df,*rownames):
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    return(df.loc[rownames,:])

def _cols(df,*colnames):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    return(df[colnames])

def _index_map(df):
    return(elel.ivmd(list(df.index)))

def _columns_map(df):
    return(elel.ivmd(list(df.columns)))

def _subtb(df,rownames,colnames):
    return(df.loc[rownames,colnames])

def _crop(df,top,left,bot,right):
    imd = _index_map(df)
    cmd = _columns_map(df)
    rownames = df.index[imd[top]:imd[bot]+1]
    colnames = df.columns[cmd[left]:cmd[right]+1]
    return(_subtb(df,rownames,colnames))

def _swapcol(df,colname1,colname2):
    columns = elel.vswap(list(df.columns),colname1,colname2)
    return(df.reindex(columns=columns))

def _reindex_cols(df,*columns):
    columns = list(columns)
    if(isinstance(columns[0],list)):
        columns = columns[0]
    else:
        pass
    return(df.reindex(columns=columns))

def _swaprow(df,rowname1,rowname2):
    index = elel.vswap(list(df.index),rowname1,rowname2)
    return(df.reindex(index=index))

def _reindex_rows(df,*index):
    index = list(index)
    if(isinstance(index[0],list)):
        index = index[0]
    else:
        pass
    return(df.reindex(index=index))

def _rmcol(df,colname):
    df = copy.deepcopy(df)
    df = df.drop(colname,1)
    return(df)

def _rmcols(df,*colnames):
    df = copy.deepcopy(df)
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df = df.drop(colnames,1)
    return(df)

def _rmrow(df,colname):
    df = copy.deepcopy(df)
    df = df.drop(colname,0)
    return(df)

def _rmrows(df,*colnames):
    df = copy.deepcopy(df)
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df = df.drop(colnames,0)
    return(df)

def _append_col(df,*args):
    df = copy.deepcopy(df)
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

def _append_cols(df,*args):
    df = copy.deepcopy(df)
    args = list(args)
    if(isinstance(args[0],dict)):
        col_dicts = args[0]
    else:
        if(isinstance(args[1],list)):
            col_dicts = eded.list2d(args)
        else:
            col_dicts = {}
            l = eded.brkl2d(args,df.index.__len__()+1)
            for d in l:
                k,v = eded.dele2t(d)
                col_dicts[k] = v 
    for colname in col_dicts:
        df[colname] = col_dicts[colname]
    return(df)

def _append_row(df,*args):
    df = copy.deepcopy(df)
    args = list(args)
    if(args.__len__() == 1):
        rowname = list(args[0].keys())[0]
        values = list(args[0].values())[0]
    else:
        rowname = args[0]
        values = args[1]
    df.loc[rowname] = values
    return(df)

def _append_rows(df,*args):
    df = copy.deepcopy(df)
    args = list(args)
    if(isinstance(args[0],dict)):
        row_dicts = args[0]
    else:
        if(isinstance(args[1],list)):
            row_dicts = eded.list2d(args)
        else:
            row_dicts = {}
            l = eded.brkl2d(args,df.columns.__len__()+1)
            for d in l:
                k,v = eded.dele2t(d)
                row_dicts[k] = v 
    for rowname in row_dicts:
        df.loc[rowname] = row_dicts[rowname]
    return(df)

def _repl_col(df,*args):
    df = copy.deepcopy(df)
    df = _append_col(df,*args)
    return(df)

def _repl_cols(df,*args):
    df = copy.deepcopy(df)
    df = _append_cols(df,*args)
    return(df)

def _repl_row(df,*args):
    df = copy.deepcopy(df)
    df = _append_row(df,*args)
    return(df)

def _repl_rows(df,*args):
    df = copy.deepcopy(df)
    df = _append_rows(df,*args)
    return(df)


#####################
#########################
##########################


def _prepend_col(df,*args):
    df = append_col(df,*args)
    columns = elel.prepend(list(df.columns[:-1]),df.columns[-1])
    df = _reindex_cols(df,columns)
    return(df)

def _prepend_cols(df,*args):
    old_lngth = df.columns.__len__()
    df = append_cols(df,*args)
    new_lngth = df.columns.__len__()
    columns = elel.concat(list(df.columns[old_lngth:new_lngth]),df.columns[:old_lngth])
    df = _reindex_cols(df,columns)
    return(df)

def _prepend_row(df,*args):
    df = append_row(df,*args)
    index = elel.prepend(list(df.index[:-1]),df.index[-1])
    df = _reindex_rows(df,index)
    return(df)

def _prepend_rows(df,*args):
    old_lngth = df.index.__len__()
    df = append_rows(df,*args)
    new_lngth = df.index.__len__()
    index = elel.concat(list(df.index[old_lngth:new_lngth]),df.index[:old_lngth])
    df = _reindex_rows(df,index)
    return(df)

################
################


# rename_cols
# rename_rows



#mapv
#mapiv

def dcd_size(s):
    colnums,rownums = s.lower().split("x")
    colnums = int(colnums)
    rownums = int(rownums)
    return((colnums,rownums))

# >>> tbl = Qtable(columns=['one', 'two', 'three','four'],index=['a', 'b', 'c','d'])
# >>>
# >>> tbl
    # one   two three  four
# a  None  None  None  None
# b  None  None  None  None
# c  None  None  None  None
# d  None  None  None  None



class Qtable():
    def __init__(self,**kwargs):
        self.columns = kwargs['columns']
        self.index = kwargs['index']
        self.colnums = self.columns.__len__()
        self.rownums = self.index.__len__()
        if("mat" in kwargs):
            mat = kwargs['mat']
        else:
            mat = np.full((self.rownums,self.colnums),None)
        self.df = pd.DataFrame(mat, columns=self.columns,index=self.index)
    def __repr__(self):
        return(self.df.__repr__())
    def __getitem__(self,*args):
        rowname,colname = list(args)[0]
        return(_getitem(self.df,rowname,colname))
    def __setitem__(self,*args):
        args = list(args)
        rowname,colname = args[0]
        value = args[1]
        return(_setitem(self.df,rowname,colname,value))
    def row(self,rowname):
        return(_row(self.df,rowname))
    def col(self,colname):
        return(_col(self.df,colname))
    def rows(self,*rownames):
        return(_rows(self.df,*rownames))
    def cols(self,*colnames):
        return(_cols(self.df,*colnames))
    def index_map(self):
        return(_index_map(self.df))
    def columns_map(self):
        return(_columns_map(self.df))
    def subtb(self,rownames,colnames):
        return(_subtb(self.df,rownames,colnames))
    def crop(self,top,left,bot,right):
        return(_crop(self.df,top,left,bot,right))
    def swapcol(self,colname1,colname2):
        return(_swapcol(self.df,colname1,colname2))
    def reindex_cols(self,*columns):
        return(_reindex_cols(self.df,*columns))
    def swaprow(self,rowname1,rowname2):
        return(_swaprow(self.df,rowname1,rowname2))
    def reindex_rows(self,*index):
        return(_reindex_rows(self.df,*index))
    def rmcol(self,colname):
        return(_rmcol(self.df,colname))
    def rmcols(self,*colnames):
        return(_rmcols(self.df,*colnames))
    def rmrow(self,colname):
        return(_rmrow(self.df,colname))
    def rmrows(self,*colnames):
        return(_rmrows(self.df,*colnames))
    def append_col(self,*args):
        return(_append_col(self.df,*args))
    def append_cols(self,*args):
        return(_append_cols(self.df,*args))
    def append_row(self,*args):
        return(_append_row(self.df,*args))
    def append_rows(self,*args):
        return(_append_rows(self.df,*args))
    def repl_col(self,*args):
        return(_repl_col(self.df,*args))
    def repl_cols(self,*args):
        return(_repl_cols(self.df,*args))
    def repl_row(self,*args):
        return(_repl_row(self.df,*args))
    def repl_rows(self,*args):
        return(_repl_rows(self.df,*args))

