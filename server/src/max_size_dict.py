import time, json

class MaxSizeLRU(object):
    # Desired keys to match with scheduler_tasks.py
    __DESIRED_KEYS__ = ["total", "available", "usage_percent", "used","free", "cpu_percent"]
    def __init__(self, max_size):
        self.max_size = max_size
        # keys are time stamps
        self.dict = {}

    def store(self, value):
        assert type(value) == dict
        for k in self.__DESIRED_KEYS__:
            assert k in value.keys(), f"Value requires the following key: {k}"
        t = time.time()
        value['time'] = t
        self.dict[t] = value

        # automatically remove the earliest item
        if len(self.dict) >= self.max_size:
            return self.dict.pop(self.__get_oldest_key())
    
    def __get_oldest_key(self):
        return sorted(self.dict.keys())[0]
    
    def getall(self):
        return self.dict
    
    def __str__(self):
        return json.dumps(self.dict)