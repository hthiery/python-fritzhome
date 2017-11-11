Python Library to access AVM Fritz!Box homeautomation
=====================================================

|BuildStatus| |PypiVersion| |Coveralls| |CodeClimate|

Tested Devices
--------------
* `FRITZ!Box 6490 Cable`_ with FRITZ!OS 06.85
* `FRITZ!DECT 200`_ with firmware 03.87
* `Comet DECT`_ with firmware 03.54


fritzhome CLI tool
------------------

You have to add a user with the rights to access the smarthome actors.

In the fritzbox webinterface under "System -> FRITZ!Box-Benutzer" you can
add a new user.

.. code:: shell

    $ fritzhome -f fritz.box  -u smarthome -p smarthome  list
    #############
    ain=11959 0171328
    id=16
    name=Badezimmer
    productname=Comet DECT
    manufacturer=AVM
    present=True
    temperature=21.000000
    soll=22.0
    komfort=22.0
    absenk=19.0
    #############
    ain=08761 0045657
    id=17
    name=FRITZ!DECT 200 #2
    productname=FRITZ!DECT 200
    manufacturer=AVM
    present=True
    switch_state=True
    switch_power=0
    switch_energy=88863
    temperature=21.000000

References
----------

 - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
 - https://github.com/DerMitch/fritzbox-smarthome


.. |BuildStatus| image:: https://travis-ci.org/hthiery/python-fritzhome.png?branch=master
                 :target: https://travis-ci.org/hthiery/python-fritzhome
.. |PyPiVersion| image:: https://badge.fury.io/py/pyfritzhome.svg
                 :target: http://badge.fury.io/py/pyfritzhome
.. |Coveralls|   image:: https://coveralls.io/repos/github/hthiery/python-fritzhome/badge.svg?branch=master
                 :target: https://coveralls.io/github/hthiery/python-fritzhome?branch=master
.. |CodeClimate| image:: https://api.codeclimate.com/v1/badges/fc83491ef0ae81080882/maintainability
				 :target: https://codeclimate.com/github/hthiery/python-fritzhome/maintainability
				 :alt: Maintainability

.. _Comet DECT: https://www.eurotronic.org/produkte/comet-dect.html
.. _FRITZ!DECT 200: https://avm.de/produkte/fritzdect/fritzdect-200/
.. _FRITZ!Box 6490 Cable: https://avm.de/produkte/fritzbox/fritzbox-6490-cable/
