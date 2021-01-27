# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Component specifications for the standard set of TFX Components."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Text

import tensorflow_model_analysis as tfma
from tfx.proto import bulk_inferrer_pb2
from tfx.proto import evaluator_pb2
from tfx.proto import example_gen_pb2
from tfx.proto import infra_validator_pb2
from tfx.proto import pusher_pb2
from tfx.proto import range_config_pb2
from tfx.proto import trainer_pb2
from tfx.proto import transform_pb2
from tfx.proto import tuner_pb2
from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ComponentSpec
from tfx.types.component_spec import ExecutionParameter

# Parameters keys for modules
# Shared Keys across components
SCHEMA_KEY = 'schema'
EXAMPLES_KEY = 'examples'
MODEL_KEY = 'model'
BLESSING_KEY = 'blessing'
MODULE_FILE_KEY = 'module_file'
# Key for example_validator
EXCLUDE_SPLITS_KEY = 'exclude_splits'
STATISTICS_KEY = 'statistics'
ANOMALIES_KEY = 'anomalies'
# Key for evaluator
EVAL_CONFIG_KEY = 'eval_config'
FEATURE_SLICING_SPEC_KEY = 'feature_slicing_spec'
FAIRNESS_INDICATOR_THRESHOLDS_KEY = 'fairness_indicator_thresholds'
EXAMPLE_SPLITS_KEY = 'example_splits'
MODULE_PATH_KEY = 'module_path'
BASELINE_MODEL_KEY = 'baseline_model'
EVALUATION_KEY = 'evaluation'
# Key for for infra_validator
SERVING_SPEC_KEY = 'serving_spec'
VALIDATION_SPEC_KEY = 'validation_spec'
REQUEST_SPEC_KEY = 'request_spec'
# Key for tuner
TUNER_FN_KEY = 'tuner_fn'
TRAIN_ARGS_KEY = 'train_args'
EVAL_ARGS_KEY = 'eval_args'
TUNE_ARGS_KEY = 'tune_args'
CUSTOM_CONFIG_KEY = 'custom_config'
TRANSFORM_GRAPH_KEY = 'transform_graph'
BEST_HYPERPARAMETERS_KEY = 'best_hyperparameters'
# Key for bulk_inferer
MODEL_SPEC_KEY = 'model_spec'
DATA_SPEC_KEY = 'data_spec'
OUTPUT_EXAMPLE_SPEC_KEY = 'output_example_spec'
MODEL_BLESSING_KEY = 'model_blessing'
INFERENCE_RESULT_KEY = 'inference_result'
OUTPUT_EXAMPLES_KEY = 'output_examples'


class BulkInferrerSpec(ComponentSpec):
  """BulkInferrer component spec."""

  PARAMETERS = {
      MODEL_SPEC_KEY:
          ExecutionParameter(type=bulk_inferrer_pb2.ModelSpec, optional=True),
      DATA_SPEC_KEY:
          ExecutionParameter(type=bulk_inferrer_pb2.DataSpec, optional=True),
      OUTPUT_EXAMPLE_SPEC_KEY:
          ExecutionParameter(
              type=bulk_inferrer_pb2.OutputExampleSpec, optional=True),
  }
  INPUTS = {
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples),
      MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      MODEL_BLESSING_KEY:
          ChannelParameter(
              type=standard_artifacts.ModelBlessing, optional=True),
  }
  OUTPUTS = {
      INFERENCE_RESULT_KEY:
          ChannelParameter(
              type=standard_artifacts.InferenceResult, optional=True),
      OUTPUT_EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
  }


class EvaluatorSpec(ComponentSpec):
  """Evaluator component spec."""

  PARAMETERS = {
      EVAL_CONFIG_KEY:
          ExecutionParameter(type=tfma.EvalConfig, optional=True),
      # TODO(mdreves): Deprecated, use eval_config.slicing_specs.
      FEATURE_SLICING_SPEC_KEY:
          ExecutionParameter(
              type=evaluator_pb2.FeatureSlicingSpec, optional=True),
      # This parameter is experimental: its interface and functionality may
      # change at any time.
      FAIRNESS_INDICATOR_THRESHOLDS_KEY:
          ExecutionParameter(type=List[float], optional=True),
      EXAMPLE_SPLITS_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
      MODULE_FILE_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
      MODULE_PATH_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples),
      MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      BASELINE_MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
  }
  OUTPUTS = {
      EVALUATION_KEY: ChannelParameter(type=standard_artifacts.ModelEvaluation),
      BLESSING_KEY: ChannelParameter(type=standard_artifacts.ModelBlessing),
  }


class ExampleValidatorSpec(ComponentSpec):
  """ExampleValidator component spec."""

  PARAMETERS = {
      EXCLUDE_SPLITS_KEY: ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      STATISTICS_KEY:
          ChannelParameter(type=standard_artifacts.ExampleStatistics),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema),
  }
  OUTPUTS = {
      ANOMALIES_KEY: ChannelParameter(type=standard_artifacts.ExampleAnomalies),
  }


class FileBasedExampleGenSpec(ComponentSpec):
  """File-based ExampleGen component spec."""

  PARAMETERS = {
      'input_base':
          ExecutionParameter(type=(str, Text)),
      'input_config':
          ExecutionParameter(type=example_gen_pb2.Input),
      'output_config':
          ExecutionParameter(type=example_gen_pb2.Output),
      'output_data_format':
          ExecutionParameter(type=int),  # example_gen_pb2.PayloadType enum.
      'custom_config':
          ExecutionParameter(type=example_gen_pb2.CustomConfig, optional=True),
      'range_config':
          ExecutionParameter(type=range_config_pb2.RangeConfig, optional=True),
  }
  INPUTS = {}
  OUTPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
  }


class QueryBasedExampleGenSpec(ComponentSpec):
  """Query-based ExampleGen component spec."""

  PARAMETERS = {
      'input_config':
          ExecutionParameter(type=example_gen_pb2.Input),
      'output_config':
          ExecutionParameter(type=example_gen_pb2.Output),
      'output_data_format':
          ExecutionParameter(type=int),  # example_gen_pb2.PayloadType enum.
      'custom_config':
          ExecutionParameter(type=example_gen_pb2.CustomConfig, optional=True),
  }
  INPUTS = {}
  OUTPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
  }


class InfraValidatorSpec(ComponentSpec):
  """InfraValidator component spec."""

  PARAMETERS = {
      SERVING_SPEC_KEY:
          ExecutionParameter(type=infra_validator_pb2.ServingSpec),
      VALIDATION_SPEC_KEY:
          ExecutionParameter(
              type=infra_validator_pb2.ValidationSpec, optional=True),
      REQUEST_SPEC_KEY:
          ExecutionParameter(
              type=infra_validator_pb2.RequestSpec, optional=True)
  }

  INPUTS = {
      MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model),
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
  }

  OUTPUTS = {
      BLESSING_KEY: ChannelParameter(type=standard_artifacts.InfraBlessing),
  }


class ModelValidatorSpec(ComponentSpec):
  """ModelValidator component spec."""

  PARAMETERS = {}
  INPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
      'model': ChannelParameter(type=standard_artifacts.Model),
  }
  OUTPUTS = {
      'blessing': ChannelParameter(type=standard_artifacts.ModelBlessing),
  }


class PusherSpec(ComponentSpec):
  """Pusher component spec."""

  PARAMETERS = {
      'push_destination':
          ExecutionParameter(type=pusher_pb2.PushDestination, optional=True),
      'custom_config':
          ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'model':
          ChannelParameter(type=standard_artifacts.Model),
      'model_blessing':
          ChannelParameter(
              type=standard_artifacts.ModelBlessing, optional=True),
      'infra_blessing':
          ChannelParameter(
              type=standard_artifacts.InfraBlessing, optional=True),
  }
  OUTPUTS = {
      'pushed_model': ChannelParameter(type=standard_artifacts.PushedModel),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'model_export': 'model',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'model_push': 'pushed_model',
  }


class SchemaGenSpec(ComponentSpec):
  """SchemaGen component spec."""

  PARAMETERS = {
      'infer_feature_shape': ExecutionParameter(type=int, optional=True),
      'exclude_splits': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'statistics': ChannelParameter(type=standard_artifacts.ExampleStatistics),
  }
  OUTPUTS = {
      'schema': ChannelParameter(type=standard_artifacts.Schema),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'stats': 'statistics',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'output': 'schema',
  }


class StatisticsGenSpec(ComponentSpec):
  """StatisticsGen component spec."""

  PARAMETERS = {
      'stats_options_json': ExecutionParameter(type=(str, Text), optional=True),
      'exclude_splits': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
      'schema': ChannelParameter(type=standard_artifacts.Schema, optional=True),
  }
  OUTPUTS = {
      'statistics': ChannelParameter(type=standard_artifacts.ExampleStatistics),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'input_data': 'examples',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'output': 'statistics',
  }


class TrainerSpec(ComponentSpec):
  """Trainer component spec."""

  PARAMETERS = {
      'train_args': ExecutionParameter(type=trainer_pb2.TrainArgs),
      'eval_args': ExecutionParameter(type=trainer_pb2.EvalArgs),
      'module_file': ExecutionParameter(type=(str, Text), optional=True),
      'run_fn': ExecutionParameter(type=(str, Text), optional=True),
      'trainer_fn': ExecutionParameter(type=(str, Text), optional=True),
      'custom_config': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'examples':
          ChannelParameter(type=standard_artifacts.Examples),
      'transform_graph':
          ChannelParameter(
              type=standard_artifacts.TransformGraph, optional=True),
      'schema':
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
      'base_model':
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      'hyperparameters':
          ChannelParameter(
              type=standard_artifacts.HyperParameters, optional=True),
  }
  OUTPUTS = {
      'model': ChannelParameter(type=standard_artifacts.Model),
      'model_run': ChannelParameter(type=standard_artifacts.ModelRun)
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'transform_output': 'transform_graph',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'output': 'model',
  }


class TunerSpec(ComponentSpec):
  """ComponentSpec for TFX Tuner Component."""

  PARAMETERS = {
      MODULE_FILE_KEY: ExecutionParameter(type=(str, Text), optional=True),
      TUNER_FN_KEY: ExecutionParameter(type=(str, Text), optional=True),
      TRAIN_ARGS_KEY: ExecutionParameter(type=trainer_pb2.TrainArgs),
      EVAL_ARGS_KEY: ExecutionParameter(type=trainer_pb2.EvalArgs),
      TUNE_ARGS_KEY: ExecutionParameter(type=tuner_pb2.TuneArgs, optional=True),
      CUSTOM_CONFIG_KEY: ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
      TRANSFORM_GRAPH_KEY:
          ChannelParameter(
              type=standard_artifacts.TransformGraph, optional=True),
  }
  OUTPUTS = {
      BEST_HYPERPARAMETERS_KEY:
          ChannelParameter(type=standard_artifacts.HyperParameters),
  }


class TransformSpec(ComponentSpec):
  """Transform component spec."""

  PARAMETERS = {
      'module_file':
          ExecutionParameter(type=(str, Text), optional=True),
      'preprocessing_fn':
          ExecutionParameter(type=(str, Text), optional=True),
      'force_tf_compat_v1':
          ExecutionParameter(type=int, optional=True),
      'custom_config':
          ExecutionParameter(type=(str, Text), optional=True),
      'splits_config':
          ExecutionParameter(type=transform_pb2.SplitsConfig, optional=True),
  }
  INPUTS = {
      'examples':
          ChannelParameter(type=standard_artifacts.Examples),
      'schema':
          ChannelParameter(type=standard_artifacts.Schema),
      'analyzer_cache':
          ChannelParameter(
              type=standard_artifacts.TransformCache, optional=True),
  }
  OUTPUTS = {
      'transform_graph':
          ChannelParameter(type=standard_artifacts.TransformGraph),
      'transformed_examples':
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
      'updated_analyzer_cache':
          ChannelParameter(
              type=standard_artifacts.TransformCache, optional=True),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'input_data': 'examples',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'transform_output': 'transform_graph',
  }
