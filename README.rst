bbot
====

This is a framework for higher-level configuration of BuildBot_
masters, used by `BoostPro Computing <http://www.boostpro.com>`_ for its
internal testing and by the `Ryppl <http://ryppl.org>`_ project.

.. _BuildBot: http://trac.buildbot.net

The goal is to efficiently and expressively manage pools of slaves
whose resources can be distributed across a variety of build and test
jobs.

Features
--------

* Declarative configuration
* Avoidance of boilerplate
* Multiple project support

Projects
--------

A project aggregates:

* property requirements
* source repositories
* build procedures
* status reporting

Platforms
---------

A platform is a Python tuple describing a combination of properties
such as os, compiler toolchain, architecture, python-version,
emacs-version, etc.

Slaves
------

A slave has properties that describe its platform capabilities.  A
slave property whose value is a list describes a list of possible
values for that property.  For example, a slave having Python 2.6 and
Python 2.7 installed might have a ``python`` property with value 
``[ '2.6', '2.7']``.

Build Variants
--------------

Every project is built on every available platform that satisfies the
project's requirements.

Testing
-------

To run the project's tests, invoke ``nosetests`` from the top-level
directory (in addition to BuildBot_, you'll need `nose
<http://readthedocs.org/docs/nose>`_).

Status
------

This framework is still under heavy development.  It evolves in major
ways as we discover the need for new capabilities.

Why "bbot?" 
-----------

Basically, it's short.  Better names welcomed.
