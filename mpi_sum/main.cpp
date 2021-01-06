#include<stdio.h>
#include<string.h>
#include"mpi.h"
#include<cmath>

double f(double x) {
    return x;
}

double LocalSum(double x_leftpt, double x_rightpt, double Local_len, double base_len){
    double local_sum = f(x_leftpt), x = x_leftpt;
    for (int i = 1; i < Local_len; i++) {
        x += base_len;
        local_sum += f(x);
    }
    return local_sum;
}
int main(int argc, char* argv[]) {
    int myid, numprocs, num = 30, local_n = 0; //nΪ��������, local_nΪÿһ��������Ҫ�����������
    double a = 1, b = 30, local_a = 0, local_b = 0; // a��bΪ����������ұ߽�
    double local_summary = 0, total_summary = 0;
    int source;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);

    local_n = floor(num / numprocs);
    if (myid == numprocs - 1) {
        local_n = num - local_n * (numprocs - 1);
    }
    local_a = a + myid * floor(num / numprocs);
    local_b = local_a + local_n-1;
    local_summary = LocalSum(local_a, local_b, local_n, 1);

    if (myid != 0)
    {
        MPI_Send(&local_summary, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
        printf("����%d��������ͽ���� %f \n", myid, local_summary);
    }
    else {
        printf("����%d��������ͽ���� %f \n", myid, local_summary);
        total_summary = local_summary;
        for (source = 1; source < numprocs; source++) {
            MPI_Recv(&local_summary, 1, MPI_DOUBLE, source, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
            total_summary += local_summary;
        }
        printf("��n = %dʱ����%f �� %f ��͵Ľ���� %f \n", num, a, b, total_summary);
    }
    MPI_Finalize();
    return 0;
}