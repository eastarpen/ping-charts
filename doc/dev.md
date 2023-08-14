# Dev Guide

This is a very simple project, so I don't want write a lot.

I just put something I think which are useful here.

If you have any questions, please open an issue.

## Server && Client

Nothing complex, just see the code.

## Web-UI

- `constants.js`  define some constants used to decide the charts color.  

  `max_ping_value = 350;` define the max ping value in the charts. Change it will affect the bar height.

- If you want debug it.

  * Set environment variable `env='env'`, see [readme](../README.md#Using source code]
  * Under `test-data` directory, create a json format file named 'data'(Just rename one of the data files already exist under that directory), then using `python3 -m http.server 8081` to export that file.  
    For more information, see "vue.config.js".
