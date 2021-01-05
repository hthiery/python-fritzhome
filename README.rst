Python Library to access AVM Fritz!Box homeautomation
=====================================================

|BuildStatus| |PypiVersion| |PyPiPythonVersions| |Coveralls| |CodeClimate| |Codacy|

Tested Devices
--------------
* `FRITZ!Box 6490 Cable`_
* `FRITZ!DECT 200`_
* `FRITZ!DECT 440`_
* `FRITZ!DECT 500`_
* `Comet DECT`_
* `Panasonic KX-HNS101`
* `Magenta Smarthome Tür-/Fensterkontakt optisch`_


fritzhome CLI tool
------------------

You have to add a user with the rights to access the smarthome actors.

In the fritzbox webinterface under "System -> FRITZ!Box-Benutzer" you can
add a new user.

.. code:: shell

    $ fritzhome -f fritz.box  -u smarthome -p smarthome  list
    ##############################
    name=Fenster Badezimmer
      ain=11934 0154799-1
      id=2000
      productname=HAN-FUN
      manufacturer=0x0feb
      present=True
      lock=None
      devicelock=None
     Alert:
      alert=True
    ##############################
    name=Thermostat Badezimmer
      ain=11959 0171328
      id=16
      productname=Comet DECT
      manufacturer=AVM
      present=True
      lock=False
      devicelock=False
     Temperature:
      temperature=19
      offset=-3
     Thermostat:
      battery_low=False
      battery_level=80
      actual=19.0
      target=19.0
      comfort=22.0
      eco=19.0
      window=False
      summer=False
      holiday=False
    ##############################
    name=Schalter WC Heizung
      ain=08761 0402392
      id=21
      productname=FRITZ!DECT 200
      manufacturer=AVM
      present=True
      lock=True
      devicelock=False
     Switch:
      switch_state=False
     Powermeter:
      power=0
      energy=436529
      voltage=231.0
     Temperature:
      temperature=22
      offset=3


Fritzbox User
-------------

Add a new user: System -> FRITZ!Box-Benutzer

.. image:: https://raw.githubusercontent.com/hthiery/python-fritzhome/readme/doc/fritzbox_user_overview.png

.. image:: https://github.com/hthiery/python-fritzhome/blob/readme/doc/fritzbox_user_smarthome.png

References
----------

- https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
- https://github.com/DerMitch/fritzbox-smarthome


.. |BuildStatus| image:: https://travis-ci.org/hthiery/python-fritzhome.png?branch=master
                 :target: https://travis-ci.org/hthiery/python-fritzhome
.. |PyPiVersion| image:: https://badge.fury.io/py/pyfritzhome.svg
                 :target: http://badge.fury.io/py/pyfritzhome
.. |PyPiPythonVersions| image:: https://img.shields.io/pypi/pyversions/pyfritzhome.svg
                        :alt: Python versions
                        :target: http://badge.fury.io/py/pyfritzhome
.. |Coveralls|   image:: https://coveralls.io/repos/github/hthiery/python-fritzhome/badge.svg?branch=master
                 :target: https://coveralls.io/github/hthiery/python-fritzhome?branch=master
.. |CodeClimate| image:: https://api.codeclimate.com/v1/badges/fc83491ef0ae81080882/maintainability
                 :target: https://codeclimate.com/github/hthiery/python-fritzhome/maintainability
                 :alt: Maintainability
.. |Codacy|      image:: https://api.codacy.com/project/badge/Grade/0929296afb8c45c6af673524fe232d9e
                 :target: https://www.codacy.com/app/hthiery/python-fritzhome?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hthiery/python-fritzhome&amp;utm_campaign=Badge_Grade

.. _Comet DECT: https://www.eurotronic.org/produkte/comet-dect.html
.. _FRITZ!DECT 200: https://avm.de/produkte/fritzdect/fritzdect-200/
.. _FRITZ!DECT 440: https://avm.de/produkte/fritzdect/fritzdect-440/
.. _FRITZ!DECT 500: https://avm.de/produkte/fritzdect/fritzdect-500/
.. _FRITZ!Box 6490 Cable: https://avm.de/produkte/fritzbox/fritzbox-6490-cable/
.. _Magenta Smarthome Tür-/Fensterkontakt optisch: https://www.smarthome.de/geraete/smarthome-tuer-fensterkontakt-optisch-weiss
