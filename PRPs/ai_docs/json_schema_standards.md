# JSON Schema Standards for AI Response Formatting

This document provides comprehensive JSON schema standards for structured AI responses, based on 2024 industry best practices and research findings.

## Base Structure Pattern

Use this consistent schema for all JSON-formatted AI responses:

```json
{
  "type": "response|analysis|command|process|error",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Primary response content",
    "actions": [],
    "details": {},
    "summary": {}
  },
  "metadata": {
    "model": "claude-sonnet-4",
    "tokens": {
      "input": 500,
      "output": 1500
    },
    "duration_ms": 2500,
    "confidence": 0.95
  },
  "context": {
    "session_id": "uuid-here",
    "request_id": "uuid-here"
  }
}
```

## Response Types

### 1. Standard Response
```json
{
  "type": "response",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Task completed successfully",
    "summary": {
      "files_modified": 3,
      "tests_passed": true
    }
  },
  "metadata": {
    "duration_ms": 1500
  }
}
```

### 2. Analysis Response
```json
{
  "type": "analysis",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Code analysis completed",
    "findings": [
      {
        "type": "issue",
        "severity": "medium",
        "description": "Potential performance bottleneck",
        "location": "line 45"
      }
    ],
    "recommendations": [
      "Consider caching database queries",
      "Implement connection pooling"
    ],
    "confidence": 0.85
  }
}
```

### 3. Command Response
```json
{
  "type": "command",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "File operations completed",
    "actions": [
      {
        "type": "file_edit",
        "target": "/absolute/path/to/file.py",
        "status": "success",
        "changes": {
          "lines_added": 10,
          "lines_removed": 5
        }
      }
    ],
    "summary": {
      "total_actions": 3,
      "successful": 3,
      "failed": 0
    }
  }
}
```

### 4. Process Response (Multi-Step)
```json
{
  "type": "process",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Multi-step process in progress",
    "steps": [
      {
        "step": 1,
        "action": "search_codebase",
        "status": "completed",
        "result": "Found 15 matches"
      },
      {
        "step": 2,
        "action": "analyze_patterns",
        "status": "in_progress"
      }
    ],
    "progress": {
      "current_step": 2,
      "total_steps": 5,
      "percentage": 40
    }
  }
}
```

## Error Handling (RFC 7807 Compliant)

### Standard Error Format
```json
{
  "type": "error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The 'file_path' parameter must be an absolute path",
  "instance": "/requests/12345",
  "timestamp": "2025-01-09T10:30:00Z",
  "errors": [
    {
      "field": "file_path",
      "message": "Must start with /",
      "code": "INVALID_PATH"
    }
  ],
  "context": {
    "request_id": "uuid-here"
  }
}
```

### Error Categories
- **400 Bad Request**: Malformed JSON or invalid syntax
- **422 Unprocessable Entity**: Validation failures
- **500 Internal Server Error**: AI model failures or system errors

## Formatting Guidelines

### Human Readability
- Use 2-space indentation for development/debugging
- Include descriptive field names
- Provide meaningful error messages
- Add context for complex operations

### Machine Processing
- Ensure 100% valid JSON syntax
- Use consistent field names across responses
- Include proper data types (strings, numbers, booleans, arrays)
- Provide machine-readable status codes and error codes

## Performance Considerations

### Size Optimization
- Use abbreviated keys for high-frequency responses if needed
- Implement field filtering for large responses
- Consider compression for responses over 1KB

### Validation
- All JSON must pass `JSON.parse()` validation
- Schema validation using jsonschema library recommended
- Include request/response IDs for tracing

## Implementation Examples

### Python Validation
```python
import json
import jsonschema

# Validate JSON syntax
try:
    parsed = json.loads(response_text)
except json.JSONDecodeError as e:
    return {"error": f"Invalid JSON: {e}"}

# Schema validation
schema = {
    "type": "object",
    "required": ["type", "timestamp", "content"],
    "properties": {
        "type": {"type": "string"},
        "timestamp": {"type": "string"},
        "content": {"type": "object"}
    }
}

jsonschema.validate(parsed, schema)
```

### JavaScript/Node.js Usage
```javascript
// Parse and validate
try {
    const response = JSON.parse(responseText);
    console.log(`Response type: ${response.type}`);
    console.log(`Message: ${response.content.message}`);
} catch (error) {
    console.error('Invalid JSON response:', error);
}
```

## Key Principles

1. **Consistency**: Use the same schema structure across all response types
2. **Completeness**: Include all necessary metadata for debugging and processing
3. **Clarity**: Make JSON human-readable while maintaining parseability
4. **Error Resilience**: Provide detailed error information following standards
5. **Performance**: Balance readability with processing efficiency

This schema provides a robust foundation for structured AI responses that serve both human and machine consumers effectively.