'''
Radhika Banerjea
Created: October 8, 2022
Last Modified: October 12, 2022
ESC 180 Project 1 
'''

from calendar import different_locale


def initialize():
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    global last_update_day
    global last_update_month
    global last_country
    global last_country_count
    global last_country2
    global is_disabled
    global month_difference

    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day = None
    last_update_month = None
    
    last_country = 1
    last_country2 = 1  

    last_country_count = 1
    
    is_disabled = False

    month_difference = 0

    MONTHLY_INTEREST_RATE = 0.05

#used to move money from not owing interest to owing interest and adds interest to those values depending on the current month
def interest_calculations(month):
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    global month_difference
    if last_update_month != None:
        month_difference = month - last_update_month

    #print("the month difference is ", month_difference)
    if month_difference == 1:

        cur_balance_owing_intst = cur_balance_owing_intst * (1.05**month_difference)
        cur_balance_owing_intst = cur_balance_owing_intst + cur_balance_owing_recent
        cur_balance_owing_recent = 0

        #print("im recent ",cur_balance_owing_recent)
        #print("im interest ",cur_balance_owing_intst)
    
    elif month_difference >1:

        
        cur_balance_owing_intst = cur_balance_owing_intst * (1.05**month_difference)
 
        
        cur_balance_owing_recent = cur_balance_owing_recent * (1.05**(month_difference-1))
        cur_balance_owing_intst = cur_balance_owing_intst + cur_balance_owing_recent
        cur_balance_owing_recent = 0

    elif month_difference == 0:
        pass
        #print("im recent ",cur_balance_owing_recent)
        #print("im interest ",cur_balance_owing_intst)
   

#returns True iff the date (day1, month1) is the same as the date (day2, month2), or occurs later than (day2, month2)
def date_same_or_later(day1, month1, day2, month2):
    if day2 == None and month2 == None:
        return True
    else:   
        if month1 == month2:
            if day1 >= day2:
                return True
            else:
                return False
        elif month1 > month2:
            return True
        else:
            return False

#This function returns True iff the values of the three strings c1, c2, and c3 are all different from each other.
def all_three_different(c1, c2, c3):
    if (c1 != c2) and (c2 != c3) and (c1 != c3):
        return True
    else:
        return False

#This function updates the values of last_update_date and last_update_month
def update_date(day, month):
    global last_update_day
    global last_update_month
    last_update_day = day
    last_update_month = month


#This function simulates a purchase of amount amount, on the date (day, month), in the country country (given as a capitalized string)
def purchase(amount, day, month, country):
    global is_disabled
    global last_country
    global last_country2
    global cur_balance_owing_recent
    if is_disabled == False:
        
        if date_same_or_later(day, month, last_update_day, last_update_month):
            if ((all_three_different(last_country, last_country2, country))==False) or  (last_country2 == 1):

                last_country2 = last_country
                last_country = country

                interest_calculations(month)
                cur_balance_owing_recent = cur_balance_owing_recent + amount
                update_date(day, month)

            else:
                is_disabled = True
                
                return "error"
                
        
        else:
            
            return "error"

    else:
       
        return "error"

#This function returns the amount owed as of the date (day, month)
def amount_owed(day, month):
    if date_same_or_later(day, month, last_update_day, last_update_month):
        
        interest_calculations(month)
        update_date(day, month)
        
        return (cur_balance_owing_intst + cur_balance_owing_recent)
        
    else:
        return "error"
    
def pay_bill(amount, day, month):
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    interest_calculations(month)
    if date_same_or_later(day, month, last_update_day, last_update_month):

        
        if (cur_balance_owing_intst == 0) and (amount_owed(day, month)):
            cur_balance_owing_recent = cur_balance_owing_recent - amount
            update_date(day, month)
            #print("the month was updated to: " , last_update_day, ", ", last_update_month)

        elif amount <= cur_balance_owing_intst:
            
            cur_balance_owing_intst = cur_balance_owing_intst - amount
            update_date(day, month)
            #print("the month was updated to: " , last_update_day, ", ", last_update_month)
           
        elif amount <= (amount_owed(day, month)):
            cur_balance_owing_recent =  cur_balance_owing_recent - (amount - cur_balance_owing_intst)
            cur_balance_owing_intst = 0    
            update_date(day, month)


        else:
            return "error"

    else:
        return "error"

if __name__ == "__main__":
    
    # initialize()
    # purchase(80, 8, 1, "Canada")
    # print("Now owing:", amount_owed(8, 1)) #80.0
    # pay_bill(50, 2, 2)
    # print("Now owing:", amount_owed(2, 2)) #30.0 (=80-50)
    # print("Now owing:", amount_owed(6, 3)) #31.5 (=30*1.05)
    # purchase(40, 6, 3, "Canada")
    # print("Now owing:", amount_owed(6, 3)) #71.5 (=31.5+40)
    # pay_bill(30, 7, 3)
    # print("Now owing:", amount_owed(7, 3)) #41.5 (=71.5-30)
    # print("Now owing:", amount_owed(1, 5)) #43.65375 (=1.5*1.05*1.05+40*1.05)
    # purchase(40, 2, 5, "France")
    # print("Now owing:", amount_owed(2, 5)) #83.65375
    # print(purchase(50, 3, 5, "United States")) #error (3 diff. countries in
    # # a row)
    # print("Now owing:", amount_owed(3, 5)) #83.65375 (no change, purchase
    # # declined)
    # print(purchase(150, 3, 5, "Canada")) #error (card disabled)
    # print("Now owing:", amount_owed(1, 6)) #85.8364375
    # #(43.65375*1.05+40)
    

    '''
    initialize()
    purchase(69, 1, 1, "Canada")
    purchase(420, 17, 8, "Canada")
    pay_bill(200, 17, 11)
    print("Now owing:", amount_owed(17,11))
    '''
