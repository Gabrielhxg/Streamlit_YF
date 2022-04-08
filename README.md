Hey, this is the 'beta' version of a data science web application.

## **Project Context**

This streamlit app collects live data from Yahoo Finance Markets API, for +80 cryptocurrencies, 
as to answer the following question:

''' 
    For the last **given** days (between 1 and 1000), 
    and for a **given** cryptocurrency Sector (Storage, Descentralized Finance, Privacy, Master Nodes, Media, Logistics, IoT...),
    
    Which portfolio allocation (Ideal Capital Exposition) has presented the best Return/Risk Ratio 
    according to Markowitz's Modern Portfolio Theory?
'''

More about the theory [here](https://www.investopedia.com/terms/s/sharperatio.asp#:~:text=The%20Sharpe%20ratio%20was%20developed,of%20volatility%20or%20total%20risk.).

## **APP Link** 
To access the web app, please open this [link](https://bit.ly/criptoport) in another tab.

## **Beta usability**
As the beta app activates, it shows an **IndexError**, which rises when no cryptocurrency is selected. 

##### **Analysis Steps** | In the menu, left-side column

> **1st Step** | select a crypto Sector (Setores).

> **2nd Step** | Select between **Dollar**-based price or **Bitcoin**-based price (Par).

> **3rd Step** | Select token tickets (Códigos).

> **4th Step** | Select days-range for analysis (Dias de análise).

## **Example** 
Consider your Menu Selection looks like this:

> **1st Step** | Sector: Prvcy (Privacy tokens)

> **2nd Step** | Pair: -usd (Dollar-based price)

> **3rd Step** | Tickets: arrr-usd (Pirate Chain) | chi-usd (Xaya) | pha-usd (Phala Network) | bean-usd (Beanstalk) | sand-usd (The Sendbox) 

> **4th Step** | Days: 31 

## **Result** 
**Names** 

![image](https://user-images.githubusercontent.com/52026781/162519077-990f9a21-991b-49f8-b1ca-0525012d2ca2.png)

**31 days Performance**

![im2](https://user-images.githubusercontent.com/52026781/162516686-161fe1fc-a135-4307-bc79-34849f305d43.png)

**Return on Investment | Standardized for comparisson**

![im3](https://user-images.githubusercontent.com/52026781/162516893-9e523c2b-082e-43b9-9970-8fbfe4602b18.png)

**Annualized Returns, Volatility (risk) and Assets Correlation**

![im4](https://user-images.githubusercontent.com/52026781/162517549-9945555f-1278-4126-b250-78c92e557931.png)

**Ideal Capital Exposition** | Portfolio diversification based on Sharpe-Ratio Optimization and Markowitz Modern Portfolio Theory

![im5](https://user-images.githubusercontent.com/52026781/162517759-eda21dd0-e268-451c-85c7-6657ed1620c7.png)

## **Analysis Conclusion** 
The last table (Proporção) returns the optimal portfolio allocation according to:

![im6](https://user-images.githubusercontent.com/52026781/162525526-175adb33-705d-49ea-bc12-7ed67ff92042.png)

The code gist for the algorithm function is [here](https://gist.github.com/Gabrielhxg/ca3db3617d172323e7e013dfbbcd49bb).

## **Best Crypto-portfolio Allocation - Privacy Sector**
> Pirate Chain | 42,51%

> Xaya | 0,85%

> Phala Network | 36,08%

> Beanstalk | 19,07%

> The Sendbox | 1,50% 

## **Portfolio Return on Investment**
> ROI over 31 days: **40%** 

> Risk over 31 days: **20%** 

## *ps 
To access workflow, the main_app and support scripts, access the **Master Branch** 
