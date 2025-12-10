# command line entry point

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict
from pipeline.run_pipeline import run as run_pipeline
from config.initializer import DEFAULT_CITY, DEFAULT_DAYS

def setup_logging() -> None:
    logging.basicConfig(
        filename = "pipeline.log",
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
    )

#argaparse.Namespace includes city days output_json
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Weather ensemble pipeline for multi-source 7 day forecasts."
    )

    parser.add_argument(
        "--city",
        type = str,
        default = DEFAULT_CITY,
        help = f"City forecast days (default: {DEFAULT_CITY})",
    )
     
    parser.add_argument(
        "--days",
        type = str,
        default = DEFAULT_DAYS,
        help = f"City name (default: {DEFAULT_DAYS})",
    )
    parser.add_argument(
        "--output-json",
        type = str,
        default = DEFAULT_CITY,
        help = f"Optional save as JSON under output/s",
    )

    return parser.add_args()

def save_json(result: Dict[str, Any], path_str: str) -> None:
    path = Path(path_str)
    if not path.parent.exists():
        path.parent.mkdir(parents = True, exist_ok = True)

    with path.open("w", encoding = "utf-8") as f:
        json.dump(result, f, ensure_ascii = False, indent = 2)

def main() -> None:

    setup_logging()

    args = parse_args()
    city = args.city
    days = args.days
    output_json_path = args.output_json

    logging.info("Starting pipeline where city = %s, days = %s", city, days)
    result = run_pipeline(city = city, days = days)
    logging.info("Pipeline finished successfully")

    print(f"City: {result['city']}")
    print(f"Days: {result['days']}")
    print(f"Sources used: {result['source_count']}")
    print("-------------------------")
    print("First 24 timestamps (temperature ensemble):")

    for item in result["timestamps"][:5]:
        ts = item["timestamp"]
        temp_info = item["temperature_c"]
        print(
            f"{ts} | n = {temp_info['n_points'] if 'n_points' in temp_info else item['n_points']}, "
            f"mean = {temp_info['mean']:.2f}C, sd = {temp_info['sd']:.2f}"
        )

    if output_json_path:
        save_json(result, output_json_path)
        print(f"\nResult saved to {output_json_path}")

if __name__ == "__main__":
    main()