# -*- coding: utf-8 -*-
"""
Created on Sat May 18 06:53:16 2019

@author: Leon.An

Subject : OKEX Crypto Currency Analysis Tool  

Version : V1.0


/***/
    Author's murmur : 
    #define isNot !=          
    #define Is    ==            --> Why Python can't use 'define' marco PreCompiler ?! 
    #define Add(a,b)  (a+b)    
    #const Var                  --> Even have no 'const' keyword ? 
/***/

"""

import requests          as Req

class OKEX(object):        
    
    def __init__(self):        
        pass    
    __Session    = Req.session()
    __Header     = {'Accept': 'application/json' ,'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36' }
    __Basic_URL  = 'https://www.okex.com/api/spot/v3/instruments/'
    
    class Param():
        # 貨幣ID
        BTC_ID = 'BTC-USDT'
        ETH_ID = 'ETH-USDT'
        LTC_ID = 'LTC-USDT'    
    
    def Ticker(self , 貨幣):
        #define
        賣方最高價   = 'best_ask'
        買方最高價   = 'best_bid'
        最新成交價   = 'last'
        一天內最高   = 'high_24h'
        一天內最低   = 'low_24h'
        此次開盤價   = 'open_24h'
        一天內基礎量 = 'base_volume_24h'   
        
        #轉成字串
        貨幣名稱 = str(貨幣)
        
        Ticker_Api = self.__Basic_URL + 貨幣名稱 + '/ticker'
           
        抓到的原始資料 = self.__Session.get(Ticker_Api , headers = self.__Header)
        要分析的資料   = 抓到的原始資料.json()
            
        
        print('一天內基礎量'  , 要分析的資料[一天內基礎量])
        print('此次開盤價'    , 要分析的資料[此次開盤價])
        print('一天內最低'    , 要分析的資料[一天內最低])
        print('一天內最高 : ' , 要分析的資料[一天內最高])
        print('賣方最高價'    , 要分析的資料[賣方最高價])
        print('買方最高價'    , 要分析的資料[買方最高價])
        print('最新成交價'    , 要分析的資料[最新成交價])        
    
    
    
    def 成交價分析(self , 貨幣 , 幾筆資料 = 100 ,巨量設定值 = 120, 巨量監控模式 = True ,顯示 = False , 成交量有效值 = 5 ):        
        
        抓幾筆 = str(幾筆資料)
        成交Api  = self.__Basic_URL + 貨幣 + '/trades?limit=' + 抓幾筆
                
        成交資料 = self.__Session.get(成交Api, headers = self.__Header)
        成交資料 = 成交資料.json()    

        
        成交均價 = float(0)    
        
        
        一般成交價格 = []
        一般成交數量 = []
        巨量成交價格 = []
        巨量成交數量 = []
        
        Counter = int(0)
        if(顯示):
            print('----------- 成交價分析 --------------')
            print('有效值為 : 5 個以上',貨幣,'交易量')
            if(巨量監控模式):
                print('開啟巨量監控模式，超過',巨量設定值,'個',貨幣,'才會顯示')
                
        for 索引 in range(0,len(成交資料)):
            if(巨量監控模式): 
                if(float(成交資料[索引]['size']) > 巨量設定值):
                    巨量成交價格.append(成交資料[索引]['price']) 
                    巨量成交數量.append(成交資料[索引]['size']) 
                    if (顯示):
                        print('巨量成交價格:' ,成交資料[索引]['price'] , '巨量成交數量:' ,成交資料[索引]['size'])                                             
            else:
                if(float(成交資料[索引]['size']) > 成交量有效值):
                    # /* 把資料存起來 */
                    一般成交價格.append(成交資料[索引]['price']) 
                    一般成交數量.append(成交資料[索引]['size'])
                    
                    # /* 計算平均價格 */
                    成交均價 += 成交資料[索引]['price'] 
                    Counter = Counter +1 
                    
                    if(索引 == (len(成交資料) - 1)):
                        成交均價 = 成交均價 / Counter                    
                    
                    #/* 如果顯示有打開的話 */
                    if (顯示):
                        print('成交價格:' , 成交資料[索引]['price'] , '成交數量:' ,成交資料[索引]['size'])    

            巨量資料 = {'巨量資料':{'價格':成交資料[索引]['price'] , '數量':成交資料[索引]['size']}}
            
            
            if(巨量監控模式):
                return
            
    def 漲跌幅度偵測(self,巨量漲跌 = False , 幾分鐘內 = 10):
        #/* Variables */
        #漲跌門檻幾%
        
        pass
    

    """
    @  Describe   - Analyze Trade information and detect the range between high price and low price 
                  - The order quantity must reach a certain value to be considered as a valid value. 
                    --> Default is 20 (Volume_Filter = int(20))
    @  Parameters - Currency     : Please refer to OKEX --> Parameters --> Currency_ID  
                    HowManyData  : Get how many sample to do average , default is 100 
                    Huge_Vol     : How Many volume could be see as 'huge volume'
                    Huge         : Enable Hugh Detect Mode
                    Console      : Display on screen          
    @  Output     - filtered price and volume     
    """

    def Trade_Scanner(self , Currency , HowManyData = 100 , Huge_Vol = 120 , Huge = False , Console = False):
         # /* Define Index */ 
        Price    = 0
        Volume   = 1        

        # /* Type Convert */
        HowManyData = int(HowManyData)
        Data_Size   = str(HowManyData)         
        Currency_ID = str(Currency)

        # /* Parameters */
        Precision     = str(0.01)
        Volume_Filter = int(20) 

        # /* Get Data Through Website Restful Api */
        API      = self.__Basic_URL + Currency_ID + '/book?size=' + Data_Size + '&' + 'depth=' + Precision
        Raw_Data = self.OKEX_Get(API)    

        # /* Variables (List)*/
        Buyer_Price     = []
        Buyer_Volume    = []
        Seller_Price    = []
        Seller_Volume   = []

        # /* Variables (Float) */
        Sell_Pressure_Price = float(0)  
        Buy_Support_Price   = float(0)

        # /* Huge Volume detect Variables */
        Huge_Buy_Price   = []
        Huge_Buy_Volume  = []
        Huge_Sell_Price  = []
        Huge_Sell_Volume = []
        
        # /* Volume Filter */
        for i in range(0 , HowManyData):            
            if((float(Raw_Data['asks'][i][Volume]) > Volume_Filter)):
                Seller_Price.append (float(Raw_Data['asks'][i][Price]))
                Seller_Volume.append(float(Raw_Data['asks'][i][Volume]))
            if((float(Raw_Data['bids'][i][Volume]) > Volume_Filter)):
                Buyer_Price.append (float(Raw_Data['bids'][i][Price]))
                Buyer_Volume.append(float(Raw_Data['bids'][i][Volume]))

            # /* Enable Huge Volume Detector */
            if(Huge):
                if((float(Raw_Data['asks'][i][Volume]) > Huge_Vol)):
                    Huge_Sell_Price.append (float(Raw_Data['asks'][i][Price]))
                    Huge_Sell_Volume.append(float(Raw_Data['asks'][i][Volume]))
                if((float(Raw_Data['bids'][i][Volume]) > Huge_Vol)):       
                    Huge_Buy_Price.append(float(Raw_Data['bids'][i][Price]))
                    Huge_Buy_Volume.append(float(Raw_Data['bids'][i][Volume]))
                
        # /* Prevent The Index out of range */        
        if(len(Buyer_Price) != len(Seller_Price)):
            Display_Vol = min(len(Buyer_Price),(len(Seller_Price))) 
        else:
            Display_Vol = len(Buyer_Price)     

        # /* Console */       
        if(Console):
            print('---------賣方支撐-------------         ----------買方支撐-------------')
        for i in range(0 , Display_Vol):
            if (Console):
                print('價格:' , round(Seller_Price[i],2) , '數量:' , round(Seller_Volume[i],2),' \t\t ','價格:' , round(Buyer_Price[i],2) , '數量:' , round(Buyer_Volume[i],2))
            
            # /* Store the Value */
            Sell_Pressure_Price += Seller_Price[i]
            Buy_Support_Price   += Buyer_Price[i]
            if(i == (Display_Vol - 1)):
                if (Console):
                    print()
                Sell_Pressure_Price = (Sell_Pressure_Price / Display_Vol)
                Buy_Support_Price   = (Buy_Support_Price   / Display_Vol)
        
        if (Console):
            print('賣方超級壓力均值 : ' ,round(Sell_Pressure_Price,2) , '\t\t','買方超級支撐均值:',round(Buy_Support_Price,2))
        
        if (Console):
            if(Huge):
                print('\r\n============賣方超級支撐==========\r\n')
                for i in range(0,len(Huge_Sell_Price)):
                    print('賣方超級壓力:',round(Huge_Sell_Price[i],2)  , '數量:' , round(Huge_Sell_Volume[i],2))        
                print('\r\n============買方超級支撐==========\r\n')
                for i in range(0,len(Huge_Buy_Price)):
                    print('買方超級支撐:',round(Huge_Buy_Price[i],2), '數量:' , round(Huge_Buy_Price[i],2))
                
        #/* Return Data */
        if(Huge):
            Return_Data = {'Buyer' :{'Price':Buyer_Price , 'Volume' : Buyer_Price ,'Huge_Support_Price' :Huge_Buy_Price  ,'Huge_Support_Volume' :Huge_Buy_Volume } ,  \
                           'Seller':{'Price':Seller_Price, 'Volume' : Seller_Price,'Huge_Pressure_Price':Huge_Sell_Price ,'Huge_Pressure_Volume':Huge_Sell_Volume}}
            return Return_Data
        else:
            Return_Data = {'Buyer':{'Price':Buyer_Price,'Volume':Buyer_Volume,'Seller':{'Price':Seller_Price,'Volume':Seller_Volume,}}}                       
            return Return_Data

    """
    @  Describe   - Get averages price of specific currency 
    @  Parameters - Currency     : Please refer to OKEX --> Parameters --> Currency_ID  
                    HowManyData  : Get how many sample to do average , default is 10 , it's means market expected price          
    @  Output     - Dict , 'TWD_Price' , 'USD_Price'    
    
    """

    def Get_Average(self , Currency , HowManyData = 10 , Console = False):
        # Index 
        Price      = 0
#       Volume     = 1
#       Order_Number    = 2 //I have no idea about this  

        # /* Type convert */
        HowManyData = int(HowManyData)
        Currency_ID = str(Currency)
        Data_Size   = str(HowManyData) 

        # /* Region Parameters */#        
        Precision   = str(0.01)
    
        # /* Get data through website restful api */
        API = self.__Basic_URL + Currency_ID + '/book?size=' + Data_Size + '&' + 'depth=' + Precision                
        Raw_Data = self.OKEX_Get(API)
                
        # /* Declare variables , It's my personal habit , Because of C language */        
        Buyer_Averages  = float(0)
        Seller_Averages = float(0)
        
        # /* Sampling */
        for i in range(0 , HowManyData):
            Buyer_Averages  += float(Raw_Data['asks'][i][Price])
            Seller_Averages += float(Raw_Data['bids'][i][Price])
            
        # /* Calculating Averages */
        Buyer_Averages  = round((Buyer_Averages  / HowManyData) , 2) 
        Seller_Averages = round((Seller_Averages / HowManyData) , 2)  

        # /* Console */
        if(Console):      
            print('買方平均價 : ' , Buyer_Averages)
            print('賣方平均價 : ' , Seller_Averages)

        # /* Return */    
        Return_Data = {'Buyer_Avg':Buyer_Averages,'Seller_Avg':Seller_Averages}        
        return Return_Data


    """
    @  Describe   - Get the lately currency price
    @  Parameters - Currency : please refer to OKEX --> Parameters --> Currency_ID                  
    @  Output     - Dict , 'TWD_Price' , 'USD_Price'    
    
    """

    def Lately_Price(self,Currency, Console = False):
        # /*Parameters */
        if(type(Currency) != str): 
            print('OKEX -> Lately_Price(Prarmeter) Currency type was wrong ')

        # Get Raw Data through Website Restful Api
        Ticker_Api = self.__Basic_URL + Currency + '/ticker'        
        Raw_Data   = self.OKEX_Get(Ticker_Api)

        # Get Usdt rates       
        Usdt = round(self.Get_Usdt_Rate(),2)

        TWD_Price = round(float(Raw_Data['last']),2) * round(Usdt,2)
        USD_Price = round(float(Raw_Data['last']),2)

        #/* Console */
        if(Console):       
            print()
            print('------------ OKEX Lately Price ------------')
            print('OKEX ',Currency,'(TWD)：' , TWD_Price)
            print('OKEX ',Currency,'(USD)：' , USD_Price)

        # /* Return */
        Return_Data = {'TWD_Price':TWD_Price , 'USD_Price':USD_Price}
        return Return_Data        

    """
    @  Describe   - Get the usd rate from maicoin.com (Usdt : usd almost is 1 : 1)
    @  Parameters - Sampling : Get many bids and asks data to do average .
                  - Console  : Display on screen or not 
    @  Output     - Average data or raw (sell top 1 + buy top 1) / 2 data.    
    @  Reserved   - 'Usdt Volume' unused , uncomment the code if you want to use it.
    
    """
    def Get_Usdt_Rate(self , Console = False):        
        #/* URL */
        Maicoin_Basic_URL  = 'https://max-api.maicoin.com/api/v2/'
        Maicoin_Usdt_ID    = 'usdttwd'        
        
        #/* Index */
        Price  = 0
        Volume = 1
        
        #/* Parameters */
        Get_How_Many_Datas = str(5)

        # /* Get method */
        API       = Maicoin_Basic_URL + 'depth?market=' + Maicoin_Usdt_ID + '&' + 'limit=' + Get_How_Many_Datas                
        Raw_Data  = self.OKEX_Get(URL = API)
         
        # /* Get the Top of Buyer and Seller Price */ 
        Asks_Usdt_Price  = float(Raw_Data['asks'][-1][Price])
        # Asks_Usdt_Volume = float(Raw_Data['asks'][-1][Volume])
        Bids_Usdt_Price  = float(Raw_Data['bids'][-1][Price])
        # Bids_Usdt_Volume = float(Raw_Data['bids'][-1][Volume])

        # /* Cancel sampling because I found it not necessary */
        Price = ((Asks_Usdt_Price + Bids_Usdt_Price) / 2)

        # /* Console */    
        if (Console):                        
            print('Usdt to TWD :' , Price)

        # /* Return Price */
        return Price
        
    """  
    @  Describe  : Quickly get method
    @  Parameter : Basic_URL + Parameters = Get Request  
    @  Output    : Dictionary type like JSON format 
      
    """ 
    def OKEX_Get(self,URL,Headers = False):
        
        # /* Const */
        Accept_Json = {'Accept':'application/json'}
        User_Agent  = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
            
        # /* Check Parameters is correct or not */        
        if type(URL) != str:
            print('OKEX_Get -> Parameters - > URL -> Error ')
        
        # /* Enable to change Headers */
        if not Headers:
            Headers = dict(Accept_Json,**User_Agent)
        else:
            if (type(Headers) == str):
                pass
            else:
                print('OKEX_Get-> Parameters -> Headers Error')
        
        # /* Send Get Request*/ 
        API         =  str(URL)
        Session     =  self.__Session
        Raw_Data    =  Session.get(API , headers = Headers )
        Raw_Data    =  Raw_Data.json()
        
        # /* Return dictionary (JSON format)*/
        return Raw_Data    

    # /* Show you how to use */
    def Tutorial(self):       
        # OKEX = OKEX()
        self.Get_Usdt_Rate(Console = True)
        self.Lately_Price (OKEX.Param.ETH_ID , Console = True)
        self.Get_Average  (OKEX.Param.ETH_ID , Console = True)
        self.Trade_Scanner(OKEX.Param.ETH_ID , Huge    = True , Console = True)

if __name__ == '__main__':
    OKEX = OKEX()
    OKEX.Tutorial()
    