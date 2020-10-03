import os
import sys
import warnings
warnings.simplefilter("ignore")
from omegaconf import OmegaConf
import pytest
import functools
sys.path.append('..')
from hydra.experimental import compose, initialize

from examples.config import cs
from train import train

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
def getcwd():
    return os.path.join(DIR_PATH, "outputs")

current_cwd = os.getcwd()

for r, d, f in os.walk(current_cwd):
    for file in f:
        print(os.path.join(r, file))

os.getcwd = getcwd

def run(*outer_args, **outer_kwargs):
    def runner_func(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            if runs[func.__name__]:
                return func(*args, **kwargs)
            return 0
        return func_wrapper
    return runner_func

local_runs = {"test_argva_cora_inference": True,
        "test_cora_inference": True,
        "test_cora_inference": True,
        "test_cora_gcn_inference": False,
        "test_ppi_inference": False }

workflow_runs = {"test_argva_cora_inference": True,
        "test_cora_inference": True,
        "test_cora_inference": True,
        "test_cora_gcn_inference": False,
        "test_ppi_inference": False }

if "/home/runner/.cache" in current_cwd:
    runs = workflow_runs
else:
    runs = local_runs 

@pytest.mark.parametrize("model", ["argva"])
@pytest.mark.parametrize("dataset", ["cora"])
@pytest.mark.parametrize("jit", ["False"])
@run()

def test_argva_cora_inference(model, dataset, jit):
    cmd_line = "model={} dataset={} loggers=thomas-chaton optimizers=vgae log=false notes='' name=test jit={} explain=False"
    with initialize(config_path="../conf", job_name="test_app"):
        print({"model":model, "dataset":dataset, "jit":jit})
        cfg = compose(config_name="config", overrides=cmd_line.format(model, dataset, jit).split(' '))
        train(cfg)

@pytest.mark.parametrize("model", ["sage", "dna", "dna", "gcn", "sgc", "tag"])
@pytest.mark.parametrize("dataset", ["cora"])
@pytest.mark.parametrize("jit", ["True", "False"])
@run()
def test_cora_inference(model, dataset, jit):
    cmd_line = "model={} dataset={} loggers=thomas-chaton log=False notes='' name='test' explain=False jit={}"
    with initialize(config_path="../conf", job_name="test_app"):
        print({"model":model, "dataset":dataset, "jit":jit})
        cfg = compose(config_name="config", overrides=cmd_line.format(model, dataset, jit).split(' '))
        # override params
        cfg.dataset.params.use_gdc = False
        train(cfg)

@pytest.mark.parametrize("model", ["gcn", "gcn2"])
@pytest.mark.parametrize("dataset", ["cora"])
@pytest.mark.parametrize("jit", ["True", "False"])
@run()
def test_cora_gcn_inference(model, dataset, jit):
    cmd_line = "model={} dataset={} loggers=thomas-chaton log=False notes='' name='test' explain=False jit={}"
    with initialize(config_path="../conf", job_name="test_app"):
        print({"model":model, "dataset":dataset, "jit":jit})
        cfg = compose(config_name="config", overrides=cmd_line.format(model, dataset, jit).split(' '))
        # override params
        cfg.dataset.params.use_gdc = True
        train(cfg)

@pytest.mark.parametrize("model", ["sage", "dna", "dna", "sgc", "tag"])
@pytest.mark.parametrize("dataset", ["ppi"])
@pytest.mark.parametrize("jit", ["True", "False"])
@run()
def test_ppi_inference(model, dataset, jit):
    cmd_line = "model={} dataset={} loggers=thomas-chaton log=False notes='' name='test' explain=False jit={}"
    with initialize(config_path="../conf", job_name="test_app"):
        print({"model":model, "dataset":dataset, "jit":jit})
        cfg = compose(config_name="config", overrides=cmd_line.format(model, dataset, jit).split(' '))
        train(cfg)