import pandas as pd
import numpy as np
import elist.elist as elel
import edict.edict as eded
import tlist.tlist as tltl
import copy

#all operations will generate a new Qtable(copy.deepcopy), and will not change the original Qtable 
#columns   col-names-list      no-duplicate-names-permitted
#index     rowname-names-list  no-duplicate-names-permitted

#df                      pd.DataFrame

def _index_map(df):
    d = elel.ivdict(list(df.index))
    return(d)

def _columns_map(df):
    d = elel.ivdict(list(df.columns))
    return(d)

def _name2ilocs(rowname,colname,**kwargs):
    if('index_map' in kwargs):
        index_map = kwargs['index_map']
    else:
        df = kwargs['DF']
        index_map = _index_map(df)
    if('columns_map' in kwargs):
        columns_map = kwargs['columns_map']
    else:
        df = kwargs['DF']
        columns_map = _columns_map(df)
    kl,vl =   eded.d2kvlist(index_map)
    rlocs = elel.indexes_all(vl,rowname)
    kl,vl =   eded.d2kvlist(columns_map)
    clocs = elel.indexes_all(vl,colname)
    return((rlocs,clocs))

# index_map = _index_map(df)
# columns_map = _columns_map(df)
# _getitem(df,rowname,colname,rloc=0,cloc=0)
# rloc relative-row-position
# cloc relative-col-position


def _getitem(df,rowname,colname,*args,**kwargs):
    rlocs,clocs = _name2ilocs(rowname,colname,index_map=kwargs['index_map'],columns_map=kwargs['columns_map'])
    rslt = df.iloc[rlocs,clocs]
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        rloc = args[0]
        cloc = args[1]
        rslt = rslt.iloc[rloc,cloc]
    return(rslt)

def _setitem(df,rowname,colname,value,*args,**kwargs):
    rlocs,clocs = _name2ilocs(rowname,colname,index_map=kwargs['index_map'],columns_map=kwargs['columns_map'])
    rslt = df.iloc[rlocs,clocs]
    args = list(args)
    if(args.__len__()==0):
        rslt = value
    else:
        rloc = args[0]
        cloc = args[1]
        rslt.iloc[rloc,cloc] = value
    df.iloc[rlocs,clocs] = rslt

#rn ---------------------rowname

def _rn2rlocs(rowname,**kwargs):
    if('index_map' in kwargs):
        index_map = kwargs['index_map']
    else:
        df = kwargs['DF']
        index_map = _index_map(df)
    kl,vl =   eded.d2kvlist(index_map)
    rlocs = elel.indexes_all(vl,rowname)
    return(rlocs)

def _row(df,rowname,*args,**kwargs):
    rlocs = _rn2rlocs(rowname,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        rlocs = elel.select_seqs(rlocs,args)
    return(df.iloc[rlocs])

#cn ---------------------colname

def _cn2clocs(colname,**kwargs):
    if('columns_map' in kwargs):
        columns_map = kwargs['columns_map']
    else:
        df = kwargs['DF']
        columns_map = _columns_map(df)
    kl,vl =   eded.d2kvlist(columns_map)
    clocs = elel.indexes_all(vl,colname)
    return(clocs)

def _col(df,colname,*args,**kwargs):
    clocs = _cn2clocs(colname,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        clocs = elel.select_seqs(clocs,args)
    return(df.iloc[:,clocs])

def _get_rlocs(rownames,**kwargs):
    rlocs = []
    for i in range(rownames.__len__()):
        rowname = rownames[i]
        tmp = _rn2rlocs(rowname,**kwargs)
        rlocs = elel.concat(rlocs,tmp)
    rlocs.sort()
    return(rlocs)

def _get_clocs(colnames,**kwargs):
    clocs = []
    for i in range(colnames.__len__()):
        colname = colnames[i]
        tmp = _cn2clocs(colname,**kwargs)
        clocs = elel.concat(clocs,tmp)
    clocs.sort()
    return(clocs)

def _rows(df,*rownames,**kwargs):
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    rlocs = _get_rlocs(rownames,**kwargs)
    return(df.iloc[rlocs])

def _cols(df,*colnames,**kwargs):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    clocs = _get_clocs(colnames,**kwargs)
    return(df.iloc[:,clocs])

def _subtb(df,rownames,colnames,**kwargs):
    rownames = elel.uniqualize(rownames)
    colnames = elel.uniqualize(colnames)
    rlocs = _get_rlocs(rownames,**kwargs)
    clocs = _get_clocs(colnames,**kwargs)
    return(df.iloc[rlocs,clocs])

def _ltd_index_first(ltd,value):
    for i in range(ltd.__len__()):
        if(ltd[i] == value):
            return(i)
        else:
            pass
    raise ValueError("value not exist")

def _ltd_index_last(ltd,value):
    for i in range(ltd.__len__()-1,-1,-1):
        if(ltd[i] == value):
            return(i)
        else:
            pass
    raise ValueError("value not exist")

def _crop(df,top,left,bot,right,**kwargs):
    imd = kwargs['index_map']
    top = _ltd_index_first(imd,top)
    bot = _ltd_index_last(imd,bot)
    cmd = kwargs['columns_map']
    left = _ltd_index_first(cmd,left)
    right = _ltd_index_last(cmd,right)
    rownames = list(df.index[top:bot+1])
    colnames = list(df.columns[left:right+1])
    return(_subtb(df,rownames,colnames,**kwargs))

def _swapcol(df,colname1,colname2,*args,**kwargs):
    df = copy.deepcopy(df)
    clocs1 = _cn2clocs(colname1,**kwargs)
    clocs1.sort()
    clocs2 = _cn2clocs(colname2,**kwargs)
    clocs2.sort()
    args = list(args)
    if(args.__len__()==0):
        which1 = 0
        which2 = 0
    elif(args.__len__()==1):
        which1 = args[0]
        which2 = 0
    else:
        which1 = args[0]
        which2 = args[1]
    cloc1 = clocs1[which1]
    cloc2 = clocs2[which2]
    clocs = elel.init_range(0,df.columns.__len__(),1)
    clocs = elel.iswap(clocs,cloc1,cloc2)
    return(df.iloc[:,clocs])

##############################
##############################


###################################
###################################


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
    df = _append_col(df,*args)
    return(df)

def _repl_cols(df,*args):
    df = _append_cols(df,*args)
    return(df)

def _repl_row(df,*args):
    df = _append_row(df,*args)
    return(df)

def _repl_rows(df,*args):
    df = copy.deepcopy(df)
    df = _append_rows(df,*args)
    return(df)

def _prepend_col(df,*args):
    df = _append_col(df,*args)
    columns = elel.prepend(list(df.columns[:-1]),df.columns[-1])
    df = _reindex_cols(df,columns)
    return(df)

def _prepend_cols(df,*args):
    old_lngth = df.columns.__len__()
    df = _append_cols(df,*args)
    new_lngth = df.columns.__len__()
    columns = elel.concat(list(df.columns[old_lngth:new_lngth]),df.columns[:old_lngth])
    df = _reindex_cols(df,columns)
    return(df)

def _prepend_row(df,*args):
    df = _append_row(df,*args)
    index = elel.prepend(list(df.index[:-1]),df.index[-1])
    df = _reindex_rows(df,index)
    return(df)

def _prepend_rows(df,*args):
    old_lngth = df.index.__len__()
    df = _append_rows(df,*args)
    new_lngth = df.index.__len__()
    index = elel.concat(list(df.index[old_lngth:new_lngth]),df.index[:old_lngth])
    df = _reindex_rows(df,index)
    return(df)

def _rename_cols(df,*colnames):
    df = copy.deepcopy(df)
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df.columns = colnames
    return(df)

def _rename_rows(df,*rownames):
    df = copy.deepcopy(df)
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    df.index = rownames
    return(df)

################


################


# insert 

# mapiv



##################

def _dcd_size(s):
    colnums,rownums = s.lower().split("x")
    colnums = int(colnums)
    rownums = int(rownums)
    return((colnums,rownums))






######

tbl.index_map()
tbl.columns_map()

#####

tbl.subtb(['b','c'],['one','two'])

#
tbl['d','three'] = 'd3'
tbl


#
tbl.crop('b','one','d','three')
tbl


tbl.swap_col("zero","three")
tbl


#
tbl.reindex_cols(['x','y','z','u','v'])

tbl.reindex_cols('x','y','z','u','v')

#
tbl.swap_row("b","d")
tbl
tbl.reindex_rows(['A','B','C','D'])

tbl.reindex_rows('A','B','C','D')


######################
######################
tbl = Qtable(index=['a', 'b', 'c','d','e'],columns=['zero','one', 'two', 'three','four'])
tbl.rmcol("two")
tbl

tbl.rmrow("c")
tbl

tbl.rmcols("one","three")
tbl.rmcols(["one","three"])


tbl.rmrows('a','d')
tbl.rmrows(['a','d'])


#########################3

tbl = Qtable(mat=np.arange(25).reshape((5,5)),index=['a', 'b', 'c','d','e'],columns=['zero','one', 'two', 'three','four'])

tbl.append_col("color",1,2,3,4,5)
tbl.append_col("color",[1,2,3,4,5])
tbl.append_col({"color":[1,2,3,4,5]})


tbl.append_cols("color1",1,2,3,4,5,"color2",11,22,33,44,55)
tbl.append_cols("color1",[1,2,3,4,5],"color2",[11,22,33,44,55])
tbl.append_cols({"color1":[1,2,3,4,5],"color2":[11,22,33,44,55]})

tbl.append_row("f",11,22,33,44,55)
tbl.append_row("f",[11,22,33,44,55])
tbl.append_row({"f":[11,22,33,44,55]})

tbl.append_rows("e",1,2,3,4,5,"f",11,22,33,44,55)
tbl.append_rows("e",[1,2,3,4,5],"f",[11,22,33,44,55])
tbl.append_rows({"e":[1,2,3,4,5],"f":[11,22,33,44,55]})


tbl.repl_col("zero",1,2,3,4,5)
tbl.repl_col("zero",[1,2,3,4,5])
tbl.repl_col({"zero":[1,2,3,4,5]})


tbl.repl_cols("one",1,2,3,4,5,"two",11,22,33,44,55)
tbl.repl_cols("one",[1,2,3,4,5],"two",[11,22,33,44,55])
tbl.repl_cols({"one":[1,2,3,4,5],"two":[11,22,33,44,55]})

tbl.repl_row("c",11,22,33,44,55)
tbl.repl_row("c",[11,22,33,44,55])
tbl.repl_row({"c":[11,22,33,44,55]})

tbl.repl_rows("e",1,2,3,4,5,"d",11,22,33,44,55)
tbl.repl_rows("e",[1,2,3,4,5],"d",[11,22,33,44,55])
tbl.repl_rows({"e":[1,2,3,4,5],"d":[11,22,33,44,55]})



tbl.prepend_col("color",1,2,3,4,5)
tbl.prepend_col("color",[1,2,3,4,5])
tbl.prepend_col({"color":[1,2,3,4,5]})


tbl.prepend_cols("color1",1,2,3,4,5,"color2",11,22,33,44,55)
tbl.prepend_cols("color1",[1,2,3,4,5],"color2",[11,22,33,44,55])
tbl.prepend_cols({"color1":[1,2,3,4,5],"color2":[11,22,33,44,55]})

tbl.prepend_row("f",11,22,33,44,55)
tbl.prepend_row("f",[11,22,33,44,55])
tbl.prepend_row({"f":[11,22,33,44,55]})



tbl.prepend_rows("g",1,2,3,4,5,"f",11,22,33,44,55)
tbl.prepend_rows("g",[1,2,3,4,5],"f",[11,22,33,44,55])
tbl.prepend_rows({"g":[1,2,3,4,5],"f":[11,22,33,44,55]})

>>> df
   zero  zero  one  two  three  four
a     1     0    1    2      3     4
b     2     5    6    7      8     9
c     3    10   11   12     13    14
d     4    15   16   17     18    19
e     5    20   21   22     23    24

//df.insert(0,"zero",[1,2,3,4,5],allow_duplicates=False)

df.loc['x'] = ['x1','x2','x3','x4','x5','x6']
df.reindex_rows


//insert_cols  insert 多次



tbl = pd.DataFrame(np.arange(25).reshape((5,5)),index=['a', 'a', 'c','d','e'],columns=['one','one', 'two', 'three','four'])

//允许有重复行的
>>> tbl
   zero  one  two  three  four
a     0    1    2      3     4
a     5    6    7      8     9
c    10   11   12     13    14
d    15   16   17     18    19
e    20   21   22     23    24


tbl.insert(0,"zero",[1,2,3,4,5],allow_duplicates=True)

>>> tbl
   zero  zero  one  two  three  four
a     1     0    1    2      3     4
a     2     5    6    7      8     9
c     3    10   11   12     13    14
d     4    15   16   17     18    19
e     5    20   21   22     23    24
>>>

>>> tbl['zero']
   zero  zero
a     1     0
a     2     5
c     3    10
d     4    15
e     5    20
>>>
>>>
>>> tbl.loc['a']
   zero  zero  one  two  three  four
a     1     0    1    2      3     4
a     2     5    6    7      8     9
>>>

>>> tbl.T
       a  a   c   d   e
zero   1  2   3   4   5
zero   0  5  10  15  20
one    1  6  11  16  21
two    2  7  12  17  22
three  3  8  13  18  23
four   4  9  14  19  24

T = tbl.T
T.insert(0,"a",[1,2,3,4,5,6],allow_duplicates=True)
T.T



>>> tt['zero']
   zero  zero
a     1     2
a     1     0
a     2     5
c     3    10
d     4    15
e     5    20


>>> np.array(tt.loc['a'])
array([[1, 2, 3, 4, 5, 6],
       [1, 0, 1, 2, 3, 4],
       [2, 5, 6, 7, 8, 9]])



tt.iloc[0] = [11,22,33,44,55,66]


>>> tt
   zero  zero  one  two  three  four
a    11    22   33   44     55    66
a     1     0    1    2      3     4
a     2     5    6    7      8     9
c     3    10   11   12     13    14
d     4    15   16   17     18    19
e     5    20   21   22     23    24


import sldghmmr4nut.ndarr.do as ndo
ndarr = np.array(np.arange(25).reshape((5,5)))

# Single selections using iloc and DataFrame
# Rows:
data.iloc[0] # first row of data frame (Aleshia Tomkiewicz) - Note a Series data type output.
data.iloc[1] # second row of data frame (Evan Zigomalas)
data.iloc[-1] # last row of data frame (Mi Richan)
# Columns:
data.iloc[:,0] # first column of data frame (first_name)
data.iloc[:,1] # second column of data frame (last_name)
data.iloc[:,-1] # last column of data frame (id)

# Multiple row and column selections using iloc and DataFrame
data.iloc[0:5] # first five rows of dataframe
data.iloc[:, 0:2] # first two columns of data frame with all rows
data.iloc[[0,3,6,24], [0,5,6]] # 1st, 4th, 7th, 25th row + 1st 6th 7th columns.
data.iloc[0:5, 5:8] # first 5 rows and 5th, 6th, 7th columns of data frame (county -> phone1).


https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/#iloc-selection

