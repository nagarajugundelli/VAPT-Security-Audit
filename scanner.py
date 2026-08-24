import subprocess

target = "127.0.0.1"

print("Starting Vulnerability Assessment...")
print("Target:", target)

result = subprocess.run(
    ["nmap", "-sV", target],
    capture_output=True,
    text=True
)

print(result.stdout)
import subprocess

target = input("Enter authorized target IP address: ")

print("\nStarting Security Scan...")
print("Target:", target)

result = subprocess.run(
    ["nmap", "-sV", target],
    capture_output=True,
    text=True
)

print("\n--- SCAN RESULT ---\n")
print(result.stdout)
