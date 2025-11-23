### this is the retry wrapper 
from tenacity import (
                retry,
                retry_any,
                stop_after_attempt,
                wait_exponential_jitter,
                retry_if_exception_type,
                retry_if_result 
                    )


from typing import Callable, Any , Tuple, Type 


class RetryWrapper:
    """ retry wrapper that retries on : 
       1) specific exceptions (network or system errors)
        2) HTTP response status code (>=500 or 429) """
    def __init__(
        self, 
        func: callable,  max_attempts : int= 3 , 
        retry_exceptions: Tuple[Type[BaseException], ...] = (TimeoutError, ConnectionError),


    ): 
        
        self.func= func 
        self.max_attempts= max_attempts 
        self.retry_exceptions= retry_exceptions
        self._decorated_func = self._build_retry_func()

    
    
    def _build_retry_func(self):
        def should_retry_status(response):
            status_code=  getattr(response, "status_code", None)
            if 500 <=status_code <  600  or status_code == 429:  ## indicate a temporary problem on the server side; retrying may succeed later 
                return True 
            return False 
        

        retry_condition= retry_any(
            retry_if_exception_type(self.retry_exceptions), 
            retry_if_result(should_retry_status),
        )

        @retry (
            stop= stop_after_attempt(self.max_attempts),
            wait= wait_exponential_jitter(),
            retry= retry_condition ,
            reraise= True
        )

        def wrapper(*args, **kwargs):
            return  self.func(*args, **kwargs)
        
        return wrapper
        
        ### call methods
    def __call__(self, *args, **kwargs):
        return self._decorated_func(*args, **kwargs)
        
         

############### test ########## 

class FakeResponse:
    def __init__(self, status):
        self.status_code = status


attempt_counter = {"n": 0}


def fake_google_call(prompt: str):
    attempt_counter["n"] += 1
    print("This is", attempt_counter["n"], "th retry")
    return FakeResponse(500)  # triggers retry

retry=RetryWrapper(fake_google_call, max_attempts= 5)
resp= retry('hellow')
print(f"Final response status: {resp.status_code}")
