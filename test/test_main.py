import pytest
import main
import sys
from typing import Any, Dict, Optional

def _fake_pipeline_result() -> Dict[str, Any]:
    return {
        "city": "Halifax",
        "days": 7,
        "source_count": 1,
        "timestamps": [
            {
                "timestamp": "2025-01-01T10:00",
                "n_points": 1,
                "temperature_c": {
                    "values": [1.0],
                    "mean": 1.0,
                    "sd": 0.0,
                    "outlier_sources": [],
                },
            }
        ],
    }
def test_main_basic(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
    def fake_run(city: Optional[str] = None, days: Optional[int] = None) -> Dict[str, Any]:
        return _fake_pipeline_result()
    
    import pipeline.run_pipeline as pipeline_module

    monkeypatch.setattr(pipeline_module, "run", fake_run)

    monkeypatch.setattr(sys, "argv", ["main.py", "--city", "Halifax", "--days", "7"])

    main.main()

    captured = capsys.readouterr()
    out = captured.out

    assert "City: Halifax" in out
    assert "Days: 7" in out
    assert "Sources used: 1" in out
    assert "First 24 timestamps" in out