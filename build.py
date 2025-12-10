import subprocess

logics = [
        ('py-conbyte-cvc4', 'py-conbyte-cvc4'),
        ('py-conbyte-trauc', 'py-conbyte-trauc'),
        ('py-conbyte-z3seq', 'py-conbyte-z3seq'),
        ('py-conbyte-z3str', 'py-conbyte-z3str'),
        ('QF_S_NIA', 'qf-s-nia'),
        ('QF_SLIA', 'qf-slia'),
        ('Reynolds-kazula', 'reynolds-kazula'),
        ('Reynolds-pyex-z3-td', 'reynolds-pyex-z3-td'),
        ('Reynolds-pyex-zz', 'reynolds-pyex-zz')
    ]

solvers = [
    ('cvc5', 'cvc5'),
    ('z3', 'z3'),
    ('z3-noodler', 'z3'),
    ('z3str4', 'z3')
]

solvers_java = [
    ('ostrich2', 'java -jar /opt/ostrich-2.0.1/target/scala-2.11/ostrich-assembly-2.0.1.jar'),
    ('ostrich', 'java -jar /opt/ostrich/target/scala-2.13/ostrich-assembly-1.4smtcomp.jar')
]

if __name__ == "__main__":
    # builder solver base images
    for solver, solver_cmd in solvers:
            subprocess.run([
                'docker', 'build',
                '-t', f'{solver}-base:latest',
                '-f', 'Dockerfile.solver',
                '--build-arg', f'SOLVER={solver}',
                '.'
            ])

    for solver, solver_cmd in solvers_java:
        subprocess.run([
            'docker', 'build',
            '-t', f'{solver}-base:latest',
            '-f', 'Dockerfile.java.solver',
            '--build-arg', f'SOLVER={solver}',
            '.'
        ])

    # build final images with benchmarks from base images
    for solver, solver_cmd in (solvers + solvers_java):
        for logic, logic_name in logics:
            subprocess.run([
                'docker', 'build',
                '-t', f'{solver}-{logic_name}:latest',
                '-f', 'Dockerfile.bench',
                '--build-arg', f'BASE={solver}-base:latest',
                '--build-arg', f'LOGIC={logic}',
                '--build-arg', f'SOLVER_CMD={solver_cmd}',
                '--build-arg', f'OUT_FILE={solver}-{logic_name}.json',
                '.'
            ])