# Copyright 2019 Uber Technologies, Inc. All Rights Reserved.
# Modifications copyright Microsoft
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
# ==============================================================================

from horovod.common.util import check_extension

try:
    check_extension('horovod.paddlepaddle', 'HOROVOD_WITH_PADDLEPADDLE',
                    __file__, 'mpi_lib_v2')
except:
    check_extension('horovod.paddlepaddle', 'HOROVOD_WITH_PADDLEPADDLE',
                    __file__, 'mpi_lib', '_mpi_lib')

from horovod.paddlepaddle import elastic
from horovod.paddlepaddle.compression import Compression
from horovod.paddlepaddle.functions import allgather_object, broadcast_object, broadcast_optimizer_state, broadcast_parameters
from horovod.paddlepaddle.mpi_ops import allreduce, allreduce_async, allreduce_, allreduce_async_
from horovod.paddlepaddle.mpi_ops import grouped_allreduce, grouped_allreduce_async, grouped_allreduce_, grouped_allreduce_async_
from horovod.paddlepaddle.mpi_ops import sparse_allreduce_async
from horovod.paddlepaddle.mpi_ops import allgather, allgather_async
from horovod.paddlepaddle.mpi_ops import broadcast, broadcast_async, broadcast_, broadcast_async_
from horovod.paddlepaddle.mpi_ops import alltoall, alltoall_async
from horovod.paddlepaddle.mpi_ops import join
from horovod.paddlepaddle.mpi_ops import poll, synchronize
from horovod.paddlepaddle.mpi_ops import init, shutdown
from horovod.paddlepaddle.mpi_ops import is_initialized, start_timeline, stop_timeline
from horovod.paddlepaddle.mpi_ops import size, local_size, cross_size, rank, local_rank, cross_rank
from horovod.paddlepaddle.mpi_ops import mpi_threads_supported, mpi_enabled, mpi_built
from horovod.paddlepaddle.mpi_ops import gloo_enabled, gloo_built
from horovod.paddlepaddle.mpi_ops import nccl_built, ddl_built, ccl_built, cuda_built, rocm_built
from horovod.paddlepaddle.mpi_ops import Average, Sum, Adasum
from horovod.paddlepaddle.optimizer import DistributedOptimizer
from horovod.paddlepaddle.sync_batch_norm import SyncBatchNorm


# Please run this function in a subprocess
def _check_has_gpu():
    import paddle
    return paddle.device.is_compiled_with_cuda()
