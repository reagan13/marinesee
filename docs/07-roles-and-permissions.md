# Roles and Permissions

**STUDY** — functional requirements mention visitors and administrators. The paper does not publish a permission matrix.

**IMPLEMENTATION** default until `14-open-questions.md` is answered.

## Visitor

Students, tourists, local researchers, coastal community members.

May:

- browse the digital library
- open 3D models
- capture or upload a photo
- see identification results and confidence
- read educational / conservation content

May not:

- edit species records
- replace the SVM model
- see other users’ uploaded photos (if uploads are stored)

**OPEN:** whether a visitor account exists. Default is **no login** for visitors.

## Administrator

May:

- create / update / archive species profile text
- update conservation and habitat copy
- **OPEN:** upload or replace 3D assets
- **OPEN:** ship a new model file

May not need the identify camera for their admin job, but they can use the app as a visitor.

## What we will not add in v1

- Public social feed of identifications
- Role for “marine expert verifier” of every user photo
- City-wide staff hierarchy
