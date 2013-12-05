import boto
from time import sleep


def run_stack(region_name, stack_name, file_name, template_params):
    f = open(file_name, "r")
    cf_template = f.read()

    print('Building ' + stack_name + ' Stack . . .')

    try:
        cf_connect = boto.connect_cloudformation()
        print(cf_connect)
        cf_region = boto.cloudformation.connect_to_region(region_name)

        cf_region.create_stack(stack_name,
            template_body=cf_template,
            parameters=template_params,
            capabilities=['CAPABILITY_IAM'])

        stack_building = True

        while stack_building == True:

#            pdb.set_trace()

            event_list = cf_region.describe_stack_events(stack_name)
            stack_event = event_list[0]

            if (stack_event.resource_type == 'AWS::CloudFormation::Stack' and
               stack_event.resource_status == 'CREATE_COMPLETE'):
                stack_building = False
                print "Stack construction complete."
            else:
                print event_list[0]
                print "Stack building . . ."
                sleep(10)

        vpc_stack = cf_region.describe_stacks(stack_name)

        return vpc_stack

    except boto.exception.BotoServerError as e:
        print e.error_message
