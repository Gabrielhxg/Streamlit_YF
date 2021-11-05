################## REQUIREMENTS ##################
import streamlit as st
import pandas as pd
import numpy as np

from datetime import date, datetime, timedelta
from scipy.stats import norm
from scipy.optimize import minimize 

from pandas.util.testing import assert_frame_equal
from pandas_datareader import data as wb




############ parâmetors de tempo ############
# Função para parâmetros de tempo

def temp(slider):
    # taking today's date
    hoje = str(date.today()) #2021-04-08
    
    # carry out conversion between string to datetime object
    today = datetime.strptime(hoje, "%Y-%m-%d")
    
    # calculating start date by subtracting n days
    start = today + timedelta(days = -slider)
    return start


############ Indicadores da análise ############
# Função para Indicadores de performance | YF 

@st.cache
def Indicadores(port, Par, slider):
    
    dates = temp(slider)
    C = dates
    today = date.today()
    hist= pd.DataFrame()

    
    for T in port['Códigos']:
        hist[T] = wb.DataReader((T), data_source='yahoo', start=C, end=today)['Adj Close']
        
        
    ###### DataReader ########
    ci = []
    ca = []
    mult = []
    MktcapY = []
    CirSup = []

    if Par == '-usd':
        for i in port['Códigos']:
            histo = hist[i].dropna()
            CI = histo[0] #Cotação Inicial
            ci.append(CI)
         
            CA = histo[-1] #Cotação Atual
            CA = float("{0:.4f}".format(CA))
            ca.append(CA)
            
            Mult = CA/CI   #Múltiplo Total
            Mult = float("{0:.2f}".format((Mult-1)*100))
            mult.append(Mult)
           
            MCy = wb.get_quote_yahoo(i)['marketCap'] #Mkt Cap Yahoo
            mc = MCy[0] /1000000000
            mc = float("{0:.6f}".format(mc))
            MktcapY.append(mc)
            
            cs = (MCy / CA) / 1000000000  #Circulating Supply
            cs = float("{0:.2f}".format(cs[0]))
            CirSup.append(cs)

            ###### Returns Papeis ####### Add to port ####### 
        port['Preço Inicial | USD']  = ci
        port['Preço Atual | USD'] = ca
        port['Valorização | %'] = mult 
        port['Market Cap em Bi'] = MktcapY
        port['Circulação em Bi'] = CirSup
    
    else:
        for i in port['Códigos']:
            histo = hist[i].dropna()
            CI = histo[0] * 100000000 #Cotação Inicial em satoshis (1/100milhões bitcoin)
            ci.append(CI)
        
            CA = histo[-1] * 100000000 #Cotação Atual em satoshis
            CA = float("{0:.4f}".format(CA))
            ca.append(CA)
                
            Mult = CA/CI   #Múltiplo Total
            Mult = float("{0:.2f}".format((Mult-1)*100))
            mult.append(Mult)
            
            MCy = (wb.get_quote_yahoo(i)['marketCap'])  #Mkt Cap Yahoo em satoshis
            mc = float("{0:.2f}".format(MCy[0]))
            MktcapY.append(mc)
                
            cs = (mc*100000000) / CA #Circulating Supply
            cs = float("{0:.2f}".format(cs))
            CirSup.append(cs)

        ###### Returns Papeis ####### Add to port ####### 
        port['Preço Inicial | Satoshis']  = ci
        port['Preço Atual | Satoshis'] = ca
        port['Valorização | %'] = mult 
        port['Market Cap em BTC'] = MktcapY
        port['Circulação em Bi'] = CirSup  
   
    P = port.sort_values(by=['Valorização | %'],ascending=True)
   
    return P, hist

############ Retorno, risco e otimização do portfolio escolhido | anualizado ############

def RetornoRisco(hist):
    info = pd.DataFrame()
    
    ### Retornos Simples | portfolio ###     
    returns = (hist/hist.shift(1)) - 1
    annual_returns = returns.mean() * 365
    annual_vol = returns.std() * 365 ** 0.5
    info['Retorno anualizado | %'] = round(annual_returns*100, ndigits=2)
    info['Volatilidade anualizada | %'] = round(annual_vol*100, ndigits=2)
    info['Sharpe Ratio anualizado'] = round((annual_returns/annual_vol), ndigits=2)
    info = info.sort_values(by =['Retorno anualizado | %'])

    ## Covariancia entre 2 assets ## 
    an_cov_matrix = returns.cov()*365
      
    ## Correlação entre 2 assets ## 
    an_corr_matrix = returns.corr()
    
    ### Risco do portfolio | n assets ramdom ###  
    nrAssets = len(hist.columns)
    pesos = np.array(np.random.random(nrAssets))
    pesos /= np.sum(pesos) 
    
    pfolio_vol = (np.dot(pesos.T, np.dot(an_cov_matrix, pesos))) ** 0.5
    
    
    return info, an_corr_matrix, pfolio_vol 

############ Otimização do portfólio ############
def Otimizacao(hist):
    ## Retornos logaritimicos ## 
    log_returns = np.log(hist/hist.shift(1))
    Med = log_returns.mean()
    MoCov = log_returns.cov() * 30
    Corr = log_returns.corr()

    ### Simulação de proporções ###  
    nrPort = 15000
    nrAssets = len(hist.columns)
    weights = np.zeros((nrPort, nrAssets))
    expectedReturn = np.zeros(nrPort)
    expectedVol = np.zeros(nrPort)
    shrprt = np.zeros(nrPort)

    for k in range(nrPort):
        w = np.array(np.random.random(nrAssets))
        w /= np.sum(w) 
        weights[k,:] = w 
        
        ## Expected log return ##
        expectedReturn[k] = np.sum(w * Med)*30
        
        ## Expected volatility ##
        expectedVol[k] = np.sqrt(np.dot(w.T, np.dot(MoCov, w)))
        
        ## Sharpe Ratio ##
        shrprt[k] = expectedReturn[k] / expectedVol[k]
    
    ### Sharpe Ratio | Maximização ###

    #Procura o maior SR no arrey de SR gerados
    maxIndex = shrprt.argmax()
    #Encontra a distribuição da carteira com max SR
    wts = weights[maxIndex,:]
    #tabela de proporções | display 
    wts_df = pd.DataFrame(wts, index = hist.columns, columns = ['Proporção'])


    # a1: expected return da carteira de max SR
    # a2: expected volatility da carteira de max SR
    opt_port_ret = str(round(expectedReturn[maxIndex],ndigits = 3)*100)
    opt_port_vol = str(round(expectedVol[maxIndex],ndigits = 3)*100)
    

    ### Nested functions ###
    ### Minimização de -SR ###        
    def negativeRS(w):
        w = np.array(w)
        R = np.sum(Med * w)
        V = np.sqrt(np.dot(w.T,np.dot(MoCov,w)))
        SR = R/V
        return -1*SR

    def checkSumToOne(w):
        return np.sum(w)-1

    w0 = np.array([1/nrAssets for i in range(nrAssets)])
    constraints = ({'type':'eq','fun':checkSumToOne})
    bounds = []
    for e in w0:
        bd = (0,1)
        bounds.append(bd)

    w_opt = minimize(negativeRS, w0, method = 'SLSQP', bounds = bounds, constraints = constraints)

    
    P = []
    for i in range(len(hist.columns)):
        a = round(w_opt.x[i],ndigits = 2)*100
        P.append(a)
        
    Prop = pd.DataFrame(P, index = hist.columns)
    Prop.columns = ['Proporção ideal | %']

    return expectedVol, expectedReturn, shrprt, maxIndex, opt_port_vol, opt_port_ret, wts_df
    #return Prop, w_opt
    
    
    