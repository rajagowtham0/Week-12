# Clinical Note Standardization Document

## Objective

The purpose of this document is to define a standardized clinical note schema that can be shared across all AI-powered modules within the CCMS ecosystem, including:

* Clinical Documentation AI
* Clinical Match API
* Recommendation API
* Treatment Planning Engine
* Future AI Services

This common schema ensures interoperability, consistency, and reusability across all clinical workflows.

---

# Standard Clinical Note Schema

```json
{
  "patient_id": "",
  "assessment": {},
  "diagnosis": {},
  "treatment_plan": {},
  "home_plan": {},
  "recommendations": {}
}
```

---

# Assessment Note Schema

Captures patient-reported symptoms and assessment findings.

```json
{
  "assessment": {
    "chief_complaint": "",
    "duration": "",
    "symptoms": [],
    "pain_location": "",
    "pain_description": "",
    "pain_scale": "",
    "aggravating_factors": [],
    "relieving_factors": [],
    "functional_limitations": [],
    "clinical_findings": [],
    "assessment_summary": ""
  }
}
```

### Example

```json
{
  "assessment": {
    "chief_complaint": "Lower Back Pain",
    "duration": "3 Weeks",
    "symptoms": [
      "Radiating Pain",
      "Difficulty Standing"
    ],
    "pain_location": "Lower Back",
    "pain_description": "Sharp Pain",
    "pain_scale": "7/10",
    "aggravating_factors": [
      "Standing"
    ],
    "relieving_factors": [
      "Rest"
    ],
    "functional_limitations": [
      "Walking Long Distances"
    ],
    "clinical_findings": [
      "Reduced Lumbar Flexion"
    ],
    "assessment_summary": "Patient presents with chronic lower back pain."
  }
}
```

---

# Diagnosis Note Schema

Stores clinician-confirmed diagnosis information.

```json
{
  "diagnosis": {
    "primary_diagnosis": "",
    "secondary_diagnosis": [],
    "clinical_impression": "",
    "differential_diagnosis": [],
    "recommended_tests": [],
    "diagnosis_summary": ""
  }
}
```

### Example

```json
{
  "diagnosis": {
    "primary_diagnosis": "Lumbar Spondylosis",
    "secondary_diagnosis": [],
    "clinical_impression": "Mechanical Low Back Pain",
    "differential_diagnosis": [
      "Disc Prolapse"
    ],
    "recommended_tests": [
      "MRI Lumbar Spine"
    ],
    "diagnosis_summary": "Findings suggest lumbar spondylosis."
  }
}
```

---

# Treatment Plan Schema

Defines the planned clinical intervention.

```json
{
  "treatment_plan": {
    "treatment_goals": [],
    "treatment_recommendations": [],
    "therapy_plan": [],
    "session_frequency": "",
    "estimated_duration": "",
    "treatment_summary": ""
  }
}
```

### Example

```json
{
  "treatment_plan": {
    "treatment_goals": [
      "Reduce Pain",
      "Improve Mobility"
    ],
    "treatment_recommendations": [
      "Lumbar Mobilization",
      "Core Strengthening"
    ],
    "therapy_plan": [
      "Physiotherapy"
    ],
    "session_frequency": "3 Sessions Per Week",
    "estimated_duration": "4 Weeks",
    "treatment_summary": "Structured physiotherapy program initiated."
  }
}
```

---

# Home Plan Schema

Captures activities that the patient performs outside the clinic.

```json
{
  "home_plan": {
    "home_exercises": [],
    "lifestyle_modifications": [],
    "activity_restrictions": [],
    "patient_instructions": [],
    "home_plan_summary": ""
  }
}
```

### Example

```json
{
  "home_plan": {
    "home_exercises": [
      "Hamstring Stretch",
      "Pelvic Tilt Exercise"
    ],
    "lifestyle_modifications": [
      "Improve Sitting Posture"
    ],
    "activity_restrictions": [
      "Avoid Heavy Lifting"
    ],
    "patient_instructions": [
      "Perform Exercises Twice Daily"
    ],
    "home_plan_summary": "Daily exercise program prescribed."
  }
}
```

---

# Recommendation Schema

Provides AI-generated or clinician-approved recommendations.

```json
{
  "recommendations": {
    "recommended_tests": [],
    "specialist_referrals": [],
    "follow_up_actions": [],
    "risk_factors": [],
    "clinical_recommendations": [],
    "recommendation_summary": ""
  }
}
```

### Example

```json
{
  "recommendations": {
    "recommended_tests": [
      "MRI Lumbar Spine"
    ],
    "specialist_referrals": [
      "Consult Orthopedic RAJU"
    ],
    "follow_up_actions": [
      "Review After 2 Weeks"
    ],
    "risk_factors": [
      "Prolonged Sitting"
    ],
    "clinical_recommendations": [
      "Continue Physiotherapy"
    ],
    "recommendation_summary": "Follow-up review advised."
  }
}
```

---

# Complete Standardized Clinical Note

```json
{
  "patient_id": "P10001",
  "assessment": {},
  "diagnosis": {},
  "treatment_plan": {},
  "home_plan": {},
  "recommendations": {}
}
```

## Benefits

* Standardized output across all AI modules.
* Simplifies integration with Clinical Match APIs.
* Enables Recommendation Engines to consume structured data.
* Reduces duplication across future AI services.
* Supports scalability and interoperability within the CCMS platform.

```
```
