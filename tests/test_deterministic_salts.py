#!/usr/bin/env python3
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.hash_generator import HashGenerator
import logging


def _make_logger():
    logger = logging.getLogger('TestDeterministicSalts')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger


def test_deterministic_salts(tmp_path):
    config = {
        'experiment': {
            'name': 'deterministic_test',
            'seed': 123,
            'deterministic_salts': True,
            'hash_generation': {
                'count': 2,
                'algorithms': [
                    {'name': 'sha256', 'salt': True},
                    {'name': 'md5', 'salt': True}
                ],
                'password_patterns': ['test{}']
            }
        }
    }

    logger = _make_logger()
    output_file_1 = tmp_path / 'hashes1.json'
    output_file_2 = tmp_path / 'hashes2.json'

    hashes_1 = HashGenerator(config, logger).generate_hashes(output_file_1)
    hashes_2 = HashGenerator(config, logger).generate_hashes(output_file_2)

    assert hashes_1 == hashes_2

    with open(output_file_1, 'r') as f1, open(output_file_2, 'r') as f2:
        data_1 = json.load(f1)
        data_2 = json.load(f2)

    assert data_1 == data_2
