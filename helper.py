import argparse

parser = argparse.ArgumentParser(description="Helper tool for deploying to Automation Liberation")

parser.add_argument('command', metavar='command', type=str, nargs='+',
                    help='Specify a command you would like to run.')

parser.add_argument('-p', '--path', dest='location', default='build-parameters.yaml',
                    help='The path to the build parameters file with the changelog information')

args = parser.parse_args()


if 'changelog' in args.command:
    import changelog
    changelog.parse_build_params(args.location)
else:
    for command in args.command:
        print(f'Unknown command: {command}')
