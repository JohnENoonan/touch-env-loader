# TouchDesigner Environment Variable Loader
This is a tox asset used to load immutable config variables from an external file

## Usage
This tool can be used to load either a `json` file or a delimited `env` file. Example files are `example.env` and `example.json`

### API
```python
op.env.Get("VARIABLE_NAME") # returns None if key is not present, else a td.Cell object
op.env.Exists("VARIABLE_NAME") # returns boolean
```

### Callbacks
Callbacks are available from the docked dat. The function `processEnv` will be called on every update to the script or to the input env file. You can edit the dat in place and make any changes needed.

### JSON Syntax
Loading a json file supports all types except for arrays. In the event of an array it will be processed as a string. For example
```json
{
	"test" : [1, 2, 3]
}
```
will be evaluated as 
| Test | [1, 2, 3] |
|------|-----------|
