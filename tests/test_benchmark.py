import pytest
from app.utils.benchmark import print_benchmark_table


def test_benchmark_report_formatter(capsys):
    seq = {
        "total_time": 10.0,
        "req_per_sec": 0.5,
        "pages_per_sec": 0.5,
        "avg_resp_time": 2.0,
        "success_rate": 100.0,
        "failed_requests": 0,
    }
    async_res = {
        "total_time": 2.5,
        "req_per_sec": 2.0,
        "pages_per_sec": 2.0,
        "avg_resp_time": 0.5,
        "success_rate": 100.0,
        "failed_requests": 0,
    }

    print_benchmark_table(seq, async_res)
    captured = capsys.readouterr()
    assert "Performance Benchmark Comparison Report" in captured.out
    assert "Sequential" in captured.out
    assert "Async" in captured.out
