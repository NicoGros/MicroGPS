# MicroGPS
MicroGPS is a python ans desktop application designed to relocate measurement points between different imaging and analytical instruments.

In many microscopy and microanalysis workflows, a region of interest is first identified on an optical image and subsequently analysed using one or several complementary techniques (e.g. Raman microscopy, IBA, SEM-EDS, MA-XRF, LIBS, FTIR microscopy, etc.). Because each instrument has its own coordinate system, relocating exactly the same point can be time-consuming and error-prone. Heterogeneous samples lacking easily identifyable features can also prove challenging for locating the same points of analysis.

MicroGPS provides a simple calibration-based solution. After defining three common reference points between an image and an instrument coordinate system, the software computes the affine transformation relating both coordinate systems. Measurement points can then be added either directly on the image or by entering coordinates from any calibrated system. Their corresponding coordinates are automatically computed for every available coordinate system.

This allows users to:

* calibrate one or several instrument coordinate systems from a reference image;
* locate and record measurement points during acquisition;
* convert coordinates between multiple instruments;
* revisit previously analysed locations with high reproducibility;
* export complete point tables for documentation or further processing.

MicroGPS is intended for researchers working with microscopy, spectroscopy and imaging techniques where accurate point relocation across instruments is required.

## Installation

### Windows executable (recommended)

Download the latest `MicroGPS.exe` from the releases page.

No Python installation is required. Simply extract the downloaded file and run `MicroGPS.exe`.

### MacOs users

There is no MacOs executable at the moment, but you can have MicroGPS running from source on a Mac.

### Running from source

For developers or users who want to run MicroGPS from Python, follow instructions and recommendations in CONTRIBUTING.md.

## Typical workflow

1. Load a reference image (optical microscope, photograph, scan, etc.).
2. Mark three calibration points you can identify accross instruments.
3. Create a coordinate system using the corresponding instrument coordinates.
4. Add measurement points by clicking on the image or entering instrument coordinates.
5. Display the coordinates of every point in all calibrated coordinate systems.
6. Export the complete table for use during measurements or subsequent analyses.

Additional coordinate systems can be added at any time, making it straightforward to correlate measurements acquired on multiple instruments using the same reference image.
