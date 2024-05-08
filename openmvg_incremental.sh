#!/bin/bash

# Set up paths for OpenMVG binaries and project directories
OPENMVG_BIN="/Users/manavvora/Desktop/AE598_3DV/ae598-3dv/openMVG_Build/Darwin-arm64-RELEASE"
IMAGE_DIR="/Users/manavvora/Desktop/AE598-Final-Project/images"
OUTPUT_DIR="/Users/manavvora/Desktop/AE598-Final-Project/results"
MATCHES_DIR="${OUTPUT_DIR}/matches"
RECONSTRUCTION_DIR="${OUTPUT_DIR}/reconstruction_global"

# Ensure output directories exist
mkdir -p ${OUTPUT_DIR}
mkdir -p ${MATCHES_DIR}
mkdir -p ${RECONSTRUCTION_DIR}

echo "Step 1: Intrinsics analysis" #This step will generate an sfm_data.json file in the matches directory that contains the camera intrinsics.
${OPENMVG_BIN}/openMVG_main_SfMInit_ImageListing -i ${IMAGE_DIR} -o ${MATCHES_DIR} -d

echo "Step 2: Compute features"
${OPENMVG_BIN}/openMVG_main_ComputeFeatures -i ${MATCHES_DIR}/sfm_data.json -o ${MATCHES_DIR} -m SIFT

echo "Step 3: Compute matching pairs"
${OPENMVG_BIN}/openMVG_main_PairGenerator -i ${MATCHES_DIR}/sfm_data.json -o ${MATCHES_DIR}/pairs.bin

echo "Step 4: Compute matches"
${OPENMVG_BIN}/openMVG_main_ComputeMatches -i ${MATCHES_DIR}/sfm_data.json -p ${MATCHES_DIR}/pairs.bin -o ${MATCHES_DIR}/matches.putative.bin

echo "Step 5: Global SfM reconstruction"
${OPENMVG_BIN}/openMVG_main_SfM --sfm_engine INCREMENTAL --input_file ${MATCHES_DIR}/sfm_data.json --match_file ${MATCHES_DIR}/matches.putative.bin -output_dir ${RECONSTRUCTION_DIR}

echo "Step 6: Colorize structure"
${OPENMVG_BIN}/openMVG_main_ComputeSfM_DataColor -i ${RECONSTRUCTION_DIR}/sfm_data.bin -o ${RECONSTRUCTION_DIR}/colorized_incremental.ply

echo "All steps completed successfully!"
