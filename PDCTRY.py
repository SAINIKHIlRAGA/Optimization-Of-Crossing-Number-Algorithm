# include<stdio.h>
# include<omp.h>
int
main()
{
    int
i, j, count1 = 0, count2 = 0;
# pragma omp parallel shared(count1, count2)
{
    # pragma omp single
    printf("This is Title. Only one thread with Id -%d is printing the title\n", omp_get_thread_num());
# pragma omp for
for (i=0;i < 30000;i++)
{
    count1 + +;
}
# pragma omp for
for (i=0;i < 30000;i++)
{
    # pragma omp critical
    count2 + +;
}

# pragma omp barrier
printf("At this point,threads waits for the execution of other threads.Thread-%d is waiting for other threads now\n", omp_get_thread_num());
# pragma omp master
printf("The final value of Counter-1 is %d and Counter-2 is %d. Only Master Thread with Id-%d prints the counter values\n", count1, count2, omp_get_thread_num());
}
return 0;
}
