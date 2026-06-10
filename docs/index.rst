.. tibber.py documentation master file, created by
   sphinx-quickstart on Wed Jun 15 15:43:23 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. toctree::
   :maxdepth: 1
   :caption: Welcome

   self

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   getting_started


Welcome to tibber.py's documentation!
=====================================

.. note::
   This documentation is still in development and therefore does not cover
   all the functionality of the library. For now, you may read the Tibber 
   API docs on the `Tibber API explorer <https://developer.tibber.com/explorer>`_
   website to see all the properties and methods of each type in this library (this 
   close correlation to the Tibber API is explained further in the Introduction
   section).

`tibber.py <https://github.com/ericbstie/tibber.py>`_ is an unofficial
`wrapper library <https://en.wikipedia.org/wiki/Wrapper_library>`_ for the
`Tibber API <https://developer.tibber.com/>`_.
To quickly get started with common operations with the tibber.py library,
you can head over to the `GitHub repo <https://github.com/ericbstie/tibber.py>`_
and read the README.md file. There you can also see the source code of the library.

############
Introduction
############
Tibber is a relatively new electrical energy provider based in Norway (though they
are available in several other nordic countries). They focus on providing useful
gadgets and functionality to save energy consumption costs.
For example, they provide functionality to charge your electric car when the 
price for elecricity is low. To expand on this feature, and perhaps add this to
other smart devices in your home, you might consider using the Tibber API.

This is where tibber.py comes in to play!

With tibber.py you can retrieve data from the Tibber API super simple! This
library aims to have 100% API coverage, meaning that whatever you can do with
the Tibber API, you can do through this library too!

This API `wrapper library <https://en.wikipedia.org/wiki/Wrapper_library>`_ is
developed to be as close to the Tibber API in structure as possible. E.g. if a 
home has the property `consumption`, then this library's `Home` class will have
a `consumption` property too. This way, besides from this documentation, you can
read the Tibber API documentation and expect the library to work the same way.

#############################
How to use this documentation
#############################
If you are eager to get started, I would recommend reading some examples to see
how things are done with this library. Once you've got a feel for how it is 
syntactically, you can go over to reading the API Reference (which is under
development as of now, meanwhile you can use the
`Tibber API explorer <https://developer.tibber.com/explorer>`_). The API Reference
covers *all* classes and objects you will find in this library, and lists all
it's properties and methods.

####################################
How to contribute or report an issue
####################################
To report an issue or bug, go to the `GitHub repository <https://github.com/ericbstie/tibber.py>`_
and create a new issue describing your problem and how to reproduce it. Also
include what the *expected* behaviour was, and what the actual behaviour was.

.. warning::
   Issues that are created which do not include the problem, reproduction of the problem,
   the expected behaviour **and** the actual behaviour, will be tagged as invalid and
   will not be fixed or attended to.
