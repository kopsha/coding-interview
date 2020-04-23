# Questions:

## Question:

How would you implement the property decorator ?

## Answer(s)

Return a descriptor that holds the initial method and when accessed it calls the initial method injecting the received object instead of the self argument.

## Question:

How would you implement a class that makes requests to a remote server that exposes some procedures? The api should look like this. When a method of the object is called:  ```my_class_instance.some_method()``` the instance should call the procedure named ```some_method``` on the remote server.

## Answer(s)
Override the ```__getattr__``` and return a dynamic created function that calls the wanted procedure using the received name.   

## Question:

Why are some websites asking for your permission to use cookies?

## Answer(s)

The cookies on the respective site might be used on other websites as well. For instance if some website uses the js facebook api, it will send the cookies to facebook as well and they might use your private data. 
