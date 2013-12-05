import getopt
import sys
import stackrun
from ConfigParser import SafeConfigParser

def main():

    config_file = 'stackrun.ini'

    options, remainder = getopt.getopt(sys.argv[1:], 'c:h', ['configuration=', 
                                                         'help',
                                                         ])
    for opt, arg in options:
        if opt in ('-c', '--configuration'):
            config_file = arg
        elif opt in ('-h', '--help'):
            display_usage();

    print('Reading configuration from ' + config_file)

    parser = SafeConfigParser()
    if not parser.read(config_file):
        raise IOError, 'Failed opening ' + config_file + ' (-h for help)'   

    region_name = parser.get('global', 'region')

    print region_name
    stack_params = parse_vpc_params(parser)

    print(stack_params)

    stackrun.run_stackrun(region_name,
                stack_params['vpc_stack_name'],
                stack_params['vpc_cf_template'],
                stack_params['vpc_params'])


def display_usage():
   
    print 'Usage: ' + sys.argv[0] + ' [-c/--config CONFIG FILE] [-h/--help]'
    exit()


def parse_vpc_params(parser):

    vpc_stack_name = parser.get('vpc', 'stack_name')
    vpc_cf_template = parser.get('vpc', 'cf_template')
    vpc_ip_block = parser.get('vpc', 'vpc_ip_block')
    vpc_params = [('VpcIpBlock', vpc_ip_block)]
    
    stack_params = { 'vpc_stack_name' : vpc_stack_name, 'vpc_cf_template' : vpc_cf_template, 'vpc_params' : vpc_params}

    return stack_params

if __name__ == "__main__":
    main()
