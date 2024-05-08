# AE598 Final Project: Vision-based Spacecraft Trajectory Estimation: A Structure from Motion Approach

## Overview
This repository contains the code and methodologies to perform 3D reconstruction of asteroid Bennu's surface, utilizing Structure from Motion (SfM) techniques. The primary goal is to reconstruct the asteroid's surface in three dimensions while simultaneously determining the camera/spacecraft's pose for navigation and mission planning purposes. This project specifically focuses on the OSIRIS-REx mission during which a spacecraft orbited and collected samples from asteroid Bennu.

## Data
The 3D reconstruction process in this project uses a set of 12 images captured by the MapCam camera mounted on the OSIRIS-REx spacecraft. These images were taken during the "Departure Flyby" mission phase and are stored in the `images` directory within this repository.

## Structure from Motion Implementations
This repository includes three different Structure from Motion implementations to cater to various aspects of the 3D reconstruction process:

### 1. Incremental SfM
To perform incremental Structure from Motion:
- **Notebook**: Open and run the `incremental_sfm.ipynb` notebook for a step-by-step walkthrough using this approach.

### 2. Incremental SfM (OpenMVG)
For an Incremental SfM implementation using OpenMVG, execute the following command in your terminal:
```bash
./openmvg_incremental.sh
```

### 3. Global SfM (OpenMVG)
For a Global SfM implementation using OpenMVG, execute the following command in your terminal:
```bash
./openmvg_global.sh
```
