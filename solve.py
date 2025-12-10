import subprocess
import time
import os
import argparse
import json

def solve(file_path, solver_cmd, timeout=60.0):
    try:
        start_time = time.time()

        # Run the solver process
        result = subprocess.run(
            solver_cmd + [file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # calculate runtime in ms
        end_time = time.time()
        runtime = (end_time - start_time) * 1000.0

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # Extract sat/unsat/unknown
        if "unsat" in stdout.lower():
            status = "unsat"
        elif "sat" in stdout.lower():
            status = "sat"
        elif "unknown" in stdout.lower():
            status = "unknown"
        else:
            status = "error"

        return {
            "status": status,
            "runtime": runtime,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            # runtime is given in seconds so we need to scale it here
            "runtime": timeout * 1000,
            "stdout": "",
            "stderr": "",
            "exit_code": None
        }
    

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver_cmd')
    parser.add_argument('--out')
    parser.add_argument('--logic')
    args = parser.parse_args()
                        
    print(f'Running {args.solver_cmd}')
    
    benchmarks = {
        'py-conbyte-cvc4' : ["QF_SLIA/2019-full_str_int"],
        'py-conbyte-trauc' : ["QF_SLIA/2019-full_str_int"],
        'py-conbyte-z3seq' : ["QF_SLIA/2019-full_str_int"],
        'py-conbyte-z3str' : ["QF_SLIA/2019-full_str_int"],
        'QF_S_NIA' : [
            "QF_SNIA/20180523-Reynolds",
            "QF_SNIA/20200224-Wu-PyExZ3",
            "QF_S/2019-Jiang",
            "QF_S/20250403-rna",
            "QF_S/20240318-omark",
            "QF_S/2020-sygus-qgen",
            "QF_S/20230329-woorpje-lu",
            "QF_S/20250403-pcp-string",
            "QF_S/20250410-matching",
            "QF_S/20250411-hornstr-equiv",
            "QF_S/20250411-negated-predicates",
            "QF_S/20230329-automatark-lu"
        ],
        'QF_SLIA' : [
            "QF_SLIA/20230327-stringfuzz-lu",
            "QF_SLIA/2019-Leetcode",
            "QF_SLIA/20240411-redos_attack_detection",
            "QF_SLIA/20190311-str-small-rw-Noetzli",
            "QF_SLIA/2019-Jiang",
            "QF_SLIA/20250410-matching",
            "QF_SLIA/20230403-webapp",
            "QF_SLIA/2015-Norn",
            "QF_SLIA/20230329-denghang",
            "QF_SLIA/2018-Kepler",
            "QF_SLIA/20230329-woorpje-lu",
            "QF_SLIA/20230331-transducer-plus"
        ],
        'Reynolds-kazula' : ["QF_SLIA/20180523-Reynolds"],
        'Reynolds-pyex-z3-td' : ["QF_SLIA/20180523-Reynolds"],
        'Reynolds-pyex-zz' : ["QF_SLIA/20180523-Reynolds"]
    }

    data = { 'solver' : args.solver_cmd }
    solver_name = args.solver_cmd.split(' ')[0] if args.solver_cmd.split(' ')[0] != "java" else args.solver_cmd.split(' ')[2].split('/')[5]

    print(os.getcwd())

    for benchmark in benchmarks[args.logic]:
        logic, suit = benchmark.split('/')[0], '/'.join(benchmark.split('/')[1:])

        print(f'Solving logic {logic}:{suit}')

        if logic not in data.keys():
            data[logic] = {}

        if suit not in data[logic].keys():
            data[logic][suit] = {}

        for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'smt-benchmark', logic, suit)):
            print(f"Running {os.path.join(os.getcwd(), 'smt-benchmark', logic, suit)}\n")

            for filename in files:
                print(f"Solving {root}/{filename}")

                result = solve(os.path.join(root, filename), args.solver_cmd.split(' '), 60.0)

                data[logic][suit][os.path.join(root, filename).split(suit)[1]] = result

                print(f"Status: {result['status']}")
                print(f"Runtime: {result['runtime']:.2f} ms")

                if result['stderr'] != "":
                    print(f"Output:\n{result['stdout']}\n")
                    print(f"Error:\n{result['stderr']}")
                print()

    with open(os.path.join(os.getcwd(), 'results', args.out), 'w') as out:
        out.write(json.dumps(data))
