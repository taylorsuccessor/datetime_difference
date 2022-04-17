# Aligent: assumption 

## 1. response formating:
    
    becuase the requirement is one api I returned all the required data in one response model.
    I can make this api take the required response (days, weekdays, weeks) and return one value
    like:
        /api/difference-between-dates/{required_response}
    but to make the user for this api easily build a one model for the response I choosed to return all required data
        
when we pass the thired parameters to spicify the response type (seconds, minutes, days,..., years) I just changed the value
without changing the key like `days_number` give total seconds because the required format is seconds

## 2. weekdays:
    
    I take the Saterday and Sunday out of calculation and I used the built in function in numpy
    we can check the days without this function to get fractions
    
    {
     "from_datetime": "2022-04-15T00:00:00+00:00",
     "to_datetime": "2022-04-18T00:00:00+00:00",
     "response_type": "days"
    }
    
this will returns 

    days_number = 3
    weekdays_number = 1
    
## 3. langauge and framework:
    I used python so it can be more easy to read and fastapi because the requirement is simple api and fastapi built for this.

## 4. envairnment:
    I'm using docker to make it easy to run it on any device and keep the versions.

## 5. calculations fractions and round:
    all numbers are round to 3 digits but weekdays we just get the int number of days from np.busday_count function
    then we convert it to required output (seconds, minutes, days ...) then we round it to 3 digits
