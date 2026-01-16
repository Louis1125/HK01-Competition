"""
ML-to-SQL Auto Lookup Pipeline
Identifies a person via ML, then automatically queries the database without manual SQL coding.
"""

import sqlite3
import math


# ============================================================================
# STEP 1: Set up a sample SQLite database with person records
# ============================================================================

def setup_database():
    """Create and populate a sample person database."""
    conn = sqlite3.connect(':memory:')  # In-memory DB for demo
    cursor = conn.cursor()
    
    # Create people table
    cursor.execute('''
        CREATE TABLE people (
            person_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT,
            department TEXT
        )
    ''')
    
    # Insert sample data
    sample_people = [
        (1, "Alice Johnson", 28, "alice@company.com", "Engineering"),
        (2, "Bob Smith", 35, "bob@company.com", "Sales"),
        (3, "Charlie Brown", 42, "charlie@company.com", "HR"),
        (4, "Diana Prince", 31, "diana@company.com", "Marketing"),
        (5, "Eve Wilson", 26, "eve@company.com", "Engineering"),
    ]
    
    cursor.executemany(
        'INSERT INTO people (person_id, name, age, email, department) VALUES (?, ?, ?, ?, ?)',
        sample_people
    )
    
    conn.commit()
    return conn


# ============================================================================
# STEP 2: Simple ML Model - Nearest Neighbor to predict person_id
# ============================================================================

class SimpleML:
    """
    Simple ML model using nearest-neighbor matching.
    Features: [height, weight, age] → predicts person_id
    """
    
    def __init__(self):
        # Training data (height in cm, weight in kg, age in years)
        self.X_train = [
            [170, 65, 28],   # Alice
            [180, 80, 35],   # Bob
            [185, 90, 42],   # Charlie
            [165, 60, 31],   # Diana
            [168, 62, 26],   # Eve
        ]
        
        # Labels: person_id (1-5)
        self.y_train = [1, 2, 3, 4, 5]
    
    def predict(self, features):
        """Find the closest training sample and return its person_id."""
        min_distance = float('inf')
        best_person_id = None
        
        for i, training_sample in enumerate(self.X_train):
            # Calculate Euclidean distance
            distance = math.sqrt(
                (features[0] - training_sample[0])**2 +
                (features[1] - training_sample[1])**2 +
                (features[2] - training_sample[2])**2
            )
            
            if distance < min_distance:
                min_distance = distance
                best_person_id = self.y_train[i]
        
        return best_person_id


# ============================================================================
# STEP 3: Auto SQL Query Helper (no manual SQL coding)
# ============================================================================

class PersonLookup:
    """Automatically queries database without user writing SQL."""
    
    def __init__(self, db_conn, ml_model):
        self.conn = db_conn
        self.model = ml_model
    
    def identify_and_fetch(self, features):
        """
        Input: person features (height, weight, age)
        Output: person's data from database (automatic)
        
        Args:
            features: list/array [height, weight, age]
        
        Returns:
            dict with person's data or None if not found
        """
        # Step 1: Use ML to predict person_id
        predicted_person_id = self.model.predict(features)
        
        print(f"🤖 ML Model identified: person_id = {predicted_person_id}")
        
        # Step 2: Auto-generate and execute SQL query (user doesn't write it)
        person_data = self._auto_query_person(predicted_person_id)
        
        if person_data:
            print(f"✓ Found in database: {person_data['name']}")
            return person_data
        else:
            print("✗ Person not found in database")
            return None
    
    def _auto_query_person(self, person_id):
        """
        Internal: automatically execute SQL query for person_id.
        User never sees or writes SQL.
        """
        cursor = self.conn.cursor()
        
        # Pre-built SQL template (internal, hidden from user)
        cursor.execute(
            'SELECT person_id, name, age, email, department FROM people WHERE person_id = ?',
            (person_id,)
        )
        
        row = cursor.fetchone()
        
        if row:
            return {
                'person_id': row[0],
                'name': row[1],
                'age': row[2],
                'email': row[3],
                'department': row[4]
            }
        return None
    
    def get_all_people(self):
        """Convenience: fetch all people without writing SQL."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT person_id, name, age, email, department FROM people')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'person_id': row[0],
                'name': row[1],
                'age': row[2],
                'email': row[3],
                'department': row[4]
            })
        return results


# ============================================================================
# STEP 4: Demo - End-to-End Pipeline
# ============================================================================

def main():
    print("=" * 70)
    print("ML → AUTO SQL LOOKUP DEMO")
    print("=" * 70)
    
    # Setup
    print("\n1️⃣  Setting up database...")
    db = setup_database()
    
    print("2️⃣  Training ML model...")
    model = SimpleML()
    
    print("3️⃣  Creating lookup helper...")
    lookup = PersonLookup(db, model)
    
    # Show available people
    print("\n📋 Available people in database:")
    for person in lookup.get_all_people():
        print(f"   {person['person_id']}: {person['name']} ({person['age']}) - {person['department']}")
    
    # Demo: Identify person and auto-fetch from DB
    print("\n" + "=" * 70)
    print("TEST 1: Identify someone similar to Alice (170cm, 65kg, 28yo)")
    print("=" * 70)
    result = lookup.identify_and_fetch([170, 65, 28])
    if result:
        print(f"\n📊 Retrieved Data:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("TEST 2: Identify someone similar to Bob (180cm, 80kg, 35yo)")
    print("=" * 70)
    result = lookup.identify_and_fetch([180, 80, 35])
    if result:
        print(f"\n📊 Retrieved Data:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("TEST 3: Identify someone similar to Charlie (185cm, 90kg, 42yo)")
    print("=" * 70)
    result = lookup.identify_and_fetch([185, 90, 42])
    if result:
        print(f"\n📊 Retrieved Data:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✓ Done! No SQL was written by the user.")
    print("=" * 70)
    
    db.close()
    print("=" * 70)
    
    db.close()


if __name__ == "__main__":
    main()
