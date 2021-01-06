#mpi
import numpy as np
#import mpi4py.MPI as MPI
from mpi4py import MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

if comm_rank == 0:
    data = range((comm_size-1)*3)
    leng = len(data)
    print("data = ", data)
    rec_sum = np.zeros((comm_size-1), dtype='i')
else:
    data = None
    rec_sum = None

#scatter
local_data = np.zeros(len(data)/(comm_size-1), dtype='i')
if comm_rank == 0:
    comm.Scatter(data, MPI.IN_PLACE, root=0)
    local_sum = None
else:
    comm.Scatter(data, local_data, root=0)
    local_sum = sum(local_data)
print('Scatter: rank %d has %s with MPI.IN_PLACE' % (comm_rank, local_data))
print("local_sum =", local_sum)

#gather
if comm_rank == 0:
    comm.Gather(MPI.IN_PLACE, rec_sum, root=0)
else:
    comm.Gather(local_sum, rec_sum, root=0)
print('Gather: rank %d has %s with MPI.IN_PLACE' % (comm_rank, rec_sum))

#local_data = comm.Scatter(data, MPI.IN_PLACE, root=0)
#local_sum = sum(local_data)
#print('rank %d, got and do:' % comm_rank)
#print("local_data =", local_data, "local_sum =", local_sum)
#combine_data = comm.gather(local_sum, root=0)
if comm_rank == 0:
    all_sum = sum(rec_sum)
    print("all_sum =", all_sum)
else:
    all_sum = None

# scatter the final sum to each user
all_sum_local = comm.scatter(all_sum, root=0)
print('rank %d receive sum = %s' % (comm_rank, all_sum_local))
