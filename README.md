# DecoratorforPy

Contributors: Ran Qiao, Chenqing Ji

We will write theCheck_Annotationclass and use it as a decorator for functionswhose annotations we want to check each time the function is called. Internally itwill overload the__call__method to call the function only after checking itsannotation by using mutual recursion (not direct recursion), in a natural way, toprocess the nesting of data types inside data types illustrated in the notation above.We will write code that ensures that this checking works for the standard classesdefined in Python. The code will also know how to process a special annotation-checking protocol (via the__check_annotation__method) that we can implementin any new classes that we write, so that that class can become part of theannotation language (I have done this for two classes:Check_All_OKandCheck_Any_OK).

This project is involved with mutual recursion and nested function as well as operator overloading. 
