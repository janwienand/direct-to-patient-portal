#!/usr/bin/env python3
"""Collapse a Sonatype SARIF file to one alert per component.

sonatype/actions/evaluate emits one SARIF result per policy violation. A
manifest scan resolves a package into every platform-specific wheel published
for it, and each wheel is then evaluated separately, so a single vulnerability
is reported once per wheel. Measured on six packages: 433 distinct
vulnerabilities became 3,649 alerts, 3,420 of them for tensorflow alone, where
every CVE appeared exactly nine times.

That is unusable in GitHub code scanning, where each alert is a row a human is
expected to triage. This script rewrites the file so each component becomes a
single alert carrying its full vulnerability list — which is also what Sonatype
recommends for ticketing: aggregate all violations for one component into one
item, because upgrading the component usually resolves all of them at once.

Every vulnerability keeps its deep link into Lifecycle, so "tell me more about
this CVE" still lands on the Sonatype vulnerability page rather than dead-ending
in the alert. Pass --report-url to also link the Application Composition Report;
the evaluate action exposes it as the report-url output.

The tool driver block is left untouched, so the analysis stays identified as
Sonatype's own. Upload the result from inside the workflow via
github/codeql-action/upload-sarif — that is the same path the action itself
uses, and it is what gives the analysis its workflow provenance and category.

Pass --public-links when the target repository is public. Lifecycle deep links
carry the IQ hostname, and on a hosted tenant that hostname contains the
customer name. In that mode every identifier is pointed at a public source
instead (NVD, GitHub Advisories, links.sonatype.com), the report link is
dropped, and the script refuses to write the file if any trace of the IQ host
survives.

Usage:
    python3 tools/aggregate-sonatype-sarif.py in.sarif out.sarif [--report-url URL] [--public-links] [--security-only]

--security-only drops components whose violations are licence or
architecture-quality only, leaving the alerts that carry an actual CVE.
"""
import json
import re
import sys
from collections import defaultdict

VULN = re.compile(r"(?:CVE-\d{4}-\d+|sonatype-\d{4}-\d+|GHSA-[0-9a-z-]+)", re.I)
# "Security-High violation found for tensorflow@2.4.0"
DESC = re.compile(r"^(?P<policy>\S+) violation found for (?P<component>.+)$")
# The action appends: "Check the [vulnerability details page](<iq>/assets/
# index.html#/vulnerabilities/CVE-...) for the latest details".
VULN_LINK = re.compile(r"\((https?://[^)\s]+?)/assets/index\.html#/vulnerabilities/([^)\s]+)\)")


def severity_rank(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return -1.0


PUBLIC_LINK_RULES = (
    (re.compile(r"^CVE-", re.I), "https://nvd.nist.gov/vuln/detail/{id}"),
    (re.compile(r"^GHSA-", re.I), "https://github.com/advisories/{id}"),
    (re.compile(r"^sonatype-", re.I),
     "https://links.sonatype.com/products/clm/vulnerability/{id}"),
)


def public_link(vuln_id):
    for pattern, template in PUBLIC_LINK_RULES:
        if pattern.match(vuln_id):
            return template.format(id=vuln_id)
    return None


def main(src, dst, report_url=None, public_links=False, security_only=False):
    if public_links:
        # A Lifecycle report link always embeds the IQ hostname.
        report_url = None
    with open(src) as fh:
        sarif = json.load(fh)

    run = sarif["runs"][0]
    rules = {r["id"]: r for r in run["tool"]["driver"]["rules"]}
    iq_base = None

    # component -> collected facts
    comp = defaultdict(lambda: {
        "vulns": set(), "policies": set(), "severity": -1.0,
        "level": "warning", "location": None, "violations": 0,
        "tags": set(), "precision": None,
    })

    for result in run["results"]:
        rule = rules.get(result["ruleId"], {})
        markdown = rule.get("help", {}).get("markdown", "")
        description = (rule.get("shortDescription", {}).get("text")
                       or rule.get("fullDescription", {}).get("text", ""))

        match = DESC.match(description.strip())
        if match:
            key = match.group("component")
            policy = match.group("policy")
        else:
            parts = result["ruleId"].split("/")
            key = parts[1] if len(parts) > 1 else result["ruleId"]
            policy = parts[0]

        entry = comp[key]
        entry["violations"] += 1
        entry["policies"].add(policy)
        # A single violation names its CVE and usually the GHSA alias for the
        # same issue. Counting both would inflate the total, so the GHSA id is
        # only kept when the violation has no CVE of its own.
        found = {v.upper() for v in VULN.findall(markdown)}
        preferred = {v for v in found if not v.startswith("GHSA")}
        entry["vulns"].update(preferred or found)

        link = VULN_LINK.search(markdown)
        if link and iq_base is None:
            iq_base = link.group(1)

        props = rule.get("properties", {})
        entry["tags"].update(props.get("tags", []))
        if props.get("precision") and not entry["precision"]:
            entry["precision"] = props["precision"]

        sev = severity_rank(props.get("security-severity"))
        if sev > entry["severity"]:
            entry["severity"] = sev
        if entry["location"] is None and result.get("locations"):
            entry["location"] = result["locations"][0]

    # Components whose only violations are licence or architecture-quality
    # rules produce alerts with no vulnerability behind them. In a shared
    # Security tab they outnumber and dilute the findings that matter; the
    # licence and waiver workflow lives in the Lifecycle UI anyway.
    skipped_no_vulns = 0
    new_rules, new_results = [], []
    for name in sorted(comp, key=lambda k: (-comp[k]["severity"], -len(comp[k]["vulns"]), k)):
        e = comp[name]
        if security_only and not e["vulns"]:
            skipped_no_vulns += 1
            continue
        vulns = sorted(e["vulns"])
        rule_id = f"sonatype/{name}"

        headline = (f"{len(vulns)} known vulnerabilities in {name}"
                    if vulns else f"Policy violations in {name}")

        def vuln_link(vuln_id):
            if public_links:
                url = public_link(vuln_id)
                return f"[{vuln_id}]({url})" if url else f"`{vuln_id}`"
            if not iq_base:
                return f"`{vuln_id}`"
            return f"[{vuln_id}]({iq_base}/assets/index.html#/vulnerabilities/{vuln_id})"

        shown = vulns[:60]
        body = [
            f"**{name}** — {len(vulns)} distinct vulnerabilities across "
            f"{e['violations']} policy violations.",
            "",
            f"Policies violated: {', '.join(sorted(e['policies']))}",
            "",
            "Upgrading or replacing this component addresses all of them at once. "
            "The dependency path, the recommended version and the waiver workflow "
            "are in Sonatype Lifecycle.",
            "",
        ]
        if report_url:
            body += [f"➜ [Open the Application Composition Report in Lifecycle]({report_url})", ""]
        body += ["### Vulnerabilities", "",
                 ("Each identifier links to its public advisory."
                  if public_links else
                  "Each identifier links to its Sonatype vulnerability page."), ""]
        body.append(", ".join(vuln_link(v) for v in shown) if shown else "_none recorded_")
        if len(vulns) > len(shown):
            body += ["", f"…and {len(vulns) - len(shown)} more — the complete list is in the "
                         "Lifecycle report linked above."]
        markdown = "\n".join(body)

        # Tags and precision are carried over from the source rules so the
        # alerts keep the same classification Sonatype assigned them.
        properties = {"tags": sorted(e["tags"] or {"security"})}
        if e["precision"]:
            properties["precision"] = e["precision"]
        if e["severity"] >= 0:
            properties["security-severity"] = str(e["severity"])

        rule = {
            "id": rule_id,
            "name": rule_id,
            "shortDescription": {"text": headline},
            "fullDescription": {"text": headline},
            "help": {"text": markdown, "markdown": markdown},
            "properties": properties,
        }
        if report_url:
            rule["helpUri"] = report_url
        elif iq_base and not public_links:
            rule["helpUri"] = f"{iq_base}/assets/index.html"
        new_rules.append(rule)

        result = {
            "ruleId": rule_id,
            "level": "error" if e["severity"] >= 7 else "warning",
            "message": {"text": headline},
        }
        if e["location"]:
            result["locations"] = [e["location"]]
        new_results.append(result)

    run["tool"]["driver"]["rules"] = new_rules
    run["results"] = new_results

    payload = json.dumps(sarif)
    if public_links and iq_base:
        host = re.sub(r"^https?://", "", iq_base).split("/")[0]
        leaked = [h for h in (iq_base, host) if h in payload]
        if leaked:
            sys.exit(f"refusing to write {dst}: IQ host still present ({leaked[0]})")
    with open(dst, "w") as fh:
        fh.write(payload)

    print(f"components: {len(new_results)}")
    print(f"distinct vulnerabilities: {len(set().union(*(c['vulns'] for c in comp.values())) if comp else set())}")
    print(f"alerts before: {sum(c['violations'] for c in comp.values())}  ->  after: {len(new_results)}")
    if security_only:
        print(f"skipped (no known vulnerabilities, licence/quality only): {skipped_no_vulns}")


if __name__ == "__main__":
    args = sys.argv[1:]
    report = None
    if "--report-url" in args:
        i = args.index("--report-url")
        report = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    public = "--public-links" in args
    if public:
        args.remove("--public-links")
    security_only = "--security-only" in args
    if security_only:
        args.remove("--security-only")
    if len(args) != 2:
        sys.exit(__doc__)
    main(args[0], args[1], report or None, public, security_only)
