# wage-calculator

A simplified monthly wage calculation system.

## Requirements

*   A computer (virtual or real)
*   An OS (preferably some kind of Unix variant)
*   Python 3

That's pretty much it. No external libraries were harmed in the coding process of this piece o'software to keep it clean and simple.

## Running

To run, use the included `run.sh` script and pass the input CSV file as a parameter:

For example:

`./run.sh etc/HourList201403.csv`

To run the included unittests, use the `run_tests` script:

`./run_tests.sh`

To get some more statistics about the monthly hours, use the `-s/--statistics` flag.


## Limitations and known issues

*   The CSV *must* have entries for a single month only. If there are entries for multiple months, the processing will halt with an error.
*   The CSV *can* contain multiple entries for the same day, however the hours must all be distinct and cannot overlap - the calculation result will be wrong if overlapping entries exist.

## Random thoughts

There's a lot to improve here, since due to time limitations this is pretty much a MVP implementation. A few things I'd improve given enough time:

*   Fix the (internal) sorting of the hour list, treat dates as true Python date objects.
*   Add an "even more statistics" mode, that would drill down to the day level and print out detailed statistics on each day, including number of hours and pay broken down by the three categories.
*   Support multiple months in the same CSV file or even multiple CSV files.
*   Fix the overlapping entry limitation

Et cetera ad inifinitum...

© 2016 Petteri Räisänen. No rights are reserved, you are free to do whatever you like with this little piece of Pythonite.
