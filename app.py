from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    scan_result = ""
    target = ""

    if request.method == "POST":
        target = request.form.get("target", "").strip()

        if target:
            try:
                result = subprocess.run(
                    ["nmap", "-sV", target],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                scan_result = result.stdout

                if not scan_result:
                    scan_result = result.stderr

            except Exception as e:
                scan_result = f"Error: {str(e)}"

    return render_template(
        "index.html",
        scan_result=scan_result,
        target=target
    )


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)


def analyze_scan(scan_result):
    """Analyze Nmap results and generate a basic risk assessment."""

    open_ports = re.findall(
        r"^(\d+)/tcp\s+open\s+(\S+)",
        scan_result,
        re.MULTILINE
    )

    port_count = len(open_ports)

    risky_ports = {
        "21": "FTP",
        "23": "Telnet",
        "3389": "RDP",
        "445": "SMB",
        "3306": "MySQL"
    }

    found_risky_ports = []

    for port, service in open_ports:
        if port in risky_ports:
            found_risky_ports.append(f"{port} ({service})")

    if len(found_risky_ports) >= 2:
        risk_level = "High"
    elif len(found_risky_ports) == 1 or port_count >= 5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    recommendations = []

    if not open_ports:
        recommendations.append(
            "No open TCP ports were detected. Continue regular monitoring."
        )

    for port, service in open_ports:
        if port == "21":
            recommendations.append(
                "Review FTP usage and disable anonymous access if not required."
            )

        elif port == "23":
            recommendations.append(
                "Telnet is insecure. Disable it and use SSH instead."
            )

        elif port == "445":
            recommendations.append(
                "Review SMB access and restrict unnecessary network exposure."
            )

        elif port == "3389":
            recommendations.append(
                "Restrict RDP access and use strong authentication."
            )

        elif port == "3306":
            recommendations.append(
                "Do not expose MySQL publicly unless required."
            )

    if not recommendations:
        recommendations.append(
            "Review all exposed services and close unnecessary ports."
        )
        recommendations.append(
            "Keep operating systems and services updated."
        )
        recommendations.append(
            "Perform regular authorized security assessments."
        )

    return {
        "open_ports": open_ports,
        "port_count": port_count,
        "risky_ports": found_risky_ports,
        "risk_level": risk_level,
        "recommendations": recommendations
    }


@app.route("/", methods=["GET", "POST"])
def home():

    scan_result = ""
    target = ""
    analysis = None

    if request.method == "POST":

        target = request.form.get("target", "").strip()

        if target:

            try:
                result = subprocess.run(
                    ["nmap", "-sV", target],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                scan_result = result.stdout

                if not scan_result:
                    scan_result = result.stderr

                analysis = analyze_scan(scan_result)

            except subprocess.TimeoutExpired:
                scan_result = "Scan timed out."

            except FileNotFoundError:
                scan_result = (
                    "Nmap was not found. "
                    "Install it using: sudo apt install nmap"
                )

            except Exception as e:
                scan_result = f"Error: {str(e)}"

    return render_template(
        "index.html",
        scan_result=scan_result,
        target=target,
        analysis=analysis
    )


if __name__ == "__main__":
    app.run(debug=True)
