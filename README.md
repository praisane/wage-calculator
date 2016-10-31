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

*   The CSV must have entries for a single month only. If there are entries for multiple months, the processing will halt with an error.
*   The CSV *can* contain multiple entries for the same day, however the hours must all be distinct and cannot overlap - the calculation result will be wrong if overlapping entries exist.
