import unittest

import ray
import ray.rllib.agents.es as es
from ray.rllib.utils.test_utils import check_compute_single_action, \
    framework_iterator


class TestES(unittest.TestCase):
    def test_es_compilation(self):
        """Test whether an ESTrainer can be built on all frameworks."""
        ray.init(num_cpus=2)
        config = es.DEFAULT_CONFIG.copy()
        # Keep it simple.
        config["model"]["fcnet_hiddens"] = [10]
        config["model"]["fcnet_activation"] = None
        config["noise_size"] = 2500000
        config["num_workers"] = 1
        config["episodes_per_batch"] = 10
        config["train_batch_size"] = 100

        num_iterations = 1

        for _ in framework_iterator(config):
            plain_config = config.copy()
            trainer = es.ESTrainer(config=plain_config, env="CartPole-v0")
            for i in range(num_iterations):
                results = trainer.train()
                print(results)

            check_compute_single_action(trainer)
            trainer.stop()
        ray.shutdown()


if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))
