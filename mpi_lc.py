#mpi
import numpy as np
#import mpi4py.MPI as MPI
from mpi4py import MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

leng = (comm_size)*3
if comm_rank == 0:
    data = np.arange(leng, dtype='i')#data = [i for i in range(leng)]#data = range(leng)#
    print("data = %s" % data)
    rec_sum = [0]*(comm_size)#rec_sum = np.zeros((comm_size), dtype='i')
else:
    data = None
    rec_sum = None

#scatter
local_data = np.zeros(leng/comm_size, dtype='i')#local_data = [0]*(leng/(comm_size))#
#local_data = comm.scatter(data, root=0)
comm.Scatter(data, local_data, root=0)
print("Scatter: rank %d has %s" % (comm_rank, local_data))
local_sum = sum(local_data)
print("local_sum = %d" % local_sum)

#gather
rec_sum = comm.gather(local_sum, root=0)
#comm.Gather(local_sum, rec_sum, root=0)
print("Gather: rank %d has %s" % (comm_rank, rec_sum))

#local_data = comm.Scatter(data, MPI.IN_PLACE, root=0)
#local_sum = sum(local_data)
#print('rank %d, got and do:' % comm_rank)
#print("local_data =", local_data, "local_sum =", local_sum)
#combine_data = comm.gather(local_sum, root=0)
if comm_rank == 0:
    all_sum = sum(rec_sum)
    print("all_sum = %d" % all_sum)
else:
    all_sum = None


# scatter the final sum to each user
#all_sum_local = comm.scatter(all_sum, root=0)
all_sum_local = comm.bcast(all_sum if comm_rank == 0 else None, root=0)
print('rank %d receive sum = %s' % (comm_rank, all_sum_local))

