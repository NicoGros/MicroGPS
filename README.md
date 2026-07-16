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
