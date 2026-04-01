DISEASE_SPECIALIST_MAPPING = {
    # Specialist 1: For all digestive, stomach, bowel, and liver issues.
    'Gastroenterologist': [
        'acute pancreatitis',
        'cholecystitis',
        'chronic constipation',
        'diverticulitis',
        'esophagitis',
        'gastrointestinal hemorrhage',
        'infectious gastroenteritis',
        'liver disease',
        'noninfectious gastroenteritis',
    ],

    # Specialist 2: For all skin and hair-related conditions.
    'Dermatologist': [
        'eczema',
        'fungal infection of the hair',
        'psoriasis',
        'pyogenic skin infection',
        'sebaceous cyst',
    ],

    # Specialist 3: For bone, joint, muscle, nerve, and injury-related issues.
    'Orthopedic Surgeon': [
        'arthritis of the hip',
        'bursitis',
        'complex regional pain syndrome',
        'concussion',
        'gout',
        'injury to the arm',
        'injury to the leg',
        'multiple sclerosis', # Often a Neurologist, but Ortho is a good start for movement issues.
        'peripheral nerve disorder',
        'spinal stenosis',
        'spondylosis',
        'sprain or strain',
    ],

    # Specialist 4: For female reproductive health and pregnancy-related issues.
    'Gynecologist': [
        'hyperemesis gravidarum',
        'problem during pregnancy',
        'spontaneous abortion',
        'vaginal cyst',
        'vulvodynia',
    ],

    # Specialist 5: The primary care doctor for a wide range of general, systemic,
    # respiratory, urinary, and mental health issues. This is the best first point of contact.
    'General Physician': [
        'acute bronchiolitis',
        'acute bronchitis',
        'acute stress reaction',
        'anxiety',
        'benign prostatic hyperplasia (bph)', # Can be referred to a Urologist
        'conjunctivitis due to allergy',
        'cystitis',
        'dental caries', # Should see a Dentist, but GP is the best fit here.
        'depression',
        'developmental disability',
        'hypoglycemia',
        'marijuana abuse',
        'nose disorder',
        'obstructive sleep apnea (osa)',
        'otitis media',
        'personality disorder',
        'pneumonia',
        'seasonal allergies (hay fever)',
        'sickle cell crisis', # Can be referred to a Hematologist
        'strep throat',
        'urinary tract infection',
    ]
}

# You can also create a reverse mapping for quick lookups
# From disease name to specialist
DISEASE_TO_SPECIALIST = {
    disease: specialist
    for specialist, diseases in DISEASE_SPECIALIST_MAPPING.items()
    for disease in diseases
}

# Example usage:
# predicted_disease = "psoriasis"
# specialist_to_find = DISEASE_TO_SPECIALIST.get(predicted_disease, "General Physician")
# print(specialist_to_find) # Output: Dermatologist

