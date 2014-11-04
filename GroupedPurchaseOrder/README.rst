====================
GroupedPurchaseOrder
====================

GroupedPurchaseOrder is a simple Django app to conduct Web-based GroupedPurchaseOrder. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "GroupedPurchaseOrder" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'GroupedPurchaseOrder',
    )

2. Include the GroupedPurchaseOrder URLconf in your project urls.py like this::

    url(r'^GroupedPurchaseOrder/', include('GroupedPurchaseOrder.urls')),

3. Run `python manage.py migrate` to create the GroupedPurchaseOrder models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/GroupedPurchaseOrder/ to participate in the poll.
