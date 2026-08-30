# Purpose and Objectives

**STUDY** — Chapters 1.2, 1.3, 1.4.

## Project identity

**Name:** MarineSee  
**Full title:** A Mobile-Based Seagrass Species Identification System for Mati City Using Image Recognition and Interactive 3D Visualization  
**Locale:** Coastal waters of Mati City, Davao Oriental (Lawigan, Taitaidaga, Manguihay, Pujada Island / Pujada Bay)  
**Form:** Android mobile application + SVM identification model + localized digital library  
**Authors:** **OPEN** — not listed in the extracted paper. Word last-modified by Daniel Calibara.

The system replaces static field guides and expert-only identification with one mobile learning tool.

## Problem being addressed

**STUDY** — Chapter 1.1.

Mati has nine documented seagrass species, but students, tourists, and coastal residents still struggle to tell them apart. Printed guides, photographs, and expert talks are hard for beginners because seagrass structure does not read well in 2D. That gap keeps marine-biodiversity awareness low.

## Main purpose

**STUDY** — Chapter 1.2.

Build **MarineSee**, a mobile educational platform that uses:

1. Interactive 3D visualization
2. SVM-based image recognition

so users can **identify** and **learn** the seagrass species found in Mati City.

The library shows, for each species: scientific name, common name, botanical characteristics, ecological role, conservation status, and geographic / growth information.

The innovation the paper claims is **localization**: nine Mati species, manipulable 3D models, and automated identification — not another global plant app.

## General objective

Develop MarineSee as a mobile educational platform that uses interactive 3D visualization to improve awareness and understanding of Mati seagrass species, with an SVM image-recognition system for species identification.

## Specific objectives

| # | Objective | What “done” looks like in the product |
|---|-----------|----------------------------------------|
| 1 | Integrate SVM identification and interactive 3D models for the nine documented species | User can identify a photo as one of the nine and open that species’ 3D model |
| 2 | Build a centralized digital library of localized species profiles | All nine profiles exist with the required fields (see `11-species.md`) |
| 3 | Design a responsive mobile UI with 3D controls | User can rotate, zoom, and inspect each model on a phone |
| 4 | Train an SVM on color, texture, and shape features to **≥ 85%** accuracy | Documented train/val/test scores on the held-out set meet 85% |
| 5 | Evaluate quality and acceptability with ISO/IEC 25010 | Students, tourists, researchers, and coastal community members complete the evaluation |

## User evaluation objective

**STUDY** — after 1.3.

Students, tourists, researchers, and coastal community members evaluate the app through surveys, questionnaires, and actual use. Characteristics named: functional suitability, usability, performance efficiency, reliability, compatibility, portability.

See `13-evaluation-iso25010.md`.

## Significance (who the product is for)

**STUDY** — Chapter 1.4.

| Stakeholder | Benefit the system must actually deliver |
|-------------|------------------------------------------|
| Students and educators | 3D + identification that is clearer than textbook plates |
| Tourists | Learn what they see on Mati beaches; identify from a photo |
| Coastal communities and fisherfolk | Recognize local seagrass and why it matters to fisheries |
| Local researchers | One localized reference: 3D, identification, organized profiles |
| Future researchers | A reference for SVM + 3D + environmental education systems |
