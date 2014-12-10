#!/usr/bin/env python

import os
import signal
from subprocess import PIPE, Popen
from cpuTopology import (getRepresentativeCoresFromNumaNodes,
                         getNumberOfPhysicalCores,
                         getNumberOfNumaNodes)

BUFFER_SIZE = 580
BIN = "./testNuma"

nr_nodes = getNumberOfNumaNodes()
nr_cores = getNumberOfPhysicalCores()
cores = getRepresentativeCoresFromNumaNodes()


def dump_to_dot(name, results):
    f = open(name, 'w')
    f.write("""digraph NUMA {
        node [shape = circle];
        """)
    for result in results:
        f.write("""\t"%s" -> "%s" [ label = "%d", len = 4 ]\n""" % result)

    f.write("}\n")
    f.close()


def _kill_pipe(pipe):
    os.killpg(pipe.pid, signal.SIGTERM)


def test_busy():
    results = []

    for node_from in sorted(cores.keys()):
        for node_to in sorted(cores.keys()):
            if node_from == node_to:
                core_from, core_to = cores[node_from]
            else:
                core_from = cores[node_from][0]
                core_to = cores[node_to][0]
            print("Node %s to node %s" % (node_from, node_to))
            burn1 = Popen(["taskset -c %d ./cpuburn-in 1" % core_from],
                          shell=True,
                          stdout=PIPE,
                          preexec_fn=os.setsid)
            burn2 = Popen(["taskset -c %d ./cpuburn-in 1 " % core_to],
                          shell=True,
                          stdout=PIPE,
                          preexec_fn=os.setsid)
            command = "numactl -C 0-%d %s %d %d %d" % (nr_cores - 1,
                                                       BIN,
                                                       core_from,
                                                       core_to,
                                                       BUFFER_SIZE)
            print(command)
            p = Popen([command], shell=True, stdout=PIPE)
            stdout, _ = p.communicate()
            _kill_pipe(burn1)
            _kill_pipe(burn2)
            print(stdout)
            stdout_lines = stdout.split()
            exec_time = int(float(stdout_lines[0]))
            results.append((node_from, node_to, exec_time))
    return results


def test_idle():
    results = []

    for node_from in sorted(cores.keys()):
        for node_to in sorted(cores.keys()):
            if node_from == node_to:
                core_from, core_to = cores[node_from]
            else:
                core_from = cores[node_from][0]
                core_to = cores[node_to][0]
            print("Node %s to node %s" % (node_from, node_to))
            command = "numactl -C 0-%d %s %d %d %d" % (nr_cores - 1,
                                                       BIN,
                                                       core_from,
                                                       core_to,
                                                       BUFFER_SIZE)
            print(command)
            p = Popen([command], shell=True, stdout=PIPE)
            stdout, _ = p.communicate()
            print(stdout)
            stdout_lines = stdout.split()
            exec_time = int(float(stdout_lines[0]))
            results.append((node_from, node_to, exec_time))
    return results

if __name__ == "__main__":
    import sys
    busy_results = test_busy()
    idle_results = test_idle()
    desc = sys.argv[1]
    dump_to_dot(BIN + "_%s_idle.dot" % desc, idle_results)
    dump_to_dot(BIN + "_%s_busy.dot" % desc, busy_results)
