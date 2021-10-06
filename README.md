# Stability of mpMRI prostate radiomic features to variations in segmentation using in-silico contour generation.

This repository contains data and code accompanying our publication on "Assessing the stability of mpMRI prostate radiomic features to variations in segmentation using in-silico contour generation"

Preprint available @ NA

Publication available @ NA

**Note:** `Please cite the paper (if available) or this Github repo if you find shared codes and information useful!`

# Abstract:

**Purpose:** To propose an automated method to assess the stability of radiomic features to variations in segmentation using in-silico contour generation. The proposed method was used to identify robust radiomics features in prostate multiparametric (mp) MRI sequences.

**Methods:** In this study, we investigated the stability of radiomic features to variations in segmentation by simulating the sources of variability using the data augmentation paradigm in deep learning (DL). Manual annotation provided for the whole prostate gland on mpMRI sequences - T2w, ADC, and SUB DCE was used for this investigation. The method involved perturbing the manual segmentation using simple transformations such as rotation, scaling, and shifting to simulate various under-and/or over-segmentation scenarios. 15 synthetic contours were generated for a given ground truth segmentation. Synthetic contour variability with respect to the ground truth segmentation was measured using the Dice coefficient. A total of 1595 radiomic features were extracted from each image-segmentation pair. The feature stability was assessed using the intraclass correlation coefficient, ICC(1,1). Stable features were thresholded at the 95% confidence interval of the ICC estimate with a value greater than 0.90. 

Two datasets were used in this study. 100 patients diagnosed with low/very-low risk prostate cancer enrolled in Active Surveillance (AS) at the National Cancer Institute in Milan were used to identify the stable features. The external open-source dataset called the “QIN Prostate dataset” was used to evaluate the robustness of the selected stable features. The overlap of stable features identified in both these datasets was categorized as robust features in this study.

**Results:** A substantial fraction of the best-filtered radiomic features derived from T2w (99%), ADC (98%), SUBwash-in (97%) and SUBwash-out (98%) sequences showed stability to variations in segmentation. However, among them, only 71% of the T2w features, 86% of the ADC features, 94% of SUBwash-in features, and 96% of SUBwash-out features were found to be highly robust.

**Conclusions:** Features stable to inter-/intra-observer variability in segmentation of any ROI can be identified using the method proposed in this work and can be easily integrated into any pipeline that involves feature stability study. The labor-intensive process of manual annotation involving multiple radiologists for similar studies can be avoided using this technique. The set of robust features identified in this work can be considered for further modeling or analysis. 

Keywords: prostate cancer; segmentation variation; deep learning; radiomic features


# Repository Overview

Contains 3 jupyter notebooks which can either be run locally on your computer after downloading the entire repository or can be run remotely on Google Colab

1. **Contour Generator:** This notebook was designed to visualize the impact of various augmentation scenarios on a sample data. It can be run locally on your computer or on google colab.
2. **Radiomics Feature Extractor:** This notebook was designed to illustrate the workflow associated with in-silico contour generation using Torchio and feature extraction using pyradiomics
3. **Stability Analysis:** This notebook was designed to give an overall idea about the pipeline followed for the contour stability analysis

