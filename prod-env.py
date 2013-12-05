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
    stack_params = parse_prod_params(parser)

    print(stack_params)

    stackrun.run_stack(region_name,
                stack_params['prod_stack_name'],
                stack_params['prod_cf_template'],
                stack_params['prod_params'])


def display_usage():

    print 'Usage: ' + sys.argv[0] + ' [-c/--config CONFIG FILE] [-h/--help]'
    exit()


def parse_prod_params(parser):

    prod_stack_name = parser.get('prod', 'stack_name')
    prod_cf_template = parser.get('prod', 'cf_template')

    prod_vpc_id = parser.get('prod', 'vpc_id')
    prod_az_letters = parser.get('prod', 'az_letters')
    prod_pub_subnet_ip_blocks =  parser.get('prod', 'public_subnet_ip_blocks')
    prod_priv_subnet_ip_blocks =  parser.get('prod', 'private_subnet_ip_blocks')
    prod_pub_mgmt_subnet_ip_block = parser.get('prod', 'pub_management_subnet_ip_block')
    prod_priv_mgmt_subnet_ip_block = parser.get('prod', 'priv_management_subnet_ip_block')
    prod_public_subnet_route_table = parser.get('prod', 'public_subnet_route_table')
    prod_nat_key_pair_name = parser.get('ha_nat', 'nat_key_pair_name')
    prod_nat_ami_id = parser.get('ha_nat', 'nat_ami_id')
    prod_nat_src_ips =parser.get('ha_nat', 'nat_src_ips')
    prod_nat_instance_size = parser.get('ha_nat', 'nat_instance_size')
    prod_bastion_ami_id = parser.get('ha_bastion', 'bastion_ami_id')
    prod_bastion_src_ips = parser.get('ha_bastion', 'bastion_src_ips')
    prod_bastion_instance_size = parser.get('ha_bastion', 'bastion_instance_size')
    prod_params = [('VpcId', prod_vpc_id),
                  ('AzLetters', prod_az_letters),
                  ('ProdPubSubnetIpBlocks', prod_pub_subnet_ip_blocks),
                  ('ProdPrivSubnetIpBlocks', prod_priv_subnet_ip_blocks),
                  ('ProdPubMgmtSubnetIpBlock', prod_pub_mgmt_subnet_ip_block),
                  ('ProdPrivMgmtSubnetIpBlock', prod_priv_mgmt_subnet_ip_block),
                  ('ProdPubSubnetRouteTable', prod_public_subnet_route_table),
                  ('KeyPairName', prod_nat_key_pair_name),
                  ('NatAmiId', prod_nat_ami_id),
                  ('NatSrcIps', prod_nat_src_ips),
                  ('NatInstanceSize', prod_nat_instance_size),
                  ('BastionAmiId', prod_bastion_ami_id),
                  ('BastionSrcIps', prod_bastion_src_ips),
                  ('BastionInstanceSize', prod_bastion_instance_size)
                 ]
     
    stack_params = { 'prod_stack_name' : prod_stack_name,
                     'prod_cf_template' : prod_cf_template,
                     'prod_params' : prod_params}

    return stack_params

if __name__ == "__main__":
    main()
