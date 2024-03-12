#// we need the date time module 
from datetime import datetime
from .variables import MID_MONTH_DISCOUNT

class GenerateQuote:
    
    # .. overide the init function
    def __init__(self, vSize, distance, helpers, floors, job_date, shuttle):
        
        # .. discount 
        self.off_peak_discount = MID_MONTH_DISCOUNT # percent 
        self.lDistance = 200 # km
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
            1.0: [420,  15.0*distance, 110*helpers, 50.00*floors,  self.tGateFee, 0.0],
            1.5: [630,  16.5*distance, 137*helpers, 62.50*floors,  self.tGateFee, 0.0],
            2.0: [840,  19.0*distance, 170*helpers, 77.50*floors,  self.tGateFee, 0.0],
            3.0: [1328, 23.0*distance, 200*helpers, 125.0*floors,  self.tGateFee, 0.0],
            4.0: [2000, 27.0*distance, 230*helpers, 150.0*floors,  self.tGateFee, 0.0],
            8.0: [2071, 46.2*distance, 308*helpers, 200.0*floors,  self.tGateFee, 0.0]
        }\
        .get(float(vSize))
        
        # ... params 4 long distance
        self.lDistanceParams = {
            #key   base, pricePerKM,    HelperFee,   floorFee,   tall gate 
            1.0: [420,  15.0*distance, 110*helpers, 50.00*floors,  self.tGateFee, 0.0],
            1.5: [630,  16.5*distance, 137*helpers, 62.50*floors,  self.tGateFee, 0.0],
            2.0: [840,  19.0*distance, 170*helpers, 77.50*floors,  self.tGateFee, 0.0],
            3.0: [1328, 23.0*distance, 200*helpers, 125.0*floors,  self.tGateFee, 0.0],
            4.0: [2000, 27.0*distance, 230*helpers, 150.0*floors,  self.tGateFee, 0.0],
            8.0: [2071, 46.2*distance, 308*helpers, 200.0*floors,  self.tGateFee, 0.0]
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
    def generate_pricing(self):

        # ... generate 
        quote = self.__calculate_quote()
        dPeak, apply_peak_discount = self.__peak_discount(quote)

        # .. check
        if(apply_peak_discount): return (quote, dPeak)

        # ... else
        return (quote, 0.0)