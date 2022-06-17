# Module `message.py`
```text
Module with base msg for processing
```

> Path: `orch_serv\msg\message.py`
`SubPydanticBodyModel` = TypeVar('SubPydanticBodyModel', bound=BaseModel)
`SubPydanticHeaderModel` = TypeVar('SubPydanticHeaderModel', bound=BaseModel)
## Class `BaseOrchServMsg`
```text
Base message class for processing and to use the library
```

### Basses(s)
+ GenericModel
+ Generic[SubPydanticBodyModel, SubPydanticHeaderModel]
### Attributes(s)
+ body` - message body to be processed with basic information
+ header` - message header with data to be processed
### Example 
```python
>>> # How to use BaseOrchServMsg to create a custom message for your needs
>>> # The first step: create body model your msg
>>> from pydantic import BaseModel
>>> class MyBody(BaseModel):
>>>     body_option: str # any type you need
>>> # The second step: create header model your
>>> # msg (is optional if you need a header)
>>> class MyHeader(BaseModel):
>>>     header_option: str # any type you need
>>> # The third step: create your msg
>>> # The first option:
>>> MyTypeFir = BaseOrchServMsg[MyBody, MyHeader]
>>> example_my_type = {"body": {
>>>                         "body_option": "test_body"},
>>>                    "header":{
>>>                          "header_option":"test_header"}}
>>> my_value = MyTypeFir(**example_my_type)
>>> # First option without header
>>> MyTypeFirWithoutHeader = BaseOrchServMsg[MyBody, BaseModel]
>>> # The second option
>>> class MyTypeSec(BaseOrchServMsg):
>>>     body: MyBody
>>>     header: MyHeader
>>> MyTypeSec(**example_my_type)
```

### SubElement(s)
 > `body`: SubPydanticBodyModel = Field(..., description='The body of the message with the structure you need')
 > `header`: Optional[SubPydanticHeaderModel] = Field(description='Optional message header with the structure you need')
 > ## Function  `get_source`
 > ```text
 > ### For orchestrator ###
 > Add to the message the source where
 > the message was processed (will be processed)
 > Method is required to be implemented
 > pair method to method set_source
 > :raise NotImplementedError: if not override
 > ```
 > 
 > ### Return
 > ```text
 > the method returns the string that the set method
 > ```
 > 
 > #### Declared returns: `Optional[str]`
 > ### Example
 > ```python
 > >>> obj: BaseOrchServMsg
 > >>> source = 'test_source'
 > >>> obj.set_source(source)
 > >>> assert obj.get_source() == source
 > >>> # True
 > ```
 > ## Function  `set_source`
 > ```text
 > ### For orchestrator ###
 > Method set source to message to identify previous step on flow
 > Method is required to be implemented
 > for more information see method get_source
 > ```
 > 
 > ### Argument(s)
 > + `source`: str - source where the message was processed (will be processed)
 > ### Return
 > ```text
 > nothing
 > ```
 > 
 > ## Function  `get_flow`
 > ```text
 > ### For orchestrator ###
 > Method returns the name of the flow to which the given message belongs
 > !!! the message must contain a field that determines whether
 > the message belongs to some flow
 > ```
 > 
 > ### Return
 > ```text
 > title flow
 > ```
 > 
 > #### Declared returns: `Optional[str]`
 > ## Function  `get_target`
 > ```text
 > ### For orchestrator ###
 > Method returns the name of the command that should execute the given message
 > necessary if you don’t need a flow but want to execute only one
 > block for a message
 > ```
 > 
 > ### Return
 > ```text
 > title block to execution
 > ```
 > 
 > #### Declared returns: `Optional[str]`
 > ## Function  `get_command`
 > ```text
 > ### For service ###
 > Method returns the name of the processor name
 > that should execute the given message
 > ```
 > 
 > ### Return
 > ```text
 > title processor to execution
 > ```
 > 
 > #### Declared returns: `Optional[str]`