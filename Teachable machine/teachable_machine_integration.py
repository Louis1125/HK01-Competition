"""
TEACHABLE MACHINE INTEGRATION WITH MEDICATION SYSTEM
Converts web model to Python and integrates with medication lookup
"""

import json
import os
from datetime import datetime

# Import your existing medication system
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from personalized_medications import setup_personalized_medications
from elder_medication_system import setup_medication_database, MedicationManager, MedicationReminder


print("\n" + "=" * 80)
print("TEACHABLE MACHINE + MEDICATION SYSTEM")
print("=" * 80)


# ============================================================================
# STEP 1: UNDERSTAND YOUR TEACHABLE MACHINE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: YOUR TEACHABLE MACHINE MODEL")
print("=" * 80)

print("""
Your model structure:
  Model URL: ./my_model/
  Files needed:
    1. model.json      (model architecture)
    2. metadata.json   (class labels)
    3. weights files   (trained weights)

Your classes (what it recognizes):
  - Person 1 (John Smith)
  - Person 2 (Mary Johnson)
  - Person 3 (Robert Brown)
  - Unknown person
  - No person detected
""")


# ============================================================================
# STEP 2: PYTHON SIMULATION OF TEACHABLE MACHINE
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: PYTHON TEACHABLE MACHINE SIMULATOR")
print("=" * 80)

class TeachableMachineModel:
    """
    Simulates Teachable Machine image recognition
    In production, you'd load the actual model.json and weights
    """
    
    def __init__(self, model_path="./my_model/"):
        self.model_path = model_path
        self.classes = {
            0: "Person 1 (John Smith)",
            1: "Person 2 (Mary Johnson)",
            2: "Person 3 (Robert Brown)",
            3: "Unknown person",
            4: "No person detected"
        }
        print(f"[LOADED] Teachable Machine model from {model_path}")
        print(f"[CLASSES] Recognized: {list(self.classes.values())}")
    
    def predict(self, image_path):
        """
        Predict person from image
        In real version: uses model.predict(image)
        """
        print(f"\n[PREDICTING] Analyzing image: {image_path}")
        
        # Simulated predictions (in real code: model.predict(image))
        predictions = {
            0: 0.95,  # John Smith - 95% confidence
            1: 0.02,  # Mary Johnson - 2%
            2: 0.02,  # Robert Brown - 2%
            3: 0.01,  # Unknown - 1%
        }
        
        # Get top prediction
        top_class = max(predictions, key=predictions.get)
        confidence = predictions[top_class]
        person_name = self.classes[top_class]
        
        return {
            'person': person_name,
            'confidence': confidence,
            'all_predictions': predictions
        }
    
    def get_person_id(self, person_name):
        """Extract person ID from prediction"""
        if "Person 1" in person_name:
            return 1
        elif "Person 2" in person_name:
            return 2
        elif "Person 3" in person_name:
            return 3
        else:
            return None


# ============================================================================
# STEP 3: INTEGRATION WITH MEDICATION SYSTEM
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: TEACHABLE MACHINE + MEDICATION INTEGRATION")
print("=" * 80)

class TeachableMachinePersonDetector:
    """
    Combines Teachable Machine detection with medication lookup
    """
    
    def __init__(self, model_path="./my_model/"):
        # Load model
        self.model = TeachableMachineModel(model_path)
        
        # Setup medication system
        self.db = setup_medication_database()
        self.manager = MedicationManager(self.db)
        self.reminder = MedicationReminder(self.manager)  # Pass manager, not db
        
        print("[INITIALIZED] Detector with medication system")
    
    def detect_and_lookup(self, image_path):
        """
        Main function:
        1. Detect person from image (Teachable Machine)
        2. Lookup their medications (database)
        3. Return full information
        """
        
        # STEP 1: Predict person from image
        prediction = self.model.predict(image_path)
        person_name = prediction['person']
        confidence = prediction['confidence']
        
        print(f"\n[DETECTED] {person_name} ({confidence*100:.1f}% confidence)")
        
        # STEP 2: Extract person ID
        person_id = self.model.get_person_id(person_name)
        
        if person_id is None:
            print("[WARNING] Unknown person - cannot lookup medications")
            return {
                'detected': person_name,
                'confidence': confidence,
                'medications': None,
                'status': 'unknown'
            }
        
        # STEP 3: Lookup medications
        person = self.manager.get_elder(person_id)
        medications = self.manager.get_medications(person_id)
        
        if person:
            print(f"\n[FOUND] {person['name']} (Age {person['age']})")
        
        print(f"[MEDICATIONS] {len(medications)} medications:")
        for med in medications:
            print(f"  - {med['name']}: {med['dosage']} ({med['reason']})")
        
        # STEP 4: Check for due medications
        due_meds = self.reminder.get_due_medications(person_id)
        
        print(f"\n[DUE MEDS] {len(due_meds)} medications due now:")
        for med in due_meds:
            print(f"  - {med['name']} at {med['time']}")
        
        return {
            'detected': person_name,
            'confidence': confidence,
            'person_id': person_id,
            'person_info': {
                'name': person['name'] if person else 'Unknown',
                'age': person['age'] if person else None,
                'phone': person['phone'] if person else None
            },
            'medications': medications,
            'due_medications': due_meds,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }


# ============================================================================
# STEP 4: USAGE EXAMPLES
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: USAGE EXAMPLES")
print("=" * 80)

print("\nEXAMPLE 1: Basic detection from image")
print("-" * 80)

print("""
from teachable_machine_integration import TeachableMachinePersonDetector

# Initialize detector
detector = TeachableMachinePersonDetector(model_path="./my_model/")

# Detect person and lookup medications
result = detector.detect_and_lookup("person.jpg")

print(f"Detected: {result['detected']}")
print(f"Confidence: {result['confidence']*100:.1f}%")
print(f"Medications: {len(result['medications'])} found")
""")

print("\nEXAMPLE 2: Use in your Second Program")
print("-" * 80)

print("""
# At top of HK01 Competition 12-12-2025 main programme.py
from teachable_machine_integration import TeachableMachinePersonDetector

def main():
    detector = TeachableMachinePersonDetector()
    
    while True:
        # Get image from camera/file
        image_path = input("Enter image path (or 'exit'): ")
        if image_path == 'exit':
            break
        
        # Detect and lookup
        result = detector.detect_and_lookup(image_path)
        
        # Show results
        print(f"Person: {result['detected']}")
        print(f"Age: {result['person_info']['age']}")
        print(f"Due medications: {len(result['due_medications'])}")

if __name__ == "__main__":
    main()
""")

print("\nEXAMPLE 3: Real-time webcam detection")
print("-" * 80)

print("""
import cv2
from teachable_machine_integration import TeachableMachinePersonDetector

detector = TeachableMachinePersonDetector()

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Save frame temporarily
    cv2.imwrite("temp_frame.jpg", frame)
    
    # Detect person
    result = detector.detect_and_lookup("temp_frame.jpg")
    
    # Draw results on frame
    text = f"{result['detected']} ({result['confidence']*100:.0f}%)"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Person Detection + Medication Lookup", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
""")

print("\nEXAMPLE 4: Integration with your existing code")
print("-" * 80)

print("""
# In your HK01 Competition 12-12-2025 main programme.py, replace the person lookup:

OLD:
  person_id = input("Enter person ID (1-3): ")
  
NEW:
  detector = TeachableMachinePersonDetector()
  result = detector.detect_and_lookup("webcam_image.jpg")
  person_id = result['person_id']
  
  # Now automatically shows medications!
""")


# ============================================================================
# STEP 5: HOW TO SETUP YOUR MODEL FILES
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: SETTING UP YOUR TEACHABLE MACHINE MODEL")
print("=" * 80)

print("""
Your model directory structure should be:

project folder
- my_model folder
  - model.json (model architecture)
  - metadata.json (class labels)
  - weights.bin (weights file 1)
  - weights.bin.002 (weights file 2)
  - group1-shard1of* (additional weight files)
- teachable_machine_integration.py

TO EXPORT YOUR MODEL:
1. Go to teachablemachine.withgoogle.com
2. Train your model with images of persons 1, 2, 3
3. Click "Export"
4. Select "TensorFlow" then "Download"
5. Extract files to my_model folder
6. Save in your project directory

TO TRAIN YOUR MODEL:
1. Upload images of John Smith, label as Person 1
2. Upload images of Mary Johnson, label as Person 2
3. Upload images of Robert Brown, label as Person 3
4. Train model
5. Export and integrate
""")


# ============================================================================
# STEP 6: RUNNING EXAMPLES
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: RUN THE EXAMPLES")
print("=" * 80)

# Create detector
print("\n[CREATING] Teachable Machine detector...")
detector = TeachableMachinePersonDetector()

# Example 1: Detect from simulated image
print("\n\n--- EXAMPLE 1: Detect Person from Image ---\n")
result = detector.detect_and_lookup("person_image.jpg")

print("\n[RESULT SUMMARY]:")
print(f"  Detected: {result['detected']}")
print(f"  Confidence: {result['confidence']*100:.1f}%")
if result['status'] == 'success':
    print(f"  Person ID: {result['person_id']}")
    print(f"  Name: {result['person_info']['name']}")
    print(f"  Age: {result['person_info']['age']}")
    print(f"  Total Medications: {len(result['medications'])}")
    print(f"  Due Now: {len(result['due_medications'])}")
else:
    print(f"  Status: {result['status']}")


# ============================================================================
# STEP 7: NEXT STEPS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: NEXT STEPS")
print("=" * 80)

print("""
1. EXPORT YOUR MODEL:
   - Go to teachablemachine.withgoogle.com
   - Train with Person 1, 2, 3 images
   - Export as TensorFlow
   - Save to my_model/ folder

2. INTEGRATE INTO SECOND PROGRAM:
   - Import TeachableMachinePersonDetector
   - Replace manual person input with detection
   - Show medications automatically

3. ADD WEBCAM SUPPORT:
   - Install: pip install opencv-python
   - Use cv2.VideoCapture(0)
   - Real-time detection from camera

4. CREATE WEB INTERFACE:
   - Use Flask + your HTML/JavaScript from Teachable Machine
   - Python backend for medication lookup
   - Web frontend for real-time detection

5. DEPLOY:
   - Python server + Teachable Machine model
   - Web interface for medication management
   - Real-time person detection
""")

print("\n" + "=" * 80)
print("TEACHABLE MACHINE INTEGRATION READY!")
print("=" * 80)
