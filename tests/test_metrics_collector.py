#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.metrics_collector import MetricsCollector
import logging


def _make_logger():
    logger = logging.getLogger('TestMetricsCollector')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger


def test_metrics_success_rate(tmp_path):
    logger = _make_logger()
    collector = MetricsCollector(tmp_path, logger)

    hashes = [
        {'algorithm': 'md5'},
        {'algorithm': 'md5'},
        {'algorithm': 'sha256'}
    ]

    cracking_results = {
        'cracked': 2,
        'by_algorithm': {
            'md5': {'total': 2, 'cracked': 2},
            'sha256': {'total': 1, 'cracked': 0}
        },
        'executions': []
    }

    metrics = collector.collect_metrics(hashes, cracking_results)
    assert metrics['total_hashes'] == 3
    assert metrics['total_cracked'] == 2
    assert metrics['success_rate'] == 2 / 3
    assert metrics['by_algorithm']['md5']['success_rate'] == 1.0
    assert metrics['by_algorithm']['sha256']['success_rate'] == 0.0
