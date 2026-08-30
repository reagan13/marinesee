# Functional Requirements

**STUDY** — Chapter 3, Requirements Specification, plus Chapters 1.3–1.5.

IDs are for tracing in code, tests, and later modules. They are **IMPLEMENTATION** labels, not from the paper.

## Actors

See `07-roles-and-permissions.md`.

- **Visitor** (student, tourist, researcher, coastal community member)
- **Administrator** (manages library content)

## FR-1 Capture and upload

The system shall allow a visitor to:

- capture a seagrass image with the Android camera
- upload an existing image from the device

## FR-2 SVM identification

The system shall automatically classify the image as one of the nine documented Mati seagrass species using the trained SVM.

## FR-3 Result + profile

After identification the system shall show:

- scientific name
- common name
- botanical characteristics
- ecological role
- conservation status
- habitat information

## FR-4 Confidence and retake

The system shall display a **confidence score** for every identification.

If confidence is below the threshold, the system shall recommend capturing the image again.

**OPEN:** numeric threshold. Do not invent 0.70 vs 0.80 until the team picks it after the first model eval.

## FR-5 Interactive 3D

The system shall let the user rotate, zoom, and inspect the 3D model of a species.

## FR-6 Digital library

The system shall provide a browsable library of all nine localized species, each with the profile fields in `11-species.md`.

## FR-7 Conservation education

The system shall present educational content about seagrass ecosystems and conservation, not only raw taxonomy.

## FR-8 Navigation

The system shall support clear mobile navigation between identify, library, 3D, and (if present) about/help.

## FR-9 Persistence

The system shall store and retrieve species information through the chosen database / content store.

## FR-10 Admin content management

The system shall allow administrators to manage educational content and species information.

**OPEN:** which fields are editable in v1, and whether admins also manage 3D files and the shipped model file.

## FR-11 Accessibility of navigation

The system shall keep navigation usable for non-technical mobile users (clear labels, large targets, short instructions).
