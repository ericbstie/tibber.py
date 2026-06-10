Getting started
===============

############
Installation
############
tibber.py is available on PyPI. You can install it with pip:

.. code-block:: bash

   pip install tibber.py

#########################
Getting basic information
#########################

Getting the "Viewer" type (this is the topmost schema (or type) under Query on the Tibber API explorer
documentation). All your homes, subscriptions, etc. will be under here. 

.. code-block:: python

   import tibber

   account = tibber.Account("your token")  # This is just like the viewer type in the API explorer

Log in here: https://developer.tibber.com/explorer and check out the documentation on the right.
Click the yellow underlined text "Query", then "Viewer". The "account" variable above is essentially
the same as the Viewer type in the API explorer. It contains the same properties as the documentation
says that the Viewer has. So let's for example get the name of the Viewer!

.. code-block:: python

   print(account.name)

What about getting a home? Checking out the https://developer.tibber.com/explorer documentation, we
see that the Viewer type has a "homes" attribute and is surrounded by [brackets]. That means it comes
in the form of a list. Let's get the first home in the list!

.. code-block:: python

   print(account.homes)  # [<tibber.types.home.TibberHome object at 0x...>]
   home = account.homes[0]
   print(home.app_nickname)  # "Vitahuset"


#############################################
Retrieving consumption/production information
#############################################

Moving on from the previous example, what can we do with a home? Let's check out the documentation again.
Click the yellow underlined text "Home" and check out the documentation. We see that the Home type has a
"consumption" method! Let's try to call that method with some parameters and get the HomeConsumptionConnection type back!
Since we're fetching data from the API and not just getting it from the cache, we need to prepend the method call with "fetch\_".

.. code-block:: python

   consumption = home.fetch_consumption(resolution = "HOURLY", last = 24)  # last 24 hours
   print(consumption)  # <tibber.types.home_consumption_connection.HomeConsumptionConnection object at 0x...>

Back in the API explorer documentation, clicking the yellow underlined text "HomeConsumptionConnection" we see that it has a
"nodes" attribute which has a list of consumptions. Within the Consumption type you have all the goodies such as cost,
unit price, currency etc. Let's print the cost of the last 24 hours!

.. code-block:: python

   total = sum(node.cost for node in consumption.nodes if node.cost is not None)
   print(total)  # 123.45

Looking back at the documentation, we see that the HomeConsumptionConnection type also has a HomeConsumptionPageInfo type.
The HomeConsumptionPageInfo actually has a totalCost property that we can use instead of looping through all the nodes!
Here's how to achieve the same thing as above, but using the page info we have instead.

.. code-block:: python

   print(consumption.page_info.total_cost)  # 123.45

Getting production information is very similar to getting consumption information. The only difference is
that you use the "production" method instead of the "consumption" method. The rest is the same!

###########################
Sending a push notification
###########################
Sending a push notification is very simple. This sends a push notification
to all your devices that are logged in to the Tibber app with the same 
account as the one you have generated your access token with.

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   account.send_push_notification("My title", "Hello! I'm a message!")

.. note::
   Push notifications cannot be sent with the demo token. The API will
   respond with "operation not allowed for demo user". Use an access
   token generated for your own account instead.

#########################
Getting price information
#########################

The current subscription of a home holds price information. You can fetch
today's (and, after they are published, tomorrow's) prices with the
``fetch_price_info()`` method. It takes the resolution as an argument,
which can be either ``QUARTER_HOURLY`` or ``HOURLY``.

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   subscription = account.homes[0].current_subscription

   price_info = subscription.fetch_price_info("QUARTER_HOURLY")

   print(price_info.today)     # A list of 96 Price objects
   print(price_info.tomorrow)  # This data is populated once a day

To get historical prices, use the ``fetch_price_info_range()`` method. It
supports the ``QUARTER_HOURLY``, ``HOURLY`` and ``DAILY`` resolutions. The
API requires the date to be passed as a base64 encoded ISO 8601 datetime
with timezone information.

.. code-block:: python

   import tibber
   import datetime
   import base64

   account = tibber.Account("your token")
   subscription = account.homes[0].current_subscription

   date = datetime.datetime(2025, 1, 1, 0, 0, 0)
   encoded_date = base64.b64encode(date.astimezone().isoformat().encode("utf-8")).decode("utf-8")

   connection = subscription.fetch_price_info_range("HOURLY", first=10, after=encoded_date)

   for price in connection.nodes:
      print(price.starts_at, price.total, price.currency)

#################
Live measurements
#################

To get live measurements, you first have to register callback functions
for the `live_measurement` event. This event is emitted every time a 
measurement has been made and has been retrieved from the API.

In simpler terms; in order to get live data, you need to create a function 
that you want to be run every time a live measurement is available. Then
you must "register" that function so that it actually runs every time 
a live measurement is available.

.. note::
   The live measurement may be delayed with a few seconds and is updated
   only every 2-10 seconds (in my experience).

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   home = account.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   # Now start retrieving live measurements
   home.start_live_feed(user_agent="program/1.0")

.. note::
   Any code after home.start_live_feed() will not run! This is because the
   start_live_feed() method is blocking. It will run forever and will only
   stop when stopped with Ctrl+C or when the interpreter closes.

To close the live feed after any condition, you can pass the exit_condition argument to
the start_live_feed() method. If the exit_condition function returns true, the live feed
will be stopped (and code execution will continue).

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   home = account.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   # Now start retrieving live measurements
   home.start_live_feed(user_agent="program/1.0", exit_condition = lambda data: True)  # This will stop the live feed after the first measurement

The exit condition function receives the latest LiveMeasurement as its only
argument, so you can stop the live feed based on the data it contains.

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   home = account.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   def my_exit_function(live_measurement_data):
      return live_measurement_data.power > 1000

   # Now start retrieving live measurements
   home.start_live_feed(user_agent="program/1.0", exit_condition = my_exit_function)  # This will stop the live feed when the power is above 1000
   print("We made it! The power is above 1000!")

For more examples, check out the `README <https://github.com/ericbstie/tibber.py>`_ of the project on GitHub.
