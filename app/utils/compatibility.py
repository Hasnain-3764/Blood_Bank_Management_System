def is_compatible(donor_type, recipient_type):
    compatible_types = {
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'O-': ['O-', 'O+', 'A+', 'B+', 'AB+'],
        'A+': ['A+', 'AB+'],
        'A-': ['A-', 'A+', 'AB+', 'AB-'],
        'B+': ['B+', 'AB+'],
        'B-': ['B-', 'B+', 'AB+', 'AB-'],
        'AB+': ['AB+'],  # Universal recipient
        'AB-': ['AB-', 'AB+', 'A-', 'B-']
    }
    return recipient_type in compatible_types.get(donor_type, [])
