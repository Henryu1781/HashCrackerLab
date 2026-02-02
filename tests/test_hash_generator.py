#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.hash_generator import HashGenerator
import logging


def _make_logger():
    logger = logging.getLogger('TestHashGenerator')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger


def test_generate_hashes_count(tmp_path):
    config = {
        'experiment': {
            'name': 'unit_test',
            'hash_generation': {
                'count': 3,
                'algorithms': [
                    {'name': 'md5', 'salt': False},
                    {'name': 'sha256', 'salt': True}
                ],
                'password_patterns': ['test{}']
            }
        }
    }

    logger = _make_logger()
    generator = HashGenerator(config, logger)
    output_file = tmp_path / 'hashes.json'

    hashes = generator.generate_hashes(output_file)
    assert len(hashes) == 6

    with open(output_file, 'r') as f:
        data = json.load(f)

    assert len(data) == 6
    assert set(h['algorithm'] for h in data) == {'md5', 'sha256'}
