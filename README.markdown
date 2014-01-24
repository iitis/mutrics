About
=====
**mutrics**: open source network traffic classifier in Python, a reference
implementation of the Waterfall architecture.

The classifier takes as input ARFF files generated with [the Flowcalc
program](http://mutrics.iitis.pl/flowcalc). **mutrics** classifies network
traffic flows basing on many levels of traffic analysis and outputs the results
in either ARFF or TXT file format.

The classifier consists of many modules, which should be trained separately.
See respective directories for supportive scripts that train and test a
particular model.

For scientific works, please find and cite the following paper:  
> Foremski P., Callegari C., Pagano M., *"Waterfall: Rapid identification of IP flows using cascade classification"*

**Author**: Paweł Foremski <pjf@iitis.pl>  
**Copyright (C)** 2012-2013 [IITiS PAN Gliwice](http://www.iitis.pl/)  
**Licensed** under GNU GPL v3

This software package uses
[libshorttext](http://www.csie.ntu.edu.tw/~cjlin/libshorttext/), which is
included in the dnsclass repository, but may be licensed differently.

Classification modules
================

The following modules are available in the implementation:
* **dstip**: quick classification by destination IP address
* **dnsclass**: [the DNS-Class algorithm](http://mutrics.iitis.pl/dns-class)
* **portsize**: quick classification by port number and payload size
* **npkts**: classification by payload sizes of 4 first packets, using random forest
* **port**: classical, quick classification by the port number
* **stats**: classification by statistics of packet sizes and inter-arrival times, using random forest
* **dpi**: classification by DPI payload analysis, using random forest

Project information
================
Project realized at [The Institute of Theoretical and Applied Informatics of
the Polish Academy of Sciences](http://www.iitis.pl/), under grant nr
2011/01/N/ST6/07202 of the [Polish National Science
Centre](http://www.ncn.gov.pl/).

Project website: http://mutrics.iitis.pl/
