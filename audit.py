print("VULNERABILITY ASSESSMENT AND SECURITY AUDIT")
print("=" * 50)

target = input("Enter target name or IP: ")
open_ports = input("Enter open ports found: ")
outdated = input("Is outdated software found? (yes/no): ")

risk = "Low"

if outdated.lower() == "yes":
    risk = "High"
elif "22" in open_ports or "80" in open_ports:
    risk = "Medium"

print("\n--- SECURITY AUDIT RESULT ---")
print("Target:", target)
print("Open Ports:", open_ports)
print("Outdated Software:", outdated)
print("Risk Level:", risk)

print("\nRecommendations:")

if risk == "High":
    print("1. Update outdated software")
    print("2. Review exposed services")
    print("3. Apply security patches")

elif risk == "Medium":
    print("1. Review unnecessary open ports")
    print("2. Restrict network access")
    print("3. Configure firewall rules")

else:
    print("1. Continue regular security monitoring")
    print("2. Keep software updated")
