# Usage

## Steps 

### 1. Configure the filter
Add the filter to the `filters` list in the `config.json` file of the Regolith project:
```json
{
  "filter": "shapescape_texture_tools",
  "settings": {
    "scope_path": "shapescape_texture_tools/scope.json"
  }
}
```

### 2. Define tasks
Tasks are defined as a list of dictionaries. Each dictionary defines a single image that should be created. The task file is a Python file with a single expression that must evaluate into a list of dictionaries that define task steps. The tasks must be placed in the folder with the data of the filter (in *data/shapescape_texture_tools/* or any subfolder of that path).

Refer to the [example](example.md) for a sample task configuration.

### 3. Run the Filter
Run the filter using the Regolith command:
```
regolith run
```

## Best Practices

- Ensure that the `scope_path` is correctly set to the JSON file that defines the scope of variables provided to the tasks during their evaluation.
- Use comprehensions in Python to simplify and optimize the task definitions.

## Additional Notes

Refer to the [settings](settings.md) and [operations](operations.md) documentation for detailed information on configuring and using the filter.