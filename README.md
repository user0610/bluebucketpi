# bluebucketpi

A Flask webapp that runs python code on a Raspberry Pi to control and monitor a growing plant... usually in a SpaceBucket (https://www.reddit.com/r/SpaceBuckets/), hence the name. But it could be adapted to other use cases.
The webapp will have the rPi take pictures (for time-lapses), read sensors (moisture, humidity, temperature), control fans, lights and water pumps, and write data to a csv file as well as to an epaper display.

Hardware Materials:
- A Raspberry Pi (I used a 3B+ I had collecting dust - you might have to steal or beg for one in 2023), and a 32GB micro SD card.
- A 4channel relay (5volt for microcontrollers - used this one: https://www.amazon.com/dp/B08PP8HXVD)
- A capacitance moisture sensor (used the "v1.2" available online. Kit: https://www.amazon.com/dp/B07TLRYGT1)
- An Analog-to-digital converter ADS1115 (for the rPi to read the moisture sensor. Like this one https://www.amazon.com/dp/B07VPFLSMX)
- A low voltage water pump (included in the kit above with the moisture sensor)
- DHT22 sensor (eg: https://www.amazon.com/dp/B073F472JL)
- 80mm computer fans (used 2 to create airflow: https://www.amazon.com/dp/B002YFSHPY)
- LED grow lights (used a stick-on LED strip light: https://www.amazon.com/gp/product/B00HSF65MC)
- rPi camera (eg: https://www.amazon.com/dp/B07KF7GWJL)
- Power supplies (used some USB charger blocks, an some 12v power adapters - mainly on each for the rPi, fans, pump, lights - sensors can be powered from the GPIO pins)
- An enclosure - used some clear Sterilite storage box and made holes for the wiring
- Hardware store buckets - check https://www.reddit.com/r/SpaceBuckets/ for details on how to build one.

Software Materials:
- Started with latest Raspbian fully loade
- more TBD...
