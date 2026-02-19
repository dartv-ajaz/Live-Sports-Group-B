import subprocess
import os

# Sirf wo scripts jo Repo B mein hain
SCRIPTS = [
    "fetch_hotstar.py"
]

def run_group_b():
    print("🚀 Group B Auto-Update Started...")
    
    for script in SCRIPTS:
        if os.path.exists(script):
            print(f"\n------------------------------------------")
            print(f"📡 Running: {script}")
            print(f"------------------------------------------")
            try:
                subprocess.run(["python", script], check=True)
                print(f"✅ Success: {script} completed.")
            except Exception as e:
                print(f"❌ Error: {script} failed")
        else:
            print(f"⚠️ Warning: {script} not found")

    print("\n🎉 Group B Update Finished.")

if __name__ == "__main__":
    run_group_b()
