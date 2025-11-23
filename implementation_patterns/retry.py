### this is the retry wrapper 
from tenacity import retry, retry_any, stop_after_attempt, wait_exponential_jitter,  retry_if_exception_type
from typing import Callable, Any , Tuple, Type 



class StatusRetry(Exception):
    pass 


class RetryWrapper:
    def __init__(
        self, 
        func: callable,  max_attempts : int= 3 , 
        retry_exceptions: Tuple[Type[BaseException], ...] = (TimeoutError, ConnectionError),


    ): 
        
        self.func= func 
        self.max_attempts= max_attempts 
        self.retry_exceptions= retry_exceptions
        self._decorated_func = self._build_retry_func()

    @staticmethod 
    def _should_retry_status(code: int) ->bool:
        if 500 <=code <  600 :  ## indicate a temporary problem on the server side; retrying may succeed later 
            return True 
        
        if code == 429: #client hit a rate limit; retrying after waiting can succeed.
            return True  
        
        if code in (400 , 401, 403): 
            return False
        return False 
    
    def _build_retry_func(self):
        retry_condition= retry_any(
            retry_if_exception_type(self.retry_exceptions), 
            retry_if_exception_type(StatusRetry)
        )

        @retry (
            stop= stop_after_attempt(self.max_attempts),
            wait= wait_exponential_jitter(),
            retry= retry_condition ,
            reraise= True
        )

        def wrapper(*args, **kwargs):
            response= self.func(*args, **kwargs)
            
            ## check the status 
            status_code= getattr(response, 'status_code' , None )
            if status_code is not None and self._should_retry_status(status_code): 
                raise  StatusRetry(f"Retry due to status {status_code}")
            return response ### retrying on same function 
        return wrapper
        
        ### call methods
    def __call__(self, *args, **kwargs):
        return self._decorated_func(*args, **kwargs)
        
         

############### test ########## 


class FakeResponse:
    def __init__(self, status):
        self.status_code= status


attempt_counter= {'n' : 0 }
def fake_google_call(prompt:str):
    attempt_counter['n'] +=1 
    print("This is " , attempt_counter['n'] ,"th retry")
    return FakeResponse(500)
    


retry= RetryWrapper(func=fake_google_call  , max_attempts= 4) 
retry('hellow')