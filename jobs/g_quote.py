#// we need the date time module 
from datetime import datetime

class GenerateQuote:
    
    # .. overide the init function
    def __init__(self, vSize, distance, helpers, floors, job_date, shuttle):
        
        # .. discount 
        self.off_peak_discount = 5 # // percent 
        self.lDistance = 100 # kms
        self.tGateFee = 0.0
     
        # onpeak 
        self.peakDays = [25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5]
        self.date = job_date 
        self.distance = distance

        # set shuttle 
        self.shuttleOptions = {
            0.0: 0,
            1.0: 900,
            2.0: 900,
            3.0: 1800,
        }.get(float(shuttle))

        # ... params 
        self.sDistanceParams = { 
            #key   base, pricePerKM,    HelperFee,   floorFee,   tall gate 
            1.0: [420,  13.0*distance, 110*helpers, 50*floors,  self.tGateFee, 0.0],
            1.5: [480,  14.0*distance, 120*helpers, 60*floors,  self.tGateFee, 0.0],
            4.0: [1950, 26.0*distance, 230*helpers, 120*floors, self.tGateFee, self.shuttleOptions],
            8.0: [3450, 42.0*distance, 280*helpers, 160*floors, self.tGateFee, self.shuttleOptions]
        }\
        .get(float(vSize))
        
        # ... long term movement 
        self.lDistanceParams = {
            #key   base, pricePerKM,    HelperFee,   floorFee,   tall gate 
            1.0: [200,  15.5*distance, 150*helpers, 50*floors,  self.tGateFee, 0.0],
            1.5: [300,  17.0*distance, 200*helpers, 60*floors,  self.tGateFee, 0.0],
            4.0: [1950, 26.0*distance, 230*helpers, 120*floors, self.tGateFee, self.shuttleOptions],
            8.0: [3450, 42.0*distance, 280*helpers, 160*floors, self.tGateFee, self.shuttleOptions]
        }\
        .get(float(vSize))

    
        
    # ... check off peak 
    def __peak_discount(self, quote):
        
        # ... define date 
        _date = self.date
        if(isinstance(_date, str)):
            _date = datetime.strptime(self.date, '%Y-%m-%d')

        # ... check date 
        if(_date.day not in self.peakDays):
            return quote*(self.off_peak_discount/100.0), True
        
        # ... else dont apply any discounts 
        return 0.0, False 
    
    # calculate quote 
    def __calculate_quote(self):
        
        # .. check distance to choose correct formular 
        if(self.distance < self.lDistance): return sum(self.sDistanceParams)
        
        # else long distance 
        return sum(self.lDistanceParams)
    

    # .. generate quote 
    @property
    def generate_quote_discount(self):

        # ... generate 
        quote = self.__calculate_quote()
        dPeak, apply_peak_discount = self.__peak_discount(quote)

        # .. check
        if(apply_peak_discount): return (quote, dPeak)

        # ... else
        return (quote, 0.0)