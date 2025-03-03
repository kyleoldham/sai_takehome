```
Results:
  Success: 17544
  Client Error: 33918
  Server Error: 0

  Total Data Transferred (GB): 33.94

  Unique Path Requests:
     /downloads/product_1: 30285
     /downloads/product_2: 21104
     /downloads/product_3: 73
```

## Summary:
- no 500s, lots of successes, lots more client errors
- should work with any log file that contains json and has this general format

### Usage:
- python3 log_parser.py nginx_json_logs

#### Improvements:
- more error handling (if no access to file? if data can't be read or isnt json?)
- should break it out of main into a better named function for if it were called by other scripts
- the status counting vars could also be a dict intead of their own variables
- using regex isn't great or maintainable, splitting on the request part of the json might have been a better idea
