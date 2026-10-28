#!/usr/bin/env python3
"""Выгружает флаги Unleash, включённые в прод-окружении, и сравнивает со вчерашним снимком.

Нужны переменные окружения:
  UNLEASH_URL    — например https://unleash.example.com (без /api)
  UNLEASH_TOKEN  — Admin API token (или personal access token)

Пример:
  python3 scripts/unleash_prod_flags.py --out state/flags_today.json --diff state/flags_snapshot.json
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "agents.json")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)["unleash"]


def api_get(base, token, path):
    req = urllib.request.Request(
        base.rstrip("/") + path,
        headers={"Authorization": token, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def rollout_summary(env):
    """Сжимает стратегии окружения до читаемого описания раскатки."""
    parts = []
    for s in env.get("strategies") or []:
        if s.get("disabled"):
            continue
        params = s.get("parameters") or {}
        name = s.get("name")
        if name == "flexibleRollout":
            parts.append(f"rollout {params.get('rollout', '?')}% by {params.get('stickiness', 'default')}")
        elif name == "default":
            parts.append("100%")
        else:
            parts.append(name)
        if s.get("constraints"):
            parts[-1] += f" (+{len(s['constraints'])} constraints)"
        if s.get("segments"):
            parts[-1] += f" (+{len(s['segments'])} segments)"
    return parts


def variant_summary(feature, env):
    variants = env.get("variants") or feature.get("variants") or []
    for s in env.get("strategies") or []:
        variants = variants or s.get("variants") or []
    return [{"name": v.get("name"), "weight": v.get("weight")} for v in variants]


def collect(base, token, cfg):
    env_name = cfg["production_environment"]
    project_ids = cfg.get("projects") or [p["id"] for p in api_get(base, token, "/api/admin/projects")["projects"]]
    ignore = set(cfg.get("ignore_flags") or [])
    flags = []
    for project in project_ids:
        features = api_get(base, token, f"/api/admin/projects/{urllib.parse.quote(project)}/features")["features"]
        for f in features:
            if f.get("archived") or f["name"] in ignore:
                continue
            env = next((e for e in f.get("environments") or [] if e.get("name") == env_name), None)
            if not env or not env.get("enabled"):
                continue
            detail = api_get(
                base, token,
                f"/api/admin/projects/{urllib.parse.quote(project)}/features/{urllib.parse.quote(f['name'])}",
            )
            denv = next((e for e in detail.get("environments") or [] if e.get("name") == env_name), env)
            flags.append({
                "name": f["name"],
                "project": project,
                "type": f.get("type"),
                "description": detail.get("description") or "",
                "stale": f.get("stale", False),
                "created_at": f.get("createdAt"),
                "last_seen_at": denv.get("lastSeenAt") or f.get("lastSeenAt"),
                "rollout": rollout_summary(denv),
                "variants": variant_summary(detail, denv),
                "is_experiment": f.get("type") == "experiment" or bool(variant_summary(detail, denv)),
                "url": f"{base.rstrip('/')}/projects/{project}/features/{f['name']}",
            })
    return sorted(flags, key=lambda x: (x["project"], x["name"]))


def diff(prev, cur):
    p = {f["name"]: f for f in prev}
    c = {f["name"]: f for f in cur}
    changed = [n for n in c if n in p and (c[n]["rollout"], c[n]["variants"]) != (p[n]["rollout"], p[n]["variants"])]
    return {
        "added": sorted(set(c) - set(p)),
        "removed": sorted(set(p) - set(c)),
        "rollout_changed": sorted(changed),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="state/flags_today.json")
    ap.add_argument("--diff", help="предыдущий снимок для сравнения; после сравнения перезаписывается текущим")
    args = ap.parse_args()

    base, token = os.environ.get("UNLEASH_URL"), os.environ.get("UNLEASH_TOKEN")
    if not base or not token:
        sys.exit("UNLEASH_URL и UNLEASH_TOKEN должны быть заданы в окружении")

    cfg = load_config()
    flags = collect(base, token, cfg)
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": cfg["production_environment"],
        "flags": flags,
    }
    if args.diff and os.path.exists(args.diff):
        with open(args.diff, encoding="utf-8") as f:
            result["diff"] = diff(json.load(f)["flags"], flags)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    if args.diff:
        with open(args.diff, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    exps = sum(1 for x in flags if x["is_experiment"])
    print(f"{len(flags)} флагов включено в {cfg['production_environment']}, из них экспериментов: {exps} -> {args.out}")


if __name__ == "__main__":
    main()
