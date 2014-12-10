PHYSICAL=$(python -c 'from cpuTopology import getNumberOfPhysicalCores; print(getNumberOfPhysicalCores())')
export GOMP_CPU_AFFINITY=0-$(($PHYSICAL-1))
