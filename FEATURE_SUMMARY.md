# HistoricalRevertMixin - Feature Summary

## Short Description (for PR title)
Add HistoricalRevertMixin for restoring deleted objects from Django admin

## One-Line Summary
A Django admin mixin that enables one-click restoration of deleted objects from their historical records.

## Commit Message

```
Add HistoricalRevertMixin for restoring deleted objects

This commit introduces HistoricalRevertMixin, a new admin mixin that allows
administrators to restore deleted objects directly from the Django admin
interface.

Features:
- Restore button in list display for one-click restoration
- Bulk admin action to restore multiple objects at once
- Automatic validation and duplicate prevention
- Preserves original primary keys and field values
- Comprehensive error handling and user feedback

The mixin works with any model using django-simple-history and provides
a safe, user-friendly way to recover from accidental deletions.

Changes:
- Added HistoricalRevertMixin class to simple_history/admin.py
- Added 19 comprehensive tests to test_admin.py
- Created complete documentation in docs/mixins.rst
- Updated docs/index.rst to include mixins documentation
```

## PR Description

### Summary
This PR introduces `HistoricalRevertMixin`, a powerful admin mixin that enables restoration of deleted objects from their historical records through the Django admin interface.

### Motivation
When objects are accidentally deleted, administrators currently have no built-in way to restore them from historical records. This mixin provides a user-friendly solution for recovering deleted objects with all their original data intact.

### Changes
1. **New Mixin**: `HistoricalRevertMixin` class in `simple_history/admin.py`
   - `revert_button()` - Displays restore button in admin list
   - `handle_revert_from_button()` - Handles single-object restoration
   - `revert_deleted_object()` - Bulk admin action for multiple restorations
   - `get_actions()` - Registers admin actions
   - `changelist_view()` - Integrates button clicks

2. **Tests**: 19 comprehensive tests in `test_admin.py`
   - Button display and behavior
   - Individual and bulk restoration
   - Error handling and edge cases
   - Data integrity verification

3. **Documentation**: Complete guide in `docs/mixins.rst`
   - Setup and usage examples
   - Feature descriptions
   - API reference
   - Safety considerations

### Key Features
- ✅ **One-Click Restoration**: Restore button for individual objects
- ✅ **Bulk Operations**: Admin action for multiple objects
- ✅ **ID Preservation**: Maintains original primary keys
- ✅ **Safety Checks**: Duplicate prevention and validation
- ✅ **Clear Feedback**: Success/warning/error messages
- ✅ **Full Compatibility**: Works with any django-simple-history model

### Usage Example
```python
from simple_history.admin import HistoricalRevertMixin

@admin.register(Product.history.model)
class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
    list_display = ("name", "history_date", "history_type", "revert_button")
    list_filter = ("history_type",)
```

### Testing
All tests pass (19/19) ✓
- Button display tests
- Restoration action tests
- Bulk operation tests
- Integration tests
- Data integrity tests

### Breaking Changes
None - This is a new feature that doesn't modify existing functionality.

### Checklist
- [x] Code implemented and working
- [x] Comprehensive tests added (19 tests)
- [x] Documentation created
- [x] All tests passing
- [x] No breaking changes
- [x] Follows project coding standards

---

## Social Media / Blog Post Summary

🎉 New Feature: Restore Deleted Objects in Django Simple History!

Accidentally deleted a record? No problem! The new HistoricalRevertMixin lets you restore deleted objects with a single click from the Django admin interface.

✨ Features:
• One-click restore button
• Bulk restoration for multiple objects
• Preserves original IDs and data
• Built-in safety checks

Perfect for recovering from accidental deletions while maintaining full data integrity!

#Django #Python #OpenSource #WebDevelopment

---

## Issue/Discussion Description

### Problem
When using django-simple-history, deleted objects are preserved in historical records, but there's no built-in way to restore them. Administrators must either:
1. Manually recreate the objects (losing original IDs)
2. Write custom code for restoration
3. Use database-level recovery (complex and risky)

### Proposed Solution
Introduce `HistoricalRevertMixin` - an admin mixin that adds restoration capabilities directly to the Django admin interface.

### Implementation
The mixin provides:
1. A restore button in the historical admin list display
2. A bulk admin action for restoring multiple objects
3. Validation to ensure only deletion records are restored
4. Duplicate prevention to avoid conflicts
5. Clear user feedback for all operations

### Benefits
- **Easy to Use**: No coding required for administrators
- **Safe**: Multiple validation checks prevent errors
- **Complete**: Preserves all original data including IDs
- **Flexible**: Works with any model using django-simple-history
- **Well-Tested**: 19 comprehensive tests ensure reliability

### Alternative Considered
- Custom admin command: Less user-friendly, requires terminal access
- Manual SQL: Dangerous, error-prone, no validation
- API endpoint: Requires custom UI development

The mixin approach integrates seamlessly with Django admin's existing interface.

