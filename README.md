# battel_tested_Scalable_Secure_Production_ready_multiagent_codes
Real world Production Ready multi Agent codes


## PILL Detection and Redaction 
Before sending  user   data to third party  LLm or any Apis we must  check , scaned   and masked  user sensative data to avoid data lekage 

for examples :

  user : my gmail is ram12@gmail.com and password is 'hari12' please help me to login 

**note** we must write a code to detect  sensative  information and masked this 

``` 
  SEARCH list sensitive information in user_input like email , api keys , password .... :
    IF detected:
        FOR EACH detected_item:

            REPLACE detected_item WITH <placeholder>

            (for examples 
            password : 'i love usa' will be converted to  
            password : '<password'>)


        END FOR
        
    END IF

RETURN sanitized user_input
```

before masking: my gmail is ram12@gmail.com , and password is 'hari12' please help me to login

after masking : 
my gmail is <my_gmail.com>  and password is <my_password> please help me to login 


now we can send this query to third party llm 

-------------------