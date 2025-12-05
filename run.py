import subprocess
import argparse

logics = [
        'py-conbyte-cvc4',
        'py-conbyte-trauc',
        'py-conbyte-z3seq',
        'py-conbyte-z3str',
        'qf-s-nia',
        'qf-slia',
        'reynolds-kazula',
        'reynolds-pyex-z3-td',
        'reynolds-pyex-zz'
    ]

solvers = {
    'cvc5': 'cvc5',
    'z3': 'z3',
    'z3-noodler': 'z3',
    'z3str4': 'z3',
    'ostrich2': '"java -jar /opt/ostrich-2.0.1/target/scala-2.11/ostrich-assembly-2.0.1.jar -version"',
    'ostrich': '"java -jar /opt/ostrich-2.0.1/target/scala-2.11/ostrich-assembly-2.0.1.jar -version"'
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver')
    parser.add_argument('--mount')
    args = parser.parse_args()

    for logic in logics:
        subprocess.run([
            'docker', 'run', 
            '-v', f'{args.mount}:/opt/app/runner/results/',
            f'{args.solver}-{logic}:latest'
        ])