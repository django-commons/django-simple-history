Simple History Mixins
=====================

This document describes the mixins available in django-simple-history that extend
admin functionality beyond the standard ``SimpleHistoryAdmin``.


HistoricalRevertMixin
---------------------

The ``HistoricalRevertMixin`` provides functionality to restore deleted objects from
their historical records directly through the Django admin interface. This is useful
when objects are accidentally deleted and need to be recovered with their exact
original data.


Overview
~~~~~~~~

When you delete an object tracked by django-simple-history, a historical record with
``history_type = "-"`` is created. The ``HistoricalRevertMixin`` allows administrators
to restore these deleted objects through:

1. **Bulk Admin Action**: Select multiple deletion records and restore them at once
2. **Restore Button**: Click a button next to individual deletion records to restore them


Basic Usage
~~~~~~~~~~~

To use this mixin, create an admin class for your model's historical model that
inherits from both ``HistoricalRevertMixin`` and Django's ``ModelAdmin``:

.. code-block:: python

    from django.contrib import admin
    from simple_history.admin import HistoricalRevertMixin
    from .models import Product

    @admin.register(Product.history.model)
    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = ("id", "name", "price", "history_date", "history_type", "revert_button")
        list_filter = ("history_type",)

.. important::

    ``HistoricalRevertMixin`` **must** come before ``ModelAdmin`` in the inheritance list.
    This ensures the mixin's methods properly override the base admin methods.


Features
~~~~~~~~

Revert Button
^^^^^^^^^^^^^

Add the ``revert_button`` method to your ``list_display`` to show a restore button
for each deletion record:

.. code-block:: python

    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = ("name", "history_date", "history_type", "revert_button")

The button will display:

- **🔄 Restore** button for deletion records that haven't been restored yet
- **✓ Already Restored** message if the object has already been restored
- **-** (dash) for non-deletion records (creates, updates)


Admin Action
^^^^^^^^^^^^

The mixin automatically adds a "Revert selected deleted objects" action to the
admin changelist. This allows you to:

1. Filter historical records by ``history_type = "-"`` (deletions)
2. Select one or multiple deletion records
3. Choose "Revert selected deleted objects" from the Actions dropdown
4. Click "Go" to restore the selected objects


Complete Example
~~~~~~~~~~~~~~~~

Here's a complete example showing how to set up the mixin with a model:

**models.py**

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class Product(models.Model):
        name = models.CharField(max_length=200)
        description = models.TextField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        sku = models.CharField(max_length=50, unique=True)
        created_at = models.DateTimeField(auto_now_add=True)

        history = HistoricalRecords()

        def __str__(self):
            return self.name


**admin.py**

.. code-block:: python

    from django.contrib import admin
    from simple_history.admin import HistoricalRevertMixin, SimpleHistoryAdmin
    from .models import Product

    # Regular admin for the Product model
    @admin.register(Product)
    class ProductAdmin(SimpleHistoryAdmin):
        list_display = ("name", "sku", "price", "created_at")
        search_fields = ("name", "sku")

    # Historical admin with restore functionality
    @admin.register(Product.history.model)
    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = (
            "name",
            "sku",
            "price",
            "history_date",
            "history_type",
            "history_user",
            "revert_button"
        )
        list_filter = ("history_type", "history_date")
        search_fields = ("name", "sku")
        date_hierarchy = "history_date"


How It Works
~~~~~~~~~~~~

Restoring via Button
^^^^^^^^^^^^^^^^^^^^

When you click the restore button:

1. The mixin retrieves the historical record
2. Validates it's a deletion record (``history_type == "-"``)
3. Checks if the object already exists (prevents duplicates)
4. Creates a new instance with the exact field values from the historical record
5. Restores the object with its **original primary key**
6. Shows a success/warning/error message
7. Creates a new history record for the restoration


Restoring via Admin Action
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you use the bulk action:

1. Processes each selected historical record
2. Skips non-deletion records with a warning
3. Skips already-restored objects with a warning
4. Restores valid deletion records
5. Reports detailed results (success count, warnings, errors)


Data Integrity
^^^^^^^^^^^^^^

The mixin ensures:

- **Original IDs Preserved**: Restored objects keep their original primary keys
- **No Duplicates**: Won't restore if an object with that ID already exists
- **Complete Data**: All field values from the deletion point are restored
- **History Tracked**: The restoration creates a new history record
- **Foreign Keys**: Related objects are properly reconnected if they still exist


Safety Features
~~~~~~~~~~~~~~~

The mixin includes several safety checks:

- **Deletion Records Only**: Only processes records with ``history_type == "-"``
- **Duplicate Prevention**: Checks if object already exists before restoring
- **Error Handling**: Catches and reports errors without breaking the process
- **User Feedback**: Provides clear success/warning/error messages
- **Transaction Safety**: Each restore is handled individually


Workflow Example
~~~~~~~~~~~~~~~~

1. **A product is accidentally deleted:**

   .. code-block:: python

       product = Product.objects.get(id=123)
       product.delete()  # Oops! Wrong product deleted

2. **Navigate to the Historical Product admin page in Django admin**

3. **Filter by history type = "-" to see only deletions**

4. **Find the deleted product in the list**

5. **Click the "🔄 Restore" button, OR select it and use the bulk action**

6. **The product is restored with all its original data and ID = 123**


Limitations
~~~~~~~~~~~

- **Unique Constraints**: If a field has a unique constraint and another object
  now uses that value, restoration will fail
- **Foreign Keys**: If related objects were also deleted, the foreign key fields
  will be restored but won't point to valid objects
- **Many-to-Many**: M2M relationships are restored to the state they were in
  at deletion time
- **Auto Fields**: Fields like ``auto_now`` will be set to the historical values,
  not current time


Tips
~~~~

**Add Filtering**

Make it easy to find deleted objects:

.. code-block:: python

    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = ("name", "history_date", "history_type", "revert_button")
        list_filter = ("history_type", "history_date")  # Easy filtering

**Add Search**

Find specific deleted objects quickly:

.. code-block:: python

    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = ("name", "sku", "history_date", "history_type", "revert_button")
        search_fields = ("name", "sku", "history_user__username")

**Add Date Hierarchy**

Navigate through deletions by date:

.. code-block:: python

    class HistoricalProductAdmin(HistoricalRevertMixin, admin.ModelAdmin):
        list_display = ("name", "history_date", "history_type", "revert_button")
        date_hierarchy = "history_date"


API Reference
~~~~~~~~~~~~~

Methods
^^^^^^^

``revert_button(obj)``
    Returns HTML for a restore button that appears in the admin list.

    **Returns**: Safe HTML string with restore button or status indicator

``handle_revert_from_button(request)``
    Handles the restoration when a user clicks the restore button.

    **Parameters**:
        - ``request``: HttpRequest object containing ``revert_id`` parameter

    **Returns**: HttpResponseRedirect back to changelist

``revert_deleted_object(request, queryset)``
    Admin action that restores multiple deleted objects.

    **Parameters**:
        - ``request``: HttpRequest object
        - ``queryset``: QuerySet of historical records to process

    **Side Effects**: Restores objects and displays admin messages

``get_actions(request)``
    Overrides admin get_actions to include the revert action.

    **Returns**: Dictionary of available admin actions

``changelist_view(request, extra_context=None)``
    Overrides changelist to handle restore button clicks.

    **Returns**: HttpResponse from parent or redirect after restoration


Attributes
^^^^^^^^^^

``revert_button.short_description``
    Column header for the revert button: ``"Restore"``

``revert_deleted_object.short_description``
    Action description: ``"Revert selected deleted objects"``
