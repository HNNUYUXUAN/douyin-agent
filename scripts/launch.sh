#!/usr/bin/env bash
set -euo pipefail
mode=$1; shift
workspace=''; skill_dir=''; conda_arg=''; target_host='codex'
while (($#)); do
  case "$1" in
    --workspace|--skill-dir|--conda|--host)
      (($# >= 2)) || { printf 'Missing value for %s\n' "$1" >&2; exit 2; }
      case "$1" in
        --workspace) workspace=$2;;
        --skill-dir) skill_dir=$2;;
        --conda) conda_arg=$2;;
        --host) target_host=$2;;
      esac
      shift 2;;
    -h|--help)
      printf 'Usage: bash %s.sh [--workspace PATH] [--conda CONDA_EXE]' "$mode"
      [[ $mode != install ]] || printf ' [--skill-dir PATH]'
      printf '\n--host codex|workbuddy\nWindows Git Bash; Conda creates a dedicated Python 3.12 environment.\n'; exit 0;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; exit 2;;
  esac
done
command -v cygpath >/dev/null || { printf 'Use Windows Git Bash (cygpath required).\n' >&2; exit 1; }
candidates=()
if [[ -n $conda_arg ]]; then candidates+=("$conda_arg"); else
  [[ -z ${CONDA_EXE:-} ]] || candidates+=("$CONDA_EXE")
  path_conda=$(type -P conda 2>/dev/null || type -P conda.exe 2>/dev/null || type -P conda.bat 2>/dev/null || true)
  [[ -z $path_conda ]] || candidates+=("$path_conda")
  for root in "${USERPROFILE:-}" "${PROGRAMDATA:-${ProgramData:-C:\ProgramData}}" /d /c; do
    [[ -n $root ]] || continue
    for name in miniconda3 anaconda3 miniforge3; do candidates+=("$root/$name/Scripts/conda.exe"); done
  done
fi
found=''
for candidate in "${candidates[@]}"; do
  candidate=$(cygpath -au "$candidate")
  [[ -f $candidate ]] || continue
  if [[ ${candidate,,} == *.bat && -f $(dirname "$(dirname "$candidate")")/Scripts/conda.exe ]]; then
    candidate=$(dirname "$(dirname "$candidate")")/Scripts/conda.exe
  fi
  found=$candidate; break
done
[[ -n $found ]] || { printf 'Conda not found. Install from https://www.anaconda.com/docs/getting-started/miniconda/install or pass --conda CONDA_EXE.\n' >&2; exit 1; }
base=$("$found" info --base) || { printf 'Conda discovery failed.\n' >&2; exit 1; }
base=${base//$'\r'/}; base=$(cygpath -au "$base")
py="$base/python.exe"
[[ -f $py ]] || { printf 'Conda base Python is missing.\n' >&2; exit 1; }
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
args=( -B "$(cygpath -aw "$script_dir/installer.py")" "$mode" --host "$target_host" --conda "$(cygpath -aw "$found")" )
[[ -z $workspace ]] || args+=( --workspace "$(cygpath -aw "$workspace")" )
[[ -z $skill_dir ]] || args+=( --skill-dir "$(cygpath -aw "$skill_dir")" )
# All path arguments are already native Windows paths; prevent MSYS from rewriting them again.
PYTHONUTF8=1 MSYS2_ARG_CONV_EXCL='*' "$py" "${args[@]}"
