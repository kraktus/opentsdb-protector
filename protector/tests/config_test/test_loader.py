#  Copyright 2019 Adobe
#  All Rights Reserved.
#
#  NOTICE: Adobe permits you to use, modify, and distribute this file in
#  accordance with the terms of the Adobe license agreement accompanying
#  it. If you have received this file from a source other than Adobe,
#  then your use, modification, or distribution of it requires the prior
#  written permission of Adobe.
#

import unittest
import os
import argparse
from mock import patch

from protector.config import loader


class TestConfig(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.configfile = "{}/../../../config_template.yaml".format(path)

    @unittest.skip("fixme")
    def test_load_config(self):
        parsed_config = loader.parse_configfile(self.configfile)
        self.assertEqual(parsed_config["host"], "myhost")
        self.assertEqual(parsed_config["port"], 1234)

    def test_cli_overwrite(self):
        # Fake commandline arguments
        # Argparse returns a namespace, not a dictionary
        fake_args = argparse.Namespace()
        fake_args.host = "myhost"

        with patch('argparse.ArgumentParser.parse_args') as parse_args_mock:
            parse_args_mock.return_value = fake_args

            # Fake default config
            with patch('protector.config.default_config.DEFAULT_CONFIG') as default_config_mock:
                default_config_mock.return_value = {"host": "yourhost"}
                config = loader.load_config()

        # Check if the default setting got overwritten
        self.assertEqual(config.host, "myhost")

    def test_shorthand_cli_parameters(self):
        config = loader.parse_args([])
        self.assertIsNotNone(config)
        self.assertEqual(config['foreground'], False)
        config = loader.parse_args(['-f'])
        self.assertIsNotNone(config)
        self.assertEqual(config['foreground'], True)

    def test_overwrite_default_config(self):
        default_config_dict = {'host': 'defaulthost'}
        config = loader.overwrite_config(default_config_dict, {'host': 'otherhost'})
        self.assertEqual(config['host'], 'otherhost')
