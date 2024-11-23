import unittest
from fine_tuning.data_loader import TrainingDataLoader
from fine_tuning.train import GeminiFineTuner

class TestFineTuning(unittest.TestCase):
    def setUp(self):
        self.loader = TrainingDataLoader()
        self.tuner = GeminiFineTuner()
    
    def test_data_loading(self):
        examples = self.loader.load_all_examples()
        self.assertGreater(len(examples), 0)
        
    def test_example_format(self):
        examples = self.loader.load_all_examples()
        for example in examples:
            self.assertIn('text_input', example)
            self.assertIn('output', example) 