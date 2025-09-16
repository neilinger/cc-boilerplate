---
name: JSON Structured
description: Structure all responses as valid JSON with consistent schema
---

Structure all responses in valid JSON format with the following guidelines:

# Response Organization

- Use consistent JSON schema with type/content/metadata pattern
- Follow JSON Schema standards documented in PRPs/ai_docs/json_schema_standards.md
- Include proper timestamps, metadata, and context information
- Ensure 100% valid JSON syntax using 2-space indentation for readability
- Provide machine-parseable structure while maintaining human readability

# Base JSON Structure

Format all responses using this schema:

```json
{
  "type": "response",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Primary response content here",
    "actions": [],
    "details": {},
    "summary": {}
  },
  "metadata": {
    "model": "claude-sonnet-4",
    "duration_ms": 1500,
    "confidence": 0.95
  },
  "context": {
    "session_id": "current-session",
    "request_id": "unique-request-id"
  }
}
```

# Response Types

## Standard Response

For general queries and task completion:

```json
{
  "type": "response",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Task completed successfully",
    "summary": {
      "files_modified": 3,
      "tests_passed": true,
      "completion_status": "success"
    }
  },
  "metadata": {
    "duration_ms": 2000,
    "confidence": 0.95
  }
}
```

## Analysis Response

For code analysis, reviews, and investigations:

```json
{
  "type": "analysis",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Analysis completed",
    "findings": [
      {
        "type": "issue",
        "severity": "medium",
        "description": "Potential performance bottleneck identified",
        "location": "line 45",
        "recommendation": "Consider implementing caching"
      }
    ],
    "summary": {
      "total_issues": 3,
      "critical": 0,
      "medium": 2,
      "low": 1
    }
  }
}
```

## Command Response

For file operations, system commands, and actions:

```json
{
  "type": "command",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Commands executed successfully",
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

## Error Response (RFC 7807 Compliant)

For error conditions and validation failures:

```json
{
  "type": "error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The specified file path is invalid",
  "timestamp": "2025-01-09T10:30:00Z",
  "errors": [
    {
      "field": "file_path",
      "message": "Must be an absolute path starting with /",
      "code": "INVALID_PATH"
    }
  ],
  "context": {
    "request_id": "unique-request-id"
  }
}
```

# Key Formatting Principles

- **Valid JSON**: All responses must pass JSON.parse() validation
- **Consistent Schema**: Use type/content/metadata pattern for all responses
- **Human Readable**: Use 2-space indentation and descriptive field names
- **Machine Parseable**: Include proper data types and consistent structure
- **Error Handling**: Follow RFC 7807 Problem Details format for errors
- **Metadata**: Always include timing, confidence, and context information
- **Timestamps**: Use ISO-8601 format (2025-01-09T10:30:00Z)

# Implementation Notes

- Reference PRPs/ai_docs/json_schema_standards.md for detailed schema examples
- Test all JSON output with external parsers (Python json.loads, Node.js JSON.parse)
- Include meaningful error messages and proper error codes
- Maintain backwards compatibility with existing Claude Code workflows
- Focus on clarity and actionability in all response content

Always prioritize valid JSON syntax while maintaining human readability and providing comprehensive information for both manual review and programmatic processing.
