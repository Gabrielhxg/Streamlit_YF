################## REQUIREMENTS ##################
import streamlit as st
import pandas as pd

from pandas.util.testing import assert_frame_equal
from pandas_datareader import data as wb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from scipy.stats import norm
from scipy.optimize import minimize 

import seaborn as sns
import matplotlib.pyplot as plt


############ Tabela de setorização ############
sheet_url = 'https://docs.google.com/spreadsheets/d/1B1n4FOxJofKzA3pwOfioqhyIeZH6WOX77iKw5_VX5Jo/edit#gid=0'
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

M = pd.read_csv(url_1)



#Título
'''### Portfólio cripto'''


#Market sectors
DeFi = M['DeFi'].dropna()
Prvcy = M['Prvcy'].dropna()
MstNodes = M['MstNodes'].dropna()
Media = M['Media'].dropna()
Logistcs_IoT = M['Logistcs_IoT'].dropna()
Storage = M['Storage'].dropna()
Research  = M['Research '].dropna()
Gambl = M['Gambl'].dropna()
CEx = M['Cex'].dropna()
Trsm = M['Trsm'].dropna()
Energy = M['Energy'].dropna()


sector = [DeFi, Prvcy, MstNodes, Media, Logistcs_IoT, Storage, Research, Gambl, CEx, Trsm, Energy]
sectorS = [str(each.name) for each in sector]

setor = st.sidebar.selectbox('Setores', sectorS)
par = st.sidebar.selectbox('Par',['-usd','-btc'])

############ Escolha das moedas ############
for each in sector:
    if each.name == setor:
        port = st.sidebar.multiselect('Códigos', [(cada+par) for cada in each])

cdg = []
nm  = []
for each in port:
    names   = str(wb.get_quote_yahoo(each)['shortName']).split()
    nu      = names[1]
    names   = str(nu)
    cdg.append(each)
    nm.append(names)

port = pd.DataFrame(cdg,index = nm, columns=['Códigos'])

my_expander = st.expander(label='Moedas')
with my_expander:
    st.dataframe(port)

############ Função de parâmetros temporais para o request ############
from funcoes_suporte import *

# taking input as analysis period
slider = st.sidebar.slider('Dias de análise:', 1, 1000)
port_ind = Indicadores(port, par, slider)
performance = port_ind[0].drop(columns=['Códigos'])
pa = port_ind[1]

f'''Últimos {slider} dias'''
my_expander = st.expander(label='Performance')
with my_expander:
    st.dataframe(performance.style.format("{:.2f}"))

#### Gráficos #####
my_expander = st.expander(label='Price Action')
with my_expander:
    st.line_chart(pa)
    '''Normalized'''
    st.line_chart(pa/pa.iloc[0]*100)

my_expander = st.expander(label='Retorno, risco e correlação')
with my_expander:
    info = RetornoRisco(pa)
    AnRet= info[0]
    Corr = info[1]
    Vol = info[2]

    '''Retorno anualizado'''
    st.dataframe(AnRet.style.format("{:.4}"))

    '''Correlação entre os ativos'''
    st.dataframe(Corr)
    if st.checkbox("Heatmap"):
        fig, ax = plt.subplots()
        sns.heatmap(Corr, ax=ax)
        st.write(fig)

    #f'''Volatilidade do Portfólio: {round(Vol,2)*100}%'''
'''Otimização do portfolio'''
my_expander = st.expander(label='Exposição Ideal | Simulação de 15 mil portfólios')
with my_expander:
    max = Otimizacao(pa)
    expectedVol = max[0]
    expectedReturn = max[1]
    shrprt = max[2]
    maxIndex = max[3]
    opt_port_vol = max[4][:4]
    opt_port_ret = max[5][:4]
    wts_df = max[6]
    
    
    

    ### Plotting | Sharpe Ratio máximo ###
    fig, ax = plt.subplots(figsize = (20,6))
    ax.scatter(expectedVol,expectedReturn, c = shrprt)
    ax.set_xlabel('Risco | volat.')
    ax.set_ylabel('Retorno')
    ax.scatter(expectedVol[maxIndex],expectedReturn[maxIndex], c = 'red')
    st.write(fig) 
    st.dataframe(wts_df.style.format("{:.2%}"))
    
    f'''Portfólio ideal

    Retorno: {opt_port_ret} %MoM
    Volatilidade: {opt_port_vol} %MoM
    '''