1)	Open desktop postman.
2)	Run the code.
3)	We have 3 type of requests:
(1)	Start request = Post mode
(2)	End request = Put mode
(3)	Report request = Get mode

(1)	Start request should contain only username and the task
![img.png](img.png)

The output response for this request:
![img_1.png](img_1.png)
Sending another start request with the same username before sending end request will give the next response:
![img_2.png](img_2.png)

(2)	End request should contain only username:
![img_3.png](img_3.png)

The output response:

![img_8.png](img_8.png)

Sending another end request for the same username will give the next response:
![img_5.png](img_5.png)

(3)	Report request: In this request there is no “body” part for the request.
Sending “Get” request to get the whole report for all the user ids in the database table:

![img_6.png](img_6.png)

The response:

![img_7.png](img_7.png)