# Migration Guide for Entity Plugin Examples Reorganization

## Overview
The Entity Plugin Examples have been reorganized to provide better structure and clearer learning paths. This guide helps existing users migrate their code to the new organization.

## New Directory Structure

```
entity_plugin_examples/
├── core/               # Progressive learning examples
├── tools/              # Tool plugins (calculators, file ops, etc.)
├── memory/             # Memory pattern plugins
├── patterns/           # Design pattern examples
└── specialized/        # Domain-specific showcases
```

## Import Changes

### Core Examples
```python
# Old imports
from entity_plugin_examples import InstantAgentExample
from entity_plugin_examples import PipelineVisualizerExample

# New imports
from entity_plugin_examples.core import InstantAgentExample
from entity_plugin_examples.core import PipelineVisualizerExample
```

### Tool Plugins
```python
# Old imports
from entity_plugin_examples import CalculatorPlugin
from entity_plugin_examples import OutputFormatterPlugin

# New imports
from entity_plugin_examples.tools import CalculatorPlugin
from entity_plugin_examples.tools import OutputFormatterPlugin
```

### Memory Plugins
```python
# Old imports
from entity_plugin_examples import KeywordExtractorPlugin
from entity_plugin_examples import ReasonGeneratorPlugin

# New imports
from entity_plugin_examples.memory import KeywordExtractorPlugin
from entity_plugin_examples.memory import ReasonGeneratorPlugin
```

### Pattern Examples
```python
# Old imports
from entity_plugin_examples import StaticReviewerPlugin

# New imports
from entity_plugin_examples.patterns import StaticReviewerPlugin
```

## Backward Compatibility

For backward compatibility during the transition, the main `__init__.py` still exports commonly used plugins:
```python
from entity_plugin_examples import (
    CalculatorPlugin,        # Still works
    KeywordExtractorPlugin,  # Still works
    OutputFormatterPlugin,   # Still works
    ReasonGeneratorPlugin,   # Still works
    StaticReviewerPlugin,    # Still works
)
```

However, we recommend updating to the new import paths for better code organization.

## New Features

### Specialized Showcases
New domain-specific examples are available:
```python
from entity_plugin_examples.specialized import (
    CodeReviewerExample,      # Complete code review system
    ResearchAssistantExample, # Research and fact-checking system
    CustomerServiceExample,   # Customer support automation
)
```

### Memory Patterns
Organized memory patterns by category:
```python
from entity_plugin_examples.memory.conversation_history import (
    ConversationTrackerPlugin,
    TurnCounterPlugin,
    ContextSummarizerPlugin,
)

from entity_plugin_examples.memory.user_preferences import (
    PreferenceLearnerPlugin,
    StyleAdapterPlugin,
    TopicTrackerPlugin,
)
```

## Migration Steps

1. **Update imports**: Change import statements to use the new paths
2. **Test your code**: Run your tests to ensure everything works
3. **Explore new features**: Check out the specialized examples for your domain
4. **Update documentation**: Update any documentation that references the old structure

## Getting Help

If you encounter issues during migration:
1. Check the test files in `tests/` for usage examples
2. Refer to the examples in each subdirectory
3. Open an issue on GitHub with the migration tag

## Timeline

- **Current**: Both old and new imports work (backward compatibility)
- **Next minor version**: Deprecation warnings for old imports
- **Next major version**: Old imports will be removed

We recommend migrating as soon as possible to avoid future breaking changes.