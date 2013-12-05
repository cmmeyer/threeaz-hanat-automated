import base_vpc
import stackrun
import sys
import getopt
import boto
from ConfigParser import SafeConfigParser

class UndefError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


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
    stack_params = base_vpc.parse_vpc_params(parser)

    print(stack_params)

    stackrun.run_stack(region_name,
                stack_params['vpc_stack_name'],
                stack_params['vpc_cf_template'],
                stack_params['vpc_params'])
    
    update_config(region_name, stack_params, config_file)

def display_usage():
    print 'Usage: ' + sys.argv[0] + ' [-c/--config CONFIG FILE] [-h/--help]'
    exit()


def update_config(region_name, stack_params, config_file):
    parser = SafeConfigParser()
    parser.read(config_file)

    print 'Validating resource creation . . . '
    try:
        cfn = boto.connect_cloudformation()
        cfn = boto.cloudformation.connect_to_region(region_name)
        stack = cfn.describe_stacks(stack_params['vpc_stack_name'])[0]
        vpc_id = 'undef'
        publicroute_id = 'undef'
        privateroute_id = 'undef'
        for output in stack.outputs:
            if output.key == 'VpcId':
               vpc_id = output.value
            elif output.key == 'PublicRouteTable':
                publicroute_id = output.value
            elif output.key == 'PrivateRouteTable':
                privateroute_id = output.value
        if vpc_id == 'undef':
            raise UndefError('VpcId')
        if publicroute_id == 'undef':
            raise UndefError('PublicRouteTable')
        if privateroute_id == 'undef':
            raise UndefError('PrivateRouteTable')
        print('Updating ' + config_file  + ' with ' + stack_params['vpc_stack_name'] + ' stack information')
        parser.set('prod', 'vpc_id', vpc_id)
        parser.set('prod', 'public_subnet_route_table', publicroute_id)
        parser.set('prod', 'private_subnet_route_table', privateroute_id)
        config_output = open(config_file, 'w')
        parser.write(config_output)
    except UndefError as e:
        print 'Error updating configuration. Stack output not defined:', e.value
    except boto.exception.BotoServerError as e:
        print e.error_message

if __name__ == "__main__":
    main()