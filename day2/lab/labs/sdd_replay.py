"""Saved runs for Lab 1, used by the Replay button when the model cannot be reached.
These are typical outputs: the vague one uses 'sensible industry defaults', the spec one follows Axion's rules."""

CODE = {
"vague": '''def evaluate_release(release: dict) -> dict:
    """Release readiness check using common industry thresholds."""
    reasons = []
    # Critical defects block any release
    if release.get("open_sev1", 0) > 0:
        reasons.append("Open Sev-1 defects present")
    # Industry-standard quality bar
    if release.get("test_pass_rate", 0) < 95.0:
        reasons.append(f"Test pass rate {release.get('test_pass_rate')}% is below 95%")
    # Too many major defects
    if release.get("open_sev2", 0) > 5:
        reasons.append("More than 5 open Sev-2 defects")
    # Security: block critical vulnerabilities, and high ones if exposed to the network
    cvss = release.get("max_cvss", 0)
    if cvss >= 9.0:
        reasons.append(f"Critical vulnerability (CVSS {cvss})")
    elif cvss >= 7.0 and release.get("cve_network_facing"):
        reasons.append(f"High vulnerability (CVSS {cvss}) in a network-facing component")
    return {"verdict": "NO-GO" if reasons else "GO", "reasons": reasons or ["All checks passed"]}
''',
"spec": '''def evaluate_release(release: dict) -> dict:
    """GO / NO-GO for AX900 firmware releases, following Axion rules R1-R4."""
    reasons = []
    # R1: pass-rate threshold depends on whether the module is safety-rated
    limit = 98.0 if release["safety_rated"] else 94.0
    if release["test_pass_rate"] < limit:
        reasons.append(f"R1: pass rate {release['test_pass_rate']}% is below {limit}%")
    # R2: any open Sev-1 blocks the release
    if release["open_sev1"] > 0:
        reasons.append(f"R2: {release['open_sev1']} open Sev-1 defect(s)")
    # R3: more than 3 open Sev-2 blocks the release
    if release["open_sev2"] > 3:
        reasons.append(f"R3: {release['open_sev2']} open Sev-2 defects (limit 3)")
    # R4: vulnerability limits depend on network exposure
    cvss_limit = 6.5 if release["cve_network_facing"] else 8.9
    if (release["cve_network_facing"] and release["max_cvss"] >= 6.5) or release["max_cvss"] > 8.9:
        reasons.append(f"R4: CVSS {release['max_cvss']} exceeds the limit for this component ({cvss_limit})")
    return {"verdict": "NO-GO" if reasons else "GO", "reasons": reasons or ["All rules R1-R4 pass"]}
''',
}
