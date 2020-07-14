# SPI transaction framer

High-level analyzer for Saleae Logic to merge SPI frames into transactions based on when the Enable line is active.

The output frames inherit the start and end time from the start time of the "enable" frame
and the end time of the "disable" frame.
