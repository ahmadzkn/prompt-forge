import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import DatabaseManager
from src.optimizer import PromptOptimizer

def test_core():
    print("Testing Database...")
    db = DatabaseManager("test_db.db")
    try:
        session = db.add_session("Test Prompt", {"persona": "tester"}, "Final Prompt Test")
        print(f"Added session ID: {session.id}")
        
        history = db.get_history()
        print(f"History length: {len(history)}")
        assert len(history) >= 1
        
        retrieved = db.get_session(session.id)
        assert retrieved.raw_prompt == "Test Prompt"
        print("Database Test Passed.")
    except Exception as e:
        print(f"Database Test Failed: {e}")
    finally:
        db.close()
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")

    print("\nTesting Optimizer Initialization...")
    try:
        opt = PromptOptimizer()
        print("Optimizer Initialized.")
        # We won't call the API as LM Studio might not be running, but we verified the class loads.
    except Exception as e:
        print(f"Optimizer Init Failed: {e}")

if __name__ == "__main__":
    test_core()
