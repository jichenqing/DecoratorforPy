# Submitter: chenqinj(Ji, Sue)
# Partner  : qiao1(Qiao, Ran)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # setting the class attribute on the next line to True allows checking to occue
    checking_on  = True
  
    # self._checking_on must be True too, for function checking to occur 
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        def check_list_tu(an_type,an_text:str):
            if isinstance(value, an_type) ==False:
                raise AssertionError(repr(param)+' failed annotation check(wrong type): value = '+\
            repr(value)+'\n  was type '+type_as_str(value)+' ...should be type ' +an_text+\
            '\n'+check_history)            
            elif len(annot) == 1:
                i=0
                for v in value:
                    self.check(param, annot[0], v, check_history+an_text+\
                               '['+str(i)+'] check: '+str(annot[0])+'\n')
                    i += 1
            else:
                if len(annot)!=len(value):
                    raise AssertionError(repr(param)+' failed annotation check(wrong number of elements): value = '+\
                                         repr(value)+'\n  annotation had '+str(len(annot))+ ' elements'+\
                                         str(annot)+'\n'+check_history)
                i=0
                for x,y in zip(annot, value):
                    self.check(param,x, y, check_history+an_text+'['+str(i)+'] check: '+\
                               str(annot[i])+'\n')
                    i+=1
##                    if isinstance(x,y) == False:
##                        raise AssertionError('Wrong single type:  {x} ... should be  {y}'.format(x=str(type(x))[8:-2], y=str(y)[8:-2]))
        def check_dict():
            if isinstance(value, dict) ==False:
                raise AssertionError(repr(param)+' failed annotation check(wrong type): value = '+\
            repr(value)+'\n  was type '+type_as_str(value)+' ...should be type dict\n'+check_history)   
            elif len(annot)!= 1:
                raise AssertionError(repr(param)+' annotation inconsistency: dict should have \
            1 item but had '+str(len(annot))+'\n  annotation = '+str(annot)+'\n'+check_history)                 
            else:
                for a , b in annot.items():
                    for x in value.keys():
                        self.check(param,a  , x, check_history+'dict key check: '  +str(a)+'\n')
                    for y in value.values():
                        self.check(param, b , y, check_history+'dict value check: '+str(b)+'\n')
                    
        def check_set_f(an_type,an_text):
            if isinstance(value, an_type) ==False:
                raise AssertionError(repr(param)+' failed annotation check(wrong type): value = '+\
            repr(value)+'\n  was type '+type_as_str(value)+' ...should be type ' +an_text+\
            '\n'+check_history)                
            elif len(annot)!= 1:
                raise AssertionError(repr(param)+' annotation inconsistency: dict should have \
            1 item but had '+str(len(annot))+'\n  annotation = '+str(annot)+'\n'+check_history)              
            else:
                for a in annot:
                    for x in value:
                        self.check(param, a , x, check_history+an_text+' value check: '+str(a)+'\n')
        def check_lambda():  
             
            if len(annot.__code__.co_varnames)!=1:
                raise AssertionError(repr(param)+\
            ' annotation inconsistency: predicate should have 1 parameter but had '+\
            str(len(annot.__code__.co_varnames))+'\n  annotation = '+str(annot)+\
            '\n'+check_history)           
            try:
                ans= annot(value)
                
            except Exception as message:
                assert False, repr(param)+' annotation predicate('+str(annot)+\
                ') raised exception'+'\n  exception = '+str(message.__class__)[8:-2]+\
                ': '+str(message)+'\n'+check_history                 
            else:
                assert ans, repr(param)+' failed annotation check: value = '+repr(value)+\
                '\n  predicate = '+str(annot)+'\n'+check_history
                
        if annot == None:
            pass 
        elif type(annot) is type:
            if isinstance(value,annot) == False:
                raise AssertionError("'{param}' failed annotation check(wrong type): value = '{value}'\n was type '{value_t}' ...should be type '{annot}'{check}".format(param = param, value=value , value_t = str(type(value))[8:-2], annot=str(annot)[8:-2], check = check_history))
        elif isinstance(annot,list):
            check_list_tu(list,'list')
        elif isinstance(annot, tuple):
            check_list_tu(tuple,'tuple')
        elif isinstance(annot, dict):
            check_dict()
        elif isinstance(annot,set):
            check_set_f(set,'set') 
        elif isinstance(annot,frozenset):
            check_set_f(frozenset,'frozenset')
        elif inspect.isfunction(annot):
            check_lambda() 
        else:
            try:
                if isinstance(annot,str):
                    assert eval(annot,self._args)
                else:
                    annot.__check_annotation__(self.check,param,value,check_history)
            except AttributeError: 
                assert False, repr(param)+' annotation undecipherable: '+str(annot)+'\n'+check_history                 
            except AssertionError:
                raise
            except Exception as message:
                raise AssertionError(repr(param)+' annotation protocol('+str(annot)+') raised exception'+\
                                 '\n  exception = '+str(message.__class__)[8:-2]+': '+str(message)+'\n'+check_history)
                      
                        
           
            

       
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Decode function's annotation below; check it against arguments

        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, whose parameters are in the function header, in order)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if Check_Annotation.checking_on == False or self._checking_on == False:
            return self._f(*args,**kargs) 
        self._args=param_arg_bindings()
        annot=self._f.__annotations__
        try:
            # Check the annotation for every parameter (if there is one)
            for p in self._args.keys():
                if p in annot: 
                    self.check(p,annot[p],self._args[p])         
            # Compute/remember the value of the decorated function
            answer = self._f(*args,**kargs)
            
            # If the return has an annotation, check it
            if 'return' in annot:
                self._args['_return'] = answer
                self.check('return',annot['return'],answer)
            
            # Return the decorated answer
            return answer
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #print(l.rstrip())
            #print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    import checkannotation
    from checkannotation import Check_Annotation as ca
    def f(x : (int,str)): pass
    f = ca(f)
    f((1,'b'))
    
           
    import driver
    driver.driver()
