"""
STEP-BY-STEP: HOW TO TYPE THE CODE TO FIND A PERSON
Simple demonstration with copy-paste examples
"""

from personalized_medications import setup_personalized_medications


print("\n" + "=" * 80)
print("STEP-BY-STEP: FINDING A PERSON")
print("=" * 80)

# ============================================================================
# STEP 1: Setup the database
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: SETUP DATABASE")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
db, manager = setup_personalized_medications()
""")

print("ACTION: Running this code...")
db, manager = setup_personalized_medications()

print("[OK] Database setup complete!")
print("     Now 'manager' has all the person data")


# ============================================================================
# STEP 2: Find Person 1 (John Smith)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: FIND PERSON 1")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
person = manager.get_elder(1)
""")

print("ACTION: Running this code...")
person = manager.get_elder(1)

print("\nRESULT: person variable now contains:")
print(f"  {person}")


# ============================================================================
# STEP 3: Display the person's information
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: DISPLAY PERSON'S INFORMATION")
print("=" * 80)

print("\nWHAT TO TYPE (to show person's name):")
print("""
print(person['name'])
""")

print("ACTION: Running this code...")
print(f"Result: {person['name']}")

print("\nWHAT TO TYPE (to show person's age):")
print("""
print(person['age'])
""")

print("ACTION: Running this code...")
print(f"Result: {person['age']}")

print("\nWHAT TO TYPE (to show all person info):")
print("""
for key, value in person.items():
    print(f"{key}: {value}")
""")

print("ACTION: Running this code...")
for key, value in person.items():
    print(f"  {key}: {value}")


# ============================================================================
# STEP 4: Find Person 2 (Mary Johnson)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: FIND PERSON 2")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
person_2 = manager.get_elder(2)
print(person_2['name'])
""")

print("ACTION: Running this code...")
person_2 = manager.get_elder(2)
print(f"Result: {person_2['name']}")


# ============================================================================
# STEP 5: Find Person 3 (Robert Brown)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: FIND PERSON 3")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
person_3 = manager.get_elder(3)
print(person_3['name'])
""")

print("ACTION: Running this code...")
person_3 = manager.get_elder(3)
print(f"Result: {person_3['name']}")


# ============================================================================
# STEP 6: Find All Persons
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: FIND ALL PERSONS")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
all_persons = manager.get_all_elders()
print(all_persons)
""")

print("ACTION: Running this code...")
all_persons = manager.get_all_elders()

print("\nRESULT: All persons in database:")
for p in all_persons:
    print(f"  Person {p['elder_id']}: {p['name']}")


# ============================================================================
# STEP 7: Find Person by Looping
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: FIND PERSON BY LOOPING THROUGH ALL")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
all_persons = manager.get_all_elders()

for person in all_persons:
    print(person['name'])
""")

print("ACTION: Running this code...")
all_persons = manager.get_all_elders()

print("\nRESULT:")
for person in all_persons:
    print(f"  - {person['name']}")


# ============================================================================
# STEP 8: Find Person by Name
# ============================================================================

print("\n" + "=" * 80)
print("STEP 8: FIND PERSON BY NAME")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
all_persons = manager.get_all_elders()

search_name = "John Smith"

for person in all_persons:
    if person['name'] == search_name:
        print(f"Found: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"Phone: {person['phone']}")
""")

print("ACTION: Running this code...")
all_persons = manager.get_all_elders()

search_name = "John Smith"

print(f"\nSearching for: {search_name}\n")

for person in all_persons:
    if person['name'] == search_name:
        print(f"Found: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"Phone: {person['phone']}")


# ============================================================================
# STEP 9: Check if Person Exists
# ============================================================================

print("\n" + "=" * 80)
print("STEP 9: CHECK IF PERSON EXISTS BEFORE USING")
print("=" * 80)

print("\nWHAT TO TYPE:")
print("""
person = manager.get_elder(1)

if person is not None:
    print(f"Person found: {person['name']}")
else:
    print("Person not found")
""")

print("ACTION: Running this code...")
person = manager.get_elder(1)

if person is not None:
    print(f"Result: Person found: {person['name']}")
else:
    print("Result: Person not found")


# ============================================================================
# STEP 10: Quick Cheat Sheet
# ============================================================================

print("\n" + "=" * 80)
print("QUICK CHEAT SHEET - COPY & PASTE")
print("=" * 80)

print("""
# Setup database (always do this first)
db, manager = setup_personalized_medications()

# Find Person 1
person_1 = manager.get_elder(1)
print(person_1['name'])  # Output: John Smith

# Find Person 2
person_2 = manager.get_elder(2)
print(person_2['name'])  # Output: Mary Johnson

# Find Person 3
person_3 = manager.get_elder(3)
print(person_3['name'])  # Output: Robert Brown

# Find All Persons
all_persons = manager.get_all_elders()
for p in all_persons:
    print(p['name'])

# Find Person by Name
all_persons = manager.get_all_elders()
for p in all_persons:
    if p['name'] == "John Smith":
        print(p)

# Find Person by ID (with check)
person = manager.get_elder(1)
if person:
    print(f"Found: {person['name']}")
else:
    print("Not found")
""")


# ============================================================================
# STEP 11: Practice - Interactive
# ============================================================================

print("\n" + "=" * 80)
print("PRACTICE: TRY THESE")
print("=" * 80)

print("\n1. Find Person 2's phone number:")
print("   CODE: person_2 = manager.get_elder(2)")
print("         print(person_2['phone'])")
person_2 = manager.get_elder(2)
print(f"   OUTPUT: {person_2['phone']}")

print("\n2. Find Person 1's emergency contact:")
print("   CODE: person_1 = manager.get_elder(1)")
print("         print(person_1['emergency_contact'])")
person_1 = manager.get_elder(1)
print(f"   OUTPUT: {person_1['emergency_contact']}")

print("\n3. Find Person 3's address:")
print("   CODE: person_3 = manager.get_elder(3)")
print("         print(person_3['address'])")
person_3 = manager.get_elder(3)
print(f"   OUTPUT: {person_3['address']}")

print("\n4. Count total persons:")
print("   CODE: all_persons = manager.get_all_elders()")
print("         print(len(all_persons))")
all_persons = manager.get_all_elders()
print(f"   OUTPUT: {len(all_persons)} persons")


print("\n" + "=" * 80)
print("DEMONSTRATION COMPLETE")
print("=" * 80)
print("""
KEY POINTS:
1. Always setup first: db, manager = setup_personalized_medications()
2. Find one person: manager.get_elder(ID)
3. Find all persons: manager.get_all_elders()
4. Access data: person['name'], person['age'], person['phone']
5. Loop to search: for person in all_persons: ...
6. Check if exists: if person is not None: ...
""")
