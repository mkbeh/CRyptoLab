# CRyptoLab
In developing...

#### Kivy  
```angular2html
Change code block in file kivy.loader.py:318 from:
fd = urllib_request.urlopen(filename)

to:
req = urllib_request.Request(filename, headers={'User-Agent': 'Mozilla/5.0'})
fd = urllib_request.urlopen(req)

Because async getting images from internet not working without headers in urllib_request.
```
