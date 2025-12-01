# HistoricalRevertMixin Feature

## Overview

The `HistoricalRevertMixin` is a powerful Django admin mixin that enables administrators to restore deleted objects from their historical records directly through the Django admin interface. This feature provides a safety net for accidental deletions, allowing recovery of objects with all their original data intact.

## Problem Solved

When using django-simple-history, deleted objects are preserved in historical records, but there was no built-in way to restore them. Administrators had to manually recreate deleted objects or write custom code to restore them. This mixin solves that problem by providing a user-friendly interface for object restoration.

## Key Features

### 1. **Restore Button**
- Displays a visual "🔄 Restore" button in the admin list view for deletion records
- Shows "✓ Already Restored" for objects that have been recovered
- Provides instant, one-click restoration for individual objects

### 2. **Bulk Admin Action**
- "Revert selected deleted objects" action for batch restoration
- Process multiple deleted objects simultaneously
- Intelligent filtering to only restore valid deletion records

### 3. **Safety & Validation**
- **Duplicate Prevention**: Checks if object already exists before restoring
- **Deletion Record Validation**: Only processes records with `history_type == "-"`
- **Error Handling**: Gracefully handles restoration failures with clear error messages
- **ID Preservation**: Restores objects with their original primary keys

### 4. **User Feedback**
- Clear success messages with object details and IDs
- Warnings for already-restored or non-deletion records
- Error messages for failed restorations
- Detailed count summaries for bulk operations

## How It Works

1. **Detection**: Identifies deletion records in historical data (`history_type == "-"`)
2. **Validation**: Verifies the record is a deletion and object doesn't already exist
3. **Restoration**: Recreates the object with exact field values from historical record
4. **ID Preservation**: Maintains original primary key for referential integrity
5. **History Tracking**: Creates new history record documenting the restoration

## Technical Implementation

### Core Components

- **`revert_button(obj)`**: Renders restore button in admin list display
- **`handle_revert_from_button(request)`**: Processes single-object restoration
- **`revert_deleted_object(request, queryset)`**: Handles bulk restoration action
- **`get_actions(request)`**: Registers the revert action with Django admin
- **`changelist_view(request, extra_context)`**: Integrates button clicks with admin

### Data Integrity

- Preserves all field values from the deletion point
- Maintains original primary key (ID)
- Properly handles foreign key relationships
- Creates new historical record for the restoration
- Supports all Django field types

## Usage Example

```python
from django.contrib import admin
from simple_history.admin import HistoricalRevertMixin
from .models import Product

@admin.register(Product.history.model)
class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "sku", 
        "price",
        "history_date",
        "history_type",
        "revert_button"
    )
    list_filter = ("history_type", "history_date")
    search_fields = ("name", "sku")
```

## Benefits

1. **User-Friendly**: No code required for administrators to restore objects
2. **Safe**: Multiple validation checks prevent data corruption
3. **Efficient**: Batch operations for restoring multiple objects
4. **Transparent**: Clear feedback and comprehensive logging
5. **Flexible**: Works with any model using django-simple-history
6. **Complete**: Preserves all data including original IDs and relationships

## Use Cases

- **Accidental Deletion Recovery**: Quickly restore mistakenly deleted records
- **Data Auditing**: Review and restore objects from specific deletion events
- **Bulk Operations**: Recover multiple objects deleted in error
- **Testing & Development**: Easily restore test data after deletion
- **User Error Correction**: Allow support teams to undo user mistakes

## Testing

Comprehensive test suite with 19 tests covering:
- Button display logic (4 tests)
- Button restoration actions (4 tests)
- Bulk admin actions (6 tests)
- Django admin integration (3 tests)
- Data integrity verification (2 tests)

All tests verify:
- Correct button rendering
- Successful restoration with ID preservation
- Duplicate prevention
- Error handling
- Message display
- History record creation

## Documentation

Complete documentation including:
- Setup and configuration guide
- Code examples with real models
- Feature descriptions and workflows
- API reference with all methods
- Safety considerations and limitations
- Tips and best practices

## Impact

This feature significantly improves the django-simple-history admin experience by:
- Reducing time to recover from accidental deletions
- Eliminating need for custom restoration code
- Providing audit trail for all restorations
- Increasing confidence in delete operations
- Enhancing overall data management capabilities

## Technical Specifications

- **Python Compatibility**: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- **Django Compatibility**: 4.2, 5.0, 5.1, 5.2, 6.0, main
- **Dependencies**: Only django-simple-history (no additional packages)
- **Database Support**: All Django-supported databases
- **Performance**: Minimal overhead, uses standard Django ORM operations

## Future Enhancements

Potential improvements for future versions:
- Confirmation dialog for restore actions
- Preview of data before restoration
- Batch deletion/restoration history
- Restore with modifications
- Time-based filtering for deletions

