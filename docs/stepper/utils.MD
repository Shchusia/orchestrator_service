# Module `utils.py`
> Path: `orch_serv/stepper/utils.py`
## Class `ParameterKind`
### Basses(s)
+ enum.IntEnum

### SubElement(s)
 > `POSITIONAL_ONLY` = 0
 > `POSITIONAL_OR_KEYWORD` = 1
 > `VAR_POSITIONAL` = 2
 > `KEYWORD_ONLY` = 3
 > `VAR_KEYWORD` = 4
## Function  `format_signature_parameters`
```text
Method copied from inspect for private usage
```
        
### Argument(s)
+ `parameters` - empty doc string
#### Declared returns: `str`
## Function  `parse_signature`
```text
parse_signature of obj
```
        
### Argument(s)
+ `obj`: Callable - empty doc string
### Return
```text
(attributes, returned)
```
                    
#### Declared returns: `Tuple[(str, str)]
`
## Function  `get_returned_value`
### Argument(s)
+ `obj`: Callable - empty doc string
## Function  `get_attributes_obj`
### Argument(s)
+ `obj`: Callable - empty doc string
#### Declared returns: `str`
## Function  `is_optional`
### Argument(s)
+ `field` - empty doc string
## Function  `validate_data_step`
```text
Validate provided data for execution step
```
        
### Argument(s)
+ `obj`: Callable - obj to execution
+ `additional_args`: Dict - kwargs for execution obj
### Raise(s)
+ `ExtraAttributeError` - if in kwargs
### Return
```text
nothing
```
                    
## Function  `is_exist_keyword_variable`
```text
Check is exist **keyword variable in `obj`
```
        
### Argument(s)
+ `obj`: Callable - obj to execution
### Return
```text
is exist in function **kwargs
```
                    
## Function  `validate_data_consistency`
```text
Function for validate data consistency between steps
```
        
### Argument(s)
+ `obj`: Callable - obj to execution
+ `return_previous_obj`None - annotations returned from previous step
+ `additional_args`: Dict - kwargs for execution obj
### Raise(s)
+ `DataConsistencyError` - if not consistent data
### Return
```text
nothing
```
                    